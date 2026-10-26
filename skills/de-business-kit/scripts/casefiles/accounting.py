"""Onboarding choice, reviewed cash records and evidence-backed filing tracking.

No provider/ELSTER transport, statutory form calculation or credential handling.
"""
from contextlib import contextmanager
import calendar
from decimal import Decimal
import copy
import csv
import hashlib
import io
from pathlib import Path
import uuid

import workspace as ws
import workflows as wf
from . import documents as docs
from . import storage as st

STATE = "04_accounting/register.json"
STATES = {"draft", "reviewed", "authorized", "submission_unconfirmed", "submitted", "cancelled"}
PREFLIGHT_ACTIONS = {"draft": "review", "reviewed": "authorize", "authorized": "begin"}
ENTRY_VERSION = 2
# Entries recorded before line VAT existed have no schema_version; they stay readable, never postable.
LEGACY_LINE = {"kind", "amount", "category", "activity_id"}
VAT_STATUSES = {"stated", "none_stated", "unresolved"}


def template(kind):
    templates = {
        "configuration": {"system": None, "product": None, "account_reference": None,
                          "method": "unresolved", "reviewer": None, "evidence_file": None},
        "entry": {"schema_version": ENTRY_VERSION, "entry_id": None, "date": None, "account": None,
                  "transaction_id": None, "amount": None, "currency": None,
                  "lines": [{"kind": None, "amount": None, "category": None, "activity_id": None, "proposal_id": None,
                             "vat": {"status": "unresolved", "net": None, "tax": None, "rate": None}}],
                  "reviewer": None, "evidence_file": None, "note": None, "replaces": None},
        "filing": {"filing_id": None, "form": None, "form_version": None, "period": None,
                   "recipient": None, "payload_file": None, "source_files": [],
                   "unresolved_items": [], "supersedes": None},
        "filing-action": {"filing_id": None, "action": None, "actor": None,
                          "evidence_file": None, "note": None, "external_id": None,
                          "response_kind": None, "due_date": None},
    }
    if kind not in templates:
        raise ws.WorkspaceError("Unknown accounting template.")
    return copy.deepcopy(templates[kind])


def _load(root):
    path = ws._inside(root, STATE)
    ws._check_audit(root)
    history_id = next((event["details"]["history_id"] for event in reversed(ws._load(ws._inside(root, ws.EVENTS)))
                       if isinstance(event.get("details"), dict)
                       and isinstance(event["details"].get("history_id"), str)
                       and event["details"]["history_id"].startswith("accounting-")), None)
    if not path.exists():
        if history_id is not None:
            raise ws.WorkspaceError("Accounting register is missing but its history exists; recover it before continuing.")
        return {"schema_version": 1, "configuration": None, "entries": {}, "filings": {}}
    value = ws._load(path)
    wf.exact(value, {"schema_version", "configuration", "entries", "filings", "checksum"}, "accounting register")
    checksum = value.pop("checksum")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1 or checksum != st.digest(value):
        raise ws.WorkspaceError("Unsupported or changed accounting register; inspect preserved history, do not repair silently.")
    if not isinstance(value["entries"], dict) or not isinstance(value["filings"], dict):
        raise ws.WorkspaceError("Invalid accounting collections.")
    if history_id is None:
        raise ws.WorkspaceError("Accounting register has no completed audit checkpoint; inspect interrupted writes.")
    checkpoint = ws._load(ws._inside(root, "09_audit/history/" + st.identifier(history_id) + ".json"))
    if checkpoint.get("after_sha256") != checksum:
        raise ws.WorkspaceError("Accounting register and history disagree; inspect rollback or interrupted writes before continuing.")
    return value


@contextmanager
def _edit(root, action):
    with ws._locked(root):
        ws._check_audit(root)
        state = _load(root)
        before = copy.deepcopy(state)
        yield state
        if before == state:
            return
        saved = {**state, "checksum": st.digest(state)}
        if len(st.encoded(saved)) > ws.MAX_BYTES:
            raise ws.WorkspaceError("Accounting register exceeds supported size.")
        history = "accounting-" + uuid.uuid4().hex
        ws._atomic_json(ws._inside(root, "09_audit/history/" + history + ".json"),
                        {"action": action, "before": before, "after_sha256": st.digest(state)})
        ws._atomic_json(ws._inside(root, STATE), saved, replace=True)
        ws._audit(root, action, {"history_id": history})


def _config(root, state, local=False):
    value = state["configuration"]
    if value is None:
        raise ws.WorkspaceError("Choose local or existing-software accounting during onboarding first.")
    st.check_evidence(root, value["evidence"])
    if local:
        if value["system"] != "local" or value["method"] != "EÜR":
            raise ws.WorkspaceError("Local cash records require an explicitly chosen local EÜR workflow; external books stay authoritative.")
        fact = ws._load(ws._inside(root, ws.PROFILE))["facts"]["accounting_method"]
        if fact["value"] not in {None, "unresolved", "EÜR"} or fact["status"] == "needs_review":
            raise ws.WorkspaceError("Accounting method conflicts with the shared profile; resolve it before posting.")
    return value


def configure(root, value, expected=None):
    root = ws._workspace(root)
    wf.exact(value, template("configuration"), "accounting choice")
    if value["system"] not in {"local", "external"} or value["method"] not in {"EÜR", "Bilanzierung", "unresolved"}:
        raise ws.WorkspaceError("Choose local/external and an explicit accounting method or unresolved.")
    if value["system"] == "external":
        wf.text(value["product"], "exact accounting product and edition")
    elif value["product"] is not None:
        raise ws.WorkspaceError("Local accounting has no external product.")
    for key in ("account_reference", "reviewer"):
        wf.text(value[key], key)
    with _edit(root, "accounting_configured") as state:
        before = state["configuration"]
        st.version(before, expected)
        if state["entries"] or state["filings"]:
            raise ws.WorkspaceError("Existing accounting/filing records require a reviewed migration; configuration cannot switch their authority.")
        saved = {**copy.deepcopy(value), "evidence": st.evidence(root, value["evidence_file"])}
        state["configuration"] = saved
    return {"accounting_system": value["system"], "sha256": st.digest(saved)}


def _fields(entry):
    """Writer input of a saved entry, in the version it was recorded with."""
    keys = set(template("entry"))
    if "schema_version" not in entry:
        keys.discard("schema_version")
    return {key: entry[key] for key in keys}


def _vat(vat, amount):
    """Amounts as stated on the evidence; never derives VAT or decides its treatment."""
    wf.exact(vat, {"status", "net", "tax", "rate"}, "line VAT")
    if vat["status"] not in VAT_STATUSES:
        raise ws.WorkspaceError("Line VAT status must be stated, none_stated or unresolved.")
    if vat["status"] != "stated":
        if any(vat[key] is not None for key in ("net", "tax", "rate")):
            raise ws.WorkspaceError("Only stated VAT records net, VAT and rate; keep the others null.")
        return
    net, tax = (ws._amount(wf.text(vat[key], "stated " + key)) for key in ("net", "tax"))
    if ws._add(net, tax) != amount:
        raise ws.WorkspaceError("Stated net plus VAT must equal the line amount.")
    if any(part and (part < 0) != (amount < 0) for part in (net, tax)):
        raise ws.WorkspaceError("Stated net and VAT must keep the sign of the line amount.")
    if vat["rate"] is not None and not 0 <= ws._amount(wf.text(vat["rate"], "stated rate")) <= 100:
        raise ws.WorkspaceError("A stated VAT rate is a percentage between 0 and 100.")


def _entry(value, legacy=False):
    keys = set(template("entry"))
    if legacy:
        keys.discard("schema_version")
    elif (not isinstance(value, dict) or type(value.get("schema_version")) is not int
          or value["schema_version"] != ENTRY_VERSION):
        raise ws.WorkspaceError("Cash entries need schema_version 2 with line VAT status; start from accounting-template --kind entry.")
    wf.exact(value, keys, "cash entry")
    for key in ("entry_id", "account", "transaction_id"):
        st.identifier(value[key])
    for key in ("reviewer", "note"):
        wf.text(value[key], key)
    ws._day(value["date"])
    ws._currency(value["currency"])
    amount = ws._amount(value["amount"])
    if not isinstance(value["lines"], list) or not value["lines"]:
        raise ws.WorkspaceError("Cash records need classified or explicitly unresolved lines.")
    total = Decimal(0)
    for line in value["lines"]:
        wf.exact(line, LEGACY_LINE if legacy else LEGACY_LINE | {"proposal_id", "vat"}, "cash line")
        if line["kind"] not in {"income", "expense", "transfer", "unresolved"}:
            raise ws.WorkspaceError("Unsupported movement kind.")
        wf.text(line["category"], "reviewed category")
        wf.text(line["activity_id"], "activity reference")
        line_amount = ws._amount(wf.text(line["amount"], "line amount"))
        total = ws._add(total, line_amount)
        if not legacy:
            if line["proposal_id"] is not None:
                st.identifier(line["proposal_id"])
            _vat(line["vat"], line_amount)
    if total != amount:
        raise ws.WorkspaceError("Entry line amounts must equal the observed cash movement.")
    if value["replaces"] is not None:
        st.identifier(value["replaces"])


def _current(proposals):
    """Approved proposals not replaced by an approved correction."""
    replaced = {row["supersedes"] for row in proposals.values()
                if row["review"]["status"] == "approved" and row["supersedes"]}
    return {identifier: row for identifier, row in proposals.items()
            if row["review"]["status"] == "approved" and identifier not in replaced}


def linkable(root):
    """Current approved proposals a cash line may settle; caller holds the workspace lock."""
    def value(row, key):
        return row["fields"].get(key, {}).get("value")
    return [{"proposal_id": identifier, "document_id": row["document_id"], "activity_id": row["activity_id"],
             "period": row["period"], "invoice_number": value(row, "invoice_number"),
             "gross": value(row, "gross"), "currency": value(row, "currency")}
            for identifier, row in sorted(_current(st.load(root)["proposals"]).items())]


def _links(root, lines):
    """Fingerprint the current approved proposals that cash lines settle."""
    linked = [line for line in lines if line["proposal_id"] is not None]
    if not linked:
        return {}
    current = _current(st.load(root)["proposals"])
    result = {}
    for line in linked:
        identifier = line["proposal_id"]
        proposal = current.get(identifier)
        if proposal is None:
            raise ws.WorkspaceError("Link cash lines only to a current approved proposal; drafts, rejected and replaced proposals are not posted.")
        if proposal["activity_id"] != line["activity_id"]:
            raise ws.WorkspaceError("A linked cash line must keep the activity of its reviewed proposal.")
        if docs.original(root, proposal["document_id"])["sha256"] != proposal["original_sha256"]:
            raise ws.WorkspaceError("The reviewed original of a linked proposal changed; prepare a new review.")
        result[identifier] = st.digest(proposal)
    return result


def _check_links(root, entries):
    linked = [item for entry in entries for item in entry.get("linked_proposals", {}).items()]
    if not linked:
        return
    proposals = st.load(root)["proposals"]
    if any(identifier not in proposals or st.digest(proposals[identifier]) != fingerprint
           for identifier, fingerprint in linked):
        raise ws.WorkspaceError("A linked proposal changed or is missing; inspect preserved casework history before reporting.")


def post(root, value):
    root = ws._workspace(root)
    _entry(value)
    value = copy.deepcopy(value)
    value["account"] = value["account"].casefold()
    with _edit(root, "cash_entry_recorded") as state:
        _config(root, state, local=True)
        identifier = value["entry_id"]
        if identifier in state["entries"]:
            raise ws.WorkspaceError("Entry IDs are immutable; use a reversal and linked correction.")
        reversed_ids = {entry["reverses"] for entry in state["entries"].values() if entry["reverses"]}
        previous = state["entries"].get(value["replaces"])
        if value["replaces"] is not None:
            if previous is None or previous["entry_id"] not in reversed_ids or previous["reverses"]:
                raise ws.WorkspaceError("A replacement must reference a reversed original entry.")
            if any(entry["replaces"] == value["replaces"] for entry in state["entries"].values()):
                raise ws.WorkspaceError("This entry already has a replacement.")
            if any(value[key] != previous[key] for key in ("account", "transaction_id", "currency")):
                raise ws.WorkspaceError("A correction must retain the account, transaction reference and currency.")
        for entry in state["entries"].values():
            if (entry["account"].casefold(), entry["transaction_id"]) == (value["account"].casefold(), value["transaction_id"]):
                if not value["replaces"] or entry["entry_id"] not in reversed_ids and not entry["reverses"]:
                    raise ws.WorkspaceError("Duplicate account transaction; inspect and reverse before correcting.")
        saved = {**value, "reverses": None, "recorded_at": ws._now(), "evidence": st.evidence(root, value["evidence_file"]),
                 "linked_proposals": _links(root, value["lines"])}
        state["entries"][identifier] = saved
    return {"entry_id": identifier, "status": "recorded", "sha256": st.digest(saved)}


def reverse(root, entry_id, reversal_id, evidence_file, actor, note):
    root = ws._workspace(root)
    st.identifier(reversal_id)
    wf.text(actor, "reviewer")
    wf.text(note, "correction reason")
    with _edit(root, "cash_entry_reversed") as state:
        _config(root, state, local=True)
        original = state["entries"].get(entry_id)
        if original is None or original["reverses"] or reversal_id in state["entries"]:
            raise ws.WorkspaceError("Choose an existing original and a new reversal ID.")
        if any(entry["reverses"] == entry_id for entry in state["entries"].values()):
            raise ws.WorkspaceError("Entry already reversed.")
        st.check_evidence(root, original["evidence"])
        saved = copy.deepcopy(original)
        saved.update(entry_id=reversal_id, reverses=entry_id, replaces=None, reviewer=actor, note=note,
                     evidence_file=evidence_file, evidence=st.evidence(root, evidence_file), recorded_at=ws._now())
        saved["amount"] = format(ws._amount(original["amount"]).copy_negate(), "f")
        for line in saved["lines"]:
            line["amount"] = format(ws._amount(line["amount"]).copy_negate(), "f")
            vat = line.get("vat")  # Entries recorded before line VAT have none.
            if vat and vat["status"] == "stated":
                for key in ("net", "tax"):
                    vat[key] = format(ws._amount(vat[key]).copy_negate(), "f")
        state["entries"][reversal_id] = saved
    return {"entry_id": reversal_id, "reverses": entry_id, "sha256": st.digest(saved)}


def _in_period(day, period):
    if len(period) == 4:
        return day[:4] == period
    if "Q" in period:
        return day[:4] == period[:4] and (int(day[5:7]) - 1) // 3 + 1 == int(period[-1])
    return day[:7] == period


def _period_end(period):
    year = int(period[:4])
    month = 12 if len(period) == 4 else int(period[-1]) * 3 if "Q" in period else int(period[5:7])
    return f"{year:04d}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}"


def _settlement_basis(root, period, state):
    """Current reviewed evidence, with payments dated through the period end."""
    cutoff = _period_end(period)
    entries = [entry for entry in state["entries"].values() if entry["date"] <= cutoff
               and any(line.get("proposal_id") for line in entry["lines"])]
    proposals = st.load(root)["proposals"]
    reversed_ids = {entry["reverses"] for entry in entries if entry["reverses"]}
    linked = {line["proposal_id"] for entry in entries if not entry["reverses"] and entry["entry_id"] not in reversed_ids
              for line in entry["lines"] if line.get("proposal_id")}
    current = _current(proposals)
    selected = {key: row for key, row in proposals.items()
                if key in linked or key in current and row["period"] <= cutoff[:7]}
    _check_links(root, entries)
    for entry in entries:
        _entry(_fields(entry), legacy="schema_version" not in entry)
        st.check_evidence(root, entry["evidence"])
    for proposal in selected.values():
        if docs.original(root, proposal["document_id"])["sha256"] != proposal["original_sha256"]:
            raise ws.WorkspaceError("A settlement proposal original changed; inspect evidence before reporting.")
    return {"through": cutoff, "entries": entries, "proposals": selected,
            "current": sorted(set(selected) & set(current))}


def _settlements(basis):
    reversed_ids = {entry["reverses"] for entry in basis["entries"] if entry["reverses"]}
    active = [entry for entry in basis["entries"] if not entry["reverses"] and entry["entry_id"] not in reversed_ids]
    rows = []
    for identifier, proposal in sorted(basis["proposals"].items()):
        fields = proposal["fields"]
        value = lambda key: fields.get(key, {}).get("value")
        gross, currency = value("gross"), value("currency")
        issues, payments, kinds = [], [], set()
        allocated = Decimal(0)
        if identifier not in basis["current"]:
            issues.append("proposal_superseded")
        target = ws._amount(gross) if gross is not None else None
        if target is None or target < 0 or currency is None:
            issues.append("invoice_amount_unresolved")
        for entry in active:
            for index, line in enumerate(entry["lines"]):
                if line.get("proposal_id") != identifier:
                    continue
                payments.append({"entry_id": entry["entry_id"], "line": index + 1, "date": entry["date"],
                                 "amount": line["amount"], "currency": entry["currency"], "kind": line["kind"]})
                if entry["currency"] != currency:
                    issues.append("currency_mismatch")
                    continue
                if line["kind"] not in {"income", "expense"}:
                    issues.append("movement_unresolved")
                    continue
                kinds.add(line["kind"])
                amount = ws._amount(line["amount"])
                allocated = ws._add(allocated, amount if line["kind"] == "income" else amount.copy_negate())
        if len(kinds) > 1:
            issues.append("mixed_payment_directions")
        if allocated < 0:
            issues.append("refund_exceeds_payments")
        remaining = None if issues else ws._add(target, allocated.copy_negate())
        status = ("needs_review" if issues else "overpaid" if remaining < 0 else "balanced" if remaining == 0
                  else "unpaid" if allocated == 0 else "partial")
        rows.append({"proposal_id": identifier, "invoice_number": value("invoice_number"), "currency": currency,
                     "gross": gross, "allocated": format(allocated, "f"),
                     "remaining": None if remaining is None else format(remaining, "f"), "status": status,
                     "issues": sorted(set(issues)), "payments": payments})
    return rows


def period_report(root, period):
    root = ws._workspace(root)
    wf.period(period)
    with ws._locked(root):
        state = _load(root)
        return _period_report(root, period, state)


def _period_report(root, period, state):
    config = _config(root, state, local=True)
    selected = [entry for entry in state["entries"].values() if _in_period(entry["date"], period)]
    totals, categories, vat = {}, {}, {}
    unresolved = vat_unresolved = vat_not_recorded = False
    for entry in selected:
        legacy = "schema_version" not in entry
        _entry(_fields(entry), legacy=legacy)
        st.check_evidence(root, entry["evidence"])
        vat_not_recorded |= legacy
        row = totals.setdefault(entry["currency"], dict.fromkeys(("income", "expense", "transfer", "unresolved"), Decimal(0)))
        for line in entry["lines"]:
            amount = ws._amount(line["amount"])
            row[line["kind"]] = ws._add(row[line["kind"]], amount)
            key = (entry["currency"], line["kind"], line["category"], line["activity_id"])
            categories[key] = ws._add(categories.get(key, Decimal(0)), amount)
            unresolved |= line["kind"] == "unresolved"
            if legacy:
                continue
            vat_unresolved |= line["vat"]["status"] == "unresolved"
            if line["vat"]["status"] == "stated":
                rate = line["vat"]["rate"]
                # Group equal stated rates ("19", "19.00"); the entry keeps the text as stated.
                group = (entry["currency"], line["kind"], None if rate is None else format(ws._amount(rate).normalize(), "f"))
                net, tax = vat.get(group, (Decimal(0), Decimal(0)))
                vat[group] = (ws._add(net, ws._amount(line["vat"]["net"])), ws._add(tax, ws._amount(line["vat"]["tax"])))
    _check_links(root, selected)
    for row in totals.values():
        row["operating_cash_net"] = ws._add(row["income"], row["expense"])
    issues = ["coverage_not_confirmed", "statutory_adjustments_not_calculated", "tax_form_mapping_not_verified"]
    if not selected:
        issues.append("no_entries")
    if unresolved:
        issues.append("unclassified_movements")
    if vat_unresolved:
        issues.append("vat_unresolved")
    if vat_not_recorded:
        issues.append("vat_not_recorded")
    basis = _settlement_basis(root, period, state)
    settlements = _settlements(basis)
    for status in ("overpaid", "needs_review", "partial", "unpaid"):
        if any(row["status"] == status for row in settlements):
            issues.append("settlement_" + status)
    return {"schema_version": 2, "kind": "cash_movement_report", "period": period,
            "accounting_system": config["system"], "entries_sha256": st.digest(selected),
            "configuration_sha256": st.digest(config), "entries": selected,
            "totals": {currency: {key: format(value, "f") for key, value in row.items()} for currency, row in sorted(totals.items())},
            "categories": [{"currency": key[0], "kind": key[1], "category": key[2], "activity_id": key[3], "amount": format(value, "f")} for key, value in sorted(categories.items())],
            "vat": [{"currency": key[0], "kind": key[1], "rate": key[2], "net": format(value[0], "f"), "tax": format(value[1], "f")}
                    for key, value in sorted(vat.items(), key=lambda item: (item[0][0], item[0][1], item[0][2] or ""))],
            "settlements": settlements, "settlement_through": basis["through"], "settlement_basis_sha256": st.digest(basis),
            "readiness": "needs_review", "tax_return_status": "not_calculated", "open_items": issues}


def export_report(root, period):
    root = ws._workspace(root)
    report = period_report(root, period)
    relative = "07_exports/" + period + "/cash-report-" + uuid.uuid4().hex + ".json"
    language = ws._load(ws._inside(root, ws.MARKER)).get("language", "en")
    russian = language == "ru"
    title = "Отчёт о движении денег" if russian else "Cash movement report"
    boundary = ("Это движения по записанным операциям, не налогооблагаемая прибыль и не готовая декларация. "
                "Полнота счетов, налоговые корректировки и поля формы требуют отдельной проверки."
                if russian else "These are recorded cash movements, not taxable profit or a completed return. "
                "Account coverage, statutory adjustments and form fields require separate review.")
    labels = {"income": "Поступления" if russian else "Receipts", "expense": "Расходы" if russian else "Expenses",
              "transfer": "Перемещения" if russian else "Transfers", "unresolved": "Не классифицировано" if russian else "Unclassified",
              "operating_cash_net": "Разница поступлений и расходов" if russian else "Operating cash difference"}
    lines = ["# " + title, "", period, "", boundary, ""]
    for currency, totals in report["totals"].items():
        lines.extend(["## " + currency, ""])
        lines.extend("- " + labels[key] + ": " + value for key, value in totals.items())
        lines.append("")
        stated = [row for row in report["vat"] if row["currency"] == currency]
        if stated:
            lines.extend(["## " + ("НДС по документам" if russian else "VAT as stated on documents") + " (" + currency + ")", "",
                          "Суммы, указанные в документах; не декларация по НДС и не решение о налоговом режиме."
                          if russian else "Amounts as stated on the evidence; not a VAT return or a treatment decision.", ""])
            for row in stated:
                rate = row["rate"] + " %" if row["rate"] is not None else ("ставка не указана" if russian else "rate not stated")
                lines.append("- " + labels[row["kind"]] + " · " + rate + (": нетто " if russian else ": net ") + row["net"]
                             + (", НДС " if russian else ", VAT ") + row["tax"])
            lines.append("")
    if "vat_unresolved" in report["open_items"]:
        lines.extend(["НДС по некоторым строкам ещё не определён; они входят в денежные итоги, но не в суммы НДС по документам." if russian
                      else "VAT is not yet determined for some lines; they are in the cash totals but not in any stated VAT figures.", ""])
    if "vat_not_recorded" in report["open_items"]:
        lines.extend(["Некоторые записи сделаны до учёта НДС; чтобы указать НДС, сторнируйте их и создайте связанную замену." if russian
                      else "Some entries were recorded before VAT capture; reverse them and post a linked replacement to record VAT.", ""])
    if not report["entries"]:
        lines.append("Операции за период отсутствуют." if russian else "No entries supplied for this period.")
    if report["settlements"]:
        lines.extend(["", "## " + ("Распределение платежей по счетам" if russian else "Invoice payment allocation"), "",
                      ("Платежи по дату " if russian else "Payments through ") + report["settlement_through"],
                      "Сверка записанных сумм; не подтверждение оплаты во внешней системе. Валюты не конвертируются."
                      if russian else "Reconciles recorded amounts; does not confirm payment in an external system. No currency conversion.", ""])
        statuses = {"balanced": "Суммы совпадают", "partial": "Частичная оплата", "unpaid": "Нет распределённых платежей",
                    "overpaid": "Переплата", "needs_review": "Нужна проверка"} if russian else {
                        "balanced": "Amounts match", "partial": "Partly allocated", "unpaid": "No payments allocated",
                        "overpaid": "Overallocated", "needs_review": "Needs review"}
        for row in report["settlements"]:
            lines.append("- " + (row["invoice_number"] or row["proposal_id"]) + " (" + (row["currency"] or "—") + "): "
                         + statuses[row["status"]])
            lines.extend(["  " + label + ": " + (row[key] or "—") for key, label in (
                              ("gross", "По счёту" if russian else "Invoice"),
                              ("allocated", "Распределено в валюте счёта" if russian else "Allocated in invoice currency"),
                              ("remaining", "Остаток" if russian else "Remaining"))])
            if row["issues"]:
                messages = st.template("casework-messages.json")["ru" if russian else "en"]["codes"]
                lines.extend("  - " + messages.get("settlement_" + issue, issue) for issue in row["issues"])
    markdown = relative[:-5] + ".md"
    ledger_files = {}
    with ws._locked(root):
        ws._check_audit(root)
        path = ws._inside(root, relative)
        ws._mkdir(path.parent)
        ws._atomic_json(path, report)
        ws._write_exclusive(ws._inside(root, markdown), ("\n".join(lines) + "\n").encode("utf-8"))
        for account in sorted({entry["account"] for entry in report["entries"]}):
            stream = io.StringIO(newline="")
            writer = csv.DictWriter(stream, fieldnames=("entry_id", "transaction_id", "amount", "currency"), lineterminator="\n")
            writer.writeheader()
            for entry in report["entries"]:
                if entry["account"] == account:
                    writer.writerow({key: entry[key] for key in writer.fieldnames})
            target = relative[:-5] + "-" + hashlib.sha256(account.encode("utf-8")).hexdigest()[:16] + ".csv"
            ws._write_exclusive(ws._inside(root, target), stream.getvalue().encode("utf-8"))
            ledger_files[account] = ws._physical(root, target)
        ws._audit(root, "cash_report_prepared", {"path": relative, "period": period})
    return {"path": ws._physical(root, relative), "markdown_path": ws._physical(root, markdown), "ledger_files": ledger_files,
            "readiness": "needs_review", "tax_return_status": "not_calculated"}


def _snapshot(root, path, year):
    source = st.evidence(root, path)
    data = ws._read_regular(ws._inside(root, source["path"]))
    if hashlib.sha256(data).hexdigest() != source["sha256"]:
        raise ws.WorkspaceError("Evidence changed during capture.")
    suffix = Path(path).suffix.lower()
    if suffix not in {".json", ".csv", ".xml", ".pdf", ".md", ".txt", ".png", ".jpg"}:
        raise ws.WorkspaceError("Unsupported filing evidence format; do not supply credentials or certificates.")
    relative = "05_tax/" + year + "/filing-evidence/" + uuid.uuid4().hex + suffix
    target = ws._inside(root, relative)
    ws._mkdir(target.parent)
    ws._write_exclusive(target, data)
    return {"path": ws._physical(root, relative), "sha256": source["sha256"], "source": source}


def _check_snapshots(root, record):
    sources = [record["payload"], *record["sources"], *(event["evidence"] for event in record["events"])]
    for source in sources:
        st.check_evidence(root, source)


def _local_report_evidence(root, source, payload, state):
    if Path(source["path"]).suffix != ".json":
        return []
    report = ws._load(ws._inside(root, source["path"]))
    if not isinstance(report, dict) or report.get("kind") != "cash_movement_report":
        return []
    if payload:
        raise ws.WorkspaceError("A cash-movement summary is supporting evidence, not a completed tax return payload.")
    wf.period(report.get("period"))
    entries = [entry for entry in state["entries"].values() if _in_period(entry["date"], report["period"])]
    if (report.get("entries_sha256") != st.digest(entries)
            or report.get("configuration_sha256") != st.digest(state["configuration"])):
        raise ws.WorkspaceError("Source cash report is stale; regenerate it and prepare a newly reviewed filing version.")
    _check_links(root, entries)
    if "settlement_basis_sha256" in report:
        basis = _settlement_basis(root, report["period"], state)
        if report["settlement_basis_sha256"] != st.digest(basis):
            raise ws.WorkspaceError("Source settlement report is stale; regenerate it and prepare a newly reviewed filing version.")
        entries = list({entry["entry_id"]: entry for entry in [*entries, *basis["entries"]]}.values())
    return [entry["evidence"] for entry in entries]


def _scope(record):
    return tuple(str(record[key]).strip().casefold() for key in ("account_reference", "form", "period"))


def create_filing(root, value):
    root = ws._workspace(root)
    wf.exact(value, template("filing"), "filing draft")
    st.identifier(value["filing_id"])
    if value["form"] not in {form["id"] for form in wf.catalog()["forms"]}:
        raise ws.WorkspaceError("Choose the catalogue form ID (for example ustva, not its German display label); inspect workflows.py catalog. The catalogue does not establish a filing obligation.")
    for key in ("form_version", "recipient"):
        wf.text(value[key], key)
    wf.period(value["period"])
    wf.strings(value["source_files"], "source files")
    wf.strings(value["unresolved_items"], "unresolved items")
    if not value["source_files"]:
        raise ws.WorkspaceError("A filing draft needs source evidence.")
    with _edit(root, "filing_draft_recorded") as state:
        config = _config(root, state)
        identifier = value["filing_id"]
        if identifier in state["filings"]:
            raise ws.WorkspaceError("Filing versions are immutable; create a linked replacement.")
        candidate = {**copy.deepcopy(value), "account_reference": config["account_reference"]}
        prior = state["filings"].get(value["supersedes"])
        if value["supersedes"] is not None:
            if prior is None or _scope(prior) != _scope(candidate) or prior["state"] not in {"submitted", "cancelled"}:
                raise ws.WorkspaceError("Replace only a submitted/cancelled filing for the same account, form and period.")
            if any(row["supersedes"] == prior["filing_id"] for row in state["filings"].values()):
                raise ws.WorkspaceError("This filing already has a replacement; inspect the latest version.")
        for row in state["filings"].values():
            if _scope(row) != _scope(candidate):
                continue
            if row["state"] not in {"submitted", "cancelled"} or prior is None:
                raise ws.WorkspaceError("A filing for this account/form/period already exists; resolve its outcome before any replacement.")
        year = value["period"][:4]
        payload = _snapshot(root, value["payload_file"], year)
        sources = [_snapshot(root, path, year) for path in value["source_files"]]
        saved = {**candidate, "system": config["system"], "product": config["product"],
                 "configuration_sha256": st.digest(config), "payload": payload, "sources": sources,
                 "state": "draft", "events": [], "receipt": None, "responses": [], "created_at": ws._now()}
        state["filings"][identifier] = saved
    return {"filing_id": identifier, "state": "draft", "sha256": st.digest(saved)}


def get_filing(root, identifier):
    root = ws._workspace(root)
    with ws._locked(root):
        record = _load(root)["filings"].get(identifier)
        if record is None:
            raise ws.WorkspaceError("Filing not found.")
        _check_snapshots(root, record)
        return {"record": record, "sha256": st.digest(record)}


def _filing_issues(root, record, state, live):
    """Shared local gates; callers hold the workspace lock. Never assess tax law."""
    issues = []

    def check(code, operation, path=None):
        try:
            operation()
        except (OSError, ws.WorkspaceError) as exc:
            issues.append({"code": code, "path": path, "detail": str(exc)})
            return False
        return True

    sources = [record["payload"], *record["sources"]]
    intact = set()
    for source in [*sources, *(event["evidence"] for event in record["events"])]:
        if check("snapshot_changed", lambda: st.check_evidence(root, source), source["path"]):
            intact.add(source["path"])
    if live:
        for source in sources:
            check("source_changed", lambda: st.check_evidence(root, source["source"]), source["source"]["path"])
        check("configuration_evidence", lambda: _config(root, state))
        if st.digest(state["configuration"]) != record["configuration_sha256"]:
            issues.append({"code": "configuration_changed", "path": STATE,
                           "detail": "Prepare a new filing version against the current accounting configuration."})
        issues.extend({"code": "unresolved_item", "path": None, "detail": item}
                      for item in record["unresolved_items"])
        for source in sources:
            # A broken snapshot must not hide independent intact report failures.
            if source["path"] not in intact:
                continue
            try:
                evidence = _local_report_evidence(root, source, source is record["payload"], state)
            except (OSError, ws.WorkspaceError) as exc:
                issues.append({"code": "local_report_invalid", "path": source["source"]["path"], "detail": str(exc)})
                continue
            for item in evidence:
                check("local_entry_evidence", lambda: st.check_evidence(root, item), item["path"])
    return issues


def check_filing(root, identifier):
    """Read-only readiness snapshot, not approval or an external transmission check."""
    root = ws._workspace(root)
    with ws._locked(root):
        state = _load(root)
        return _check_filing(root, identifier, state)


def _check_filing(root, identifier, state):
    record = state["filings"].get(identifier)
    if record is None:
        raise ws.WorkspaceError("Filing not found.")
    current = record["state"]
    if current not in STATES:
        raise ws.WorkspaceError("Unknown filing state; inspect preserved history.")
    action = PREFLIGHT_ACTIONS.get(current)
    issues = _filing_issues(root, record, state, live=action is not None)
    next_step = action or {"submission_unconfirmed": "resolve_submission_outcome",
                           "submitted": "follow_up", "cancelled": "prepare_replacement"}[current]
    return {"filing_id": identifier, "state": current, "sha256": st.digest(record),
            "accounting_system": record["system"], "product": record["product"],
            "form": record["form"], "form_version": record["form_version"],
            "period": record["period"], "recipient": record["recipient"],
            "payload_sha256": record["payload"]["sha256"],
            "source_scope": "frozen_and_current_evidence" if action else "frozen_evidence_only",
            "issues": issues, "next_step": "resolve_issues" if issues else next_step,
            "allowed_preflight_actions": [action] if action and not issues else [],
            "tax_correctness": "not_assessed", "transmission": "not_implemented",
            "scope": "Local evidence and state only. Actions need their own evidence and current hash; "
                     "this snapshot grants no approval or external permission. Actions recheck current sources."}


def filing_action(root, value, expected):
    root = ws._workspace(root)
    wf.exact(value, template("filing-action"), "filing action")
    for key in ("actor", "note"):
        wf.text(value[key], key)
    if value["due_date"] is not None:
        ws._day(value["due_date"])
    action = value["action"]
    transitions = {"review": ("draft", "reviewed"), "authorize": ("reviewed", "authorized"),
                   "begin": ("authorized", "submission_unconfirmed"),
                   "not-submitted": ("submission_unconfirmed", "reviewed"),
                   "receipt": ("submission_unconfirmed", "submitted"), "response": ("submitted", "submitted")}
    with _edit(root, "filing_" + str(action)) as state:
        record = state["filings"].get(value["filing_id"])
        if record is None:
            raise ws.WorkspaceError("Filing not found.")
        st.version(record, expected)
        if action not in PREFLIGHT_ACTIONS.values():
            _check_snapshots(root, record)
        if action == "cancel":
            if record["state"] not in {"draft", "reviewed", "authorized"}:
                raise ws.WorkspaceError("An attempted/submitted filing cannot be cancelled locally; investigate the external result.")
            next_state = "cancelled"
        elif action in transitions:
            before, next_state = transitions[action]
            if record["state"] != before:
                raise ws.WorkspaceError("Invalid filing transition; inspect current state and evidence before proceeding.")
        else:
            raise ws.WorkspaceError("Unknown filing action.")
        if action in PREFLIGHT_ACTIONS.values():
            issues = _filing_issues(root, record, state, live=True)
            if issues:
                raise ws.WorkspaceError("Filing preflight blocked: " + "; ".join(
                    item["code"] + ": " + item["detail"] for item in issues))
        if action == "receipt":
            wf.text(value["external_id"], "actual transmission reference")
            if any(row["receipt"] and row["receipt"]["external_id"] == value["external_id"] for row in state["filings"].values()):
                raise ws.WorkspaceError("Transmission reference already recorded; inspect duplicate evidence.")
        elif value["external_id"] is not None:
            raise ws.WorkspaceError("External reference belongs only to receipt recording.")
        if action == "response":
            if value["response_kind"] not in {"acknowledgement", "request_for_information", "assessment", "rejection", "other"}:
                raise ws.WorkspaceError("Record the observed response type; do not infer acceptance.")
        elif value["response_kind"] is not None or value["due_date"] is not None:
            raise ws.WorkspaceError("Response metadata requires an actual response.")
        evidence = _snapshot(root, value["evidence_file"], record["period"][:4])
        event = {"action": action, "actor": value["actor"], "note": value["note"], "recorded_at": ws._now(),
                 "evidence": evidence, "payload_sha256": record["payload"]["sha256"],
                 "external_id": value["external_id"], "response_kind": value["response_kind"], "due_date": value["due_date"]}
        record["events"].append(event)
        record["state"] = next_state
        if action == "receipt":
            record["receipt"] = event
        elif action == "response":
            record["responses"].append(event)
    return {"filing_id": value["filing_id"], "state": record["state"], "sha256": st.digest(record),
            "execution": "local_evidence_record_only"}


def status(root):
    root = ws._workspace(root)
    with ws._locked(root):
        state = _load(root)
        config = state["configuration"]
        return {"accounting_system": config["system"] if config else "undecided",
                "configuration_sha256": st.digest(config) if config else None,
                "product": config["product"] if config else None,
                "method": config["method"] if config else "unresolved",
                "entry_count": len(state["entries"]),
                "filings": [{"filing_id": row["filing_id"], "form": row["form"], "period": row["period"],
                             "state": row["state"], "responses": len(row["responses"])} for row in state["filings"].values()],
                "transmission": "not_implemented", "tax_form_calculations": "not_implemented"}


def overview_state(root, period, state=None, filing_checks=None):
    """Projection for overview; caller holds the workspace lock across all reads."""
    state = _load(root) if state is None else state
    config = state["configuration"]
    result = {"accounting_system": config["system"] if config else "undecided",
              "product": config["product"] if config else None,
              "method": config["method"] if config else "unresolved",
              "period_entry_count": None, "totals": {}, "issues": [], "settlements": [],
              "coverage": "not_confirmed", "tax_return_status": "not_calculated"}
    if config:
        try:
            _config(root, state)
            if config["system"] == "local":
                report = _period_report(root, period, state)
                result.update(period_entry_count=len(report["entries"]), totals=report["totals"], settlements=report["settlements"],
                              settlement_through=report["settlement_through"],
                              issues=[{"code": code} for code in report["open_items"]])
        except (OSError, ws.WorkspaceError) as exc:
            result["issues"].append({"code": "accounting_evidence", "detail": str(exc)})
    filings = []
    for identifier, record in sorted(state["filings"].items()):
        # Uncertain attempts and dated authority responses remain visible across months.
        if (_in_period(period + "-01", record["period"])
                or record["state"] == "submission_unconfirmed"
                or any(event.get("due_date") for event in record["responses"])):
            check = copy.deepcopy(filing_checks[identifier]) if filing_checks is not None else _check_filing(root, identifier, state)
            check["responses"] = [{"kind": event["response_kind"], "due_date": event["due_date"],
                                    "evidence_path": event["evidence"]["path"]}
                                   for event in record["responses"]]
            filings.append(check)
    return result, filings
