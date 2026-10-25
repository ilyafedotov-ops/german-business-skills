#!/usr/bin/env python3
"""Copy the self-contained skill into a supported local skills directory.

Python 3.9+, standard library only. No network requests, dependencies, settings
changes, or automatic updates. Existing installations must be reviewed and
removed or moved by the user before installing again.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import stat
import sys
from typing import List, Optional, Tuple, Union


SKILL_NAME = "de-business-kit"
PathInput = Union[str, Path]


class InstallError(ValueError):
    """An unsafe or unsupported installation request."""


def _absolute_path(value: PathInput) -> Path:
    path = Path(value).expanduser()
    if ".." in path.parts:
        raise InstallError("Parent-directory components ('..') are not allowed.")
    # Do not resolve(): that would hide symlinks from the checks below.
    return Path(os.path.abspath(str(path)))


def _check_directory_chain(path: Path) -> None:
    """Reject symlinks and existing non-directories throughout a path."""
    for item in reversed((path, *path.parents)):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode):
            raise InstallError(f"Symlinked paths are not allowed: {item}")
        if not stat.S_ISDIR(info.st_mode):
            raise InstallError(f"A directory was expected: {item}")


def _read_package(source: Path) -> Tuple[List[Path], List[Tuple[Path, bytes, bool]]]:
    """Validate and snapshot the package before creating any destination."""
    _check_directory_chain(source)
    if not source.is_dir():
        raise InstallError(f"Skill source directory does not exist: {source}")
    manifest = source / "SKILL.md"
    if not manifest.is_file() or manifest.is_symlink():
        raise InstallError(f"A regular SKILL.md is required: {manifest}")

    directories: List[Path] = []
    files: List[Tuple[Path, bytes, bool]] = []
    for current, names, filenames in os.walk(source, followlinks=False):
        names.sort()
        filenames.sort()
        base = Path(current)
        for name in names:
            entry = base / name
            info = entry.lstat()
            if not stat.S_ISDIR(info.st_mode):
                raise InstallError(f"Symlink or special directory rejected: {entry}")
            directories.append(entry.relative_to(source))
        for name in filenames:
            entry = base / name
            info = entry.lstat()
            if not stat.S_ISREG(info.st_mode):
                raise InstallError(f"Symlink or special file rejected: {entry}")
            # Snapshot once; later target writes never read a changing package.
            files.append((entry.relative_to(source), entry.read_bytes(),
                          bool(info.st_mode & stat.S_IXUSR)))
    return directories, files


def _make_parents(path: Path, created: List[Path]) -> None:
    for item in reversed((path, *path.parents)):
        try:
            item.mkdir()
            created.append(item)
        except FileExistsError:
            _check_directory_chain(item)


def install(
    *,
    target: str,
    scope: str,
    project: Optional[PathInput] = None,
    home: Optional[PathInput] = None,
    source_skill: Optional[PathInput] = None,
    dry_run: bool = False,
) -> Tuple[Path, ...]:
    """Install one skill, preflighting every target before any write.

    ``home`` and ``source_skill`` are explicit API seams for isolated tests or
    embedding. The CLI uses Path.home() and this repository's canonical skill.
    No environment variable overrides or global configuration are needed.
    """
    if target not in {"codex", "claude", "both"}:
        raise InstallError("target must be codex, claude, or both")
    if scope not in {"project", "user"}:
        raise InstallError("scope must be project or user")
    if scope == "project":
        if project is None:
            raise InstallError("--project is required with --scope project")
        base = _absolute_path(project)
        _check_directory_chain(base)
        if not base.is_dir():
            raise InstallError(f"The project directory must already exist: {base}")
    else:
        if project is not None:
            raise InstallError("--project is only valid with --scope project")
        base = _absolute_path(home if home is not None else Path.home())
        _check_directory_chain(base)
        if not base.is_dir():
            raise InstallError(f"The home directory must already exist: {base}")

    source = _absolute_path(
        source_skill if source_skill is not None
        else Path(__file__).absolute().parent.parent / "skills" / SKILL_NAME
    )
    directories, files = _read_package(source)
    hosts = ("codex", "claude") if target == "both" else (target,)
    roots = {"codex": ".agents", "claude": ".claude"}
    destinations = tuple(base / roots[host] / "skills" / SKILL_NAME for host in hosts)

    for destination in destinations:
        _check_directory_chain(destination.parent)
        if destination.exists() or destination.is_symlink():
            raise InstallError(f"Refusing to overwrite an existing path: {destination}")
        if source == destination or source in destination.parents:
            raise InstallError("A destination cannot be inside the source skill.")

    if dry_run:
        return destinations

    created_parents: List[Path] = []
    created_destinations: List[Path] = []
    try:
        # Exclusive creation also detects collisions appearing after preflight.
        for destination in destinations:
            _make_parents(destination.parent, created_parents)
            _check_directory_chain(destination.parent)
            destination.mkdir()
            created_destinations.append(destination)
        for destination in destinations:
            for relative in directories:
                (destination / relative).mkdir()
            for relative, content, executable in files:
                output = destination / relative
                with output.open("xb") as stream:
                    stream.write(content)
                if executable:
                    output.chmod(output.stat().st_mode | stat.S_IXUSR)
    except (OSError, InstallError):
        # Roll back only directories created by this invocation; preserve all
        # pre-existing parent directories and other tools' configuration.
        for destination in reversed(created_destinations):
            shutil.rmtree(destination)
        for parent in reversed(created_parents):
            try:
                parent.rmdir()
            except OSError:
                pass  # Never remove a nonempty or independently changed parent.
        raise
    return destinations


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("codex", "claude", "both"), required=True)
    parser.add_argument("--scope", choices=("project", "user"), required=True)
    parser.add_argument("--project", type=Path, help="Existing project folder; required for project scope")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print paths without writing")
    args = parser.parse_args(argv)
    try:
        paths = install(target=args.target, scope=args.scope, project=args.project,
                        dry_run=args.dry_run)
    except (InstallError, OSError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        return 2
    for path in paths:
        print(f"{'Would install' if args.dry_run else 'Installed'}: {path}")
    if not args.dry_run:
        print("Files copied. Verify skill discovery in a local session; UI support was not tested here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
