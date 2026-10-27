"""Saved factual invoice/receipt comparisons; no provider writes or collection."""
from decimal import Decimal
import hashlib
import re
import uuid

import workspace as ws
import workflows as wf
from . import invoicing as inv, storage as st


def template():
    return dict(schema_version=1, invoice_id=None, as_of=None, amount_due=None,
                bank_account=None, bank_file=None, review_file=None, reviewer=None,
                coverage_confirmed=False, payments=[])


def _context(root, state, identifier):
    row = state["invoices"].get(identifier)
    if not row or row["state"] != "issued":
        raise ws.WorkspaceError("Select an issued invoice before comparing receipts.")
    inv._check(root, row, state)
    # A correction anywhere in this family needs reviewed provider settlement.
    def origin(record):
        seen = set()
        while record["corrects"]:
            if record["invoice_id"] in seen or record["corrects"] not in state["invoices"]:
                raise ws.WorkspaceError("Invalid correction chain.")
            seen.add(record["invoice_id"])
            record = state["invoices"][record["corrects"]]
        return record["invoice_id"]
    family = [r for r in state["invoices"].values()
              if r["state"] != "cancelled" and origin(r) == origin(row)]
    for member in family:
        inv._check(root, member, state)
    return row, sorted(family, key=lambda r: r["invoice_id"])


def _money(value):
    return ws._amount(wf.text(value, "amount"))


def _captured_bytes(root, source):
    data = ws._read_regular(ws._inside(root, source["path"]))
    if hashlib.sha256(data).hexdigest() != source["sha256"]:
        raise ws.WorkspaceError("Payment source changed before parsing.")
    return data


def prepare(root, input_path, expected, language="en"):
    root = ws._workspace(root)
    if language not in {"en", "ru"}:
        raise ws.WorkspaceError("Payment report language must be en or ru.")
    with ws._locked(root):
        state = inv._load(root)
        input_source = st.evidence(root, input_path)
        value = ws._json_bytes(_captured_bytes(root, input_source))
        wf.exact(value, template(), "invoice payment comparison")
        if type(value["schema_version"]) is not int or value["schema_version"] != 1:
            raise ws.WorkspaceError("Unsupported payment comparison schema.")
        row, family = _context(root, state, st.identifier(value["invoice_id"]))
        st.version(row, expected)
        as_of = ws._day(wf.text(value["as_of"], "as_of"))
        due = _money(value["amount_due"])
        if due < 0:
            raise ws.WorkspaceError("Use a nonnegative invoice-stated amount due; review credits separately.")
        for key in ("bank_account", "reviewer"):
            wf.text(value[key], key)
        if type(value["coverage_confirmed"]) is not bool:
            raise ws.WorkspaceError("coverage_confirmed must be boolean.")
        if not isinstance(value["payments"], list) or len(value["payments"]) > 1000:
            raise ws.WorkspaceError("Supply at most 1000 explicitly reviewed receipt references.")
        sources = {input_source["path"]: input_source}
        def evidence(path):
            captured = st.evidence(root, path)
            prior = sources.setdefault(captured["path"], captured)
            if prior != captured:
                raise ws.WorkspaceError("Repeated payment evidence changed during preparation.")
            return captured
        evidence(value["review_file"])
        bank_source = evidence(value["bank_file"])
        bank = {}
        for item in ws._rows(_captured_bytes(root, bank_source),
                             {"transaction_id", "booking_date", "amount", "currency"}):
            identifier = ws._identifier(item["transaction_id"])
            if identifier in bank:
                raise ws.WorkspaceError("Duplicate bank transaction_id; use one account export.")
            bank[identifier] = dict(transaction_id=identifier, booking_date=ws._day(wf.text(item["booking_date"], "booking_date")),
                                    amount=_money(item["amount"]), currency=ws._currency(wf.text(item["currency"], "currency")))
        issues = []
        if as_of < row["issued"]["occurred_on"]:
            issues.append("before_issue")
        if not value["coverage_confirmed"]:
            issues.append("coverage_unconfirmed")
        if row["corrects"] or len(family) > 1:
            issues.append("correction_review_required")
        selected, seen, net = [], set(), Decimal(0)
        for item in value["payments"]:
            wf.exact(item, {"transaction_id", "amount", "treatment", "evidence_file"}, "receipt comparison")
            identifier = ws._identifier(item["transaction_id"])
            if identifier in seen or identifier not in bank:
                raise ws.WorkspaceError("Receipt reference is duplicate or absent from the supplied account export.")
            seen.add(identifier)
            evidence(item["evidence_file"])
            transaction = bank[identifier]
            amount, treatment = _money(item["amount"]), wf.text(item["treatment"], "treatment")
            if treatment not in {"included_prepaid", "later_receipt", "later_refund", "uncertain"}:
                raise ws.WorkspaceError("Unsupported receipt treatment.")
            if (not amount or amount.copy_abs() > transaction["amount"].copy_abs()
                    or (amount > 0) != (transaction["amount"] > 0)
                    or treatment in {"included_prepaid", "later_receipt"} and amount < 0
                    or treatment == "later_refund" and amount > 0):
                raise ws.WorkspaceError("Compared amount must have the bank movement's sign and fit within it.")
            if transaction["currency"] != row["currency"]:
                issues.append("currency_mismatch:" + identifier)
            if transaction["booking_date"] > as_of:
                issues.append("after_as_of:" + identifier)
            if treatment == "uncertain":
                issues.append("allocation_uncertain:" + identifier)
            if treatment in {"later_receipt", "later_refund"}:
                net = ws._add(net, amount)
            selected.append({**item, "booking_date": transaction["booking_date"],
                             "currency": transaction["currency"], "bank_amount": format(transaction["amount"], "f")})
        remaining = None if issues else ws._add(due, net.copy_negate())
        status = ("needs_review" if issues else "zero_difference" if remaining == 0 else
                  "overpaid_comparison" if remaining < 0 else "partial" if net > 0 else "no_later_receipts")
        # Snapshot only the inspected bytes, checking again across each copy.
        snapshots = []
        for source in sources.values():
            st.check_evidence(root, source)
            snapshot = inv._snapshot(root, source["path"])
            if snapshot["sha256"] != source["sha256"]:
                raise ws.WorkspaceError("Payment evidence changed while saving; inspect partial output.")
            snapshots.append(snapshot)
        report = dict(schema_version=1, kind="invoice_payment_comparison", created_at=ws._now(),
                      invoice_id=row["invoice_id"], invoice_number=row["issued"]["invoice_number"],
                      system=row["system"], account_reference=row["account_reference"],
                      invoice_sha256=st.digest(row), family_sha256=st.digest(family),
                      issued_document=row["issued"]["document"], currency=row["currency"],
                      input=value, sources=snapshots, payments=selected, status=status, issues=issues,
                      comparison_remaining=None if remaining is None else format(remaining, "f"),
                      compared_net=None if issues else format(net, "f"),
                      unselected_bank_rows=len(bank)-len(seen), language=language)
        relative = "08_correspondence/payment-comparisons/" + uuid.uuid4().hex
        path = ws._inside(root, relative + ".json")
        ws._mkdir(path.parent)
        markdown = render(report)
        report["markdown"] = {"path": ws._physical(root, relative + ".md"),
                              "sha256": hashlib.sha256(markdown.encode("utf-8")).hexdigest()}
        ws._atomic_json(path, report)
        ws._write_exclusive(ws._inside(root, relative + ".md"), markdown.encode("utf-8"))
        physical = ws._physical(root, relative + ".json")
        ws._audit(root, "invoice_payment_comparison_saved", {"path": physical, "sha256": st.digest(report)})
        return {"path": physical, "markdown_path": report["markdown"]["path"],
                "status": status, "comparison_remaining": report["comparison_remaining"], "issues": issues}


def _checked(root, state, report_path):
    """Read and validate under the caller-held workspace lock."""
    physical = ws._physical(root, report_path)
    report = ws._load(ws._inside(root, physical))
    events = ws._load(ws._inside(root, ws.EVENTS))
    if not any(e.get("action") == "invoice_payment_comparison_saved" and
               e.get("details") == {"path": physical, "sha256": st.digest(report)} for e in events):
        raise ws.WorkspaceError("Payment report has no matching audit checkpoint or was changed.")
    st.check_evidence(root, report["markdown"])
    row, family = _context(root, state, report["invoice_id"])
    issues = []
    if st.digest(family) != report["family_sha256"]:
        issues.append("invoice_context_changed")
    for source in report["sources"]:
        st.check_evidence(root, source)
        try:
            st.check_evidence(root, source["source"])
        except (OSError, ws.WorkspaceError):
            issues.append("working_source_changed:" + source["source"]["path"])
    return report, {"report_sha256": st.digest(report), "current": not issues, "freshness_issues": issues,
            "comparison_issues": report["issues"], "status": report["status"],
            "comparison_remaining": report["comparison_remaining"] if not issues else None}


def check(root, report_path):
    root = ws._workspace(root)
    with ws._locked(root):
        _, result = _checked(root, inv._load(root), report_path)
        return result


def render(report):
    ru = report["language"] == "ru"
    def safe(value):
        text = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", " ").replace("\r", " ")
        return re.sub(r"([\\`*_{}\[\]()#!|])", r"\\\1", text)
    value = report["input"]
    lines = ["# " + ("Сверка оплаты" if ru else "Payment comparison"), "",
             ("Счёт: " if ru else "Invoice: ") + safe(report["invoice_number"] or report["invoice_id"]),
             ("На дату: " if ru else "As of: ") + value["as_of"],
             ("Система: " if ru else "System: ") + safe(report["system"]),
             ("Банковский счёт: " if ru else "Bank account: ") + safe(value["bank_account"]),
             ("Сумма к оплате по документу (уже учитывает предоплату): " if ru else "Invoice-stated amount due (already includes prepayments): ") + safe(value["amount_due"]) + " " + report["currency"],
             ("Остаток сравнения: " if ru else "Comparison remainder: ") + (report["comparison_remaining"] or ("не определён" if ru else "unresolved")) + " " + report["currency"], "",
             ("Нет распределения платежей, изменения статуса у провайдера, требования оплаты, возврата или налоговой проводки. Нулевая разница не доказывает оплату."
              if ru else "No payment allocation, provider status change, payment demand, refund or tax posting. A zero difference does not prove payment."), "",
             ("Предоплата ниже уже включена в сумму документа и не вычитается повторно."
              if ru else "Prepaid receipts below are already included in the document amount and are not subtracted again."), "",
             "| " + ("Транзакция | Дата | Сумма | Валюта | Учёт |" if ru else "Transaction | Date | Amount | Currency | Treatment |"),
             "| --- | --- | --- | --- | --- |"]
    treatments = {"included_prepaid": ("Already included prepaid", "Уже включённая предоплата"),
                  "later_receipt": ("Later receipt", "Последующее поступление"),
                  "later_refund": ("Later refund", "Последующий возврат"),
                  "uncertain": ("Uncertain allocation", "Неясное отнесение")}
    for item in report["payments"]:
        lines.append("| " + " | ".join(safe(item[k]) for k in ("transaction_id", "booking_date", "amount", "currency")) + " | " + treatments[item["treatment"]][ru] + " |")
    issue_labels = {
        "before_issue": ("Comparison date is earlier than recorded invoice issuance", "Дата сверки раньше записанной даты выставления счёта"),
        "coverage_unconfirmed": ("Receipt/refund coverage has not been confirmed", "Полнота поступлений/возвратов не подтверждена"),
        "correction_review_required": ("Review the invoice's correction family in the authoritative system", "Проверьте цепочку корректировок счёта в основной системе"),
        "currency_mismatch": ("Receipt currency differs from invoice currency", "Валюта поступления отличается от валюты счёта"),
        "after_as_of": ("Selected movement is after the comparison date", "Выбранное движение позже даты сверки"),
        "allocation_uncertain": ("Invoice allocation remains uncertain", "Отнесение к счёту остаётся неясным")}
    explanations = []
    for issue in report["issues"]:
        code, _, identifier = issue.partition(":")
        explanations.append(issue_labels[code][ru] + (": " + safe(identifier) if identifier else ""))
    lines += ["", ("Проблемы для проверки: " if ru else "Review issues: ") + ("; ".join(explanations) or ("не выявлены в выбранном сравнении" if ru else "none identified in the selected comparison")),
              ("Строк вне выбранного сравнения: " if ru else "Bank rows outside the selected comparison: ") + str(report["unselected_bank_rows"]),
              ("Далее: проверить актуальность отчёта, затем сверить отнесение и остаток в выбранной системе."
               if ru else "Next: check report freshness, then verify allocation and balance in the chosen system."), "",
              "## " + ("Закрытые подтверждения" if ru else "Private evidence"), ""]
    lines += ["- " + safe(s["path"]) + " / SHA-256 " + s["sha256"] for s in report["sources"]]
    return "\n".join(lines) + "\n"
