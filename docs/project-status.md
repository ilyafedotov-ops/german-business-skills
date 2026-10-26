# Current project status and roadmap

[English](project-status.md) · [Русский](project-status.ru.md) · [Technical documentation](index.md)

Reviewed against source on **2026-10-26**. German Business Kit is a seven-skill system for a natural-person entrepreneur in Germany: preparation, formation, everyday work, accounting, reporting, changes and closure. Users can ask a question before creating a workspace or choosing accounting software. Self-managed accounting remains a supported goal; consultation and sharing with an accountant are optional.

## Source and published release

`VERSION` and the published immutable [release](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.9.0-preview.1) are **0.9.0-preview.1**, from `b7f85c0422429f94159a6cc6352f8b83ab4b5d63`. The release covers beginner installation, assisted-service refinements and documentation consolidation. It provides Codex/Claude skill bundles and Windows x64/macOS arm64/macOS x86_64 application archives. See [validation](validation.md) for exact platform, security and downloaded-asset results. Earlier tags/assets are preserved. This repository distributes skills and local applications; it has no hosted production application.

## Implemented scope

| Area | Available now | Boundary |
| --- | --- | --- |
| Skills and lifecycle | Optional router plus six directly usable domain skills; shared profile, EN/RU worksheets and continuation | Guidance/preparation does not establish registration, contract, hire or closure |
| Access and assisted services | Operation-specific discovery of host connector, browser, permitted computer-use or manual routes; authorized draft entry, readback, export checks and user-held final action | Instructions over available host tools; no bundled production connectors. Real ELSTER/Lexware acceptance is open; Lexware uses local examples by user choice |
| Intake and documents | Preserved originals, hashes, catalog, reviewed proposals, bank mapping/reconciliation and bounded standalone UBL Invoice/CreditNote/CII inspection | No complete OCR, embedded-PDF XML or technical e-invoice validation pipeline |
| Accounting | Explicit local/external choice; limited reviewed EÜR cash entries, splits, reversals/corrections, period reports and account CSVs | Existing software stays authoritative when selected. No complete statutory ledger or bundled tax formulas; eligibility is not inferred |
| Filing evidence | Frozen versions, preflight, review/authorization, uncertain attempts, observed receipts and authority responses | Tracks local evidence; calculates no statutory return and sends nothing to ELSTER |
| Continuation and overview | Active tasks across periods, undated work, dependencies and changed evidence; EN/RU HTML/Markdown/JSON | Read-only projection, not approval, task completion or automatic reminder |
| Recovery | Full directory backup, manifest/hash verification and restore into a new destination; shared Python/PowerShell format | No overwrite, encryption, off-site service or scheduled backups |
| Real local GUI | EN/RU/DE interface for validated intake/review, cash records, filing evidence, drafts and recovery; bundled runtime | No automatic AI call or filing transport; ordinary-user desktop acceptance remains open |
| Standalone native Windows | PowerShell 5.1 installation, start/resume, intake, integrity, overview and full recovery without Python installation | Protected journal/filing writers and full filing preflight are not native PowerShell operations; the GUI bundles its separate engine |

Physical folder names support EN/RU/DE; full user manuals and report templates cover EN/RU. German navigation and the short German guide do not imply complete German reporting. Users need neither JSON editing nor development dependencies. Native applications, assistant tools and standalone scripts have different capability sets; see [architecture](architecture.md) and [GUI](gui.md).

## Roadmap

P1–P7 are **partially accepted**, not a completed end-to-end lifecycle. The [original correction plan](history/lifecycle-plan-2026-10-26.md) is historical; this table owns the remaining work.

| Package | Delivered foundation | Remaining acceptance or implementation |
| --- | --- | --- |
| P1 — Welcome and routing | Task-first onboarding, direct domain skills, shared continuation; fresh Codex/Claude trials | Ordinary-user first conversation and continuation across supported hosts; avoid forced setup |
| P2 — Preparation and formation | Launch/classification research, form worksheets and assisted draft workflow | Verify selected authority/form/year, real authentication, field review and separately evidenced registration outcomes |
| P3 — Daily work and questions | Proposals, invoices, letters, correction/partial-payment evidence and saved follow-up | Representative customer journeys in chosen software, actual document issue/delivery/payment evidence; complete download retrieval in the tested browser route |
| P4 — Accounting and reporting | Limited local cash journal, external-system route, monthly/annual preparation and filing evidence | Representative complete period through selected calculation/form tools and manual ELSTER; criteria below |
| P5 — Change, hire, pause and close | Before/after plans, dependencies, first-hire preparation and history/access retention | Real selected service/authority outcomes; payroll and legal filings require their own supported tools |
| P6 — Service access | Needs-led comparison, supplied-export inspection and capability/setup discovery | Real operation-scoped access/readback in selected products; account/edition permissions and source coverage. Lexware stays local until the user changes that choice |
| P7 — Delivery and usability | Illustrated installation, complete-bundle packaging, local GUI and verified preview release | Nontechnical Windows/macOS first launch, install/update/continuation and error-recovery trials; other host routes; real installation screenshots/video after those journeys are observed |

Automatic reminders require a defined authorized scheduler and verified delivery; no such service exists. Additional connectors, statutory ledger features and e-invoice validation should be selected for a concrete journey, not required for every user. Do not replace the chosen accounting system just to complete the roadmap.

## Accounting acceptance

The first developed monthly route is **explicitly chosen local cash records plus manual ELSTER**, not a default for everyone. Follow the [monthly](../skills/de-business-kit/references/monthly-workflow.md) and [annual](../skills/de-business-kit/references/annual-workflow.md) workflows. Full backup/restore and the real overview are implemented; they do not establish complete statutory accounting.

| Area | Evidence still needed before an end-to-end claim |
| --- | --- |
| Documents and ledger | Complete source/account/period coverage; reviewed treatment, assets/noncash adjustments, closing rules and verified reports in the authoritative system; format/host and technical e-invoice validation where applicable |
| Tax estimates and returns | Applicable official rules and form/year support; evidenced inputs and actual selected official/provider tool output; reconcile differences. No package tax formulas, rate tables or invented amounts |
| Submission | Supported official route/access; user-controlled authentication; exact payload preview and matching authorization; technical validation, duplicate prevention, timeout/retry investigation, actual receipt and correction workflow. A new adapter needs a supported official test environment and independent credential/authorization review |
| Authority follow-up | Observed response linked to the exact filing version; separately sourced deadline checks and objections/corrections. A transmission receipt is not substantive acceptance |

The evidence chain remains **source → proposal → review → actual accounting entry → return draft → submission authorization → observed submission → authority response**. A verified manual step can complete part of a supported assistance journey; it is not evidence of automated integration. See [validation](validation.md) for what has actually been tested.
