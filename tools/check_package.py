#!/usr/bin/env python3
"""Check package completeness and local references without network access."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "de-business-kit"


def main():
    errors = []
    required = [
        "README.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md",
        "tools/install.py", "docs/architecture.md", "docs/validation.md",
        "evals/scenarios.json", "skills/de-business-kit/SKILL.md",
        "skills/de-business-kit/agents/openai.yaml",
        "skills/de-business-kit/scripts/workspace.py",
    ]
    for name in required:
        if not (ROOT / name).is_file():
            errors.append("Missing required file: " + name)
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not skill_text.startswith("---\nname: de-business-kit\n") or "\ndescription:" not in skill_text:
        errors.append("Missing skill name/description frontmatter")
    if len(skill_text.splitlines()) >= 500:
        errors.append("SKILL.md must stay under 500 lines")
    for file in ROOT.rglob("*"):
        if any(part in {".git", "__pycache__"} for part in file.relative_to(ROOT).parts):
            continue
        if file.is_symlink():
            errors.append("Symlink in distributable: " + str(file.relative_to(ROOT)))
            continue
        if not file.is_file():
            continue
        if file.suffix == ".json":
            try:
                json.loads(file.read_text(encoding="utf-8"))
            except (ValueError, UnicodeError) as exc:
                errors.append(f"Invalid JSON: {file.relative_to(ROOT)} ({exc})")
        if file.suffix == ".md":
            text = file.read_text(encoding="utf-8")
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link) or link.startswith("#"):
                    continue
                target = (file.parent / link.split("#")[0]).resolve()
                if not target.is_file() and not target.is_dir():
                    errors.append(f"Missing local link: {file.relative_to(ROOT)} -> {link}")
                if file.is_relative_to(SKILL) and not target.is_relative_to(SKILL):
                    errors.append(f"Skill link escapes its installed package: {link}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Package structure, local links and JSON: OK (no network/legal/integration validation)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
