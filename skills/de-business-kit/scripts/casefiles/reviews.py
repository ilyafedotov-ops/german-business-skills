"""Extraction, proposals, source checks and separately observed provider state."""
from datetime import date
from decimal import Decimal, localcontext, ROUND_HALF_UP
import json
import re

import workspace as ws
import workflows as wf
from . import documents as docs
from . import storage as st

AMOUNTS = {"net", "tax", "gross", "amount_due", "quantity", "unit_price", "tax_rate"}
DATE_FIELDS = {"invoice_date", "due_date", "service_from", "service_to", "receipt_date", "payment_date"}
FIELDS = AMOUNTS | DATE_FIELDS | {"invoice_number", "supplier_reference", "customer_reference", "supplier_country", "customer_country", "currency", "description"}
CORE = {"invoice_number", "invoice_date", "currency", "net", "tax", "gross"}
SOURCE_KEYS = {"schema_version", "source_check_id", "url", "title", "checked_on", "applicable_period", "assumptions", "conclusion", "review_after", "reviewer", "evidence_file"}


def proposal_template():
    return st.template("proposal.json")


def save_source_check(root, record):
    root = ws._workspace(root)
    wf.exact(record, SOURCE_KEYS, "source check")
    if type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise ws.WorkspaceError("Unsupported source-check version.")
    identifier = st.identifier(record["source_check_id"])
    for key in ("title", "conclusion", "reviewer"):
        wf.text(record[key], key)
    if not isinstance(record["url"], str) or not re.fullmatch(r"https://[^\s/]+/[^\s]*", record["url"]):
        raise ws.WorkspaceError("Source checks require an HTTPS primary-source URL.")
    wf.strings(record["assumptions"], "assumptions")
    ws._day(record["checked_on"])
    ws._day(record["review_after"])
    wf.period(record["applicable_period"])
    if record["review_after"] < record["checked_on"]:
        raise ws.WorkspaceError("Source review date precedes the check.")
    with st.edit(root, "source_check_recorded", {"source_check_id": identifier}) as state:
        if identifier in state["source_checks"]:
            raise ws.WorkspaceError("Source checks are immutable; use a new ID for a new assessment.")
        saved = {**record, "evidence": st.evidence(root, wf.text(record["evidence_file"], "evidence_file"))}
        state["source_checks"][identifier] = saved
    return {"source_check_id": identifier, "sha256": st.digest(saved)}


def source_for_period(root, source, period, as_of=None):
    wf.exact(source, SOURCE_KEYS | {"evidence"}, "saved source check")
    st.check_evidence(root, source["evidence"])
    if source["applicable_period"] not in {period, period[:4]}:
        raise ws.WorkspaceError("Source check does not explicitly cover this proposal period.")
    if source["review_after"] < (as_of or date.today().isoformat()):
        raise ws.WorkspaceError("Source review is overdue; record a refreshed check for this period.")


def validate_field(name, field, approving):
    if name not in FIELDS:
        raise ws.WorkspaceError("Unsupported extracted field: " + name)
    wf.exact(field, {"raw", "value", "location", "status", "reviewer", "note"}, "extracted field")
    if wf.text(field["status"], "field status") not in {"extracted", "reviewed", "unavailable", "rejected"}:
        raise ws.WorkspaceError("Unknown extracted-field status.")
    for key in ("raw", "value", "location", "reviewer", "note"):
        if field[key] is not None:
            wf.text(field[key], key)
    if field["value"] is not None:
        wf.text(field["raw"], "original wording")
        wf.text(field["location"], "source location")
        if name in AMOUNTS:
            number = ws._amount(field["value"])
            if name == "tax_rate" and not 0 <= number <= 100:
                raise ws.WorkspaceError("Tax rate must be an explicit percentage between 0 and 100.")
        elif name in DATE_FIELDS:
            ws._day(field["value"])
        elif name == "currency":
            ws._currency(field["value"])
    if field["status"] == "reviewed":
        wf.text(field["reviewer"], "field reviewer")
        wf.text(field["value"], "reviewed value")
    if field["status"] == "unavailable":
        if field["value"] is not None:
            raise ws.WorkspaceError("Unavailable extraction must have a null normalized value.")
        wf.text(field["note"], "reason unavailable")
    if approving and field["status"] not in {"reviewed", "unavailable"}:
        raise ws.WorkspaceError("Every supplied extraction requires review before approval.")
    if approving and field["status"] == "unavailable":
        wf.text(field["reviewer"], "reviewer accepting unavailable field")


def arithmetic(record):
    def number(row, key):
        value = row.get(key, {}).get("value")
        return ws._amount(value) if value is not None else None
    fields, problems = record["fields"], []
    net, tax, gross = (number(fields, key) for key in ("net", "tax", "gross"))
    if None in (net, tax, gross):
        problems.append("invoice_totals_incomplete")
    elif ws._add(net, tax) != gross:
        problems.append("net_plus_tax_differs_from_gross")
    def product_matches(left, right, actual, percent=False):
        # Inputs are bounded to 200 decimal characters by workspace._amount.
        # Check at the precision explicitly supplied for the result; this is
        # not a determination of the applicable statutory rounding policy.
        with localcontext() as context:
            context.prec = 1000
            computed = left * right / (Decimal(100) if percent else Decimal(1))
            return computed.quantize(Decimal(1).scaleb(actual.as_tuple().exponent), rounding=ROUND_HALF_UP) == actual
    for collection, keys in (("lines", ("net", "tax", "gross")), ("tax_breakdown", ("net", "tax"))):
        rows = record[collection]
        if not rows:
            continue
        for key in keys:
            values = [number(row["fields"], key) for row in rows]
            if any(value is None for value in values):
                problems.append(collection + "_incomplete_" + key)
            else:
                total = Decimal(0)
                for value in values:
                    total = ws._add(total, value)
                if total != number(fields, key):
                    problems.append(collection + "_sum_differs_" + key)
        if collection == "lines":
            for row in rows:
                n, t, g = (number(row["fields"], key) for key in ("net", "tax", "gross"))
                if None not in (n, t, g) and ws._add(n, t) != g:
                    problems.append("line_total_differs:" + row["line_id"])
                quantity, price = (number(row["fields"], key) for key in ("quantity", "unit_price"))
                if None not in (quantity, price, n) and not product_matches(quantity, price, n):
                    problems.append("line_pricing_or_adjustment_unresolved:" + row["line_id"])
        for row in rows:
            n, rate, t = (number(row["fields"], key) for key in ("net", "tax_rate", "tax"))
            if None not in (n, rate, t) and not product_matches(n, rate, t, percent=True):
                problems.append("tax_rate_or_rounding_unresolved:" + row.get("line_id", row.get("tax_id")))
    return problems


def validate_proposal(root, state, record, check_current_sources=True):
    wf.exact(record, proposal_template(), "proposal")
    if type(record["schema_version"]) is not int or record["schema_version"] != 2:
        raise ws.WorkspaceError("Proposal v2 required; preserve old templates and prepare a new reviewed record.")
    identifier = st.identifier(record["proposal_id"])
    doc = docs.original(root, record["document_id"])
    ws._period(record["period"])
    wf.text(record["activity_id"], "activity_id")
    wf.exact(record["review"], {"status", "reviewer", "reviewed_on", "note"}, "proposal review")
    status = wf.text(record["review"]["status"], "review status")
    if status not in {"draft", "needs_review", "approved", "rejected"}:
        raise ws.WorkspaceError("Unknown proposal status.")
    approving = status == "approved"
    if status in {"approved", "rejected"}:
        wf.text(record["review"]["reviewer"], "proposal reviewer")
        wf.text(record["review"]["note"], "review outcome")
        ws._day(record["review"]["reviewed_on"])
    for key in ("reviewer", "note"):
        if record["review"][key] is not None:
            wf.text(record["review"][key], key)
    if record["review"]["reviewed_on"] is not None:
        ws._day(record["review"]["reviewed_on"])
    if not isinstance(record["fields"], dict):
        raise ws.WorkspaceError("fields must be an object.")
    for name, field in record["fields"].items():
        validate_field(name, field, approving)
    if approving and (not CORE <= set(record["fields"]) or any(record["fields"][key]["status"] != "reviewed" for key in CORE)):
        raise ws.WorkspaceError("Approval needs reviewed invoice number/date/currency and net/tax/gross.")
    for collection, id_key, allowed in (("lines", "line_id", {"description", "quantity", "unit_price", "net", "tax_rate", "tax", "gross"}),
                                        ("tax_breakdown", "tax_id", {"tax_rate", "net", "tax"})):
        if not isinstance(record[collection], list):
            raise ws.WorkspaceError(collection + " must be a list.")
        seen = set()
        for row in record[collection]:
            wf.exact(row, {id_key, "fields"}, collection + " item")
            key = st.identifier(row[id_key])
            if key in seen:
                raise ws.WorkspaceError("Duplicate line/tax breakdown ID.")
            seen.add(key)
            if not isinstance(row["fields"], dict) or not set(row["fields"]) <= allowed:
                raise ws.WorkspaceError("Unsupported line/tax breakdown fields.")
            for name, field in row["fields"].items():
                validate_field(name, field, approving)
    treatment = record["proposed_treatment"]
    wf.exact(treatment, {"category", "tax_rule", "reason", "source_check_ids"}, "proposed treatment")
    for key in ("category", "tax_rule", "reason"):
        if approving or treatment[key] is not None:
            wf.text(treatment[key], key)
    source_ids = wf.strings(treatment["source_check_ids"], "source_check_ids")
    if approving and not source_ids:
        raise ws.WorkspaceError("Tax-treatment approval needs period-specific source evidence.")
    for source_id in source_ids:
        if source_id not in state["source_checks"]:
            raise ws.WorkspaceError("Unknown source-check ID.")
        if approving and check_current_sources:
            source_for_period(root, state["source_checks"][source_id], record["period"])
    if record["supersedes"] is not None:
        if record["supersedes"] == identifier or record["supersedes"] not in state["proposals"]:
            raise ws.WorkspaceError("Correction must link a distinct existing proposal.")
        if state["proposals"][record["supersedes"]]["review"]["status"] not in {"approved", "rejected"}:
            raise ws.WorkspaceError("Finish reviewing the previous proposal before superseding it.")
    problems = arithmetic(record)
    if approving and problems:
        raise ws.WorkspaceError("Proposal arithmetic unresolved: " + ", ".join(problems))
    return doc, problems


def save_proposal(root, record, expected=None):
    root = ws._workspace(root)
    if not isinstance(record, dict):
        raise ws.WorkspaceError("Proposal must be an object.")
    record = json.loads(json.dumps(record, allow_nan=False))
    with st.edit(root, "proposal_saved", {"proposal_id": record.get("proposal_id")}) as state:
        doc, problems = validate_proposal(root, state, record)
        identifier = record["proposal_id"]
        before = state["proposals"].get(identifier)
        st.version(before, expected)
        if before is None and record["review"]["status"] != "draft":
            raise ws.WorkspaceError("New proposals start as draft before review.")
        if before and before["review"]["status"] in {"approved", "rejected"}:
            raise ws.WorkspaceError("Reviewed outcomes are immutable; create a linked correction.")
        saved = {**record, "original_sha256": doc["sha256"], "provider_state": "unknown", "arithmetic_issues": problems}
        state["proposals"][identifier] = saved
    return {"proposal_id": identifier, "sha256": st.digest(saved), "status": record["review"]["status"], "arithmetic_issues": problems}


def observe(root, record):
    root = ws._workspace(root)
    keys = {"observation_id", "proposal_id", "provider", "provider_record_id", "observed_status", "observed_on", "reviewer", "evidence_file"}
    wf.exact(record, keys, "provider observation")
    for key in keys - {"observed_on"}:
        wf.text(record[key], key)
    identifier = st.identifier(record["observation_id"])
    ws._day(record["observed_on"])
    with st.edit(root, "provider_state_observed", {"observation_id": identifier}) as state:
        if identifier in state["observations"] or record["proposal_id"] not in state["proposals"]:
            raise ws.WorkspaceError("Observation needs a new ID and an existing proposal.")
        saved = {**record, "evidence": st.evidence(root, record["evidence_file"])}
        state["observations"][identifier] = saved
    return {"observation_id": identifier, "sha256": st.digest(saved), "scope": "Recorded evidence only; no provider write executed."}
