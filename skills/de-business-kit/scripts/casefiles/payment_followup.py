"""Prepare customer payment queries separately from private evidence; never send."""
import hashlib
import re
import uuid

import workspace as ws
import workflows as wf
from . import invoicing as inv, invoice_payments as pay, storage as st


def template():
    return dict(schema_version=1, comparison_file=None, mode=None, recipient=None,
                customer_name=None, sender_name=None, recipient_language="de",
                prepared_on=None, review_file=None)


def _line(value, name):
    value = wf.text(value, name)
    if len(value) > 300 or any(ord(c) < 32 or ord(c) == 127 or c in "\u2028\u2029" for c in value):
        raise ws.WorkspaceError(name + " must be a short single line.")
    return value


def _recipient(value):
    wf.exact(value, {"channel", "address"}, "follow-up recipient")
    address = _line(value["address"], "recipient address")
    if value["channel"] != "email" or not re.fullmatch(r"[^\s<>@,;]+@[^\s<>@,;]+\.[^\s<>@,;]+", address):
        raise ws.WorkspaceError("Supply one reviewed email destination; this writer does not send.")


def _message(value, comparison):
    number = _line(comparison["invoice_number"], "invoice number")
    name, sender, language = value["customer_name"], value["sender_name"], value["recipient_language"]
    day = comparison["input"]["as_of"]
    amount = comparison["comparison_remaining"]
    if language in {"de", "ru"} and amount is not None:
        amount = amount.replace(".", ",")
    balance = value["mode"] == "balance_query"
    if language == "de":
        body = (f"Bei unserem Zahlungsabgleich zum {day} ergibt sich für diese Rechnung noch eine Differenz von {amount} {comparison['currency']}. "
                "Könnten Sie bitte prüfen, ob hierzu bereits eine Zahlung erfolgt ist?" if balance else
                "Wir möchten den Zahlungsstand zu dieser Rechnung mit Ihnen abgleichen. Könnten Sie uns bitte mitteilen, welche Zahlungen Sie dieser Rechnung zugeordnet haben?")
        return f"Betreff: Zahlungsabgleich zur Rechnung {number}\n\nGuten Tag {name},\n\n{body}\n\nFalls bereits eine Zahlung erfolgt ist, helfen uns Zahlungsdatum und Verwendungszweck bei der Zuordnung.\n\nVielen Dank und freundliche Grüße\n{sender}\n"
    if language == "en":
        body = (f"Our payment comparison as of {day} shows a remaining difference of {amount} {comparison['currency']} for this invoice. "
                "Could you please check whether a payment has already been made?" if balance else
                "We would like to reconcile the payment position for this invoice with you. Could you please let us know which payments you have assigned to it?")
        return f"Subject: Payment clarification for invoice {number}\n\nHello {name},\n\n{body}\n\nIf a payment has already been made, its date and reference will help us match it.\n\nThank you and best regards,\n{sender}\n"
    body = (f"По нашей сверке на {day} по этому счёту остаётся разница {amount} {comparison['currency']}. "
            "Не могли бы вы проверить, был ли уже выполнен соответствующий платёж?" if balance else
            "Хотим сверить с вами состояние оплаты этого счёта. Подскажите, пожалуйста, какие платежи вы отнесли к нему.")
    return f"Тема: Сверка оплаты счёта {number}\n\nЗдравствуйте, {name}!\n\n{body}\n\nЕсли платёж уже выполнен, его дата и назначение помогут нам сопоставить поступление.\n\nСпасибо!\nС уважением,\n{sender}\n"


def _review(value, comparison, language, recipient_path):
    ru = language == "ru"
    # Keep dynamic private fields literal rather than allowing Markdown links.
    def literal(text):
        return "<pre>" + str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre>"
    return "\n\n".join([
        "# " + ("Проверка письма об оплате" if ru else "Payment follow-up review"),
        "Не отправлено. Подготовлен только черновик." if ru else "Not sent. Draft preparation only.",
        ("Получатель: " if ru else "Destination: ") + literal(value["recipient"]["address"]),
        ("Текст для клиента: " if ru else "Customer text: ") + literal(recipient_path),
        ("Основание сверки: " if ru else "Comparison basis: ") + literal(value["comparison_file"]),
        ("Дата подготовки: " if ru else "Prepared on: ") + value["prepared_on"],
        ("Сумма не включена: требуется уточнение." if ru else "Amount omitted: clarification is required.")
        if value["mode"] == "clarification" else
        ("Указана разница сверки, а не доказанный долг или просрочка." if ru else "The amount is a comparison difference, not an established debt or overdue amount."),
        ("Проверьте адрес, номер счёта, имя, подпись и факты. Перед отправкой повторите проверку актуальности и используйте разрешённый пользователем маршрут. Не прикладывайте эту записку, банковскую выгрузку или внутренние подтверждения."
         if ru else "Review destination, invoice number, names, signature and facts. Before sending, recheck freshness and use the user-authorized delivery route. Do not attach this review, the bank export or internal evidence."),
        ("Проблемы исходной сверки перечислены в её отдельном закрытом отчёте. Нет процентов, штрафов, срока оплаты, вывода о просрочке или обещания возврата."
         if ru else "Comparison issues are explained in its separate private report. No interest, fees, payment deadline, default claim or refund promise is added.")
    ]) + "\n"


def prepare(root, input_path, expected, language="en"):
    root = ws._workspace(root)
    if language not in {"en", "ru"}:
        raise ws.WorkspaceError("Private review language must be en or ru.")
    with ws._locked(root):
        state = inv._load(root)
        source = st.evidence(root, input_path)
        value = ws._json_bytes(pay._captured_bytes(root, source))
        wf.exact(value, template(), "payment follow-up")
        if type(value["schema_version"]) is not int or value["schema_version"] != 1:
            raise ws.WorkspaceError("Unsupported follow-up schema.")
        mode = wf.text(value["mode"], "mode")
        if mode not in {"balance_query", "clarification"}:
            raise ws.WorkspaceError("Choose balance_query or clarification.")
        if wf.text(value["recipient_language"], "recipient language") not in {"de", "en", "ru"}:
            raise ws.WorkspaceError("Recipient language must be de, en or ru.")
        _recipient(value["recipient"])
        for key in ("customer_name", "sender_name"):
            value[key] = _line(value[key], key)
        day = ws._day(wf.text(value["prepared_on"], "prepared_on"))
        comparison, checked = pay._checked(root, state, value["comparison_file"])
        if checked["report_sha256"] != expected or not checked["current"]:
            raise ws.WorkspaceError("Stale comparison/hash; inspect sources and create a current comparison first.")
        if day < max(comparison["input"]["as_of"], state["invoices"][comparison["invoice_id"]]["issued"]["occurred_on"]):
            raise ws.WorkspaceError("Preparation date cannot precede the comparison or recorded invoice issue.")
        if mode == "balance_query" and (checked["comparison_issues"] or checked["comparison_remaining"] is None
                                        or pay._money(checked["comparison_remaining"]) <= 0):
            raise ws.WorkspaceError("Only a current positive, unblocked comparison supports a balance query; use amount-free clarification otherwise.")
        review = st.evidence(root, value["review_file"])
        if review["path"] == source["path"]:
            raise ws.WorkspaceError("Review evidence must be separate from the input request.")
        message = _message(value, comparison)
        sources = []
        for captured in (source, review):
            st.check_evidence(root, captured)
            snapshot = inv._snapshot(root, captured["path"])
            if snapshot["sha256"] != captured["sha256"]:
                raise ws.WorkspaceError("Follow-up evidence changed while saving; inspect partial output.")
            sources.append(snapshot)
        relative = "08_correspondence/payment-followups/" + uuid.uuid4().hex
        recipient_path = ws._physical(root, relative + "-recipient.txt")
        private = _review(value, comparison, language, recipient_path)
        artifacts = {}
        ws._mkdir(ws._inside(root, relative + ".json").parent)
        for key, suffix, content in (("recipient", "-recipient.txt", message), ("review", "-review.md", private)):
            path = relative + suffix
            ws._write_exclusive(ws._inside(root, path), content.encode("utf-8"))
            artifacts[key] = {"path": ws._physical(root, path), "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest()}
        manifest = dict(schema_version=1, kind="payment_followup", created_at=ws._now(), language=language,
                        input=value, sources=sources, artifacts=artifacts, comparison_sha256=expected,
                        delivery_state="not_sent")
        ws._atomic_json(ws._inside(root, relative + ".json"), manifest)
        physical = ws._physical(root, relative + ".json")
        ws._audit(root, "payment_followup_prepared", {"path": physical, "sha256": st.digest(manifest)})
        return {"path": physical, "recipient_path": artifacts["recipient"]["path"],
                "review_path": artifacts["review"]["path"], "delivery_state": "not_sent"}


def check(root, report_path):
    root = ws._workspace(root)
    with ws._locked(root):
        state = inv._load(root)
        physical = ws._physical(root, report_path)
        manifest = ws._load(ws._inside(root, physical))
        if not any(e.get("action") == "payment_followup_prepared" and
                   e.get("details") == {"path": physical, "sha256": st.digest(manifest)}
                   for e in ws._load(ws._inside(root, ws.EVENTS))):
            raise ws.WorkspaceError("Follow-up is changed or lacks a matching audit checkpoint.")
        for artifact in manifest["artifacts"].values():
            st.check_evidence(root, artifact)
        _, checked = pay._checked(root, state, manifest["input"]["comparison_file"])
        issues = list(checked["freshness_issues"])
        if checked["report_sha256"] != manifest["comparison_sha256"]:
            issues.append("comparison_changed")
        for source in manifest["sources"]:
            st.check_evidence(root, source)
            try:
                st.check_evidence(root, source["source"])
            except (OSError, ws.WorkspaceError):
                issues.append("working_source_changed:" + source["source"]["path"])
        return {"current": not issues, "freshness_issues": issues, "comparison_issues": checked["comparison_issues"],
                "delivery_state": "not_sent", "mode": manifest["input"]["mode"]}
