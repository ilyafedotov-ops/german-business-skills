# Current project status

[English](project-status.md) | [Русский](project-status.ru.md) | [Documentation](index.md)

Reviewed against the local source on **2026-10-26**, version **0.5.0-preview**.
This page describes implemented capabilities, not a published release, successful
host installation or a certified accounting process. Exact runs and their limits
are recorded in [validation](validation.md); older entries there are historical.

The primary workflow is **self-managed accounting and tax reporting**. The first
end-to-end route under development is the **local cash journal plus manual
ELSTER**. This does not preselect local accounting for every user: existing
accounting software remains authoritative when chosen. Consultation and sharing
an archive are optional.

| Capability | Current implementation | Boundary |
| --- | --- | --- |
| Intake and continuity | One profile, preserved originals, EN/RU/DE physical folders, start/resume and integrity checks | A folder language is not a tax fact; no silent migration |
| Native Windows | PowerShell 5.1 entry points for install, intake, integrity, real overview and full backup/restore; no Python installation required | Latest local acceptance uses Linux PowerShell 7.5; Windows 5.1 CI is a separate gate |
| Document desk | Catalog, reviewed proposals, source checks, bank mapping, reconciliation and limited XML inspection in the optional Python engine | No complete OCR, embedded-PDF XML or technical e-invoice validation pipeline |
| Accounting | Validated local cash entries, splits, reversals, period reports and account CSVs for an explicitly selected EÜR workflow | No complete statutory ledger, tax adjustments or bundled tax formulas; native protected writes remain unfinished |
| Filing evidence | Frozen versions, preflight, review/authorization, uncertain attempts, observed receipts and authority responses | Local evidence tracking sends nothing; calculation tools and manual ELSTER require actual user access and observed results |
| Real overview | EN/RU HTML/Markdown/JSON from canonical records, questions, accounting choice, filings and next action | Read-only snapshot; the native view inspects saved evidence but does not run full filing preflight |
| Recovery | Full directory backup with manifest/hashes; verified restore into a new location; shared Python/PowerShell format | No overwrite, automatic repair, encryption, off-site retention or scheduled backup service |
| Interactive GUI | Five-screen English prototype with synthetic records and browser storage | Not connected to real workspace mutations; distinct from the real generated overview |
| External sources and reminders | Guidance for host plugins/API/browser/computer access; source maps and sourced dates | No bundled production connectors or automatic reminder scheduler |

Users need neither commands nor JSON editing. The assistant chooses an actually
available route and states the exact blocked operation when the host lacks one.
Node/Playwright and developer Python tests are development requirements, not
onboarding requirements. macOS also does not guarantee Python is installed.

## Next acceptance gates

1. Complete and test protected accounting/filing writes for Windows without a
   user-installed Python runtime.
2. Check a representative real month and supported form/year through the chosen
   calculation tool and manual ELSTER; preserve real evidence without publishing it.
3. Connect controlled GUI actions to validated writers, then test first use and
   recovery with nontechnical Windows/macOS users.
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
