"""Deterministic optional personal records archive and bounded manifest verification."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import uuid
import zipfile

import workspace as ws
from . import documents as docs
from . import storage as st
from . import summary

MAX_FILES = 10000
MAX_TOTAL = 500 * 1024 * 1024


def safe_name(value):
    if (not isinstance(value, str) or not value or "\\" in value or ":" in value
            or value.startswith("/") or any(part in {"", ".", ".."} for part in value.split("/"))):
        raise ws.WorkspaceError("Unsafe bundle path.")
    return value


def verify(path):
    path = ws._absolute(path)
    ws._check_chain(path, final_file=path.suffix == ".zip")
    archive = None
    if path.suffix == ".zip":
        archive = zipfile.ZipFile(path)
        infos = archive.infolist()
        names = [safe_name(item.filename) for item in infos]
        if len(set(names)) != len(names) or len(names) > MAX_FILES or sum(item.file_size for item in infos) > MAX_TOTAL:
            archive.close()
            raise ws.WorkspaceError("Duplicate or oversized archive inventory.")
        if any(item.file_size > ws.MAX_BYTES or stat.S_ISLNK(item.external_attr >> 16) for item in infos):
            archive.close()
            raise ws.WorkspaceError("Archive contains an oversized or linked entry.")
        def read(name):
            return archive.read(name)
    else:
        names, pending = [], [path]
        while pending:
            parent = pending.pop()
            ws._check_chain(parent)
            for item in parent.iterdir():
                info = item.lstat()
                if stat.S_ISLNK(info.st_mode):
                    raise ws.WorkspaceError("Bundle symlinks are not allowed.")
                if stat.S_ISDIR(info.st_mode):
                    pending.append(item)
                elif stat.S_ISREG(info.st_mode):
                    names.append(safe_name(item.relative_to(path).as_posix()))
                else:
                    raise ws.WorkspaceError("Bundle contains a non-regular entry.")
                if len(names) + len(pending) > MAX_FILES:
                    raise ws.WorkspaceError("Bundle inventory exceeds supported size.")
        def read(name):
            return ws._read_regular(ws._inside(path, name))
    try:
        if "manifest.json" not in names:
            raise ws.WorkspaceError("Bundle has no manifest.")
        manifest = ws._json_bytes(read("manifest.json"))
        if not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1 or not isinstance(manifest.get("files"), list):
            raise ws.WorkspaceError("Unsupported bundle manifest.")
        expected, errors, total = set(), [], 0
        for entry in manifest["files"]:
            if not isinstance(entry, dict) or not {"path", "sha256", "size_bytes", "role"} <= set(entry):
                raise ws.WorkspaceError("Invalid manifest file entry.")
            name = safe_name(entry["path"])
            if name in expected or name == "manifest.json" or not isinstance(entry["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
                raise ws.WorkspaceError("Duplicate path or invalid manifest fingerprint.")
            if type(entry["size_bytes"]) is not int or not 0 <= entry["size_bytes"] <= ws.MAX_BYTES:
                raise ws.WorkspaceError("Invalid manifest size.")
            expected.add(name)
            total += entry["size_bytes"]
            if total > MAX_TOTAL:
                raise ws.WorkspaceError("Bundle exceeds supported total size.")
            if name not in names:
                errors.append({"path": name, "issue": "missing"})
                continue
            payload = read(name)
            if len(payload) != entry["size_bytes"] or hashlib.sha256(payload).hexdigest() != entry["sha256"]:
                errors.append({"path": name, "issue": "changed"})
        for name in sorted(set(names) - expected - {"manifest.json"}):
            errors.append({"path": name, "issue": "unlisted"})
        return {"status": "failed" if errors else "verified", "files": len(expected), "errors": errors,
                "scope": "Manifest and packaged bytes only; not authenticity, tax correctness, DATEV compatibility or filing or authority acceptance."}
    finally:
        if archive:
            archive.close()


def build(root, period, as_of=None):
    root = ws._workspace(root)
    period = ws._period(period)
    with ws._locked(root):
        ws._check_audit(root)
        state = st.load(root)
        catalog = {row["document_id"]: row for row in docs.catalog(root)}
        selected = {key for key, row in catalog.items() if period in row["periods"] and row["review_status"] != "excluded"}
        excluded_related = set()
        component_relations = {"attachment_of", "structured_data_for", "preview_of", "validation_for"}
        changed = True
        while changed:
            changed = False
            candidates = set()
            for identifier in selected:
                candidates.update(link["document_id"] for link in catalog[identifier]["relations"])
                candidates.update(catalog[identifier]["links"]["correspondence_ids"])
            for identifier, row in catalog.items():
                if any(link["relation"] in component_relations and link["document_id"] in selected for link in row["relations"]):
                    candidates.add(identifier)
            for identifier in candidates - selected:
                if identifier not in catalog:
                    raise ws.WorkspaceError("Related document is absent from the catalog.")
                if catalog[identifier]["review_status"] == "excluded":
                    excluded_related.add(identifier)
                else:
                    selected.add(identifier)
                    changed = True
        # Known omitted originals/derivatives must not reenter through evidence aliases.
        omitted_hashes = {docs.original(root, key)["sha256"] for key in catalog if key not in selected}
        for imported in state["bank_imports"].values():
            if imported["document_id"] not in selected:
                omitted_hashes.update(imported[key]["sha256"] for key in ("preview", "normalized", "review_evidence"))
        snapshot = summary.collect(root, period, as_of, selected)
        linked = {key: set() for key in ("task_ids", "question_ids", "decision_ids")}
        for identifier in selected:
            for key in linked:
                linked[key].update(catalog[identifier]["links"][key])
        records = {"catalog": snapshot["documents"], "proposals": snapshot["proposals"],
                   "receipts": [row for row in state["receipts"] if row["document_id"] in selected]}
        for key, collection in (("task_ids", "tasks"), ("question_ids", "questions"), ("decision_ids", "decisions")):
            records[collection] = [row for row in snapshot[collection] if row["id"] in linked[key]]
        problems = [row for row in snapshot["open_items"] if row["code"] != "task_date_overdue" or row["ref"] in linked["task_ids"]]
        problems.extend({"code": "excluded_related_document", "ref": key} for key in sorted(excluded_related))
        unlinked_questions = [row for row in snapshot["questions"] if row["status"] != "resolved" and row["id"] not in linked["question_ids"]]
        if unlinked_questions:
            problems.append({"code": "unlinked_open_questions", "ref": str(len(unlinked_questions))})
        source_ids = {key for row in snapshot["proposals"] for key in row["proposed_treatment"]["source_check_ids"]}
        records["source_checks"] = [state["source_checks"][key] for key in sorted(source_ids)]
        proposal_ids = {row["proposal_id"] for row in snapshot["proposals"]}
        records["provider_observations"] = [row for row in state["observations"].values() if row["proposal_id"] in proposal_ids]
        records["bank_imports"] = snapshot["bank_imports"]
        records["inspections"] = [row for row in state["inspections"].values() if row["document_id"] in selected]
        records["reconciliations"] = [item["report"] for item in snapshot["reports"]]
        payloads, entries = {}, {}
        def add(name, payload, role, source=None):
            safe_name(name)
            if hashlib.sha256(payload).hexdigest() in omitted_hashes:
                raise ws.WorkspaceError("Evidence belongs to an excluded or unselected document; resolve the catalog dependency before archiving.")
            if len(payload) > ws.MAX_BYTES:
                raise ws.WorkspaceError("A archive file exceeds the supported size.")
            if name in payloads and payloads[name] != payload:
                raise ws.WorkspaceError("Conflicting bundle path.")
            if source and hashlib.sha256(payload).hexdigest() != source["sha256"]:
                raise ws.WorkspaceError("Source changed while collecting the archive; no verified bundle can be produced.")
            payloads[name] = payload
            entries[name] = {"path": name, "sha256": hashlib.sha256(payload).hexdigest(), "size_bytes": len(payload), "role": role}
            if source:
                entries[name]["source"] = source
        for identifier in sorted(selected):
            original = docs.original(root, identifier)
            add("originals/" + identifier + Path(original["path"]).suffix,
                ws._read_regular(ws._inside(root, original["path"])), "original",
                {"document_id": identifier, "path": original["path"], "sha256": original["sha256"]})
        evidence = []
        for row in records["source_checks"] + records["provider_observations"]:
            evidence.append(row["evidence"])
        for row in records["tasks"] + records["questions"] + records["decisions"]:
            if row.get("evidence_file"):
                evidence.append({"path": row["evidence_file"], "sha256": row["evidence_sha256"]})
        for row in records["bank_imports"]:
            evidence.extend(row[key] for key in ("preview", "normalized", "review_evidence"))
        for row in records["inspections"]:
            evidence.extend(row[key] for key in ("source", "report"))
        for item in snapshot["reports"]:
            if not item["current"]:
                raise ws.WorkspaceError("Reconciliation sources or results changed; regenerate before archive.")
            evidence.append(st.evidence(root, item["path"]))
            evidence.extend(item["report"]["sources"].values())
        for source in evidence:
            st.check_evidence(root, source)
            path = ws._inside(root, source["path"])
            suffix = path.suffix.lower() if path.suffix.lower() in {".pdf", ".xml", ".csv", ".json", ".md", ".txt"} else ".bin"
            add("evidence/" + source["sha256"] + suffix, ws._read_regular(path), "evidence", source)
        for name, rows in records.items():
            add("records/" + name + ".json", st.encoded(rows), "record_snapshot")
        add("README.txt", ("Personal records archive / Архив собственных записей\n"
            "Verify manifest.json and every file before use. Unresolved questions remain in the manifest.\n"
            "This is not a DATEV export, proof of tax correctness, a backup, or a filing receipt.\n"
            "Проверьте манифест и файлы. Открытые вопросы сохранены. Это не экспорт DATEV, резервная копия или квитанция подачи.\n").encode("utf-8"), "guide")
        if len(payloads) > MAX_FILES or sum(len(data) for data in payloads.values()) > MAX_TOTAL:
            raise ws.WorkspaceError("Archive exceeds supported limits.")
        manifest = {"schema_version": 1, "format": "generic-records-archive", "period": period, "as_of": snapshot["as_of"],
                    "readiness": "prepared_with_open_items" if problems or not selected else "prepared_for_self_review",
                    "included_document_ids": sorted(selected),
                    "excluded_documents": [{"document_id": key, "reason": row["review_note"] if row["review_status"] == "excluded" else "outside selected month and linked evidence"} for key, row in sorted(catalog.items()) if key not in selected],
                    "excluded_record_scope": "Unlinked tasks/questions/decisions, entire profile/runtime, credentials, other periods and unrelated exports are not copied.",
                    "open_items": sorted(problems, key=lambda row: (row["code"], row["ref"])), "files": [entries[key] for key in sorted(entries)],
                    "scope": "Preserved selected originals and supplied evidence. File integrity is distinct from accounting completeness and tax review."}
        relative = f"07_exports/{period}/archive-{uuid.uuid4().hex}"
        target = ws._path(root, relative)
        ws._mkdir(target)
        for name, payload in sorted(payloads.items()):
            path = ws._inside(target, name)
            ws._mkdir(path.parent)
            ws._write_exclusive(path, payload)
        ws._atomic_json(target / "manifest.json", manifest)
        checked = verify(target)
        if checked["status"] != "verified":
            raise ws.WorkspaceError("Archive verification failed; inspect the incomplete bundle.")
        zip_path = ws._inside(root, relative + ".zip")
        with zipfile.ZipFile(zip_path, "x", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in sorted([*payloads, "manifest.json"]):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o600) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, ws._read_regular(ws._inside(target, name)))
        try:
            zip_path.chmod(0o600)
        except OSError:
            pass
        if verify(zip_path)["status"] != "verified":
            raise ws.WorkspaceError("ZIP verification failed; do not send this artifact.")
        ws._audit(root, "archive_built", {"path": relative, "zip_path": relative + ".zip", "period": period, "readiness": manifest["readiness"]})
    return {"path": ws._physical(root, relative), "zip_path": ws._physical(root, relative + ".zip"), "integrity": "verified", "readiness": manifest["readiness"], "open_items": len(problems)}
