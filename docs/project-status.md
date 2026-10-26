# Current project status

[English](project-status.md) | [Русский](project-status.ru.md) | [Documentation](index.md)

Reviewed against the source on **2026-10-26**, version **0.7.0-preview.1**.
This page describes implemented capabilities. Download availability depends on
successful platform gates, publication and verification of the matching assets on
the [version's release page](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.7.0-preview.1).
See [GUI guidance](gui.md) for delivery scope and [validation](validation.md) for
actual runs and their limits. Historical release runs do not establish acceptance
of the new GUI; neither local checks nor hosted CI establish nontechnical-user
usability or a certified accounting process.

The product is a **system of skills for the entrepreneur lifecycle**. The [full correction plan](lifecycle.md) defines structure, coverage, P0–P7 sequencing and acceptance. Guidance already covers formation, forms, questions, services, documents and reporting; daily-work, annual-preparation, change and closure instructions have been added, with real execution subject to separate acceptance. The table below primarily describes technical foundations, not the entire product scope. Self-managed accounting and filing remain important: local cash records with manual ELSTER are one route, and existing software stays authoritative when selected. Consultation and exports are optional.

| Capability | Current implementation | Boundary |
| --- | --- | --- |
| Skill system | Optional router and six directly usable domain skills; shared contract/profile; complete-set installation | Instructions and local packaging do not establish discovery in every host, legal correctness or external execution |
| Intake and continuity | One profile, preserved originals, EN/RU/DE physical folders, start/resume and integrity checks | A folder language is not a tax fact; no silent migration |
| Native Windows | PowerShell 5.1 entry points for install, intake, integrity, real overview and full backup/restore; no Python installation required | Standalone PowerShell retains its narrower operation set; exact runner evidence is in validation. GUI installation and nontechnical-user acceptance remain separate |
| Document desk | Catalog, reviewed proposals, source checks, bank mapping, reconciliation and limited XML inspection in the optional Python engine | No complete OCR, embedded-PDF XML or technical e-invoice validation pipeline |
| Accounting | Validated local cash entries, splits, reversals, period reports and account CSVs for an explicitly selected EÜR workflow | No complete statutory ledger, tax adjustments or bundled tax formulas; native protected writes remain unfinished |
| Filing evidence | Frozen versions, preflight, review/authorization, uncertain attempts, observed receipts and authority responses | Local evidence tracking sends nothing; calculation tools and manual ELSTER require actual user access and observed results |
| Real overview | EN/RU HTML/Markdown/JSON from canonical records, questions, accounting choice, filings and next action | Read-only snapshot; the native view inspects saved evidence but does not run full filing preflight |
| Recovery | Full directory backup with manifest/hashes; verified restore into a new location; shared Python/PowerShell format | No overwrite, automatic repair, encryption, off-site retention or scheduled backup service |
| Real local GUI | EN/RU/DE interface using validated import/review, cash entries/corrections, versioned filing actions, drafts and recovery | Standalone application with bundled runtime; published assets, platform CI and user acceptance must be verified separately. No ELSTER transport |
| Interactive demonstration | Separate English prototype with synthetic records and browser storage | Fictional data only; not the real GUI |
| External sources and reminders | Guidance for host plugins/API/browser/computer access; source maps and sourced dates | No bundled production connectors or automatic reminder scheduler |

Users need neither commands nor JSON editing. The assistant chooses an actually
available route and states the exact blocked operation when the host lacks one.
Node/Playwright and developer Python tests are development requirements, not
onboarding requirements. macOS also does not guarantee Python is installed.

## Next product work

After bundle separation and instruction implementation, the next work is direct-entry P1 and P2–P5 journey acceptance on supported hosts and representative tasks. P6 needs a specific chosen service and verifiable operation; P7 needs separate interface and published-package acceptance. Exact state, dependencies and criteria are in the [plan](lifecycle.md); actual checks are in [validation](validation.md).

## Technical acceptance gates for existing routes

1. Verify the exact version’s native GUI package gates and first-launch acceptance on Windows
   and both Mac architectures; the packaged engine needs no user-installed Python.
   Standalone PowerShell still has its narrower operation set.
2. Check a representative real month and supported form/year through the chosen
   calculation tool and manual ELSTER; preserve real evidence without publishing it.
3. Test the connected GUI first use, error recovery and multi-session workflow
   with nontechnical Windows/macOS users.
4. Add reminders only through a defined, authorized scheduler with verified
   delivery; a saved deadline is not a reminder.

Use [accounting](accounting.md), [the monthly recipe](../skills/de-business-kit/references/monthly-workflow.md),
[Windows](windows.md), [recovery](../skills/de-business-kit/references/recovery.md)
and [capability acceptance criteria](core-capabilities.md) for details.

## Documentation ownership

Code, CLI schemas and tests establish what exists. This page summarizes current
scope; the architecture and ontology explain mechanisms; portable references
guide the installed assistant; user guides explain tasks. Dated research records
source checks, and validation records actual runs. Updating implementation docs
does not renew legal/provider research or prove hosted CI. Maintain these
distinctions when updating the project; see [AGENTS.md](../AGENTS.md) and
[Contributing](../CONTRIBUTING.md).

Releases: canonical versions, reproducible packages and provenance verification are described in [Versions, signatures and release verification](releases.md).
