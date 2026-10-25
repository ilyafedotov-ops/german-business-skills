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
PROFILE = "01_profile/business.json"
DOCUMENTS = "00_admin/documents.json"
EVENTS = "09_audit/events.json"
MARKER = "00_admin/workspace.json"
LOCK = ".workspace.lock"
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


def _inside(root: Path, value: PathInput) -> Path:
    supplied = Path(value).expanduser()
    if ".." in supplied.parts:
        raise WorkspaceError("Parent-directory components ('..') are not allowed.")
    path = _absolute(supplied if supplied.is_absolute() else root / supplied)
    if path == root or root not in path.parents:
        raise WorkspaceError("This input/output must be inside the private workspace.")
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
            return os.fstat(stream.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise


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


def init_workspace(root: PathInput, year: int, language: str = "ru") -> Dict[str, Any]:
    if isinstance(year, bool) or not isinstance(year, int) or not 1900 <= year <= 9999:
        raise WorkspaceError("Year must be an integer between 1900 and 9999.")
    if language not in {"ru", "de", "en"}:
        raise WorkspaceError("Language must be ru, de, or en.")
    location = _absolute(root)
    _check_chain(location)
    _private_boundary(location)
    if location.exists() and any(location.iterdir()):
        raise WorkspaceError("Initialization requires a new or empty directory.")
    _mkdir(location)
    with _locked(location):
        if any(child.name != LOCK for child in location.iterdir()):
            raise WorkspaceError("Initialization requires an empty directory.")
        directories = ["00_admin", "00_admin/inbox", "01_profile", "02_registration",
                       "03_banking", "04_accounting", f"05_tax/{year}", "07_exports",
                       "08_correspondence", "09_audit/history"]
        directories.extend(f"06_bookkeeping/{year}/{month:02d}/{part}"
                           for month in range(1, 13) for part in ("originals", "derived", "proposals"))
        for relative in directories:
            _mkdir(location / relative)
        marker = {"schema": SCHEMA, "schema_version": VERSION, "workspace_id": str(uuid.uuid4()),
                  "created_at": _now(), "initial_year": year, "language": language}
        _atomic_json(location / MARKER, marker)
        _atomic_json(location / PROFILE, {"schema_version": VERSION, "facts": {field: _blank_fact() for field in FIELDS}})
        runtime = {"schema_version": VERSION, "assistant_product": None, "app_version": None,
                   "session_execution": "unknown", "model_provider": None,
                   "authentication_type": None, "contract_plan": None,
                   "training_policy_checked_at": None, "dpa_status": "unknown",
                   "retention_policy_reference": None, "residency_scope": "unknown",
                   "third_party_connectors": [], "client_data_mode": "synthetic_or_redacted_until_reviewed"}
        _atomic_json(location / "00_admin/runtime.json", runtime)
        for name in ("tasks", "questions", "decisions"):
            _atomic_json(location / f"00_admin/{name}.json", [])
        _atomic_json(location / DOCUMENTS, {"schema_version": VERSION, "documents": []})
        _atomic_json(location / EVENTS, [])
        _audit(location, "workspace_initialized", {"year": year, "language": language})
    return {"status": "initialized", "year": year, "language": language,
            "facts": len(FIELDS), "permissions": "owner POSIX modes best effort; no ACL or encryption guarantee"}


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
    source_path = _absolute(supplied if supplied.is_absolute() else location / supplied)
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

    for year in children(location / "06_bookkeeping"):
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
            for path in children(month / "originals"):
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
            expected_parent = location / f"06_bookkeeping/{period[:4]}/{period[5:]}/originals"
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


def reconcile(root: PathInput, bank: PathInput, ledger: PathInput, period: str) -> Dict[str, Any]:
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
    with _locked(location):
        _check_audit(location)
        relative = f"07_exports/{period}/reconciliation-{uuid.uuid4().hex}.json"
        path = _inside(location, relative)
        _mkdir(path.parent)
        _atomic_json(path, report)
        _audit(location, "reconciliation_prepared", {"path": relative, "status": outcome,
                                                     "bank_sha256": report["sources"]["bank"]["sha256"],
                                                     "ledger_sha256": report["sources"]["ledger"]["sha256"]})
    return {"status": outcome, "report": relative, "matched_groups": len(matches),
            "coverage": coverage, "review_notes": review_notes,
            "differences": len(differences), "unmatched_bank": len(unmatched_bank),
            "unmatched_ledger": len(unmatched_ledger), "unlinked_ledger_entries": len(unlinked)}


def workspace_status(root: PathInput) -> Dict[str, Any]:
    location = _workspace(root)
    profile = _load(_inside(location, PROFILE))
    if not isinstance(profile, dict) or not isinstance(profile.get("facts"), dict):
        raise WorkspaceError("Business profile is invalid.")
    counts = {status: 0 for status in sorted(STATUSES)}
    for fact in profile["facts"].values():
        if not isinstance(fact, dict) or fact.get("status") not in STATUSES:
            raise WorkspaceError("Fact status is invalid.")
        counts[fact["status"]] += 1
    lists = {}
    for name in ("tasks", "questions", "decisions"):
        data = _load(_inside(location, f"00_admin/{name}.json"))
        if not isinstance(data, list):
            raise WorkspaceError("Workspace task/question/decision file must be a list.")
        lists[name] = len(data)
    return {"status": "ready", "fact_status_counts": counts, "documents": len(_documents(location)["documents"]),
            "list_item_counts": lists, "locked": (location / LOCK).exists()}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create an empty private workspace outside Git and skill folders")
    init.add_argument("--root", required=True)
    init.add_argument("--year", required=True, type=int)
    init.add_argument("--language", choices=("ru", "de", "en"), default="ru")
    record = commands.add_parser("record", help="Record one evidence-backed fact; verified means checked evidence, not model confidence")
    record.add_argument("--root", required=True)
    record.add_argument("--input", required=True, help="JSON file inside workspace, or - for stdin")
    ingest = commands.add_parser("ingest", help="Copy original bytes without OCR or XML parsing")
    ingest.add_argument("--root", required=True)
    ingest.add_argument("--source", required=True, help="Local regular file; absolute path may be outside workspace")
    ingest.add_argument("--period", required=True)
    for name in ("verify", "status"):
        command = commands.add_parser(name)
        command.add_argument("--root", required=True)
    reconcile_parser = commands.add_parser("reconcile", help="Compare explicit IDs and Decimal amounts from two workspace CSVs")
    reconcile_parser.add_argument("--root", required=True)
    reconcile_parser.add_argument("--bank", required=True)
    reconcile_parser.add_argument("--ledger", required=True)
    reconcile_parser.add_argument("--period", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = init_workspace(args.root, args.year, args.language)
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
