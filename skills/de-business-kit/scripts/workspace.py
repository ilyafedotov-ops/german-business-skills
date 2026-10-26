#!/usr/bin/env python3
"""Offline private workspace tools. Python 3.9+, standard library only.

Relative input paths are relative to --root. Record/reconcile input files must
be inside that workspace. Ingest may copy in an external regular file. No
network, OCR, XML interpretation, tax filing, or accounting-provider writes.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import csv
from datetime import date, datetime, timezone
from decimal import Decimal, localcontext
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Dict, List, Optional, Union
import uuid


SCHEMA = "german-business-workspace"
VERSION = 1
MAX_BYTES = 50 * 1024 * 1024
EXTENSIONS = {".pdf", ".xml", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".csv"}
STATUSES = {"unknown", "declared", "proposed", "verified", "needs_review"}
LANGUAGES = {"ru", "en", "de"}  # de remains accepted for existing workspaces.
MODES = {"general", "bookkeeping", "tax-consultant"}
PROFILE = "01_profile/business.json"
DOCUMENTS = "00_admin/documents.json"
EVENTS = "09_audit/events.json"
MARKER = "00_admin/workspace.json"
RUNTIME = "00_admin/runtime.json"
LOCK = ".workspace.lock"
LAYOUT = ".workspace-layout.json"
FIELDS = (
    "legal_form", "activity_classification", "activities", "existing_activities",
    "owner_name", "residence_address", "business_address", "residence_country", "business_country",
    "municipality", "federal_state", "competent_tax_office", "registration_authority",
    "business_start_date", "preparation_start_date", "commercial_launch_date", "registration_date",
    "vat_existing_registration", "vat_current_regime", "vat_history",
    "vat_opt_out_date", "vat_binding_until", "vat_prior_year",
    "vat_prior_year_turnover_all_activities", "vat_current_year_turnover_all_activities",
    "vat_current_year_forecast_all_activities", "accounting_method", "bookkeeper",
    "accounting_software", "client_types", "client_countries", "supplier_countries",
    "cross_border_activity", "employees", "cash_transactions", "provider_needs",
    "bank_needs", "tax_identifiers_reference",
)
PathInput = Union[str, Path]


class WorkspaceError(ValueError):
    """Invalid input or unsafe workspace operation."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def _absolute(value: PathInput) -> Path:
    path = Path(value).expanduser()
    if ".." in path.parts:
        raise WorkspaceError("Parent-directory components ('..') are not allowed.")
    return Path(os.path.abspath(str(path)))


def _check_chain(path: Path, final_file: bool = False) -> None:
    for item in reversed((path, *path.parents)):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode):
            raise WorkspaceError("Symlinked paths are not allowed.")
        if item == path and final_file:
            if not stat.S_ISREG(info.st_mode):
                raise WorkspaceError("A regular file is required.")
        elif not stat.S_ISDIR(info.st_mode):
            raise WorkspaceError("A directory path contains a non-directory.")


def _layout(root: Path):
    descriptor = root / LAYOUT
    if not descriptor.exists() and not descriptor.is_symlink():
        if (root / '.business-kit').exists():
            raise WorkspaceError('Localized workspace layout is missing; preserve the existing files.')
        return None
    record = _load(descriptor)
    if (not isinstance(record, dict) or set(record) != {'schema_version', 'language'}
            or type(record['schema_version']) is not int or record['schema_version'] != 1
            or not isinstance(record['language'], str) or record['language'] not in LANGUAGES):
        raise WorkspaceError('Unsupported folder layout; no automatic migration performed.')
    words = _load(Path(__file__).resolve().parents[1] / 'assets/folder-layouts.json')['languages'][record['language']]
    if any((root / prefix.split('/')[0]).exists() for prefix in words['paths']):
        raise WorkspaceError('Conflicting legacy and localized directories; preserve both for review.')
    return record, words


def _mapped(relative: str, words, reverse=False) -> str:
    paths = words['paths']
    pairs = [(v, k) if reverse else (k, v) for k, v in paths.items()]
    for source, target in sorted(pairs, key=lambda pair: len(pair[0]), reverse=True):
        if relative == source or relative.startswith(source + '/'):
            suffix = relative[len(source):].lstrip('/').split('/') if relative != source else []
            if (target if reverse else source) == '06_bookkeeping' and len(suffix) >= 3:
                parts = {v: k for k, v in words['parts'].items()} if reverse else words['parts']
                suffix[2] = parts.get(suffix[2], suffix[2])
            return '/'.join([target, *suffix])
    return relative


def _path(root: Path, value: PathInput) -> Path:
    """Resolve stable record paths and physical user paths through a fixed layout."""
    supplied = Path(value).expanduser()
    if ".." in supplied.parts:
        raise WorkspaceError("Parent-directory components ('..') are not allowed.")
    if supplied.is_absolute():
        path = _absolute(supplied)
    else:
        layout = _layout(root)
        path = root / (_mapped(supplied.as_posix(), layout[1]) if layout else supplied)
    if path == root or root not in path.parents:
        raise WorkspaceError("This input/output must be inside the private workspace.")
    return path


def _physical(root: Path, relative: str) -> str:
    return _path(root, relative).relative_to(root).as_posix()


def _logical(root: Path, path: Path) -> str:
    relative = path.relative_to(root).as_posix()
    layout = _layout(root)
    return _mapped(relative, layout[1], reverse=True) if layout else relative


def _workspace_present(path: Path) -> bool:
    # Detect incomplete layouts too: they must never be re-imported as ordinary files.
    return any((path / name).exists() or (path / name).is_symlink()
               for name in (MARKER, LAYOUT, '.business-kit'))


def _inside(root: Path, value: PathInput) -> Path:
    path = _path(root, value)
    _check_chain(path, final_file=True)
    return path


def _private_boundary(root: Path) -> None:
    for candidate in (root, *root.parents):
        git = candidate / ".git"
        # An empty directory named .git has no repository metadata. Worktree
        # files, symlinks, and directories with Git metadata are boundaries.
        if (git.is_file() or git.is_symlink()
                or (git.is_dir() and any((git / part).exists() for part in ("HEAD", "config", "objects")))):
            raise WorkspaceError("Workspace cannot be inside a Git repository.")
        for name in ("SKILL.md", "skill.md"):
            marker = candidate / name
            if marker.exists() or marker.is_symlink():
                raise WorkspaceError("Workspace cannot be inside a Git repository or skill directory.")
        if ((candidate / "HEAD").is_file() and (candidate / "objects").is_dir()
                and (candidate / "refs").is_dir()):
            raise WorkspaceError("Workspace cannot be inside a bare Git repository.")


def _mkdir(path: Path) -> None:
    _check_chain(path)
    for item in reversed((path, *path.parents)):
        if item.exists():
            continue
        item.mkdir(mode=0o700)
    try:
        path.chmod(0o700)
    except OSError:
        pass  # Best effort POSIX mode; this is not an ACL/encryption guarantee.


def _read_regular(path: Path, limit: int = MAX_BYTES) -> bytes:
    _check_chain(path, final_file=True)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(str(path), flags)
    with os.fdopen(descriptor, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise WorkspaceError("Input must be a regular file no larger than 50 MiB.")
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise WorkspaceError("Input exceeds the 50 MiB limit.")
    return data


def _reject_constant(value: str) -> None:
    raise WorkspaceError("Non-finite JSON numbers are not allowed.")


def _json_bytes(data: bytes) -> Any:
    try:
        return json.loads(data.decode("utf-8"), parse_constant=_reject_constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise WorkspaceError("Expected valid UTF-8 JSON.") from exc


def _load(path: Path) -> Any:
    return _json_bytes(_read_regular(path))


def _write_exclusive(path: Path, data: bytes) -> os.stat_result:
    _check_chain(path, final_file=True)
    descriptor = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
            created = os.fstat(stream.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise
    # Windows finalizes write timestamps when the writer closes. Retain the
    # original identity if the path was replaced; never adopt another file as
    # our rollback target. Rollback additionally compares final metadata/bytes.
    try:
        closed = path.lstat()
        if (stat.S_ISREG(closed.st_mode)
                and (closed.st_dev, closed.st_ino, closed.st_size)
                == (created.st_dev, created.st_ino, created.st_size)):
            return closed
    except OSError:
        pass
    return created


def _remove_unchanged_created_copy(path: Path, created: os.stat_result, data: bytes) -> None:
    """Best-effort rollback of this invocation's still-identical original copy."""
    try:
        _check_chain(path, final_file=True)
        before = path.lstat()
        def signature(info: os.stat_result):
            return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)
        if signature(before) != signature(created) or _read_regular(path) != data:
            return
        after = path.lstat()
        if signature(after) == signature(created):
            path.unlink()
    except (OSError, WorkspaceError):
        pass  # Preserve anything we cannot establish is our unchanged copy.


def _atomic_json(path: Path, value: Any, replace: bool = False) -> None:
    _check_chain(path, final_file=True)
    if not replace and (path.exists() or path.is_symlink()):
        raise WorkspaceError("Refusing to overwrite an existing file.")
    payload = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    temporary = path.parent / (".write-" + uuid.uuid4().hex + ".tmp")
    _write_exclusive(temporary, payload)
    try:
        _check_chain(path, final_file=True)
        if not replace and path.exists():
            raise WorkspaceError("Refusing to overwrite an existing file.")
        os.replace(str(temporary), str(path))
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def _locked(root: Path):
    _check_chain(root)
    path = root / LOCK
    try:
        descriptor = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise WorkspaceError("Workspace is locked; inspect the active operation or stale lock before retrying.") from exc
    identity = os.fstat(descriptor)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "created_at": _now()}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        yield
    finally:
        try:
            current = path.lstat()
            if (current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino):
                path.unlink()
        except FileNotFoundError:
            pass


def _workspace(value: PathInput) -> Path:
    root = _absolute(value)
    _check_chain(root)
    _private_boundary(root)
    if not root.is_dir():
        raise WorkspaceError("Workspace directory does not exist.")
    marker = _load(_inside(root, MARKER))
    if not isinstance(marker, dict) or marker.get("schema") != SCHEMA or marker.get("schema_version") != VERSION:
        raise WorkspaceError("Workspace marker or schema version is invalid.")
    try:
        if not isinstance(marker.get("workspace_id"), str):
            raise ValueError("Workspace ID must be text")
        uuid.UUID(marker["workspace_id"])
    except (KeyError, TypeError, ValueError) as exc:
        raise WorkspaceError("Workspace ID is invalid.") from exc
    layout = _layout(root)
    if (layout and marker.get('folder_layout') != layout[0]) or (not layout and 'folder_layout' in marker):
        raise WorkspaceError('Folder layout does not match the workspace identity; preserve all files.')
    return root


def _period(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", value):
        raise WorkspaceError("Period must be YYYY-MM.")
    if not 1900 <= int(value[:4]) <= 9999:
        raise WorkspaceError("Period year must be between 1900 and 9999.")
    return value


def _day(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise WorkspaceError("Date must be YYYY-MM-DD.")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise WorkspaceError("Date is invalid.") from exc
    return value


def _blank_fact() -> Dict[str, Any]:
    return {"value": None, "status": "unknown", "source": {"kind": None, "ref": None},
            "recorded_at": None, "effective_from": None, "note": None}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _evidence_path(root: Path, value: str) -> Path:
    if not _text(value) or Path(value).is_absolute():
        raise WorkspaceError("Evidence must be a relative private-workspace file.")
    path = _inside(root, value)
    mutable = {PROFILE, DOCUMENTS, EVENTS, MARKER, RUNTIME, LOCK, LAYOUT,
               "00_admin/tasks.json", "00_admin/questions.json", "00_admin/decisions.json", "00_admin/casework.json",
               "04_accounting/register.json"}
    if (_logical(root, path) in mutable
            or path.exists() and any(_path(root, item).exists() and path.samefile(_path(root, item)) for item in mutable)):
        raise WorkspaceError("Use a preserved evidence document or history snapshot, not a mutable administrative file.")
    return path


def _fact_value(field: str, value: Any) -> None:
    """Validate storage types, not the truth or tax treatment of the fact."""
    if field == "vat_current_regime":
        valid = isinstance(value, str) and value in {"Kleinunternehmer", "Regelbesteuerung", "unresolved"}
    elif field == "accounting_method":
        valid = isinstance(value, str) and value in {"EÜR", "Bilanzierung", "unresolved"}
    elif field in {"employees", "cash_transactions", "cross_border_activity", "vat_existing_registration"}:
        valid = isinstance(value, bool)
    elif field == "vat_prior_year":
        valid = type(value) is int and 1900 <= value <= 9999
    elif field.endswith("_date") or field == "vat_binding_until":
        _day(value)
        return
    elif "turnover_all_activities" in field or field == "vat_current_year_forecast_all_activities":
        valid = isinstance(value, dict) and set(value) == {"amount", "currency", "period"}
        if valid:
            valid = (isinstance(value["amount"], str) and _amount(value["amount"]) >= 0
                     and isinstance(value["currency"], str)
                     and _currency(value["currency"]) == "EUR"
                     and isinstance(value["period"], str)
                     and re.fullmatch(r"[1-9]\d{3}", value["period"]) is not None)
    elif field in {"client_types", "client_countries", "supplier_countries"}:
        valid = isinstance(value, list) and all(_text(item) for item in value)
    elif field in {"activities", "existing_activities"}:
        valid = isinstance(value, list)
        ids = set()
        if valid:
            for item in value:
                if not isinstance(item, dict) or not _text(item.get("activity_id")) or item["activity_id"] in ids:
                    valid = False
                    break
                ids.add(item["activity_id"])
                if item.get("description") is not None and not _text(item["description"]):
                    valid = False
                if item.get("classification") is not None and item["classification"] not in {"freiberuflich", "gewerblich", "mixed", "unresolved"}:
                    valid = False
                if item.get("commenced_at") is not None:
                    _day(item["commenced_at"])
    elif field == "vat_history":
        valid = isinstance(value, list) and all(isinstance(item, dict) for item in value)
        if valid:
            for item in value:
                _fact_value("vat_current_regime", item.get("regime"))
                _day(item.get("effective_from"))
                if not _text(item.get("source_ref")):
                    valid = False
    elif field in {"provider_needs", "bank_needs"}:
        valid = isinstance(value, dict) and all(_text(key) for key in value)
    else:
        valid = _text(value)
    if not valid:
        raise WorkspaceError("Invalid value type or allowed value for profile field: " + field)


def _runtime_review(root: Path, record: Any, *, preparing: bool = False) -> List[str]:
    """Check recorded assessment evidence; never certify a processing setup."""
    required = {"assistant_product", "app_version", "session_execution", "model_provider",
                "authentication_type", "contract_plan", "training_policy_checked_at",
                "dpa_status", "retention_policy_reference", "residency_scope"}
    allowed = required | {"schema_version", "third_party_connectors", "client_data_mode", "review"}
    if (not isinstance(record, dict) or record.get("schema_version") != VERSION
            or set(record) - allowed or not required.issubset(record)):
        raise WorkspaceError("Runtime record is invalid; use the documented runtime format.")
    for field in required:
        if record[field] is not None and not _text(record[field]):
            raise WorkspaceError("Runtime settings must be text or null.")
    if record["session_execution"] not in {"unknown", "local", "cloud", "hybrid"}:
        raise WorkspaceError("Session execution must be unknown, local, cloud, or hybrid.")
    connectors = record.get("third_party_connectors")
    if not isinstance(connectors, list) or not all(_text(item) for item in connectors):
        raise WorkspaceError("Connectors must be a list of names/references, not credentials.")
    mode = record.get("client_data_mode")
    if mode not in {"synthetic_or_redacted_until_reviewed", "review_recorded"}:
        raise WorkspaceError("Unknown client data mode.")
    missing = sorted(field for field in required if record[field] is None or record[field].strip().lower() == "unknown")
    if record["training_policy_checked_at"] is not None:
        _day(record["training_policy_checked_at"])
    review = record.get("review")
    if mode != "review_recorded":
        return missing + ["data_processing_review"]
    if missing or not isinstance(review, dict):
        raise WorkspaceError("A recorded review requires complete settings and assessment evidence.")
    if set(review) - {"reviewed_by", "reviewed_at", "scope", "evidence_file", "evidence_sha256", "configuration_sha256"}:
        raise WorkspaceError("Unexpected review field.")
    if not all(_text(review.get(field)) for field in ("reviewed_by", "reviewed_at", "scope", "evidence_file")):
        raise WorkspaceError("Review requires reviewer, date, scope and a local evidence file.")
    _day(review["reviewed_at"])
    evidence = review["evidence_file"]
    if Path(evidence).is_absolute():
        raise WorkspaceError("Review evidence must be a relative private-workspace path.")
    try:
        payload = _read_regular(_evidence_path(root, evidence))
    except OSError as exc:
        raise WorkspaceError("Review evidence is missing or unreadable.") from exc
    if not payload.strip():
        raise WorkspaceError("Review evidence must not be empty.")
    digest = hashlib.sha256(payload).hexdigest()
    configuration = {key: value for key, value in record.items() if key != "review"}
    configuration_digest = hashlib.sha256(json.dumps(configuration, sort_keys=True).encode("utf-8")).hexdigest()
    if preparing:
        review["evidence_sha256"] = digest
        review["configuration_sha256"] = configuration_digest
    elif review.get("evidence_sha256") != digest or review.get("configuration_sha256") != configuration_digest:
        raise WorkspaceError("Review evidence or configuration changed; reassess before recording a new review.")
    return []


def configure_runtime(root: PathInput, record: Dict[str, Any]) -> Dict[str, Any]:
    location = _workspace(root)
    # Copy before adding a derived hash; callers retain ownership of inputs.
    after = json.loads(json.dumps(record, allow_nan=False))
    with _locked(location):
        _check_audit(location)
        _runtime_review(location, after, preparing=True)
        path = _inside(location, RUNTIME)
        before = _load(path)
        if before == after:
            return {"status": "unchanged"}
        history_id = uuid.uuid4().hex
        _atomic_json(_inside(location, f"09_audit/history/{history_id}.json"),
                     {"schema_version": VERSION, "action": "configure_runtime", "recorded_at": _now(),
                      "before": before, "after": after})
        _atomic_json(path, after, replace=True)
        _audit(location, "runtime_configured", {"history_id": history_id})
    return {"status": "recorded", "history_id": history_id,
            "note": "A recorded assessment is not legal certification or authorization for an external action."}


ENTRY_STATES = {
    "tasks": {"pending", "in_progress", "blocked", "completed", "cancelled"},
    "questions": {"open", "deferred", "resolved"},
    "decisions": {"proposed", "approved", "rejected", "superseded"},
}
ENTRY_INITIAL = {"tasks": "pending", "questions": "open", "decisions": "proposed"}
ENTRY_TERMINAL = {"completed", "cancelled", "resolved", "rejected", "superseded"}


def _entry_hash(record: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=False, allow_nan=False).encode("utf-8")).hexdigest()


def _entry_valid(root: Path, collection: str, record: Any, *, preparing: bool = False,
                 check_evidence: bool = True) -> None:
    required = {"schema_version", "id", "title", "owner", "status"}
    allowed = required | {"depends_on", "due_date", "deadline_source", "evidence_file", "evidence_sha256",
                          "reviewer", "supersedes", "superseded_by", "note"}
    if collection not in ENTRY_STATES or not isinstance(record, dict) or not required.issubset(record) or set(record) - allowed:
        raise WorkspaceError("Unknown register or entry fields; review the register contract.")
    if (record["schema_version"] != 1 or not isinstance(record["id"], str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", record["id"])
            or not _text(record["title"]) or not _text(record["owner"])
            or not isinstance(record["status"], str) or record["status"] not in ENTRY_STATES[collection]):
        raise WorkspaceError("Invalid register entry identity, owner, title or state.")
    dependencies = record.get("depends_on", [])
    if (not isinstance(dependencies, list) or not all(_text(item) for item in dependencies)
            or len(dependencies) != len(set(dependencies)) or record["id"] in dependencies):
        raise WorkspaceError("Dependencies must be distinct IDs other than this entry.")
    for field in ("deadline_source", "reviewer", "supersedes", "superseded_by", "note"):
        if record.get(field) is not None and not _text(record[field]):
            raise WorkspaceError("Entry metadata must be text or null.")
    if record.get("due_date") is not None:
        _day(record["due_date"])
        if not _text(record.get("deadline_source")):
            raise WorkspaceError("A deadline requires a source or a reference to an explicit user target.")
    if record["status"] in {"approved", "superseded"} and not _text(record.get("reviewer")):
        raise WorkspaceError("An approved decision requires an identified reviewer.")
    if record["status"] == "superseded" and not _text(record.get("superseded_by")):
        raise WorkspaceError("A superseded decision requires a linked record reference.")
    evidence = record.get("evidence_file")
    if evidence is None:
        if record["status"] in {"completed", "resolved", "approved", "superseded"}:
            raise WorkspaceError("This state requires an evidence file.")
        if record.get("evidence_sha256") is not None:
            raise WorkspaceError("An evidence hash requires its file.")
        return
    evidence_path = _evidence_path(root, evidence)
    if not check_evidence:
        if not isinstance(record.get("evidence_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", record["evidence_sha256"]):
            raise WorkspaceError("Evidence requires its saved hash.")
        return
    try:
        payload = _read_regular(evidence_path)
    except OSError as exc:
        raise WorkspaceError("Entry evidence is missing or unreadable.") from exc
    if not payload.strip():
        raise WorkspaceError("Entry evidence must not be empty.")
    digest = hashlib.sha256(payload).hexdigest()
    if preparing:
        record["evidence_sha256"] = digest
    elif record.get("evidence_sha256") != digest:
        raise WorkspaceError("Entry evidence changed; preserve history and review the correction.")


def _entry_links(entries: List[Dict[str, Any]]) -> None:
    by_id = {item["id"]: item for item in entries}
    # Iterative topological check avoids recursion limits on a long task chain.
    for identifier, record in by_id.items():
        for link in (*record.get("depends_on", []), record.get("supersedes"), record.get("superseded_by")):
            if link is not None and (link not in by_id or link == identifier):
                raise WorkspaceError("Register link must refer to a distinct existing entry.")
        if record["status"] == "superseded":
            replacement = by_id[record["superseded_by"]]
            if replacement["status"] not in {"approved", "superseded"} or replacement.get("supersedes") != identifier:
                raise WorkspaceError("A superseded decision requires an approved, linked replacement.")
    for relationship in ("depends_on", "supersedes"):
        remaining = {identifier: set(record.get("depends_on", [])) if relationship == "depends_on" else
                     {record["supersedes"]} if record.get("supersedes") else set()
                     for identifier, record in by_id.items()}
        while remaining:
            ready = {identifier for identifier, dependencies in remaining.items() if not dependencies}
            if not ready:
                raise WorkspaceError("Register dependencies and supersession links cannot form cycles.")
            remaining = {identifier: dependencies - ready for identifier, dependencies in remaining.items() if identifier not in ready}


def _entries(root: Path, collection: str, *, check_evidence: bool = True) -> List[Dict[str, Any]]:
    if collection not in ENTRY_STATES:
        raise WorkspaceError("Unknown register.")
    entries = _load(_inside(root, f"00_admin/{collection}.json"))
    if not isinstance(entries, list):
        raise WorkspaceError("Register must be an array.")
    ids = set()
    for record in entries:
        _entry_valid(root, collection, record, check_evidence=check_evidence)
        if record["id"] in ids:
            raise WorkspaceError("Duplicate register ID.")
        ids.add(record["id"])
    _entry_links(entries)
    return entries


def entry_status(root: PathInput, collection: str, identifier: str) -> Dict[str, Any]:
    location = _workspace(root)
    for record in _entries(location, collection, check_evidence=False):
        if record["id"] == identifier:
            try:
                _entry_valid(location, collection, record)
                evidence_status = "checked" if record.get("evidence_file") else "not_recorded"
            except (WorkspaceError, OSError):
                evidence_status = "needs_review"
            return {"id": identifier, "status": record["status"], "sha256": _entry_hash(record),
                    "evidence_status": evidence_status}
    raise WorkspaceError("Entry not found.")


def save_entry(root: PathInput, collection: str, record: Dict[str, Any],
               expected_sha256: Optional[str] = None) -> Dict[str, Any]:
    location = _workspace(root)
    after = json.loads(json.dumps(record, allow_nan=False))
    with _locked(location):
        _check_audit(location)
        _entry_valid(location, collection, after, preparing=True)
        entries = _entries(location, collection, check_evidence=False)
        before = next((item for item in entries if item["id"] == after["id"]), None)
        if before is None:
            if expected_sha256 is not None or after["status"] != ENTRY_INITIAL[collection]:
                raise WorkspaceError("New entries must start in their initial state with no previous hash.")
        else:
            if expected_sha256 != _entry_hash(before):
                raise WorkspaceError("Entry changed or previous hash missing; inspect entry status before retrying.")
            if before["status"] in ENTRY_TERMINAL or before["status"] == "approved" and after["status"] != "superseded":
                raise WorkspaceError("Preserve terminal/reviewed entries; create a linked correction instead.")
            if before["status"] == "approved":
                stable = lambda item: {key: value for key, value in item.items() if key not in {"status", "superseded_by"}}
                if stable(before) != stable(after):
                    raise WorkspaceError("Superseding must preserve the old decision and reviewer evidence.")
        dependencies = after.get("depends_on", [])
        by_id = {item["id"]: item for item in entries}
        if any(identifier not in by_id for identifier in dependencies):
            raise WorkspaceError("Create referenced dependency entries first.")
        if collection == "tasks" and after["status"] == "completed" and any(by_id[identifier]["status"] != "completed" for identifier in dependencies):
            raise WorkspaceError("Complete task dependencies before marking this task completed.")
        if collection == "tasks" and after["status"] == "completed":
            for identifier in dependencies:
                _entry_valid(location, collection, by_id[identifier])
        by_id[after["id"]] = after
        _entry_links(list(by_id.values()))
        if after["status"] == "superseded":
            replacement = by_id[after["superseded_by"]]
            if replacement["status"] != "approved":
                raise WorkspaceError("Choose the current approved replacement decision.")
            _entry_valid(location, collection, replacement)
        history_id = uuid.uuid4().hex
        _atomic_json(_inside(location, f"09_audit/history/{history_id}.json"),
                     {"schema_version": VERSION, "action": "register_entry", "collection": collection,
                      "recorded_at": _now(), "before": before, "after": after})
        _atomic_json(_inside(location, f"00_admin/{collection}.json"), list(by_id.values()), replace=True)
        _audit(location, "register_entry_saved", {"collection": collection, "id": after["id"],
                                                  "status": after["status"], "history_id": history_id})
    return {"status": "recorded", "id": after["id"], "sha256": _entry_hash(after), "history_id": history_id}


def _audit(root: Path, action: str, details: Dict[str, Any]) -> None:
    path = _inside(root, EVENTS)
    events = _load(path)
    if not isinstance(events, list):
        raise WorkspaceError("Audit log is invalid.")
    events.append({"event_id": uuid.uuid4().hex, "recorded_at": _now(),
                   "action": action, "details": details})
    _atomic_json(path, events, replace=True)


def _check_audit(root: Path) -> None:
    if not isinstance(_load(_inside(root, EVENTS)), list):
        raise WorkspaceError("Audit log is invalid.")


def _documents(root: Path) -> Dict[str, Any]:
    registry = _load(_inside(root, DOCUMENTS))
    if not isinstance(registry, dict) or registry.get("schema_version") != VERSION or not isinstance(registry.get("documents"), list):
        raise WorkspaceError("Document registry is invalid.")
    if any(not isinstance(document, dict) for document in registry["documents"]):
        raise WorkspaceError("Document registry entries must be objects.")
    return registry


def _preferences(marker: Dict[str, Any]) -> Dict[str, str]:
    """Read UI/workflow preferences without migrating or changing tax facts."""
    language = marker.get("language", "ru")
    mode = marker.get("mode", "general")
    if not isinstance(language, str) or language not in LANGUAGES:
        raise WorkspaceError("Language must be ru, en, or legacy de.")
    if not isinstance(mode, str) or mode not in MODES:
        raise WorkspaceError("Mode must be general, bookkeeping, or tax-consultant.")
    return {"language": language, "mode": mode}


def init_workspace(root: PathInput, year: int, language: str = "ru", mode: str = "general", layout: str = "legacy") -> Dict[str, Any]:
    if isinstance(year, bool) or not isinstance(year, int) or not 1900 <= year <= 9999:
        raise WorkspaceError("Year must be an integer between 1900 and 9999.")
    _preferences({"language": language, "mode": mode})
    if layout not in {"legacy", "localized"}:
        raise WorkspaceError("Folder layout must be legacy or localized.")
    location = _absolute(root)
    _check_chain(location)
    _private_boundary(location)
    if location.exists() and any(location.iterdir()):
        raise WorkspaceError("Initialization requires a new or empty directory.")
    _mkdir(location)
    with _locked(location):
        if any(child.name != LOCK for child in location.iterdir()):
            raise WorkspaceError("Initialization requires an empty directory.")
        if layout == "localized":
            _atomic_json(location / LAYOUT, {"schema_version": 1, "language": language})
        directories = ["00_admin", "00_admin/inbox", "01_profile", "02_registration",
                       "03_banking", "04_accounting", f"05_tax/{year}", "06_bookkeeping", "07_exports",
                       "08_correspondence", "09_audit/history"]
        for relative in directories:
            _mkdir(_path(location, relative))
        marker = {"schema": SCHEMA, "schema_version": VERSION, "workspace_id": str(uuid.uuid4()),
                  "created_at": _now(), "initial_year": year, "language": language, "mode": mode}
        if layout == "localized":
            marker["folder_layout"] = {"schema_version": 1, "language": language}
            words = _layout(location)[1]
            _write_exclusive(location / words["guide_name"], words["guide"].encode("utf-8"))
        _atomic_json(_inside(location, MARKER), marker)
        _atomic_json(_inside(location, PROFILE), {"schema_version": VERSION, "facts": {field: _blank_fact() for field in FIELDS}})
        runtime = {"schema_version": VERSION, "assistant_product": None, "app_version": None,
                   "session_execution": "unknown", "model_provider": None,
                   "authentication_type": None, "contract_plan": None,
                   "training_policy_checked_at": None, "dpa_status": "unknown",
                   "retention_policy_reference": None, "residency_scope": "unknown",
                   "third_party_connectors": [], "client_data_mode": "synthetic_or_redacted_until_reviewed"}
        _atomic_json(_inside(location, "00_admin/runtime.json"), runtime)
        for name in ("tasks", "questions", "decisions"):
            _atomic_json(_inside(location, f"00_admin/{name}.json"), [])
        _atomic_json(_inside(location, DOCUMENTS), {"schema_version": VERSION, "documents": []})
        _atomic_json(_inside(location, EVENTS), [])
        _audit(location, "workspace_initialized", {"year": year, "language": language, "mode": mode})
    return {"status": "initialized", "year": year, "language": language, "mode": mode,
            "facts": len(FIELDS), "permissions": "owner POSIX modes best effort; no ACL or encryption guarantee"}


def configure_workspace(root: PathInput, language: Optional[str] = None,
                        mode: Optional[str] = None) -> Dict[str, Any]:
    """Persist presentation/workflow preferences, never business or tax facts."""
    if language is None and mode is None:
        raise WorkspaceError("Configure requires at least one of --language or --mode.")
    # Validate requested values before opening or changing the workspace.
    _preferences({"language": "ru" if language is None else language,
                  "mode": "general" if mode is None else mode})
    location = _workspace(root)
    with _locked(location):
        _check_audit(location)
        path = _inside(location, MARKER)
        before = _load(path)
        preferences = _preferences(before)
        after = dict(before)
        after["language"] = preferences["language"] if language is None else language
        after["mode"] = preferences["mode"] if mode is None else mode
        changed = [key for key in ("language", "mode") if before.get(key) != after[key]]
        if not changed:
            return {"status": "unchanged", "language": after["language"],
                    "mode": after["mode"], "changed_fields": []}
        history_id = uuid.uuid4().hex
        snapshot = {"schema_version": VERSION, "action": "configure_workspace",
                    "recorded_at": _now(), "changed_fields": changed,
                    "before": before, "after": after}
        _atomic_json(_inside(location, f"09_audit/history/{history_id}.json"), snapshot)
        _atomic_json(path, after, replace=True)
        _audit(location, "workspace_configured", {"language": after["language"],
                                                   "mode": after["mode"],
                                                   "changed_fields": changed,
                                                   "history_id": history_id})
    return {"status": "configured", "language": after["language"], "mode": after["mode"],
            "changed_fields": changed, "history_id": history_id}


def record_fact(root: PathInput, record: Dict[str, Any]) -> Dict[str, Any]:
    location = _workspace(root)
    if not isinstance(record, dict) or set(record) - {"field", "value", "status", "source", "effective_from", "note"}:
        raise WorkspaceError("Record must contain only the documented fact fields.")
    field = record.get("field")
    status = record.get("status")
    if field not in FIELDS or status not in STATUSES or "value" not in record:
        raise WorkspaceError("Unknown fact field, invalid status, or missing value.")
    source = record.get("source", {"kind": None, "ref": None})
    if not isinstance(source, dict) or set(source) != {"kind", "ref"}:
        raise WorkspaceError("Source must contain kind and ref.")
    if status != "unknown":
        if record["value"] is None or any(not isinstance(source[key], str) or not source[key].strip() for key in ("kind", "ref")):
            raise WorkspaceError("Known facts require a value and a nonempty evidence source kind/ref.")
    elif record["value"] is not None or any(source[key] is not None for key in ("kind", "ref")):
        raise WorkspaceError("Unknown facts must use null value and null source kind/ref.")
    if status == "verified" and source["kind"].lower() in {"llm", "model", "inference", "confidence", "ai"}:
        raise WorkspaceError("Verified requires checked evidence; model confidence is not evidence.")
    if status == "verified" and source["kind"] != "file":
        raise WorkspaceError("Verified facts require source.kind=file and a preserved private evidence path in source.ref.")
    if status != "unknown":
        _fact_value(field, record["value"])
    effective = record.get("effective_from")
    if effective is not None:
        _day(effective)
    note = record.get("note")
    if note is not None and not isinstance(note, str):
        raise WorkspaceError("Note must be text or null.")
    try:
        json.dumps(record, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise WorkspaceError("Record values must be finite JSON-compatible data.") from exc
    with _locked(location):
        _check_audit(location)
        path = _inside(location, PROFILE)
        before = _load(path)
        if not isinstance(before, dict) or before.get("schema_version") != VERSION or not isinstance(before.get("facts"), dict) or set(before["facts"]) != set(FIELDS):
            raise WorkspaceError("Business profile is invalid.")
        after = json.loads(json.dumps(before))
        after["facts"][field] = {"value": record["value"], "status": status, "source": source,
                                 "recorded_at": _now(), "effective_from": effective, "note": note}
        if status == "verified":
            evidence_path = _evidence_path(location, source["ref"])
            evidence_data = _read_regular(evidence_path)
            if not evidence_data.strip():
                raise WorkspaceError("Verified fact evidence must not be empty.")
            after["facts"][field]["evidence"] = {"path": evidence_path.relative_to(location).as_posix(),
                                                  "sha256": hashlib.sha256(evidence_data).hexdigest()}
            after["facts"][field]["source"] = {"kind": "file", "ref": evidence_path.relative_to(location).as_posix()}
        history_id = uuid.uuid4().hex
        history_path = _inside(location, f"09_audit/history/{history_id}.json")
        snapshot = {"schema_version": VERSION, "action": "record_fact", "field": field,
                    "recorded_at": _now(), "before": before, "after": after}
        _atomic_json(history_path, snapshot)
        _atomic_json(path, after, replace=True)
        _audit(location, "fact_recorded", {"field": field, "status": status, "history_id": history_id})
    return {"status": "recorded", "field": field, "fact_status": status, "history_id": history_id}


def ingest_document(root: PathInput, source: PathInput, period: str) -> Dict[str, Any]:
    location = _workspace(root)
    period = _period(period)
    supplied = Path(source).expanduser()
    source_path = _absolute(supplied if supplied.is_absolute() else _path(location, supplied))
    suffix = source_path.suffix.lower()
    if suffix not in EXTENSIONS:
        raise WorkspaceError("Unsupported document extension.")
    data = _read_regular(source_path)
    digest = hashlib.sha256(data).hexdigest()
    with _locked(location):
        _check_audit(location)
        registry = _documents(location)
        for existing in registry["documents"]:
            if existing.get("sha256") == digest:
                stored_path = existing.get("path")
                if not isinstance(stored_path, str) or Path(stored_path).is_absolute():
                    raise WorkspaceError("Existing document path is invalid; run verify.")
                saved = _read_regular(_inside(location, stored_path))
                if len(saved) != existing.get("size_bytes") or hashlib.sha256(saved).hexdigest() != digest:
                    raise WorkspaceError("Existing indexed original failed integrity verification; no bytes were overwritten.")
                _audit(location, "document_content_seen_again", {"document_id": existing.get("document_id")})
                return {"status": "existing_content", "document_id": existing.get("document_id"),
                        "review_note": "Identical bytes already indexed; this is not a tax duplicate determination."}
        relative = f"06_bookkeeping/{period[:4]}/{period[5:]}/originals/{digest}{suffix}"
        destination = _inside(location, relative)
        _mkdir(destination.parent)
        created = _write_exclusive(destination, data)
        previous_registry = json.loads(json.dumps(registry))
        document = {"document_id": "doc-" + uuid.uuid4().hex, "sha256": digest,
                    "size_bytes": len(data), "original_name": source_path.name,
                    "path": relative, "period": period, "imported_at": _now(),
                    "status": "imported", "provider_state": "unknown"}
        registry["documents"].append(document)
        try:
            _atomic_json(_inside(location, DOCUMENTS), registry, replace=True)
        except BaseException:
            # A replace may have committed before a later error. Roll back the
            # copy only if the on-disk registry is still the pre-write state.
            try:
                if _documents(location) == previous_registry:
                    _remove_unchanged_created_copy(destination, created, data)
            except (OSError, WorkspaceError, TypeError):
                pass
            raise
        _audit(location, "document_imported", {"document_id": document["document_id"], "sha256": digest})
    return {"status": "imported", "document_id": document["document_id"], "size_bytes": len(data),
            "period_note": "Storage period only; no tax date or tax treatment inferred."}


def _scan_originals(location: Path):
    """Inspect only canonical originals folders; never descend through links."""
    files, issues = [], []

    def issue(path: Path, message: str) -> None:
        issues.append({"document_id": None, "path": path.relative_to(location).as_posix(),
                       "issue": message})

    def children(path: Path):
        try:
            _check_chain(path)
            return sorted(path.iterdir()) if path.exists() else []
        except (WorkspaceError, OSError) as exc:
            issue(path, str(exc))
            return []

    for year in children(_path(location, "06_bookkeeping")):
        if not re.fullmatch(r"\d{4}", year.name) or not 1900 <= int(year.name) <= 9999:
            continue
        for month in children(year):
            if not re.fullmatch(r"0[1-9]|1[0-2]", month.name):
                continue
            # Check the month itself even when its originals subpath is absent.
            try:
                _check_chain(month)
            except (WorkspaceError, OSError) as exc:
                issue(month, str(exc))
                continue
            for path in children(_path(location, _logical(location, month) + "/originals")):
                try:
                    if not stat.S_ISREG(path.lstat().st_mode):
                        issue(path, "Unexpected non-regular entry in originals; not followed.")
                    else:
                        files.append(path)
                except OSError as exc:
                    issue(path, str(exc))
    return files, issues


def verify_workspace(root: PathInput) -> Dict[str, Any]:
    location = _workspace(root)
    registry = _documents(location)
    errors = []
    ids, paths = set(), set()
    for number, document in enumerate(registry["documents"], 1):
        identifier = document.get("document_id")
        label = identifier if isinstance(identifier, str) else f"registry-entry-{number}"
        try:
            if not isinstance(identifier, str) or identifier in ids:
                raise WorkspaceError("Missing or duplicate document ID.")
            ids.add(identifier)
            period = _period(document.get("period"))
            digest = document.get("sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise WorkspaceError("Invalid stored SHA-256.")
            relative = document.get("path")
            if not isinstance(relative, str) or Path(relative).is_absolute():
                raise WorkspaceError("Indexed path must be relative.")
            path = _inside(location, relative)
            expected_parent = _path(location, f"06_bookkeeping/{period[:4]}/{period[5:]}/originals")
            if path.parent != expected_parent or path.stem != digest or path.suffix not in EXTENSIONS:
                raise WorkspaceError("Indexed original path does not match the document metadata.")
            canonical = path.relative_to(location).as_posix()
            if canonical in paths:
                raise WorkspaceError("Duplicate indexed path.")
            paths.add(canonical)
            data = _read_regular(path)
            if len(data) != document.get("size_bytes") or hashlib.sha256(data).hexdigest() != digest:
                raise WorkspaceError("Original content or size has changed.")
        except (WorkspaceError, OSError, TypeError) as exc:
            errors.append({"document_id": label, "issue": str(exc)})
    originals, scan_issues = _scan_originals(location)
    errors.extend(scan_issues)
    unindexed = [path.relative_to(location).as_posix() for path in originals
                 if path.relative_to(location).as_posix() not in paths]
    errors.extend({"document_id": None, "path": relative,
                   "issue": "Unindexed original file; review interrupted imports before continuing."}
                  for relative in unindexed)
    return {"status": "ok" if not errors else "needs_review", "indexed_documents": len(registry["documents"]),
            "unindexed_originals": len(unindexed), "errors": errors,
            "scope": "Indexed file integrity and canonical originals inventory; no GoBD or tax compliance certification."}


def _rows(data: bytes, required: set) -> List[Dict[str, str]]:
    try:
        reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline=""))
        fields = reader.fieldnames
        if not fields or len(fields) != len(set(fields)) or not required.issubset(fields):
            raise WorkspaceError("CSV headers are missing or duplicated.")
        rows = list(reader)
        if any(None in row or any(row.get(key) is None for key in required) for row in rows):
            raise WorkspaceError("CSV rows do not match the required columns.")
        return rows
    except (UnicodeError, csv.Error) as exc:
        raise WorkspaceError("Expected valid UTF-8 comma-separated CSV.") from exc


def _amount(value: str) -> Decimal:
    text = value.strip()
    if len(text) > 200 or not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", text):
        raise WorkspaceError("Amounts must be finite signed decimals using a dot, without grouping or exponent notation.")
    number = Decimal(text)
    if not number.is_finite():
        raise WorkspaceError("Amounts must be finite.")
    return number


def _add(left: Decimal, right: Decimal) -> Decimal:
    with localcontext() as context:
        # Retain the entire aligned coefficient, including a possible carry.
        # The larger operand's own precision alone can discard a tiny addend.
        context.prec = max(1, max(left.adjusted(), right.adjusted())
                           - min(left.as_tuple().exponent, right.as_tuple().exponent) + 2)
        return left + right


def _currency(value: str) -> str:
    if not re.fullmatch(r"[A-Z]{3}", value):
        raise WorkspaceError("Currency must be a three-letter uppercase code.")
    return value


def _identifier(value: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise WorkspaceError("Identifiers must be nonempty and have no surrounding whitespace.")
    return value


def reconciliation_report(root: PathInput, bank: PathInput, ledger: PathInput, period: str) -> Dict[str, Any]:
    """Recompute a report from supplied bytes without writing workspace state."""
    location = _workspace(root)
    period = _period(period)
    bank_path, ledger_path = _inside(location, bank), _inside(location, ledger)
    bank_data, ledger_data = _read_regular(bank_path), _read_regular(ledger_path)
    bank_rows = _rows(bank_data, {"transaction_id", "booking_date", "amount", "currency"})
    ledger_rows = _rows(ledger_data, {"entry_id", "transaction_id", "amount", "currency"})
    transactions: Dict[str, Dict[str, Any]] = {}
    groups: Dict[tuple, Dict[str, Any]] = {}
    entry_ids = set()
    unlinked = []
    totals: Dict[str, Dict[str, Decimal]] = {}

    def total(currency: str, category: str, amount: Decimal) -> None:
        row = totals.setdefault(currency, {"bank_total": Decimal(0), "ledger_total": Decimal(0)})
        row[category] = _add(row[category], amount)

    for row in bank_rows:
        identifier = _identifier(row["transaction_id"])
        if identifier in transactions:
            raise WorkspaceError("Duplicate bank transaction_id.")
        booking = _day(row["booking_date"])
        if booking[:7] != period:
            raise WorkspaceError("Every bank booking_date must belong to the requested period.")
        amount, currency = _amount(row["amount"]), _currency(row["currency"])
        transactions[identifier] = {"amount": amount, "currency": currency}
        total(currency, "bank_total", amount)
    for row in ledger_rows:
        entry = _identifier(row["entry_id"])
        if entry in entry_ids:
            raise WorkspaceError("Duplicate ledger entry_id.")
        entry_ids.add(entry)
        amount, currency = _amount(row["amount"]), _currency(row["currency"])
        total(currency, "ledger_total", amount)
        if row["transaction_id"] == "":
            unlinked.append({"entry_id": entry, "amount": format(amount, "f"), "currency": currency})
            continue
        transaction = _identifier(row["transaction_id"])
        group = groups.setdefault((transaction, currency), {"amount": Decimal(0), "entry_ids": []})
        group["amount"] = _add(group["amount"], amount)
        group["entry_ids"].append(entry)

    matches, differences, unmatched_bank, unmatched_ledger = [], [], [], []
    for identifier, transaction in transactions.items():
        key = (identifier, transaction["currency"])
        group = groups.get(key)
        if group is None:
            unmatched_bank.append({"transaction_id": identifier, "currency": transaction["currency"],
                                   "amount": format(transaction["amount"], "f")})
            continue
        difference = _add(transaction["amount"], group["amount"].copy_negate())
        item = {"transaction_id": identifier, "currency": transaction["currency"],
                "bank_amount": format(transaction["amount"], "f"), "ledger_amount": format(group["amount"], "f"),
                "difference": format(difference, "f"), "entry_ids": group["entry_ids"]}
        (matches if difference == 0 else differences).append(item)
    for (identifier, currency), group in groups.items():
        if identifier not in transactions or transactions[identifier]["currency"] != currency:
            unmatched_ledger.append({"transaction_id": identifier, "currency": currency,
                                     "amount": format(group["amount"], "f"), "entry_ids": group["entry_ids"],
                                     "reason": "unknown transaction_id or currency mismatch"})
    totals_out = {currency: {"bank_total": format(values["bank_total"], "f"),
                             "ledger_total": format(values["ledger_total"], "f"),
                             "difference": format(_add(values["bank_total"], values["ledger_total"].copy_negate()), "f")}
                  for currency, values in sorted(totals.items())}
    coverage = {"bank_rows": len(bank_rows), "ledger_rows": len(ledger_rows),
                "matched_groups": len(matches)}
    review_notes = []
    if not bank_rows or not ledger_rows:
        review_notes.append("An input has no data rows. Confirm source coverage and any no-activity period; empty inputs are not a completed match.")
    outcome = "needs_review" if differences or unmatched_bank or unmatched_ledger or unlinked or review_notes else "matched"
    report = {"schema_version": VERSION, "status": outcome, "period": period, "created_at": _now(),
              "method": "explicit transaction_id and currency only; no inferred matches",
              "sources": {"bank": {"path": bank_path.relative_to(location).as_posix(), "sha256": hashlib.sha256(bank_data).hexdigest()},
                          "ledger": {"path": ledger_path.relative_to(location).as_posix(), "sha256": hashlib.sha256(ledger_data).hexdigest()}},
              "matches": matches, "differences": differences, "unmatched_bank": unmatched_bank,
              "unmatched_ledger": unmatched_ledger, "unlinked_ledger_entries": unlinked,
              "totals_by_currency": totals_out, "coverage": coverage, "review_notes": review_notes,
              "note": "Derived review report only; no entries posted, tax treatment inferred, or period closed."}
    return report


def reconcile(root: PathInput, bank: PathInput, ledger: PathInput, period: str) -> Dict[str, Any]:
    location = _workspace(root)
    report = reconciliation_report(location, bank, ledger, period)
    outcome, coverage, review_notes = report["status"], report["coverage"], report["review_notes"]
    matches, differences = report["matches"], report["differences"]
    unmatched_bank, unmatched_ledger, unlinked = report["unmatched_bank"], report["unmatched_ledger"], report["unlinked_ledger_entries"]
    with _locked(location):
        _check_audit(location)
        relative = f"07_exports/{period}/reconciliation-{uuid.uuid4().hex}.json"
        path = _inside(location, relative)
        _mkdir(path.parent)
        _atomic_json(path, report)
        _audit(location, "reconciliation_prepared", {"path": relative, "status": outcome,
                                                     "bank_sha256": report["sources"]["bank"]["sha256"],
                                                     "ledger_sha256": report["sources"]["ledger"]["sha256"]})
    return {"status": outcome, "report": _physical(location, relative), "matched_groups": len(matches),
            "coverage": coverage, "review_notes": review_notes,
            "differences": len(differences), "unmatched_bank": len(unmatched_bank),
            "unmatched_ledger": len(unmatched_ledger), "unlinked_ledger_entries": len(unlinked)}


def workspace_status(root: PathInput) -> Dict[str, Any]:
    location = _workspace(root)
    preferences = _preferences(_load(_inside(location, MARKER)))
    profile = _load(_inside(location, PROFILE))
    if not isinstance(profile, dict) or not isinstance(profile.get("facts"), dict):
        raise WorkspaceError("Business profile is invalid.")
    counts = {status: 0 for status in sorted(STATUSES)}
    invalid_fields = []
    evidence_issues = []
    for field, fact in profile["facts"].items():
        if not isinstance(fact, dict) or fact.get("status") not in STATUSES:
            raise WorkspaceError("Fact status is invalid.")
        counts[fact["status"]] += 1
        if fact["status"] == "verified":
            try:
                evidence = fact.get("evidence")
                if (not isinstance(evidence, dict) or set(evidence) != {"path", "sha256"}
                        or fact.get("source") != {"kind": "file", "ref": evidence["path"]}
                        or hashlib.sha256(_read_regular(_evidence_path(location, evidence["path"]))).hexdigest() != evidence["sha256"]):
                    raise WorkspaceError("Verified evidence missing or changed.")
            except (OSError, WorkspaceError, TypeError, KeyError):
                evidence_issues.append(field)
        try:
            if field not in FIELDS:
                raise WorkspaceError("Unknown field")
            if fact["status"] != "unknown":
                _fact_value(field, fact.get("value"))
            elif fact.get("value") is not None:
                raise WorkspaceError("Unknown facts must be null")
        except (WorkspaceError, TypeError, ValueError):
            invalid_fields.append(field)
    invalid_fields.extend(sorted(set(FIELDS) - set(profile["facts"])))
    lists = {}
    issues = ["invalid_profile_values"] if invalid_fields else []
    if evidence_issues:
        issues.append("verified_fact_evidence_needs_review")
    if profile.get("schema_version") != VERSION:
        issues.append("profile_schema_invalid")
    try:
        _check_audit(location)
    except (WorkspaceError, OSError):
        issues.append("audit_invalid")
    for name in ("tasks", "questions", "decisions"):
        try:
            lists[name] = len(_entries(location, name))
        except (WorkspaceError, OSError, TypeError, ValueError):
            lists[name] = None
            issues.append(name + "_invalid")
    missing = []
    try:
        missing = _runtime_review(location, _load(_inside(location, RUNTIME)))
        review_status = "not_recorded" if missing else "recorded"
    except (WorkspaceError, OSError, TypeError, ValueError):
        issues.append("runtime_invalid")
        review_status = "invalid"
    locked = (location / LOCK).exists()
    if locked:
        issues.append("workspace_locked")
    result_status = "needs_attention" if issues else "setup_incomplete" if missing else "configured"
    return {"status": result_status, "workspace_health": "needs_attention" if issues else "ok",
            "data_processing_review": review_status, "setup_missing": missing, "issues": issues,
            "invalid_profile_fields": sorted(invalid_fields), "synthetic_work_available": not issues,
            "verified_fact_evidence_issues": sorted(evidence_issues),
            "next_action": "Review the listed issues without reinitializing." if issues else
                           "Review the actual data-processing route; use synthetic data meanwhile." if missing else
                           "Check the recorded assessment scope and current capabilities for this task.",
            "language": preferences["language"], "mode": preferences["mode"],
            "folder_language": _layout(location)[0]["language"] if _layout(location) else None,
            "folder_layout": "localized" if _layout(location) else "legacy",
            "fact_status_counts": counts, "documents": len(_documents(location)["documents"]),
            "list_item_counts": lists, "locked": locked}


def start_workspace(root: PathInput, year: Optional[int] = None, language: str = "en",
                    mode: str = "general", layout: str = "localized") -> Dict[str, Any]:
    location = _absolute(root)
    _check_chain(location)
    _private_boundary(location)
    exists = (_inside(location, MARKER)).exists()
    if not exists:
        init_workspace(location, date.today().year if year is None else year, language, mode, layout)
    return {"action": "resumed" if exists else "created", **workspace_status(location)}


def workspace_folders(root: PathInput) -> Dict[str, Any]:
    location = _workspace(root)
    layout = _layout(location)
    words = _load(Path(__file__).resolve().parents[1] / 'assets/folder-layouts.json')['languages']['en']
    return {'layout': 'localized' if layout else 'legacy',
            'folder_language': layout[0]['language'] if layout else None,
            'paths': {key: _physical(location, key) for key in words['paths']},
            'guide': layout[1]['guide_name'] if layout else None}


def diagnose_workspace(root: PathInput) -> Dict[str, Any]:
    result = workspace_status(root)
    verification = verify_workspace(root)
    if verification["status"] != "ok":
        result["status"] = result["workspace_health"] = "needs_attention"
        result["issues"].append("original_integrity")
        result["next_action"] = "Run verify and inspect the original-integrity issues; preserve all files."
    result.update(python_version=sys.version.split()[0], platform=sys.platform,
                  host_capabilities="not_probed", original_integrity=verification["status"],
                  note="Local diagnostics do not verify desktop discovery, cloud processing, permissions or legal compliance.")
    return result


def create_demo(root: PathInput, year: int = 2026, language: str = "en") -> Dict[str, Any]:
    if language not in {"en", "ru"}:
        raise WorkspaceError("The demo supports en and ru.")
    init_workspace(root, year, language, "bookkeeping")
    location = _workspace(root)
    period = f"{year}-01"
    bank = ("transaction_id,booking_date,amount,currency\n"
            f"DEMO-1,{period}-05,-105.00,EUR\nDEMO-2,{period}-06,500.00,EUR\n"
            f"DEMO-3,{period}-07,-100.00,USD\nDEMO-4,{period}-08,-12.00,EUR\n")
    ledger = ("entry_id,transaction_id,amount,currency\n"
              "DEMO-E1,DEMO-1,-100.00,EUR\nDEMO-E2,DEMO-1,-5.00,EUR\n"
              "DEMO-E3,DEMO-2,500.00,EUR\nDEMO-E4,DEMO-3,-100.00,USD\n")
    with _locked(location):
        _check_audit(location)
        marker = _load(_inside(location, MARKER))
        marker["purpose"] = "synthetic_demo"
        _atomic_json(_inside(location, MARKER), marker, replace=True)
        _write_exclusive(location / "03_banking/demo-bank.csv", bank.encode("utf-8"))
        _write_exclusive(location / "04_accounting/demo-ledger.csv", ledger.encode("utf-8"))
    for source in ("03_banking/demo-bank.csv", "04_accounting/demo-ledger.csv"):
        ingest_document(location, source, period)
    reconciliation = reconcile(location, "03_banking/demo-bank.csv", "04_accounting/demo-ledger.csv", period)
    text = ("# Демонстрация на вымышленных данных\n\n"
            "Это учебная папка. Храните реальные документы отдельно.\n\n"
            "Сверены 3 группы: EUR 105 с комиссией EUR 5, поступление EUR 500 и расход USD 100. "
            "Расход EUR 12 не связан с записью: требуется проверка. Валюты не суммируются.\n\n"
            "Далее: откройте отчёт, найдите несвязанный расход, затем попросите продолжить эту демонстрацию. "
            "Совпадение сумм не подтверждает налоговую правильность. Ничего не отправлено и не проведено.\n"
            if language == "ru" else
            "# Synthetic demonstration\n\nThis is a practice folder. Keep real documents elsewhere.\n\n"
            "Three groups match: EUR 105 split into expense and EUR 5 fee, EUR 500 income, and USD 100 expense. "
            "The EUR 12 outflow is unlinked and needs review. Currencies remain separate.\n\n"
            "Next: open the report, inspect the unmatched outflow, then ask to continue this demonstration. "
            "Matching amounts do not establish tax correctness. Nothing was posted or submitted.\n")
    with _locked(location):
        _check_audit(location)
        _write_exclusive(location / "START-HERE.md", (text + "\n" + reconciliation["report"] + "\n").encode("utf-8"))
        _audit(location, "synthetic_demo_created", {"period": period})
    return {"status": "demo_created", "guide": "START-HERE.md", "reconciliation": reconciliation,
            "next_action": "Open START-HERE.md; use start to resume without reinitializing."}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("start", "demo"):
        command = commands.add_parser(name, help="Create/resume private work" if name == "start" else "Create a NEW synthetic practice workspace")
        command.add_argument("--root", required=True)
        command.add_argument("--year", type=int, default=date.today().year)
        command.add_argument("--language", choices=("en", "ru", "de") if name == "start" else ("en", "ru"), default="en")
        if name == "start":
            command.add_argument("--layout", choices=("localized", "legacy"), default="localized")
            command.add_argument("--mode", choices=sorted(MODES), default="general")
    runtime = commands.add_parser("runtime", help="Record assessed processing configuration with local evidence")
    runtime.add_argument("--root", required=True)
    runtime.add_argument("--input", required=True, help="JSON inside workspace; never credentials")
    entry = commands.add_parser("entry", help="Inspect or save a validated task/question/decision with history")
    entry.add_argument("--root", required=True)
    entry.add_argument("--collection", required=True, choices=sorted(ENTRY_STATES))
    entry_input = entry.add_mutually_exclusive_group(required=True)
    entry_input.add_argument("--input", help="Entry JSON inside workspace")
    entry_input.add_argument("--id", help="Read only this entry's state and version hash")
    entry.add_argument("--expected-sha256", help="Required current entry hash for an update")
    init = commands.add_parser("init", help="Create an empty private workspace outside Git and skill folders")
    init.add_argument("--root", required=True)
    init.add_argument("--layout", choices=("localized", "legacy"), default="localized")
    init.add_argument("--year", required=True, type=int)
    init.add_argument("--language", choices=("ru", "en", "de"), default="ru",
                      help="Assistant language preference; German report templates are not yet complete")
    init.add_argument("--mode", choices=("general", "bookkeeping", "tax-consultant"), default="general",
                      help="Workflow preference only; does not change business facts or tax regime")
    configure = commands.add_parser("configure", help="Persist assistant language/workflow mode without changing business or tax facts")
    configure.add_argument("--root", required=True)
    configure.add_argument("--language", choices=("ru", "en", "de"),
                           help="Assistant language preference; German report templates are not yet complete")
    configure.add_argument("--mode", choices=("general", "bookkeeping", "tax-consultant"))
    record = commands.add_parser("record", help="Record one evidence-backed fact; verified means checked evidence, not model confidence")
    record.add_argument("--root", required=True)
    record.add_argument("--input", required=True, help="JSON file inside workspace, or - for stdin")
    ingest = commands.add_parser("ingest", help="Copy original bytes without OCR or XML parsing")
    ingest.add_argument("--root", required=True)
    ingest.add_argument("--source", required=True, help="Local regular file; absolute path may be outside workspace")
    ingest.add_argument("--period", required=True)
    for name in ("verify", "status", "doctor", "folders"):
        command = commands.add_parser(name)
        command.add_argument("--root", required=True)
    reconcile_parser = commands.add_parser("reconcile", help="Compare explicit IDs and Decimal amounts from two workspace CSVs")
    reconcile_parser.add_argument("--root", required=True)
    reconcile_parser.add_argument("--bank", required=True)
    reconcile_parser.add_argument("--ledger", required=True)
    reconcile_parser.add_argument("--period", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "start":
            result = start_workspace(args.root, args.year, args.language, args.mode, args.layout)
        elif args.command == "demo":
            result = create_demo(args.root, args.year, args.language)
        elif args.command == "runtime":
            result = configure_runtime(args.root, _load(_inside(_workspace(args.root), args.input)))
        elif args.command == "entry":
            if args.id is not None:
                if args.expected_sha256 is not None:
                    raise WorkspaceError("A previous hash is only used with an update input.")
                result = entry_status(args.root, args.collection, args.id)
            else:
                result = save_entry(args.root, args.collection,
                                    _load(_inside(_workspace(args.root), args.input)), args.expected_sha256)
        elif args.command == "doctor":
            result = diagnose_workspace(args.root)
        elif args.command == "folders":
            result = workspace_folders(args.root)
        elif args.command == "init":
            result = init_workspace(args.root, args.year, args.language, args.mode, args.layout)
        elif args.command == "configure":
            result = configure_workspace(args.root, args.language, args.mode)
        elif args.command == "record":
            if args.input == "-":
                payload = sys.stdin.buffer.read(MAX_BYTES + 1)
                if len(payload) > MAX_BYTES:
                    raise WorkspaceError("Input exceeds the 50 MiB limit.")
                value = _json_bytes(payload)
            else:
                value = _load(_inside(_workspace(args.root), args.input))
            result = record_fact(args.root, value)
        elif args.command == "ingest":
            result = ingest_document(args.root, args.source, args.period)
        elif args.command == "verify":
            result = verify_workspace(args.root)
        elif args.command == "reconcile":
            result = reconcile(args.root, args.bank, args.ledger, args.period)
        else:
            result = workspace_status(args.root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if args.command == "verify" and result["errors"] else 0
    except (WorkspaceError, OSError, TypeError) as exc:
        print(f"Operation stopped: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
