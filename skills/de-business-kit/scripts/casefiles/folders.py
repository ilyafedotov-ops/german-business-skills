"""Bounded metadata-only inventory; never import, unpack or modify source files."""
import hashlib
import os
from pathlib import Path
import stat
import uuid

import workspace as ws
from . import storage as st

KEY_SUFFIXES = {".pfx", ".p12", ".pem", ".key", ".kdbx"}


def linked(info):
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def directory(path):
    ws._check_chain(path)
    for ancestor in (path, *path.parents):
        if linked(ancestor.lstat()):
            raise ws.WorkspaceError("Linked or reparse-point source paths require a separately inspected physical/export location.")


def scan(root, source, max_entries=1000, max_depth=10):
    root = ws._workspace(root)
    source = ws._absolute(source)
    directory(source)
    if source == root or source in root.parents or root in source.parents:
        raise ws.WorkspaceError("Keep the existing source folder and destination workspace separate, without ancestor overlap.")
    if (source / ws.MARKER).exists():
        raise ws.WorkspaceError("This source is an existing workspace; resume or review an explicit migration instead of importing it.")
    if type(max_entries) is not int or not 1 <= max_entries <= 10000 or type(max_depth) is not int or not 0 <= max_depth <= 32:
        raise ws.WorkspaceError("Use 1-10000 inventory entries and depth 0-32.")
    entries, warnings, pending = [], set(), [(source, 0)]
    truncated = False
    while pending and not truncated:
        parent, depth = pending.pop()
        try:
            directory(parent)
            with os.scandir(parent) as children:
                for child in children:
                    if len(entries) >= max_entries:
                        warnings.add("entry_limit")
                        truncated = True
                        break
                    path = Path(child.path)
                    row = {"path": path.relative_to(source).as_posix(), "status": "skipped", "reason": None}
                    entries.append(row)
                    try:
                        info = child.stat(follow_symlinks=False)
                        if linked(info):
                            row["reason"] = "link_or_reparse_point"
                        elif (child.name.startswith(".")
                              or getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_HIDDEN", 2)
                              or getattr(info, "st_flags", 0) & getattr(stat, "UF_HIDDEN", 0x8000)):
                            row["reason"] = "hidden_entry"
                        elif path.suffix.lower() in KEY_SUFFIXES:
                            row["reason"] = "credential_or_key"
                        elif stat.S_ISDIR(info.st_mode):
                            if (path / ws.MARKER).exists():
                                row["reason"] = "existing_workspace"
                            elif depth >= max_depth:
                                row["reason"] = "depth_limit"
                                warnings.add("depth_limit")
                            else:
                                row["status"] = "directory"
                                pending.append((path, depth + 1))
                        elif not stat.S_ISREG(info.st_mode):
                            row["reason"] = "non_regular_file"
                        else:
                            row.update(size_bytes=info.st_size, modified_ns=info.st_mtime_ns)
                            if path.suffix.lower() not in ws.EXTENSIONS:
                                row["reason"] = "unsupported_format"
                            elif info.st_size > ws.MAX_BYTES:
                                row["reason"] = "file_too_large"
                            else:
                                row["status"] = "candidate"
                    except OSError:
                        row["reason"] = "unreadable_entry"
                        warnings.add("unreadable_entry")
        except (OSError, ws.WorkspaceError):
            warnings.add("unreadable_or_changed_directory")
            for row in entries:
                if row["path"] == parent.relative_to(source).as_posix():
                    row.update(status="skipped", reason="unreadable_or_changed_directory")
    counts = {name: sum(row["status"] == name for row in entries) for name in ("candidate", "directory", "skipped")}
    report = {"schema_version": 1, "status": "preview", "source_folder": str(source), "created_at": ws._now(),
              "limits": {"max_entries": max_entries, "max_depth": max_depth}, "traversal_complete": not warnings,
              "counts": counts, "warnings": sorted(warnings), "entries": sorted(entries, key=lambda row: row["path"]),
              "scope": "Metadata inventory within stated limits/exclusions only. No file contents read, business classification, import, hashing of source contents, cloud hydration or complete-accounting claim. Review candidates and omissions before selected intake."}
    payload = st.encoded(report)
    if len(payload) > ws.MAX_BYTES:
        raise ws.WorkspaceError("Inventory exceeds the supported report size; choose a smaller source scope.")
    relative = "00_admin/inbox/folder-scan-" + uuid.uuid4().hex + ".json"
    with ws._locked(root):
        ws._check_audit(root)
        ws._write_exclusive(ws._inside(root, relative), payload)
        ws._audit(root, "folder_previewed", {"path": relative, "counts": counts, "traversal_complete": not warnings})
    return {"status": "preview", "path": relative, "sha256": hashlib.sha256(payload).hexdigest(),
            "counts": counts, "traversal_complete": not warnings, "warnings": sorted(warnings)}
