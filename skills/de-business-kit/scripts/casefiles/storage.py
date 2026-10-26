"""Additive case records; reuse established private workspace protections."""
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import re
import uuid

import workspace as ws
import workflows as wf

STATE = "00_admin/casework.json"
COLLECTIONS = ("documents", "proposals", "source_checks", "observations", "bank_imports", "inspections")


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def load(root):
    path = ws._inside(root, STATE)
    if not path.exists():
        return {"schema_version": 1, **{key: {} for key in COLLECTIONS}, "receipts": []}
    state = ws._load(path)
    wf.exact(state, {"schema_version", "receipts", *COLLECTIONS}, "casework register")
    if type(state["schema_version"]) is not int or state["schema_version"] != 1:
        raise ws.WorkspaceError("Unsupported casework schema; preserve it and use an explicit migration.")
    if any(not isinstance(state[key], dict) for key in COLLECTIONS) or not isinstance(state["receipts"], list):
        raise ws.WorkspaceError("Invalid casework collections; no automatic repair performed.")
    return state


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,159}", value):
        raise ws.WorkspaceError("Record IDs need 1-160 letters/digits or _.:-, starting with a letter/digit.")
    return value


def version(existing, expected):
    if existing is None:
        if expected is not None:
            raise ws.WorkspaceError("Record does not exist; no prior hash is accepted.")
    elif expected != digest(existing):
        raise ws.WorkspaceError("Stale or missing record hash; inspect the current record before updating.")


@contextmanager
def edit(root, action, details):
    with ws._locked(root):
        ws._check_audit(root)
        state = load(root)
        before = json.loads(json.dumps(state))
        yield state
        if state == before:
            return
        payload = encoded(state)
        if len(payload) > ws.MAX_BYTES:
            raise ws.WorkspaceError("Casework register exceeds the supported 50 MiB size.")
        history_id = "casework-" + uuid.uuid4().hex
        ws._atomic_json(ws._inside(root, f"09_audit/history/{history_id}.json"),
                        {"schema_version": 1, "action": action, "before": before, "after_sha256": digest(state)})
        ws._atomic_json(ws._inside(root, STATE), state, replace=True)
        ws._audit(root, action, {**details, "history_id": history_id})


def evidence(root, relative):
    return wf.capture(root, relative)


def check_evidence(root, source):
    if not isinstance(source, dict) or not {"path", "sha256"} <= set(source):
        raise ws.WorkspaceError("Invalid saved evidence fingerprint.")
    if evidence(root, source["path"])["sha256"] != source["sha256"]:
        raise ws.WorkspaceError("Evidence changed; preserve history and prepare a reviewed replacement.")


def template(name):
    return ws._load(Path(__file__).resolve().parents[2] / "assets" / name)
