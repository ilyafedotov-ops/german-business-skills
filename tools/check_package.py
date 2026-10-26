#!/usr/bin/env python3
"""Check package completeness and local references without network access."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "de-business-kit"


def checked_files(root):
    """Check authored source; development dependencies and reports are not shipped."""
    local_only = {"node_modules", ".venv", "venv", "output", "dist", "test-results",
                  "playwright-report", ".playwright-mcp"}
    for file in root.rglob("*"):
        parts = file.relative_to(root).parts
        if parts[0] in local_only or any(part in {".git", "__pycache__"} for part in parts):
            continue
        yield file


def main():
    errors = []
    required = [
        "README.md", "README.ru.md", "LICENSE", "SECURITY.md", "SECURITY.ru.md",
        "CONTRIBUTING.md", "CONTRIBUTING.ru.md",
        "tools/install.py", "docs/architecture.md", "docs/architecture.ru.md",
        "docs/accounting.md", "docs/accounting.ru.md",
        "skills/de-business-kit/scripts/casefiles/accounting.py",
        "skills/de-business-kit/references/accounting-workflow.md",
        "skills/de-business-kit/references/submission-integration-sources.md",
        "docs/validation.md", "docs/validation.ru.md", "docs/modes.md", "docs/modes.ru.md",
        "evals/scenarios.json", "skills/de-business-kit/SKILL.md",
        "skills/de-business-kit/agents/openai.yaml",
        "skills/de-business-kit/scripts/workspace.py",
        "skills/de-business-kit/references/tax-consultant.md",
        "skills/de-business-kit/references/language-and-modes.md",
        "skills/de-business-kit/assets/locales.json",
        "plugin.json", ".claude-plugin/plugin.json", "tools/build_package.py",
        "packaging/README.md", "packaging/README.ru.md",
        "docs/quickstart.md", "docs/quickstart.ru.md", "docs/distribution.md", "docs/distribution.ru.md",
        "skills/de-business-kit/references/onboarding.md",
        "skills/de-business-kit/references/legal-boundaries.md",
        "skills/de-business-kit/scripts/workflows.py", "skills/de-business-kit/scripts/payments.py",
        "skills/de-business-kit/assets/form-catalog.json", "skills/de-business-kit/assets/preparation-messages.json",
        "skills/de-business-kit/references/preparation.md", "skills/de-business-kit/references/international.md",
        "skills/de-business-kit/references/payments.md", "skills/de-business-kit/references/classification.md",
        "docs/service-selection.md", "docs/service-selection.ru.md",
        "docs/windows.md", "docs/windows.ru.md",
        "skills/de-business-kit/scripts/windows.ps1", "skills/de-business-kit/assets/workspace-seed.json", "skills/de-business-kit/assets/folder-layouts.json",
        "skills/de-business-kit/references/native-windows.md",
        "skills/de-business-kit/references/document-authoring.md", "skills/de-business-kit/references/readable-output.md",
        "skills/de-business-kit/references/document-delivery-sources.md", "skills/de-business-kit/assets/readable-document.html",
        "skills/de-business-kit/assets/de/recipient-letter.md",
        "skills/de-business-kit/references/insurance.md", "skills/de-business-kit/references/service-research-sources.md",
        "docs/workflows.md", "docs/workflows.ru.md", "docs/existing-data.md", "docs/existing-data.ru.md",
        "skills/de-business-kit/scripts/casefiles/folders.py",
        "skills/de-business-kit/references/existing-data.md", "skills/de-business-kit/references/data-source-access.md",
        "docs/index.md", "docs/index.ru.md", "docs/document-workflow.md", "docs/document-workflow.ru.md",
        "docs/core-capabilities.md", "docs/core-capabilities.ru.md",
        "skills/de-business-kit/scripts/desk.py", "skills/de-business-kit/scripts/casefiles/archive.py",
        "skills/de-business-kit/references/document-workflow.md", "skills/de-business-kit/references/task-recipes.md",
        "skills/de-business-kit/assets/casework-messages.json",
    ]
    for name in required:
        if not (ROOT / name).is_file():
            errors.append("Missing required file: " + name)
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not skill_text.startswith("---\nname: de-business-kit\n") or "\ndescription:" not in skill_text:
        errors.append("Missing skill name/description frontmatter")
    if len(skill_text.splitlines()) >= 500:
        errors.append("SKILL.md must stay under 500 lines")
    try:
        manifest = json.loads((SKILL / "assets/locales.json").read_text(encoding="utf-8"))
        locales = manifest["languages"]
        if set(locales) != {"en", "ru"}:
            errors.append("Complete English and Russian locale definitions are required")
        roles = {"bookkeeping_workflow", "month_close", "form_worksheet", "tax_consultation", "overview", "source_map", "service_comparison", "readable_report", "submission_review"}
        for language, locale in locales.items():
            templates = locale["templates"]
            if set(templates) != roles:
                errors.append("Missing or unexpected localized template roles: " + language)
            for name in templates.values():
                target = (SKILL / "assets" / name).resolve()
                if not target.is_relative_to(SKILL / "assets" / language) or not target.is_file():
                    errors.append("Invalid localized template: " + str(name))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append("Invalid locale manifest: " + str(exc))
    for file in checked_files(ROOT):
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
    print("Package structure, EN/RU template coverage, local links and JSON: OK (no network/legal/integration validation)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
