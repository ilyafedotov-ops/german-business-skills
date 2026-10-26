"""Catalog metadata and receipt events without moving or rewriting originals."""
import hashlib
from pathlib import Path
import uuid

import workspace as ws
import workflows as wf
from . import storage as st

TYPES = {"unknown", "invoice", "credit_note", "bank_statement", "contract", "authority_letter", "registration_receipt", "receipt", "other"}
RELATIONS = {"corrects", "possible_duplicate_of", "attachment_of", "structured_data_for", "preview_of", "validation_for"}
DATES = {"invoice", "service_from", "service_to", "received", "due", "paid"}


def original(root, identifier):
    docs = [item for item in ws._documents(root)["documents"] if item.get("document_id") == identifier]
    if len(docs) != 1:
        raise ws.WorkspaceError("Document ID must identify one preserved original.")
    doc = docs[0]
    period = ws._period(doc.get("period"))
    path = ws._inside(root, doc.get("path"))
    if (path.parent != ws._path(root, f"06_bookkeeping/{period[:4]}/{period[5:]}/originals")
            or path.stem != doc.get("sha256") or path.suffix not in ws.EXTENSIONS):
        raise ws.WorkspaceError("Invalid indexed original path; run workspace verify.")
    data = ws._read_regular(path)
    if len(data) != doc.get("size_bytes") or hashlib.sha256(data).hexdigest() != doc.get("sha256"):
        raise ws.WorkspaceError("Original content changed; no catalog write or export is safe.")
    return doc


def blank(doc):
    return {"schema_version": 1, "document_id": doc["document_id"], "title": doc["original_name"],
            "type": "unknown", "activity_ids": [], "periods": [doc["period"]],
            "dates": dict.fromkeys(sorted(DATES)), "review_status": "new", "reviewer": None, "review_note": None,
            "links": {"task_ids": [], "question_ids": [], "decision_ids": [], "payment_refs": [], "correspondence_ids": []}, "relations": []}


def get(root, identifier):
    root = ws._workspace(root)
    doc = original(root, identifier)
    return st.load(root)["documents"].get(identifier, blank(doc))


def validate(root, record):
    doc = original(root, record.get("document_id") if isinstance(record, dict) else None)
    wf.exact(record, blank(doc), "catalog record")
    if type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise ws.WorkspaceError("Unsupported catalog record version.")
    wf.text(record["title"], "readable document title")
    if wf.text(record["type"], "document type") not in TYPES:
        raise ws.WorkspaceError("Unknown document type.")
    wf.strings(record["activity_ids"], "activity_ids")
    for month in wf.strings(record["periods"], "periods"):
        ws._period(month)
    if not record["periods"]:
        raise ws.WorkspaceError("A catalog record needs at least one organizational period.")
    wf.exact(record["dates"], DATES, "document dates")
    for value in record["dates"].values():
        if value is not None:
            ws._day(value)
    if (record["dates"]["service_from"] and record["dates"]["service_to"]
            and record["dates"]["service_from"] > record["dates"]["service_to"]):
        raise ws.WorkspaceError("Service period ends before it starts.")
    if wf.text(record["review_status"], "review status") not in {"new", "needs_review", "reviewed", "excluded"}:
        raise ws.WorkspaceError("Unknown catalog review status.")
    if record["review_status"] in {"reviewed", "excluded"}:
        wf.text(record["reviewer"], "reviewer")
        wf.text(record["review_note"], "review note / exclusion reason")
    for key in ("reviewer", "review_note"):
        if record[key] is not None:
            wf.text(record[key], key)
    wf.exact(record["links"], {"task_ids", "question_ids", "decision_ids", "payment_refs", "correspondence_ids"}, "catalog links")
    for key, values in record["links"].items():
        wf.strings(values, key)
        if key in {"task_ids", "question_ids", "decision_ids"}:
            collection = {"task_ids": "tasks", "question_ids": "questions", "decision_ids": "decisions"}[key]
            available = ws._load(ws._inside(root, "00_admin/" + collection + ".json"))
            known = {item.get("id") for item in available if isinstance(item, dict)}
            if not set(values) <= known:
                raise ws.WorkspaceError("Unknown linked task/decision.")
        elif key == "correspondence_ids":
            for value in values:
                original(root, value)
    if not isinstance(record["relations"], list):
        raise ws.WorkspaceError("relations must be a list.")
    seen = set()
    for relation in record["relations"]:
        wf.exact(relation, {"relation", "document_id"}, "document relation")
        if wf.text(relation["relation"], "relation") not in RELATIONS or relation["document_id"] == doc["document_id"]:
            raise ws.WorkspaceError("Unsupported or self-referencing document relation.")
        original(root, relation["document_id"])
        key = (relation["relation"], relation["document_id"])
        if key in seen:
            raise ws.WorkspaceError("Duplicate document relation.")
        seen.add(key)
    return doc


def save(root, record, expected=None):
    root = ws._workspace(root)
    with st.edit(root, "catalog_updated", {"document_id": record.get("document_id")}) as state:
        validate(root, record)
        identifier = record["document_id"]
        st.version(state["documents"].get(identifier), expected)
        state["documents"][identifier] = record
    return {"document_id": identifier, "sha256": st.digest(record), "status": record["review_status"]}


def receive(root, source, period, received_on, kind="unknown", title=None):
    root = ws._workspace(root)
    ws._day(received_on)
    if kind not in TYPES:
        raise ws.WorkspaceError("Unknown document type.")
    if title is not None:
        wf.text(title, "title")
    imported = ws.ingest_document(root, source, period)
    identifier = imported["document_id"]
    with st.edit(root, "document_received", {"document_id": identifier}) as state:
        doc = original(root, identifier)
        if identifier not in state["documents"]:
            record = blank(doc)
            record.update(type=kind, title=title or doc["original_name"])
            record["dates"]["received"] = received_on
            state["documents"][identifier] = record
        state["receipts"].append({"receipt_id": "receipt-" + uuid.uuid4().hex, "document_id": identifier,
            "received_on": received_on, "recorded_at": ws._now(), "original_name": Path(source).name,
            "intake_period": period, "content_sha256": doc["sha256"], "result": imported["status"]})
        version = st.digest(state["documents"][identifier])
    return {**imported, "receipt_recorded": True, "sha256": version, "period": period}


def catalog(root, period=None):
    root = ws._workspace(root)
    if period is not None:
        ws._period(period)
    state = st.load(root)
    result = []
    for doc in ws._documents(root)["documents"]:
        row = state["documents"].get(doc["document_id"], blank(doc))
        if period is None or period in row["periods"]:
            result.append(row)
    return sorted(result, key=lambda row: (row["title"].casefold(), row["document_id"]))
