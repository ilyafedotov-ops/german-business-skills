"""Versioned invoice issue/correction/delivery evidence; no external transport."""
from contextlib import contextmanager
import copy
import hashlib
from pathlib import Path
import re
import uuid

import workspace as ws
import workflows as wf
from . import storage as st

STATE = "00_admin/invoicing.json"
ISSUE = {"review-issue": ({"draft", "issue_failed"}, "reviewed"),
         "authorize-issue": ({"reviewed"}, "issue_authorized"),
         "begin-issue": ({"issue_authorized"}, "issue_unconfirmed"),
         "confirm-not-issued": ({"issue_unconfirmed"}, "issue_failed"),
         "confirm-issued": ({"issue_unconfirmed"}, "issued"),
         "adopt-issued": ({"draft"}, "issued"),
         "cancel": ({"draft", "reviewed", "issue_authorized", "issue_failed"}, "cancelled")}
DELIVERY = {"review-delivery": ({"not_prepared", "delivery_failed", "delivery_reviewed", "delivery_authorized"}, "delivery_reviewed"),
            "adopt-dispatched": ({"not_prepared", "delivery_failed", "delivery_reviewed", "delivery_authorized"}, "dispatched"),
            "authorize-delivery": ({"delivery_reviewed"}, "delivery_authorized"),
            "begin-delivery": ({"delivery_authorized"}, "delivery_unconfirmed"),
            "confirm-dispatched": ({"delivery_unconfirmed"}, "dispatched"),
            "confirm-delivered": ({"delivery_unconfirmed", "dispatched"}, "delivered"),
            "confirm-delivery-failed": ({"delivery_unconfirmed", "dispatched"}, "delivery_failed")}
LIVE = {"review-issue", "authorize-issue", "begin-issue"}
ISSUED = {"confirm-issued", "adopt-issued"}
OUTCOMES = {"confirm-issued", "confirm-not-issued", "confirm-dispatched", "confirm-delivered", "confirm-delivery-failed"}


def template(kind):
    if kind == "invoice":
        return dict(invoice_id=None, business_reference=None, period=None, system=None,
                    account_reference=None, customer_reference=None, currency=None,
                    document_file=None, source_files=[], unresolved_items=[],
                    corrects=None, correction_kind=None, replaces=None)
    if kind == "action":
        return dict(invoice_id=None, action=None, actor=None, evidence_file=None, note=None,
                    occurred_on=None, attempt_id=None, external_id=None, invoice_number=None,
                    document_file=None, recipient=None, attachment_files=[], outcome_kind=None)
    raise ws.WorkspaceError("Unknown invoicing template.")


def _load(root):
    ws._check_audit(root)
    checkpoint = next((e["details"]["history_id"] for e in reversed(ws._load(ws._inside(root, ws.EVENTS)))
                       if isinstance(e.get("details"), dict)
                       and str(e["details"].get("history_id", "")).startswith("invoicing-")), None)
    path = ws._inside(root, STATE)
    if not path.exists():
        if checkpoint:
            raise ws.WorkspaceError("Invoice register is missing but history exists; recover before continuing.")
        return {"schema_version": 1, "invoices": {}}
    state = ws._load(path)
    wf.exact(state, {"schema_version", "invoices", "checksum"}, "invoice register")
    checksum = state.pop("checksum")
    if type(state["schema_version"]) is not int or state["schema_version"] != 1 or not isinstance(state["invoices"], dict) or checksum != st.digest(state):
        raise ws.WorkspaceError("Unsupported or changed invoice register; inspect history.")
    if not checkpoint or ws._load(ws._inside(root, "09_audit/history/" + st.identifier(checkpoint) + ".json")).get("after_sha256") != checksum:
        raise ws.WorkspaceError("Invoice register and audit checkpoint disagree; inspect interrupted writes or rollback.")
    return state


@contextmanager
def _edit(root, action):
    with ws._locked(root):
        state = _load(root)
        before = copy.deepcopy(state)
        yield state
        if state == before:
            return
        saved = {**state, "checksum": st.digest(state)}
        if len(st.encoded(saved)) > ws.MAX_BYTES:
            raise ws.WorkspaceError("Invoice register exceeds supported size.")
        history = "invoicing-" + uuid.uuid4().hex
        ws._atomic_json(ws._inside(root, "09_audit/history/" + history + ".json"),
                        {"action": action, "before": before, "after_sha256": st.digest(state)})
        ws._atomic_json(ws._inside(root, STATE), saved, replace=True)
        ws._audit(root, action, {"history_id": history})


def _snapshot(root, relative):
    source = st.evidence(root, relative)
    data = ws._read_regular(ws._inside(root, source["path"]))
    if hashlib.sha256(data).hexdigest() != source["sha256"]:
        raise ws.WorkspaceError("Invoice evidence changed during capture.")
    suffix = Path(relative).suffix.lower()
    if suffix not in {".md", ".txt", ".json", ".xml", ".pdf", ".html", ".csv", ".png", ".jpg", ".eml"}:
        raise ws.WorkspaceError("Unsupported invoice evidence format; never supply credentials.")
    destination = "08_correspondence/invoice-evidence/" + uuid.uuid4().hex + suffix
    target = ws._inside(root, destination)
    ws._mkdir(target.parent)
    ws._write_exclusive(target, data)
    return {"path": ws._physical(root, destination), "sha256": source["sha256"], "source": source}


def _authority(row):
    return row["system"], row["account_reference"]


def _scope(row):
    return (*_authority(row), row["business_reference"], row["customer_reference"], row["currency"], row["corrects"], row["correction_kind"])


def _issue_scope(row):
    return {"scope": _scope(row), "draft": row["draft"], "sources": row["sources"], "parent": row["parent_issued_sha256"],
            "provider_request": row.get("provider", {}).get("request"),
            "provider_readback": row.get("provider", {}).get("readback")}


def _snapshots(row):
    result = [row["draft"], *row["sources"]]
    provider = row.get("provider")
    if provider:
        result.append(provider["request"])
        for event in provider["events"]:
            result.extend(event[k] for k in ("evidence", "response") if k in event)
    for event in row["events"]:
        result.append(event["evidence"])
        if event.get("document"):
            result.append(event["document"])
        result.extend(event.get("attachments", []))
    return result


def _provider_issue(row, action, value=None, root=None):
    provider = row.get("provider")
    if not provider:
        return
    if action == "cancel" and provider["state"] not in {"prepared", "authorized"}:
        raise ws.WorkspaceError("A provider draft/attempt exists; reconcile it without locally cancelling or recreating the operation.")
    if action in LIVE and (provider["state"] != "reviewed" or provider["remote_status"] != "draft"):
        raise ws.WorkspaceError("Read back and review the existing provider draft before issue; unresolved creation cannot be bypassed.")
    if action in ISSUED:
        if provider["state"] != "reviewed" or provider["remote_status"] not in {"open", "paid", "paidoff"} or not provider["document"]:
            raise ws.WorkspaceError("Read back the finalized provider object, download and review its actual artifact first.")
        if value:
            readback = ws._load(ws._inside(root, provider["readback"]["path"]))
            if (value["external_id"] != provider["external_id"] or value["invoice_number"] != readback.get("voucherNumber")
                    or st.evidence(root, value["document_file"])["sha256"] != provider["document"]["sha256"]):
                raise ws.WorkspaceError("Issued result differs from the linked provider ID, number or downloaded artifact.")


def _check(root, row, state, live=False):
    for source in _snapshots(row):
        st.check_evidence(root, source)
    if row["corrects"]:
        parent = state["invoices"].get(row["corrects"])
        if not parent or not parent["issued"] or st.digest(parent["issued"]) != row["parent_issued_sha256"]:
            raise ws.WorkspaceError("Correction's issued parent changed or is missing.")
        st.check_evidence(root, parent["issued"]["document"])
        if live and parent["delivery"]["state"] == "delivery_unconfirmed":
            raise ws.WorkspaceError("Resolve the original invoice's delivery attempt before correcting it.")
    if live:
        if row["unresolved_items"]:
            raise ws.WorkspaceError("Resolve draft issues through a cancelled/linked replacement before issue.")
        for source in [row["draft"], *row["sources"]]:
            st.check_evidence(root, source["source"])


def _delivery_context(root, row, state):
    provider = row.get("provider")
    if provider:
        _provider_issue(row, "confirm-issued")
        if provider["document"]["sha256"] != row["issued"]["document"]["sha256"]:
            raise ws.WorkspaceError("Provider artifact changed; reconcile the issued document before delivery.")
    def family(record):
        seen = set()
        while record["corrects"]:
            if record["invoice_id"] in seen or record["corrects"] not in state["invoices"]:
                raise ws.WorkspaceError("Invalid invoice correction chain.")
            seen.add(record["invoice_id"])
            record = state["invoices"][record["corrects"]]
        return record["invoice_id"]
    family_id = family(row)
    related = sorted((r for r in state["invoices"].values() if r["invoice_id"] != row["invoice_id"] and r["state"] != "cancelled" and family(r) == family_id), key=lambda r: r["invoice_id"])
    if any(r["state"] != "issued" for r in related):
        raise ws.WorkspaceError("Resolve the pending correction before preparing or starting delivery of the original.")
    if any(r["corrects"] == row["invoice_id"] and r["correction_kind"] in {"cancellation", "replacement"} for r in related):
        raise ws.WorkspaceError("The original has a recorded cancellation/replacement; inspect the resulting document instead of sending it.")
    for related_row in related:
        _check(root, related_row, state)
    context = [{k: r[k] for k in ("invoice_id", "correction_kind", "issued")} for r in related]
    if provider:
        context.append({"provider_readback_sha256": provider["readback"]["sha256"]})
    return st.digest(context)


def _check_delivery(root, row, state, review=False):
    context = _delivery_context(root, row, state)
    if not review and (not row["delivery"]["package"] or row["delivery"]["package"]["corrections_sha256"] != context):
        raise ws.WorkspaceError("Correction context changed; review and authorize a new delivery package.")
    return context


def create(root, value):
    root = ws._workspace(root)
    wf.exact(value, template("invoice"), "invoice draft")
    st.identifier(value["invoice_id"])
    for key in ("business_reference", "system", "account_reference", "customer_reference"):
        wf.text(value[key], key)
    wf.period(value["period"])
    ws._currency(wf.text(value["currency"], "currency"))
    wf.strings(value["source_files"], "source files")
    wf.strings(value["unresolved_items"], "unresolved items")
    if not value["source_files"] or len(value["source_files"]) > 64:
        raise ws.WorkspaceError("Supply 1-64 source files including issuing-system/account choice and business facts.")
    if value["corrects"] is None:
        if value["correction_kind"] is not None:
            raise ws.WorkspaceError("Correction kind requires an issued parent.")
    elif value["correction_kind"] not in {"amendment", "amount_credit", "cancellation", "replacement"}:
        raise ws.WorkspaceError("Choose the reviewed authoritative correction route.")
    with _edit(root, "invoice_created") as state:
        rows = state["invoices"]
        if value["invoice_id"] in rows:
            raise ws.WorkspaceError("Invoice versions are immutable; use a linked replacement.")
        prior = rows.get(value["replaces"])
        if value["replaces"] is not None:
            if not prior or prior["state"] != "cancelled" or prior["business_reference"] != value["business_reference"]:
                raise ws.WorkspaceError("Replace only a cancelled draft retaining its business reference; all changed facts need fresh review.")
            if any(r["replaces"] == value["replaces"] for r in rows.values()):
                raise ws.WorkspaceError("Draft already has a replacement; inspect latest version.")
        for row in rows.values():
            if (*_authority(row), row["business_reference"]) == (*_authority(value), value["business_reference"]):
                if row["state"] != "cancelled" or prior is None:
                    raise ws.WorkspaceError("Business operation already recorded; resolve existing outcome before retry/replacement.")
        parent = rows.get(value["corrects"])
        if value["corrects"] is not None:
            if not parent or parent["state"] != "issued" or (_authority(parent), parent["customer_reference"], parent["currency"]) != (_authority(value), value["customer_reference"], value["currency"]):
                raise ws.WorkspaceError("Correction requires the issued parent in the same system/account, customer and currency.")
            _check(root, parent, state)
            if parent["delivery"]["state"] == "delivery_unconfirmed" or any(r["corrects"] == value["corrects"] and (r["state"] not in {"issued", "cancelled"} or r["delivery"]["state"] == "delivery_unconfirmed") for r in rows.values()):
                raise ws.WorkspaceError("Resolve the existing correction or uncertain delivery first.")
        saved = {**copy.deepcopy(value), "draft": _snapshot(root, value["document_file"]),
                 "sources": [_snapshot(root, p) for p in value["source_files"]],
                 "parent_issued_sha256": st.digest(parent["issued"]) if parent else None,
                 "state": "draft", "issued": None, "issue_attempt": None,
                 "delivery": {"state": "not_prepared", "package": None, "attempt_id": None, "external_id": None},
                 "events": [], "created_at": ws._now()}
        rows[value["invoice_id"]] = saved
    return {"invoice_id": value["invoice_id"], "state": "draft", "sha256": st.digest(saved)}


def _optional_input(value):
    action = value["action"]
    permitted = set()
    if action in ISSUED:
        permitted |= {"external_id", "invoice_number", "document_file"}
    if action in OUTCOMES:
        permitted.add("attempt_id")
    if action in {"confirm-dispatched", "confirm-delivered", "confirm-delivery-failed", "adopt-dispatched"}:
        permitted.add("external_id")
    if action in {"confirm-not-issued", "confirm-delivered", "confirm-delivery-failed"}:
        permitted.add("outcome_kind")
    if action in {"review-delivery", "adopt-dispatched"}:
        permitted |= {"recipient", "attachment_files"}
    for key in ("attempt_id", "external_id", "invoice_number", "document_file", "recipient", "outcome_kind", "attachment_files"):
        if key not in permitted and value[key] != ([] if key == "attachment_files" else None):
            raise ws.WorkspaceError("Unexpected action field: " + key)


def act(root, value, expected):
    root = ws._workspace(root)
    wf.exact(value, template("action"), "invoice action")
    for key in ("actor", "note"):
        wf.text(value[key], key)
    ws._day(value["occurred_on"])
    action = value["action"]
    if action not in ISSUE and action not in DELIVERY:
        raise ws.WorkspaceError("Unknown invoice action.")
    _optional_input(value)
    with _edit(root, "invoice_" + action) as state:
        row = state["invoices"].get(value["invoice_id"])
        if row is None:
            raise ws.WorkspaceError("Invoice not found.")
        st.version(row, expected)
        _check(root, row, state, live=action in LIVE)
        _provider_issue(row, action, value, root)
        delivery = row["delivery"]
        is_delivery = action in DELIVERY
        allowed, next_state = (DELIVERY if is_delivery else ISSUE)[action]
        current = delivery["state"] if is_delivery else row["state"]
        if current not in allowed or is_delivery and row["state"] != "issued":
            raise ws.WorkspaceError("Invalid invoice transition; inspect current state before proceeding.")
        if action in {"review-delivery", "authorize-delivery", "begin-delivery"}:
            _check_delivery(root, row, state, review=action == "review-delivery")
        if action in OUTCOMES:
            attempt = delivery["attempt_id"] if is_delivery else row["issue_attempt"]
            if not attempt or value["attempt_id"] != attempt:
                raise ws.WorkspaceError("Outcome does not identify the active attempt; investigate delayed/duplicate results.")
            began = next(e for e in row["events"] if e["attempt_id"] == attempt and e["action"] in {"begin-issue", "begin-delivery", "adopt-dispatched"})
            if value["occurred_on"] < began["occurred_on"]:
                raise ws.WorkspaceError("Outcome date precedes this attempt; inspect the actual evidence.")
        if action == "confirm-not-issued" and value["outcome_kind"] != "confirmed_not_issued":
            raise ws.WorkspaceError("A timeout or missing match is not confirmation that no invoice was issued.")
        if action == "confirm-delivered" and value["outcome_kind"] not in {"delivery_receipt", "recipient_acknowledgement"}:
            raise ws.WorkspaceError("Delivery needs a reviewed receipt or recipient acknowledgement, not a send log.")
        if action == "confirm-delivery-failed" and value["outcome_kind"] != ("delivery_failure" if current == "dispatched" else "confirmed_not_dispatched"):
            raise ws.WorkspaceError("Retry needs affirmative failure evidence, not uncertainty.")
        if is_delivery and action in OUTCOMES:
            wf.text(value["external_id"], "actual dispatch/delivery correlation reference")
            if delivery["external_id"] and delivery["external_id"] != value["external_id"]:
                raise ws.WorkspaceError("Delivery reference differs from this attempt's dispatch.")
            if current == "dispatched":
                dispatched = next(e for e in row["events"] if e["attempt_id"] == delivery["attempt_id"] and e["action"] in {"confirm-dispatched", "adopt-dispatched"})
                if value["occurred_on"] < dispatched["occurred_on"]:
                    raise ws.WorkspaceError("Receipt/failure date precedes the recorded dispatch.")
        if action == "adopt-dispatched":
            wf.text(value["external_id"], "actual historical dispatch reference")
        if is_delivery and value["occurred_on"] < row["issued"]["occurred_on"]:
            raise ws.WorkspaceError("Delivery event predates the issued document outcome.")
        if action in ISSUED:
            if row["corrects"] and value["occurred_on"] < state["invoices"][row["corrects"]]["issued"]["occurred_on"]:
                raise ws.WorkspaceError("Correction outcome predates its issued parent.")
            wf.text(value["external_id"], "external_id")
            can_reuse = row["correction_kind"] in {"amendment", "cancellation"}
            if value["invoice_number"] is not None or not can_reuse:
                wf.text(value["invoice_number"], "invoice_number")
            def duplicate(other):
                if not other["issued"] or _authority(other) != _authority(row):
                    return False
                if can_reuse and (other["invoice_id"] == row["corrects"] or other["corrects"] == row["corrects"] and other["correction_kind"] in {"amendment", "cancellation"}):
                    return False
                return other["issued"]["external_id"] == value["external_id"] or value["invoice_number"] is not None and other["issued"]["invoice_number"] == value["invoice_number"]
            if any(duplicate(other) for other in state["invoices"].values()):
                raise ws.WorkspaceError("Issued reference/number already recorded in this account; inspect duplicate evidence.")
        if action in {"review-delivery", "adopt-dispatched"}:
            wf.exact(value["recipient"], {"channel", "address"}, "delivery recipient")
            if value["recipient"]["channel"] not in {"email", "portal", "post", "other"}:
                raise ws.WorkspaceError("Choose the observed delivery route.")
            wf.text(value["recipient"]["address"], "exact recipient destination")
            wf.strings(value["attachment_files"], "attachment files")
            if len(value["attachment_files"]) > 32:
                raise ws.WorkspaceError("At most 32 reviewed attachments are supported.")
        event = {"action": action, "actor": value["actor"], "note": value["note"],
                 "occurred_on": value["occurred_on"], "recorded_at": ws._now(),
                 "evidence": _snapshot(root, value["evidence_file"]), "attempt_id": value["attempt_id"],
                 "external_id": value["external_id"], "outcome_kind": value["outcome_kind"]}
        if action in ISSUED:
            event["document"] = _snapshot(root, value["document_file"])
            row["issued"] = {"external_id": value["external_id"], "invoice_number": value["invoice_number"],
                             "document": event["document"], "evidence": event["evidence"], "occurred_on": value["occurred_on"]}
        if action in {"review-delivery", "adopt-dispatched"}:
            event["attachments"] = [_snapshot(root, p) for p in value["attachment_files"]]
            delivery.update(package={"recipient": copy.deepcopy(value["recipient"]), "document": row["issued"]["document"],
                                     "scope_evidence": event["evidence"],
                                     "attachments": event["attachments"],
                                     "corrections_sha256": _delivery_context(root, row, state) if action == "review-delivery" else None}, attempt_id=None, external_id=None)
        if action in {"begin-issue", "begin-delivery", "adopt-dispatched"}:
            event["attempt_id"] = ("observed-" if action == "adopt-dispatched" else "attempt-") + uuid.uuid4().hex
            if is_delivery:
                delivery["attempt_id"] = event["attempt_id"]
            else:
                row["issue_attempt"] = event["attempt_id"]
        event["scope_sha256"] = st.digest(delivery["package"] if is_delivery else _issue_scope(row))
        if is_delivery:
            delivery["state"] = next_state
            if action in OUTCOMES or action == "adopt-dispatched":
                delivery["external_id"] = value["external_id"]
        else:
            row["state"] = next_state
        row["events"].append(event)
    return {"invoice_id": value["invoice_id"], "state": row["state"], "delivery_state": delivery["state"],
            "attempt_id": event["attempt_id"], "sha256": st.digest(row), "execution": "local_evidence_record_only"}


def _view(root, row, state, language):
    issues = []
    try:
        _check(root, row, state)
    except (OSError, ws.WorkspaceError) as exc:
        issues.append(str(exc))
    actions = []
    if not issues:
        actions = [a for a, (before, _) in ISSUE.items() if row["state"] in before]
        if row["state"] == "issued":
            actions += [a for a, (before, _) in DELIVERY.items() if row["delivery"]["state"] in before]
            for action in list(actions):
                if action in {"review-delivery", "authorize-delivery", "begin-delivery"}:
                    try:
                        _check_delivery(root, row, state, review=action == "review-delivery")
                    except (OSError, ws.WorkspaceError) as exc:
                        if str(exc) not in issues:
                            issues.append(str(exc))
                        actions.remove(action)
        if any(a in LIVE for a in actions):
            try:
                _check(root, row, state, live=True)
            except (OSError, ws.WorkspaceError) as exc:
                issues.append(str(exc))
                actions = [a for a in actions if a not in LIVE]
        for action in list(actions):
            try:
                _provider_issue(row, action)
            except ws.WorkspaceError as exc:
                if str(exc) not in issues:
                    issues.append(str(exc))
                actions.remove(action)
    return {"record": copy.deepcopy(row), "sha256": st.digest(row), "allowed_actions": actions,
            "issues": issues, "markdown": render(row, actions, issues, language)}


def show(root, identifier, language="en"):
    root = ws._workspace(root)
    with ws._locked(root):
        state = _load(root)
        if identifier not in state["invoices"]:
            raise ws.WorkspaceError("Invoice not found.")
        return _view(root, state["invoices"][identifier], state, language)


def list_invoices(root, language="en"):
    root = ws._workspace(root)
    with ws._locked(root):
        state = _load(root)
        views = [_view(root, row, state, language) for row in state["invoices"].values()]
        return {"invoices": [{"invoice_id": v["record"]["invoice_id"], "state": v["record"]["state"],
                              "provider_state": v["record"].get("provider", {}).get("state"),
                              "delivery_state": v["record"]["delivery"]["state"], "period": v["record"]["period"],
                              "allowed_actions": v["allowed_actions"], "issues": v["issues"]} for v in views],
                "markdown": "\n\n".join(v["markdown"] for v in views)}


def render(row, actions, issues, language):
    if language not in {"en", "ru"}:
        raise ws.WorkspaceError("Invoice report language must be en or ru.")
    ru = language == "ru"
    labels = {"draft": ("Draft", "Черновик"), "reviewed": ("Reviewed", "Проверено"),
              "issue_authorized": ("Issue authorized", "Выставление разрешено"),
              "issue_unconfirmed": ("Issuance outcome unknown — investigate before retry", "Результат выставления неизвестен — проверить до повтора"),
              "issue_failed": ("Confirmed not issued", "Подтверждено, что не выставлен"),
              "issued": ("Issued — recorded evidence", "Выставлен — по сохранённым подтверждениям"),
              "cancelled": ("Local draft cancelled", "Локальный черновик отменён"),
              "not_prepared": ("Delivery not prepared", "Доставка не подготовлена"),
              "delivery_reviewed": ("Delivery package reviewed", "Комплект доставки проверен"),
              "delivery_authorized": ("Delivery authorized", "Отправка разрешена"),
              "delivery_unconfirmed": ("Dispatch outcome unknown — do not resend", "Результат отправки неизвестен — не повторять"),
              "dispatched": ("Dispatched — receipt not confirmed", "Отправлено — получение не подтверждено"),
              "delivered": ("Delivered — recorded receipt evidence", "Доставлено — по подтверждению получения"),
              "delivery_failed": ("Delivery failed — inspect evidence before retry", "Доставка не удалась — проверить подтверждение до повтора")}
    def safe(value):
        text = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", " ").replace("\r", " ")
        return re.sub(r"([\\`*_{}\[\]()#!|])", r"\\\1", text)
    action_labels = {
        "review-issue": ("Review issue/correction scope", "Проверить выставление/исправление"),
        "authorize-issue": ("Record issue/correction authorization", "Записать разрешение на выставление/исправление"),
        "begin-issue": ("Record issue/correction attempt before acting", "Записать попытку перед выставлением/исправлением"),
        "confirm-issued": ("Record observed issue/correction result", "Записать наблюдаемый результат выставления/исправления"),
        "confirm-not-issued": ("Record confirmed absence of issue", "Записать подтверждение отсутствия выставления"),
        "adopt-issued": ("Record an already issued document", "Учесть уже выставленный документ"),
        "cancel": ("Cancel local unissued draft", "Отменить локальный невыставленный черновик"),
        "review-delivery": ("Review final files and destination", "Проверить итоговые файлы и адрес доставки"),
        "authorize-delivery": ("Record delivery authorization", "Записать разрешение на отправку"),
        "begin-delivery": ("Record delivery attempt before sending", "Записать попытку перед отправкой"),
        "confirm-dispatched": ("Record dispatch evidence", "Записать подтверждение отправки"),
        "adopt-dispatched": ("Record a dispatch already made outside this workflow", "Учесть отправку, уже выполненную вне этого сценария"),
        "confirm-delivered": ("Record receipt evidence", "Записать подтверждение получения"),
        "confirm-delivery-failed": ("Record confirmed delivery failure", "Записать подтверждённую неудачу доставки")}
    lines = ["# " + ("Счёт: " if ru else "Invoice: ") + safe(row["invoice_id"]), "",
             safe(row["system"]) + " / " + safe(row["account_reference"]), "",
             labels[row["state"]][ru], labels[row["delivery"]["state"]][ru], "",
             ("Клиент: " if ru else "Customer: ") + safe(row["customer_reference"]),
             ("Период: " if ru else "Period: ") + row["period"]]
    if row["issued"]:
        lines += [("Номер: " if ru else "Number: ") + safe(row["issued"]["invoice_number"] or ("новый номер не присвоен" if ru else "no new number assigned")),
                  ("Выставленный файл: " if ru else "Issued file: ") + safe(row["issued"]["document"]["path"])]
    if row["corrects"]:
        lines += [("Связанное исправление: " if ru else "Correction of: ") + safe(row["corrects"]) + " / " + safe(row["correction_kind"])]
    if row.get("provider"):
        p = row["provider"]
        provider_labels = {
            "prepared": ("Draft request prepared", "Запрос черновика подготовлен"),
            "authorized": ("Provider draft creation authorized; consumes a number", "Создание черновика разрешено; расходует номер"),
            "create_unconfirmed": ("Creation outcome unknown; do not repeat", "Результат создания неизвестен; не повторять"),
            "read_unconfirmed": ("Readback unconfirmed; inspect existing object", "Повторное чтение не подтверждено; проверить существующий объект"),
            "read_back": ("Readback awaiting review", "Данные провайдера ожидают проверки"),
            "reviewed": ("Provider readback reviewed", "Данные провайдера проверены"),
            "discrepancy": ("Provider discrepancy; investigate before continuing", "Расхождение с провайдером; разобраться до продолжения")}
        lines += [("Маршрут Lexware: " if ru else "Lexware route: ") + provider_labels[p["state"]][ru],
                  ("Объект провайдера: " if ru else "Provider object: ") + safe(p["external_id"] or "—"),
                  ("Отличия от запроса (проверить также значения по умолчанию): " if ru else "Differences from request (also inspect provider defaults): ") + "; ".join(safe(x) for x in p["differences"])]
        if p["readback"]:
            lines += [("Сохранённые данные провайдера: " if ru else "Preserved provider readback: ") + safe(p["readback"]["path"])]
    if row["delivery"]["package"]:
        recipient = row["delivery"]["package"]["recipient"]
        lines += [("Получатель: " if ru else "Destination: ") + safe(recipient["channel"]) + " / " + safe(recipient["address"])]
    lines += ["", ("Следующие локальные действия: " if ru else "Next local evidence actions: ") + "; ".join(action_labels[a][ru] for a in actions),
              "", ("Проблемы: " if ru else "Issues: ") + "; ".join(safe(i) for i in issues), "",
              ("Запись подтверждений, а не отправка, проверка налога или доказательство согласия/оплаты клиента."
               if ru else "Evidence tracking, not external execution, tax validation or proof of customer agreement/payment.")]
    lines += ["", "## " + ("История подтверждений" if ru else "Evidence history"), ""]
    for event in row["events"]:
        lines += ["- " + event["occurred_on"] + " — " + action_labels[event["action"]][ru] + "; " + safe(event["actor"]),
                  "  " + safe(event["note"]), "  " + safe(event["evidence"]["path"]) + " / SHA-256 " + event["evidence"]["sha256"]]
    return "\n".join(lines) + "\n"


def export(root, identifier, language="en"):
    root = ws._workspace(root)
    with ws._locked(root):
        state = _load(root)
        if identifier not in state["invoices"]:
            raise ws.WorkspaceError("Invoice not found.")
        view = _view(root, state["invoices"][identifier], state, language)
        relative = "08_correspondence/invoice-status-" + uuid.uuid4().hex + ".md"
        target = ws._inside(root, relative)
        ws._mkdir(target.parent)
        ws._write_exclusive(target, view["markdown"].encode("utf-8"))
        ws._audit(root, "invoice_status_exported", {"invoice_id": identifier, "record_sha256": view["sha256"], "path": relative})
    return {"path": ws._physical(root, relative), "record_sha256": view["sha256"]}
