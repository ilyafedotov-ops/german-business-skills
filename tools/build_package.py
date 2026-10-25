#!/usr/bin/env python3
"""Build fresh offline Codex and Claude marketplace folders and reproducible ZIPs.

Python 3.9+, standard library only. No installation, network, hooks or MCP servers.
ZIPs are transport archives: extract before adding a local marketplace directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
from typing import Dict, Optional, List
import zipfile


NAME = "de-business-kit"
MARKETPLACE = "de-business-kit-preview"


class BuildError(ValueError):
    """Unsafe output, incomplete resources or unreviewed package metadata."""


def absolute_path(value: Path) -> Path:
    path = value.expanduser()
    if ".." in path.parts:
        raise BuildError("Parent-directory components ('..') are not allowed.")
    return Path(os.path.abspath(str(path)))


def directory_chain(path: Path) -> None:
    for entry in reversed((path, *path.parents)):
        try:
            info = entry.lstat()
        except FileNotFoundError:
            continue
        if not stat.S_ISDIR(info.st_mode):
            raise BuildError(f"Symlink or non-directory rejected: {entry}")


def read_file(path: Path) -> bytes:
    directory_chain(path.parent)
    if not stat.S_ISREG(path.lstat().st_mode):
        raise BuildError(f"A regular file is required: {path}")
    return path.read_bytes()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def snapshot(source: Path) -> Dict[str, bytes]:
    """Read only the manifest, license and self-contained skill allowlist."""
    directory_chain(source)
    portable_bytes = read_file(source / "plugin.json")
    claude_bytes = read_file(source / ".claude-plugin/plugin.json")
    portable = json.loads(portable_bytes)
    claude = json.loads(claude_bytes)
    identity = {"name", "version", "description", "license", "author"}
    if set(portable) != identity | {"$schema", "extensions"} or set(claude) != identity:
        raise BuildError("Unexpected manifest fields; review packaging before adding capabilities.")
    if any(portable[key] != claude[key] for key in identity):
        raise BuildError("Host manifest identity/version mismatch.")
    if portable["name"] != NAME or portable["license"] != "MIT":
        raise BuildError("Unexpected package identity/license.")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[a-zA-Z0-9.-]+)?", portable["version"]):
        raise BuildError("A semantic package version is required.")
    if portable["$schema"] != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise BuildError("Unexpected portable plugin schema.")
    extensions = portable["extensions"]
    if not isinstance(extensions, dict) or set(extensions) != {"com.openai"}:
        raise BuildError("Only the reviewed OpenAI presentation extension is allowed.")
    openai = extensions["com.openai"]
    if not isinstance(openai, dict) or set(openai) != {"interface"}:
        raise BuildError("Hooks, MCP wiring and dynamic setup are not part of this package.")
    interface = openai["interface"]
    if not isinstance(interface, dict) or set(interface) != {"displayName", "shortDescription"}:
        raise BuildError("Unexpected OpenAI presentation fields.")
    if not all(isinstance(value, str) and value.strip() for value in interface.values()):
        raise BuildError("Nonempty presentation strings are required.")

    files = {"plugin.json": portable_bytes, ".claude-plugin/plugin.json": claude_bytes,
             "LICENSE": read_file(source / "LICENSE")}
    for name in ("README.md", "README.ru.md"):
        files[name] = read_file(source / "packaging" / name)
    skill = source / "skills" / NAME
    directory_chain(skill)
    if not skill.is_dir():
        raise BuildError("The canonical skill directory is missing.")
    for current, directories, filenames in os.walk(skill, followlinks=False):
        for name in sorted(directories + filenames):
            entry = Path(current) / name
            if (any(ord(character) < 32 for character in name)
                    or any(character in name for character in '\\:*?"<>|')
                    or name.endswith((".", " "))
                    or name.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL",
                        *{f"COM{number}" for number in range(1, 10)},
                        *{f"LPT{number}" for number in range(1, 10)}}):
                raise BuildError(f"Nonportable resource name rejected: {entry}")
            info = entry.lstat()
            if stat.S_ISDIR(info.st_mode):
                if name.startswith(".") or name == "__pycache__":
                    raise BuildError(f"Unexpected hidden/cache directory in skill: {entry}")
                continue
            if not stat.S_ISREG(info.st_mode):
                raise BuildError(f"Symlink or special resource rejected: {entry}")
            if name.startswith(".") or (entry.suffix not in {".md", ".json", ".yaml", ".py"}
                    and entry.relative_to(skill).as_posix() != "scripts/windows.ps1"):
                raise BuildError(f"Unreviewed skill resource type: {entry}")
            files[entry.relative_to(source).as_posix()] = read_file(entry)

    prefix = f"skills/{NAME}/"
    required = {
        "SKILL.md", "agents/openai.yaml", "scripts/workspace.py", "scripts/desk.py",
        "scripts/workflows.py", "scripts/payments.py", "assets/locales.json",
        "scripts/windows.ps1", "assets/workspace-seed.json", "references/native-windows.md",
        "assets/casework-messages.json", "assets/proposal.json", "assets/source-check.json",
        "assets/extracted-field.json",
        *("scripts/casefiles/" + name + ".py" for name in (
            "__init__", "storage", "documents", "folders", "reviews", "bank", "summary", "overview", "archive", "invoice_xml")),
    }
    if not all(prefix + name in files for name in required):
        raise BuildError("The canonical skill is missing a required runtime resource.")
    locales = json.loads(files[prefix + "assets/locales.json"])
    if set(locales["languages"]) != {"en", "ru"}:
        raise BuildError("English and Russian locale resources are required.")
    for language, locale in locales["languages"].items():
        for template in locale["templates"].values():
            relative = PurePosixPath(template)
            if relative.is_absolute() or ".." in relative.parts or relative.parts[0] != language:
                raise BuildError("A localized template escapes its language directory.")
            if prefix + "assets/" + str(relative) not in files:
                raise BuildError(f"Missing localized template: {template}")
    for name, content in files.items():
        if name.startswith(prefix) and name.endswith(".md"):
            for link in re.findall(r"\]\(([^)]+)\)", content.decode("utf-8")):
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link) or link.startswith("#"):
                    continue
                target = os.path.normpath(str(PurePosixPath(name).parent / link.split("#")[0])).replace("\\", "/")
                if not target.startswith(prefix) or (target not in files and not any(
                        item.startswith(target.rstrip("/") + "/") for item in files)):
                    raise BuildError(f"Missing or escaping skill reference: {name} -> {link}")
    return files


def build(*, source: Path, output: Path) -> Path:
    source, output = absolute_path(source), absolute_path(output)
    directory_chain(output.parent)
    if not output.parent.is_dir():
        raise BuildError("The output parent directory must already exist.")
    if output.exists() or output.is_symlink():
        raise BuildError(f"Refusing to overwrite an existing output: {output}")
    if source == output or source in output.parents:
        raise BuildError("Build outside the source checkout to preserve a clean package boundary.")
    files = snapshot(source)
    # Exclusive creation is the collision check after the read-only preflight.
    output.mkdir()
    try:
        checksums = []
        for host in ("codex", "claude"):
            catalog = {"name": MARKETPLACE, "plugins": [{"name": NAME}]}
            entry = catalog["plugins"][0]
            if host == "codex":
                catalog["interface"] = {"displayName": "German Business Kit Preview"}
                entry.update(source={"source": "local", "path": f"./plugins/{NAME}"},
                             policy={"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                             category="Productivity")
                catalog_path = ".agents/plugins/marketplace.json"
                host_files = {key: value for key, value in files.items() if not key.startswith(".claude-plugin/")}
            else:
                catalog["owner"] = {"name": "German Business Kit contributors"}
                catalog["description"] = "Local preview of German Business Kit workflows."
                entry["source"] = f"./plugins/{NAME}"
                catalog_path = ".claude-plugin/marketplace.json"
                host_files = {key: value for key, value in files.items() if key != "plugin.json"}
            package = {f"{host}/{catalog_path}": json_bytes(catalog)}
            package.update({f"{host}/plugins/{NAME}/{name}": data for name, data in host_files.items()})
            for name, data in sorted(package.items()):
                target = output / name
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("xb") as stream:
                    stream.write(data)
            archive = output / (host + ".zip")
            # Stored entries avoid platform/zlib-version variation; fixed metadata
            # removes source mtimes, permissions and local absolute paths.
            with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_STORED) as stream:
                for name, data in sorted(package.items()):
                    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                    info.create_system = 3
                    info.external_attr = (stat.S_IFREG | 0o644) << 16
                    stream.writestr(info, data)
            checksums.append(f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n")
        with (output / "SHA256SUMS").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write("".join(checksums))
    except (OSError, ValueError):
        shutil.rmtree(output)
        raise
    return output


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).absolute().parents[1],
                        help="Reviewed source checkout (defaults to this checkout)")
    parser.add_argument("--output", type=Path, required=True,
                        help="New directory outside the source checkout; parent must exist")
    args = parser.parse_args(argv)
    try:
        output = build(source=args.source, output=args.output)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"Package build stopped: {exc}", file=sys.stderr)
        return 2
    print(f"Built local marketplace folders, codex.zip, claude.zip and SHA256SUMS: {output}")
    print("Not installed or desktop-tested. Extract ZIPs before adding a marketplace directory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
