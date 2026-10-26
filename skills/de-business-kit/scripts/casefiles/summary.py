"""Read-only projection used by the overview and optional records archive."""
from datetime import date
import re

import workspace as ws
import workflows as wf
from . import documents as docs
from . import reviews
from . import storage as st


def reconciliation_reports(root, period):
    directory = ws._path(root, "07_exports/" + period)
    ws._check_chain(directory)
    if not directory.exists():
        return []
    latest = {}
    for path in sorted(directory.iterdir()):
        if not re.fullmatch(r"reconciliation-[0-9a-f]{32}\.json", path.name):
            continue
        report = ws._load(ws._inside(root, path))
        if (not isinstance(report, dict) or report.get("schema_version") != 1 or report.get("period") != period
                or not isinstance(report.get("sources"), dict) or set(report["sources"]) != {"bank", "ledger"}):
            raise ws.WorkspaceError("Invalid reconciliation report; inspect before export.")
        for key in ("matches", "differences", "unmatched_bank", "unmatched_ledger", "unlinked_ledger_entries", "review_notes"):
            if not isinstance(report.get(key), list):
                raise ws.WorkspaceError("Invalid reconciliation result lists.")
        key = tuple(report["sources"][name]["path"] for name in ("bank", "ledger"))
        stamp = str(report.get("created_at", ""))
        item = {"path": path.relative_to(root).as_posix(), "report": report, "current": True}
        try:
            for source in report["sources"].values():
                st.check_evidence(root, source)
            computed = ws.reconciliation_report(root, report["sources"]["bank"]["path"], report["sources"]["ledger"]["path"], period)
            if {k: v for k, v in report.items() if k != "created_at"} != {k: v for k, v in computed.items() if k != "created_at"}:
                item["current"] = False
                item["report"] = computed
        except (OSError, ws.WorkspaceError):
            item["current"] = False
        if key not in latest or stamp > latest[key][0]:
            latest[key] = (stamp, item)
    return [item for _, item in sorted(latest.values(), key=lambda pair: pair[1]["path"])]


def task_work(root, tasks):
    """Project existing tasks; completion dependencies require current evidence.

    Input has already passed the canonical register and graph validation. Keep
    missing/changed evidence scoped to its task so independent work can continue.
    No state, evidence hash or authorization is changed by this view.
    """
    evidence = {}
    for item in tasks:
        try:
            ws._entry_valid(root, "tasks", item)
            evidence[item["id"]] = "checked" if item.get("evidence_file") else "not_recorded"
        except (OSError, ws.WorkspaceError):
            evidence[item["id"]] = "needs_review"
    by_id = {item["id"]: item for item in tasks}
    active = []
    for item in tasks:
        if item["status"] in {"completed", "cancelled"}:
            continue
        # Inspect the entire dependency ancestry without recursion or state writes.
        ancestors = set()
        remaining = list(item.get("depends_on", []))
        while remaining:
            dependency = remaining.pop()
            if dependency not in ancestors:
                ancestors.add(dependency)
                remaining.extend(by_id[dependency].get("depends_on", []))
        pending = sorted(dep for dep in ancestors
                         if by_id[dep]["status"] != "completed" or evidence[dep] != "checked")
        needs_review = any(evidence[key] == "needs_review" for key in ancestors | {item["id"]})
        readiness = ("needs_review" if needs_review else
                     "blocked" if item["status"] == "blocked" or pending else "ready")
        active.append({**{key: item.get(key) for key in
                         ("id", "title", "owner", "status", "due_date", "deadline_source", "note")},
                       "evidence_status": evidence[item["id"]], "pending_dependencies": pending,
                       "readiness": readiness})
    active.sort(key=lambda item: (item["due_date"] or "9999-12-31",
                                 item["status"] != "in_progress", item["id"]))
    return active, next((item["id"] for item in active if item["readiness"] == "ready"), None)


def collect(root, period, as_of=None, selected_ids=None):
    root = ws._workspace(root)
    ws._period(period)
    as_of = ws._day(as_of or date.today().isoformat())
    state = st.load(root)
    catalog = docs.catalog(root)
    selected = [item for item in catalog if item["document_id"] in selected_ids] if selected_ids is not None else [item for item in catalog if period in item["periods"]]
    identifiers = {item["document_id"] for item in selected}
    problems = []
    for item in selected:
        docs.validate(root, item)
        if item["review_status"] not in {"reviewed", "excluded"}:
            problems.append({"code": "document_review_open", "ref": item["document_id"]})
        if item["type"] == "unknown":
            problems.append({"code": "document_type_unknown", "ref": item["document_id"]})
    proposals = [record for record in state["proposals"].values() if record["document_id"] in identifiers]
    replaced = {record["supersedes"] for record in proposals if record["review"]["status"] == "approved" and record["supersedes"]}
    for proposal in proposals:
        wf.exact(proposal, set(reviews.proposal_template()) | {"original_sha256", "provider_state", "arithmetic_issues"}, "saved proposal")
        _, arithmetic = reviews.validate_proposal(root, state, {key: proposal[key] for key in reviews.proposal_template()}, check_current_sources=False)
        if proposal["provider_state"] != "unknown" or proposal["arithmetic_issues"] != arithmetic:
            raise ws.WorkspaceError("Saved proposal derived state is inconsistent; preserve and inspect it.")
        source = docs.original(root, proposal["document_id"])
        if proposal["original_sha256"] != source["sha256"]:
            raise ws.WorkspaceError("Proposal original fingerprint does not match preserved document.")
        if proposal["proposal_id"] in replaced:
            continue
        if proposal["review"]["status"] != "approved":
            problems.append({"code": "proposal_review_open", "ref": proposal["proposal_id"]})
        for source_id in proposal["proposed_treatment"]["source_check_ids"]:
            if source_id not in state["source_checks"]:
                raise ws.WorkspaceError("Proposal links a missing source-check record.")
            try:
                reviews.source_for_period(root, state["source_checks"][source_id], proposal["period"], as_of)
            except (OSError, ws.WorkspaceError):
                problems.append({"code": "source_review_open", "ref": source_id})
    for item in selected:
        if item["type"] in {"invoice", "credit_note", "receipt"} and item["review_status"] != "excluded":
            active = [p for p in proposals if p["document_id"] == item["document_id"] and p["proposal_id"] not in replaced]
            if not active:
                problems.append({"code": "proposal_missing", "ref": item["document_id"]})
            elif len([p for p in active if p["review"]["status"] == "approved"]) > 1:
                problems.append({"code": "multiple_approved_proposals", "ref": item["document_id"]})
    tasks = ws._entries(root, "tasks", check_evidence=False)
    questions = ws._entries(root, "questions", check_evidence=False)
    decisions = ws._entries(root, "decisions", check_evidence=False)
    task_rows, next_task_id = task_work(root, tasks)
    active_tasks = [item for item in tasks if item["status"] not in {"completed", "cancelled"}]
    overdue = [item for item in active_tasks if item.get("due_date") and item.get("deadline_source") and item["due_date"] < as_of]
    dated_tasks = sorted((item for item in active_tasks if item.get("due_date") and item.get("deadline_source")), key=lambda item: (item["due_date"], item["id"]))
    for item in overdue:
        problems.append({"code": "task_date_overdue", "ref": item["id"]})
    bank_imports = [item for item in state["bank_imports"].values() if item["period"] == period]
    reports = reconciliation_reports(root, period)
    if selected_ids is not None:
        omitted_imports = [item for item in bank_imports if item["document_id"] not in identifiers]
        omitted_sources = {item["normalized"]["sha256"] for item in omitted_imports}
        omitted_sources.update(docs.original(root, row["document_id"])["sha256"] for row in catalog if row["document_id"] not in identifiers)
        reports = [item for item in reports if not any(source["sha256"] in omitted_sources for source in item["report"]["sources"].values())]
        bank_imports = [item for item in bank_imports if item["document_id"] in identifiers]
    if not reports and (bank_imports or any(item["type"] in {"invoice", "credit_note", "receipt", "bank_statement"} for item in selected)):
        problems.append({"code": "reconciliation_not_supplied", "ref": period})
    unmatched = 0
    for item in reports:
        report = item["report"]
        if not item["current"]:
            problems.append({"code": "reconciliation_sources_changed", "ref": item["path"]})
        count = sum(len(report[name]) for name in ("differences", "unmatched_bank", "unmatched_ledger", "unlinked_ledger_entries"))
        unmatched += count
        if count or report["review_notes"]:
            problems.append({"code": "reconciliation_items_open", "ref": item["path"], "count": count})
    for item in bank_imports:
        for key in ("preview", "normalized", "review_evidence"):
            st.check_evidence(root, item[key])
        if item["issues"]:
            problems.append({"code": "bank_import_review_note", "ref": item["import_id"]})
    return {"schema_version": 1, "period": period, "as_of": as_of, "documents": selected, "proposals": proposals,
            "workspace_has_documents": bool(catalog),
            "tasks": tasks, "active_tasks": task_rows, "next_task_id": next_task_id, "questions": questions, "decisions": decisions, "overdue_tasks": overdue, "dated_tasks": dated_tasks,
            "reports": reports, "bank_imports": bank_imports, "open_items": sorted(problems, key=lambda row: (row["code"], row["ref"])),
            "counts": {"documents": len(selected), "awaiting_review": sum(item["review_status"] in {"new", "needs_review"} for item in selected),
                       "approved_proposals": sum(p["review"]["status"] == "approved" and p["proposal_id"] not in replaced for p in proposals),
                       "overdue_tasks": len(overdue), "unmatched_items": unmatched if reports else None, "bank_imports": len(bank_imports)}}
