#!/usr/bin/env python3
"""Check repository documentation paths and Markdown anchors without network access.

This bounded checker covers inline/reference links, fenced and indented code,
ATX/setext headings and explicit HTML anchors. It is not a full Markdown parser.
Portable skill links remain covered separately by check_package.py.
"""
import argparse
from dataclasses import dataclass, field
import html
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
LABEL = re.compile(r"!?\[([^\]\n]+)\]")


@dataclass
class CheckResult:
    files: int = 0
    links: int = 0
    errors: list[str] = field(default_factory=list)


def repository_markdown_paths(root=ROOT):
    """Keep source selection independent of installed tools and generated output."""
    return sorted(set(root.glob("*.md")) | set((root / "docs").rglob("*.md"))
                  | set((root / "packaging").rglob("*.md")))


def prose(text):
    """Mask code blocks while preserving line numbers for diagnostics."""
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            lines.append("\n" if line.endswith("\n") else "")
        elif marker:
            fence = marker[1]
            lines.append("\n" if line.endswith("\n") else "")
        elif line.startswith(("    ", "\t")):
            lines.append("\n" if line.endswith("\n") else "")
        else:
            lines.append(line)
    return "".join(lines)


def destination(text, start, inline):
    """Read an angle-wrapped or balanced destination; ignore an optional title."""
    start += len(text[start:]) - len(text[start:].lstrip())
    if start >= len(text):
        return None
    index = start
    if text[start] == "<":
        end = text.find(">", start + 1)
        if end < 0:
            return None
        value = text[start + 1:end]
        index = end + 1
    else:
        depth = 0
        while index < len(text):
            char = text[index]
            if char == "\\" and index + 1 < len(text):
                index += 2
                continue
            if char.isspace() or (char == ")" and not depth):
                break
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            index += 1
        if depth:
            return None
        value = text[start:index]
    if inline:
        ending = re.match(r'''\s*(?:(?:"[^"\n]*"|'[^'\n]*'|\([^\n]*\))\s*)?\)''', text[index:])
        if not ending:
            return None
        index += ending.end()
    return html.unescape(re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])", r"\1", value)), index


def links(text):
    """Yield destinations and line numbers from the supported link forms."""
    text = re.sub(r"(`+)(.*?)\1(?!`)", lambda match: " " * len(match[0]), text)
    definitions = {}
    definition_lines = set()
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^ {0,3}\[([^\]]+)\]:\s*(.*)$", line)
        if match:
            parsed = destination(match[2], 0, inline=False)
            if parsed:
                definitions.setdefault(" ".join(match[1].lower().split()), parsed[0])
                definition_lines.add(number)
    consumed = 0
    for match in LABEL.finditer(text):
        if match.start() < consumed:
            continue
        number = text.count("\n", 0, match.start()) + 1
        if number in definition_lines:
            continue
        end = match.end()
        if text[end:end + 1] == "(":
            parsed = destination(text, end + 1, inline=True)
            if parsed:
                consumed = parsed[1]
                yield parsed[0], number
        else:
            reference = re.match(r"\[([^\]\n]*)\]", text[end:])
            key = (reference[1] or match[1]) if reference else match[1]
            if reference:
                consumed = end + reference.end()
            target = definitions.get(" ".join(key.lower().split()))
            if target is not None:
                yield target, number


def anchors(text):
    text = prose(text)
    result = set(re.findall(r'''\b(?:id|name)=["']([^"']+)["']''', text))
    used = set()
    previous = ""
    for line in text.splitlines():
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*$", line)
        title = re.sub(r"\s+#+\s*$", "", match[1]) if match else None
        if not match and previous.strip() and re.fullmatch(r" {0,3}(?:=+|-+)\s*", line):
            title = previous.strip()
        previous = line
        if title is None:
            continue
        title = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", title)
        title = re.sub(r"<[^>]+>", "", title)
        title = re.sub(r"(?<!\w)(_+)(?=\S)(.+?)(?<=\S)\1(?!\w)", r"\2", title)
        title = html.unescape(title).lower()
        slug = "".join(char for char in title
                       if char in "-_" or not unicodedata.category(char).startswith(("P", "S")))
        slug = re.sub(r"\s", "-", slug)
        candidate = slug
        suffix = 0
        while candidate in used:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        used.add(candidate)
        result.add(candidate)
    return result


def check_paths(paths):
    result = CheckResult()
    cached_anchors = {}
    for source in sorted(set(Path(path).resolve() for path in paths)):
        result.files += 1
        try:
            text = source.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            result.errors.append(f"{source}: cannot read Markdown: {error}")
            continue
        for link, line in links(prose(text)):
            if SCHEME.match(link) or link.startswith("//"):
                continue
            result.links += 1
            raw_path, _, fragment = link.partition("#")
            path = unquote(raw_path.split("?", 1)[0])
            target = (source.parent / path).resolve() if path else source
            prefix = f"{source}:{line}"
            if not target.exists():
                result.errors.append(f"{prefix}: missing path: {link}")
            elif fragment and target.suffix.lower() == ".md":
                if target not in cached_anchors:
                    try:
                        cached_anchors[target] = anchors(target.read_text(encoding="utf-8"))
                    except (OSError, UnicodeError) as error:
                        result.errors.append(f"{prefix}: cannot read anchor target: {link}: {error}")
                        continue
                if unquote(fragment) not in cached_anchors[target]:
                    result.errors.append(f"{prefix}: missing anchor: {link}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Markdown sources; defaults to root, docs and packaging Markdown")
    args = parser.parse_args()
    result = check_paths(args.paths or repository_markdown_paths())
    for error in result.errors:
        print(error)
    print(f"Checked {result.links} local links/anchors in {result.files} Markdown files; {len(result.errors)} errors")
    return int(bool(result.errors))


if __name__ == "__main__":
    raise SystemExit(main())
