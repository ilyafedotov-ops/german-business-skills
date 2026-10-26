#!/usr/bin/env python3
"""Verified, portable directory backups of a complete private workspace."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import unicodedata
import uuid

import workspace as ws

SCHEMA = 'german-business-backup'
MANIFEST = 'manifest.json'
RESERVED = re.compile(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)', re.I)


def _relative(value):
    if not isinstance(value, str) or not value or value.startswith('/') or '\\' in value:
        raise ws.WorkspaceError('Invalid backup member path.')
    parts = value.split('/')
    if any(not part or part in {'.', '..'} or part.endswith((' ', '.')) or RESERVED.match(part)
           or any(ord(c) < 32 or c in '<>:"|?*' for c in part) for part in parts):
        raise ws.WorkspaceError('Backup member is not a safe portable path.')
    if PurePosixPath(value).as_posix() != value:
        raise ws.WorkspaceError('Noncanonical backup member path.')
    return value


def _key(value):
    return unicodedata.normalize('NFC', value).casefold()


def _safe_chain(path, final_file=False):
    ws._check_chain(path, final_file=final_file)
    for candidate in (path, *path.parents):
        try:
            info = candidate.lstat()
        except FileNotFoundError:
            continue
        if getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 1024):
            raise ws.WorkspaceError('Reparse paths are not allowed.')


def _location(value):
    if not Path(value).is_absolute() or str(value).startswith(('\\\\', '//')):
        raise ws.WorkspaceError('Use an absolute local directory path.')
    path = ws._absolute(value)
    _safe_chain(path)
    ws._private_boundary(path)
    return path


def _fresh(value, outside):
    path = _location(value)
    if path == outside or outside in path.parents or path in outside.parents:
        raise ws.WorkspaceError('Recovery destinations must be outside the source tree.')
    if path.exists():
        raise ws.WorkspaceError('Destination already exists; choose a new private directory.')
    if not path.parent.is_dir():
        raise ws.WorkspaceError('Destination parent directory must already exist.')
    return path


def _file(path, destination=None):
    _safe_chain(path, final_file=True)
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    digest = hashlib.sha256()
    total = 0
    with os.fdopen(os.open(str(path), flags), 'rb') as source:
        before = os.fstat(source.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise ws.WorkspaceError('Backup members must be regular files.')
        output = None
        try:
            if destination is not None:
                _safe_chain(destination, final_file=True)
                output = os.fdopen(os.open(str(destination), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'wb')
            while True:
                chunk = source.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
                total += len(chunk)
                if output is not None:
                    output.write(chunk)
            if output is not None:
                output.flush()
                os.fsync(output.fileno())
            after = os.fstat(source.fileno())
            if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns) or total != after.st_size:
                raise ws.WorkspaceError('Source changed while being copied; retain partial files for inspection.')
        finally:
            if output is not None:
                output.close()
    return {'sha256': digest.hexdigest(), 'size_bytes': total}


def _inventory(root, exclude_lock=False):
    _safe_chain(root)
    if not root.is_dir():
        raise ws.WorkspaceError('Backup directory is missing.')
    files, directories, seen = [], [], set()
    for folder, subdirs, names in os.walk(root, followlinks=False):
        for name in sorted(subdirs + names):
            path = Path(folder) / name
            relative = path.relative_to(root).as_posix()
            if exclude_lock and relative == ws.LOCK:
                continue
            _relative(relative)
            key = _key(relative)
            if key in seen:
                raise ws.WorkspaceError('Case or Unicode-colliding backup member paths.')
            seen.add(key)
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                _safe_chain(path)
                directories.append(relative)
            elif stat.S_ISREG(mode):
                files.append(dict(path=relative, **_file(path)))
            else:
                raise ws.WorkspaceError('Linked or special backup members are not supported.')
    return sorted(directories), sorted(files, key=lambda item: item['path'])


def _validate_manifest(value):
    required = {'schema', 'schema_version', 'backup_id', 'created_at', 'excluded_paths', 'directories', 'files'}
    if not isinstance(value, dict) or set(value) != required or value['schema'] != SCHEMA or type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ws.WorkspaceError('Unsupported backup manifest.')
    try:
        uuid.UUID(value['backup_id'])
    except (ValueError, TypeError, AttributeError):
        raise ws.WorkspaceError('Invalid backup identity.')
    if not isinstance(value['created_at'], str) or not value['created_at'] or value['excluded_paths'] != [ws.LOCK]:
        raise ws.WorkspaceError('Invalid backup metadata or exclusions.')
    if not isinstance(value['directories'], list) or not isinstance(value['files'], list):
        raise ws.WorkspaceError('Invalid backup member lists.')
    seen, dirs, paths = set(), set(), []
    for directory in value['directories']:
        dirs.add(_relative(directory))
        paths.append(directory)
    for item in value['files']:
        if (not isinstance(item, dict) or set(item) != {'path', 'sha256', 'size_bytes'}
                or type(item['size_bytes']) is not int or item['size_bytes'] < 0
                or not isinstance(item['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', item['sha256'])):
            raise ws.WorkspaceError('Invalid backup file record.')
        paths.append(_relative(item['path']))
    for path in paths:
        key = _key(path)
        if key in seen or path == ws.LOCK:
            raise ws.WorkspaceError('Duplicate, colliding or excluded backup member.')
        seen.add(key)
        parent = PurePosixPath(path).parent
        while str(parent) != '.':
            if str(parent) not in dirs:
                raise ws.WorkspaceError('Backup member has an unlisted parent directory.')
            parent = parent.parent
    return value


def verify_backup(backup):
    return _verified_backup(backup)[0]


def _verified_backup(backup):
    root = _location(backup)
    if not root.is_dir() or {p.name for p in root.iterdir()} != {MANIFEST, 'files'}:
        raise ws.WorkspaceError('Backup must contain only manifest.json and files/.')
    value = _validate_manifest(ws._load(root / MANIFEST))
    directories, files = _inventory(root / 'files')
    if directories != sorted(value['directories']) or files != sorted(value['files'], key=lambda item: item['path']):
        raise ws.WorkspaceError('Backup members are missing, unexpected or changed.')
    ws._workspace(root / 'files')
    return {'status': 'verified', 'backup_id': value['backup_id'], 'file_count': len(files),
            'directory_count': len(directories), 'excluded_paths': value['excluded_paths'],
            'scope': 'Complete workspace bytes and paths; excludes the active lock. No encryption or accounting correctness assessment.'}, value


def backup_workspace(root, destination):
    root = ws._workspace(_location(root))
    destination = _fresh(destination, root)
    with ws._locked(root):
        directories, files = _inventory(root, exclude_lock=True)
        destination.mkdir(mode=0o700)
        data = destination / 'files'
        data.mkdir(mode=0o700)
        for directory in sorted(directories, key=lambda item: (item.count('/'), item)):
            (data / directory).mkdir(mode=0o700)
        for record in files:
            if _file(root / record['path'], data / record['path']) != {key: record[key] for key in ('sha256', 'size_bytes')}:
                raise ws.WorkspaceError('Source changed after backup inventory; partial destination preserved.')
        if _inventory(root, exclude_lock=True) != (directories, files):
            raise ws.WorkspaceError('Workspace changed during backup; partial destination preserved.')
        manifest = {'schema': SCHEMA, 'schema_version': 1, 'backup_id': str(uuid.uuid4()),
                    'created_at': ws._now(), 'excluded_paths': [ws.LOCK], 'directories': directories, 'files': files}
        ws._atomic_json(destination / MANIFEST, manifest)
        return verify_backup(destination)


def restore_workspace(backup, root):
    backup = _location(backup)
    destination = _fresh(root, backup)
    checked, value = _verified_backup(backup)
    destination.mkdir(mode=0o700)
    with ws._locked(destination):
        for directory in sorted(value['directories'], key=lambda item: (item.count('/'), item)):
            (destination / directory).mkdir(mode=0o700)
        for record in value['files']:
            if _file(backup / 'files' / record['path'], destination / record['path']) != {key: record[key] for key in ('sha256', 'size_bytes')}:
                raise ws.WorkspaceError('Backup changed during restore; partial destination preserved.')
        if _inventory(destination, exclude_lock=True) != (sorted(value['directories']), sorted(value['files'], key=lambda item: item['path'])):
            raise ws.WorkspaceError('Restored workspace verification failed; preserve it for inspection.')
        ws._workspace(destination)
        original_integrity = ws.verify_workspace(destination)
    diagnosis = ws.diagnose_workspace(destination)
    return dict(checked, root=str(destination), original_integrity=original_integrity['status'],
                workspace_health=diagnosis['workspace_health'], diagnosis=diagnosis,
                next_action='Inspect the restored workspace and diagnostics before resuming; keep the backup.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    backup = commands.add_parser('backup'); backup.add_argument('--root', required=True); backup.add_argument('--destination', required=True)
    verify = commands.add_parser('verify'); verify.add_argument('--backup', required=True)
    restore = commands.add_parser('restore'); restore.add_argument('--backup', required=True); restore.add_argument('--root', required=True)
    args = parser.parse_args(argv)
    try:
        result = backup_workspace(args.root, args.destination) if args.action == 'backup' else verify_backup(args.backup) if args.action == 'verify' else restore_workspace(args.backup, args.root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ws.WorkspaceError, KeyError, TypeError, ValueError) as exc:
        print('Recovery stopped: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
