"""Explicit bank CSV mapping, immutable preview, and evidenced import approval."""
import csv
from datetime import datetime
from decimal import Decimal
import hashlib
import io
import re
import uuid

import workspace as ws
import workflows as wf
from . import documents as docs
from . import storage as st

CSV_FIELDS = ("transaction_id", "booking_date", "amount", "currency", "source_row", "source_reference")


def mapping_template():
    return {"schema_version": 1, "mapping_id": None, "account_id": None, "delimiter": ";", "encoding": "utf-8-sig",
            "date_format": "%d.%m.%Y", "decimal_separator": ",", "grouping_separator": ".", "amount_mode": "signed",
            "sign": "as_is", "default_currency": None,
            "columns": dict.fromkeys(("transaction_id", "date", "amount", "credit", "debit", "currency", "reference"))}


def validate(mapping):
    wf.exact(mapping, mapping_template(), "bank mapping")
    if type(mapping["schema_version"]) is not int or mapping["schema_version"] != 1:
        raise ws.WorkspaceError("Unsupported bank mapping version.")
    st.identifier(mapping["mapping_id"])
    st.identifier(mapping["account_id"])
    for key, values in {"delimiter": {",", ";", "\t"}, "encoding": {"utf-8", "utf-8-sig", "cp1252"},
                        "date_format": {"%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%m/%d/%Y"},
                        "decimal_separator": {".", ","}, "grouping_separator": {"", ".", ",", " "},
                        "amount_mode": {"signed", "credit_debit"}, "sign": {"as_is", "invert"}}.items():
        if not isinstance(mapping[key], str) or mapping[key] not in values:
            raise ws.WorkspaceError("Unsupported explicit mapping option: " + key)
    if mapping["decimal_separator"] == mapping["grouping_separator"]:
        raise ws.WorkspaceError("Decimal and grouping separators must differ.")
    wf.exact(mapping["columns"], mapping_template()["columns"], "column mapping")
    names = [value for value in mapping["columns"].values() if value is not None]
    for value in names:
        wf.text(value, "column name")
    if len(names) != len(set(names)):
        raise ws.WorkspaceError("Each mapped source column must have one role.")
    columns = mapping["columns"]
    if not columns["date"] or (mapping["amount_mode"] == "signed" and not columns["amount"]):
        raise ws.WorkspaceError("Date and signed amount columns are required.")
    if mapping["amount_mode"] == "credit_debit" and (not columns["credit"] or not columns["debit"] or mapping["sign"] != "as_is"):
        raise ws.WorkspaceError("Credit/debit mapping requires both unsigned columns and as_is sign.")
    if mapping["default_currency"] is not None:
        ws._currency(wf.text(mapping["default_currency"], "default currency"))
    if not columns["currency"] and not mapping["default_currency"]:
        raise ws.WorkspaceError("Map currency or explicitly declare the account currency.")


def amount(raw, mapping):
    raw = raw.strip()
    sign = ""
    if raw.startswith(("+", "-")):
        sign, raw = raw[0], raw[1:]
    parts = raw.split(mapping["decimal_separator"])
    if len(parts) > 2 or not parts[0] or len(parts) == 2 and not parts[1]:
        raise ws.WorkspaceError("Invalid decimal amount in bank export.")
    whole = parts[0]
    separator = mapping["grouping_separator"]
    if separator and separator in whole:
        groups = whole.split(separator)
        if not (1 <= len(groups[0]) <= 3 and groups[0].isdigit() and all(len(g) == 3 and g.isdigit() for g in groups[1:])):
            raise ws.WorkspaceError("Ambiguous or malformed grouping in bank amount.")
        whole = "".join(groups)
    normalized = sign + whole + ("." + parts[1] if len(parts) == 2 else "")
    return ws._amount(normalized)


def normalize(data, mapping, period):
    validate(mapping)
    ws._period(period)
    try:
        reader = csv.DictReader(io.StringIO(data.decode(mapping["encoding"]), newline=""), delimiter=mapping["delimiter"])
        headers = reader.fieldnames
        required = {name for name in mapping["columns"].values() if name is not None}
        if not headers or len(headers) != len(set(headers)) or not required <= set(headers):
            raise ws.WorkspaceError("Missing or duplicate source headers; inspect the mapping.")
        raw_rows = list(reader)
    except (UnicodeError, csv.Error) as exc:
        raise ws.WorkspaceError("Bank export does not match its declared encoding/delimiter.") from exc
    if any(None in row or any(value is None for value in row.values()) for row in raw_rows):
        raise ws.WorkspaceError("Bank CSV rows do not match all declared columns.")
    rows, ids = [], set()
    columns = mapping["columns"]
    namespace = hashlib.sha256(mapping["account_id"].encode()).hexdigest()[:16]
    file_hash = hashlib.sha256(data).hexdigest()
    for index, row in enumerate(raw_rows, 2):
        try:
            booking = datetime.strptime(row[columns["date"]].strip(), mapping["date_format"]).date().isoformat()
        except ValueError as exc:
            raise ws.WorkspaceError("A bank date does not match the explicitly selected date format.") from exc
        if booking[:7] != period:
            raise ws.WorkspaceError("Every bank row must belong to the selected month; no rows were silently discarded.")
        if mapping["amount_mode"] == "signed":
            value = amount(row[columns["amount"]], mapping)
            if mapping["sign"] == "invert":
                value = value.copy_negate()
        else:
            credit, debit = [amount(row[columns[key]], mapping) if row[columns[key]].strip() else Decimal(0) for key in ("credit", "debit")]
            if credit < 0 or debit < 0 or credit and debit:
                raise ws.WorkspaceError("Credit/debit columns must be unsigned, with at most one nonzero value per row.")
            value = ws._add(credit, debit.copy_negate())
        currency = row[columns["currency"]].strip() if columns["currency"] else mapping["default_currency"]
        ws._currency(currency)
        native = row[columns["transaction_id"]].strip() if columns["transaction_id"] else file_hash + ":row:" + str(index)
        if not native or any(ord(char) < 32 for char in native):
            raise ws.WorkspaceError("Bank transaction IDs must be nonempty and contain no control characters.")
        identifier = namespace + ":" + native
        if identifier in ids:
            raise ws.WorkspaceError("Duplicate account transaction ID; no import performed.")
        ids.add(identifier)
        rows.append({"transaction_id": identifier, "booking_date": booking, "amount": format(value, "f"), "currency": currency,
                     "source_row": index, "source_reference": row[columns["reference"]] if columns["reference"] else ""})
    issues = [] if columns["transaction_id"] else ["generated_row_ids_need_overlap_review"]
    if not rows:
        issues.append("empty_bank_export")
    return rows, issues


def preview(root, document_id, mapping, period):
    root = ws._workspace(root)
    doc = docs.original(root, document_id)
    data = ws._read_regular(ws._inside(root, doc["path"]))
    rows, issues = normalize(data, mapping, period)
    report = {"schema_version": 1, "kind": "bank_mapping_preview", "document_id": document_id,
              "source": {"path": doc["path"], "sha256": doc["sha256"]}, "mapping": mapping,
              "period": period, "rows": rows, "issues": issues}
    relative = f"07_exports/{period}/bank-preview-{uuid.uuid4().hex}.json"
    with ws._locked(root):
        ws._check_audit(root)
        path = ws._inside(root, relative)
        ws._mkdir(path.parent)
        ws._atomic_json(path, report)
        ws._audit(root, "bank_mapping_previewed", {"path": relative, "document_id": document_id})
    return {"path": relative, "sha256": st.evidence(root, relative)["sha256"], "rows": len(rows), "issues": issues}


def approve(root, preview_path, expected, reviewer, evidence_file):
    root = ws._workspace(root)
    wf.text(reviewer, "mapping reviewer")
    with st.edit(root, "bank_mapping_approved", {}) as state:
        fingerprint = st.evidence(root, preview_path)
        if fingerprint["sha256"] != expected:
            raise ws.WorkspaceError("Preview changed; inspect it before applying the mapping.")
        report = ws._load(ws._inside(root, fingerprint["path"]))
        wf.exact(report, {"schema_version", "kind", "document_id", "source", "mapping", "period", "rows", "issues"}, "bank preview")
        if report["schema_version"] != 1 or report["kind"] != "bank_mapping_preview":
            raise ws.WorkspaceError("Unsupported bank preview.")
        doc = docs.original(root, report["document_id"])
        if report["source"] != {"path": doc["path"], "sha256": doc["sha256"]}:
            raise ws.WorkspaceError("Original does not match the reviewed preview.")
        rows, issues = normalize(ws._read_regular(ws._inside(root, doc["path"])), report["mapping"], report["period"])
        if rows != report["rows"] or issues != report["issues"] or not rows:
            raise ws.WorkspaceError("Preview rows are changed or empty; regenerate and review.")
        identity = st.digest({"source": report["source"], "account_id": report["mapping"]["account_id"], "period": report["period"]})
        if identity in state["bank_imports"]:
            raise ws.WorkspaceError("This source/mapping was already imported; reuse the existing normalized file.")
        ids = {row["transaction_id"] for row in rows}
        for previous in state["bank_imports"].values():
            if previous["account_id"] != report["mapping"]["account_id"]:
                continue
            st.check_evidence(root, previous["normalized"])
            previous_rows = ws._rows(ws._read_regular(ws._inside(root, previous["normalized"]["path"])), set(CSV_FIELDS))
            if ids & {row["transaction_id"] for row in previous_rows}:
                raise ws.WorkspaceError("Bank export overlaps existing account transaction IDs; review duplicates or conflicting values before import.")
        proof = st.evidence(root, evidence_file)
        # Avoid spreadsheet-formula cells in the normalized CSV: human reference
        # text is preserved in the preview/original, not exported as active cells.
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            safe = dict(row)
            reference = safe["source_reference"]
            if reference.lstrip().startswith(("=", "+", "-", "@")):
                safe["source_reference"] = "'" + reference
            writer.writerow(safe)
        relative = f"03_banking/normalized/{identity}.csv"
        path = ws._inside(root, relative)
        ws._mkdir(path.parent)
        ws._write_exclusive(path, stream.getvalue().encode("utf-8"))
        saved = {"import_id": identity, "period": report["period"], "document_id": doc["document_id"],
                 "account_id": report["mapping"]["account_id"], "preview": fingerprint,
                 "normalized": st.evidence(root, relative), "reviewer": reviewer, "review_evidence": proof,
                 "row_count": len(rows), "issues": issues}
        state["bank_imports"][identity] = saved
    return {"import_id": identity, "csv_path": relative, "status": "mapping_review_recorded", "issues": issues}
