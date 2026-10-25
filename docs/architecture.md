# German Business Kit architecture

[English](architecture.md) · [Русский](architecture.ru.md)

Project version: **0.3.0 preview**. Source review: **2026-10-25**.

## Intended result

An entrepreneur brings a task: open an activity, organize receipts, prepare a month for a Steuerberater, understand a tax question or draft an official form. The skill resumes from private files, collects the few missing facts that affect the result and produces work the user can inspect. Evidence and recorded decisions remain available after the conversation ends.

The supported scope is a natural person operating in Germany: Freiberufler, Einzelunternehmen/Gewerbe and multiple activities of the same person. Corporations, partnerships, payroll, complex international structures and cash-register systems are outside the promised automation scope. The skill can collect facts and prepare a specific specialist handoff for those cases.

## One entry point, shared state

The portable entry point is `de-business-kit`. Its `SKILL.md` routes to task-specific reference modules, loaded as the task requires. The business profile, VAT history, evidence, questions and decisions are shared, which avoids creating conflicting records for separate modes or languages. Independent skills could be extracted later while preserving the common data contract.

| Layer | Responsibility |
|---|---|
| `SKILL.md` | Task routing, language/mode selection, common invariants and result reporting |
| `references/` | Workflows, source maps and rules for the current task |
| `assets/en/`, `assets/ru/` | Equivalent user-facing report templates, indexed by `assets/locales.json` |
| Local Python utilities | Repeatable filesystem operations, preference persistence and deterministic reconciliation |
| Private workspace | Facts, originals, proposals, decisions, source checks and operation evidence |
| Host capabilities | Model, file access, web research, browser tools and task permissions |
| Accounting product / authority | Actual postings, transmissions, receipts and official responses |

The skill cannot create browser tools, API access or permissions. Availability depends on the host and current session. Bundled scripts operate offline; the host's model can still process selected data remotely.

## Languages and modes

The two named working modes are `bookkeeping` and `tax-consultant`; `general` covers startup, organization and routing. Bookkeeping prepares evidence, records, reconciliation and monthly handoff. Tax questions and preparation (`tax-consultant`) produces sourced explanations, comparisons, estimates and proposed decisions. A tax issue encountered during bookkeeping can use the consultation module without abandoning the other work or changing the saved default. See the [mode guide](modes.md) for usage rather than a second implementation of those workflows here.

`00_admin/workspace.json` stores the default `language` and `mode`. The `configure` command persists an explicit preference change with history and an audit event; `status` exposes the current values. An explicit one-task request takes priority in the conversation. A request to translate one report does not replace the saved language or rewrite historical records.

User-facing conversations and Markdown reports support **English and Russian**. Agent instructions, JSON keys, enum values, paths and IDs remain shared in English. Exact German terms and form labels are preserved and explained in the chosen language. A translation is a linked rendering of the same evidence and decision, not new verification. Legacy `de` preferences remain accepted by the CLI, but this release has no complete German template set.

The workspace format remains **schema version 1**. A v0.1 workspace without `mode` is read as `general`; it does not need to be recreated. Changing a language or mode never changes profile facts, `vat_current_regime`, bookkeeping method or authority filings. The same profile and evidence history serve both languages and all modes.

## Evidence and state

`01_profile/business.json` is the canonical profile. Each fact records a value, status, source, recording date and effective date. `unknown`, `declared`, `proposed`, `verified` and `needs_review` have distinct meanings. Verification depends on inspected evidence, not model confidence. Prior values remain in history.

`00_admin/documents.json` links originals, hashes and storage periods to subsequent work. Folder periods organize documents; they do not determine invoice, service, payment or tax dates. Activities have separate IDs, while VAT assessment considers the entrepreneur's whole enterprise. See [§2 UStG](https://www.gesetze-im-internet.de/ustg_1980/__2.html).

Document handling preserves the original, extracts facts, prepares a proposal and records review before any authorized external action. Actual external states must be read back and evidenced. A local file is not a posted entry; a transmission receipt is not substantive acceptance. Consultation reports live in `05_tax/YYYY/consultations/` and link relevant questions, proposals or decisions.

The scripts supply initialization, preference changes, evidenced profile updates, byte-preserving import, original integrity checks and explicit-reference CSV reconciliation. Locks coordinate script writers and individual JSON replacements are atomic. Copies, indexes, snapshots and audit events are separate writes, so the package does not promise a transaction across all files or a tamper-proof archive.

## Data and professional boundaries

Source code, templates and synthetic fixtures are public. Entrepreneur files belong in a separate private directory outside Git repositories. `.gitignore` is only an additional safeguard. Originals remain unchanged; OCR, extracted JSON and translations are derivatives. Review the actual AI product, plan, processing route and necessary terms before using real third-party personal data. Local storage alone does not establish local model processing or GDPR compliance; see [privacy](../skills/de-business-kit/references/privacy.md).

Tax mode explains applicable rules, applies them to stated facts and prepares reviewable conclusions. It does not establish licensed Steuerberater status or professional representation. Publishing self-help software and offering individual services to others are different operating models; a free price or disclaimer does not resolve the latter. See current [StBerG §2](https://www.gesetze-im-internet.de/stberg/__2.html), [§6](https://www.gesetze-im-internet.de/stberg/__6.html) and the [German rules reference](../skills/de-business-kit/references/german-rules.md).

Hashes, history and procedures support record organization; compliance of the complete retention and correction process requires separate assessment. The project does not declare an ordinary folder automatically compliant or automatically unlawful. See the [BMF E-Rechnung FAQ](https://www.bundesfinanzministerium.de/Content/DE/FAQ/e-rechnung.html) and the official GoBD sources in the rules reference.

## Current limits and future work

Version 0.3 adds guided setup, synthetic demo, runtime assessment records, typed profile values and validated register writes while preserving language/mode support. It contains no production bank, Lexware or ELSTER connector, automatic filings, complete personal-tax engine, integrated OCR/XML validator or scheduler. Browser instructions use only capabilities actually available in the host. No end-to-end desktop integration test is implied by local tests.

| Future work | Evidence needed before claiming support |
|---|---|
| Clean Codex / Claude Desktop checks on macOS and Windows | Recorded versions; installation, discovery, resumption and synthetic-document runs |
| Lexware Office read-only adapter | Verified API version, minimum permissions, test environment and reconciled objects |
| Draft writes and assisted forms | Concrete preview, scoped authorization, readback, timeout handling and duplicate prevention |
| Additional accounting products and e-invoice validation | Verified supported formats, actual validators and shared behavioral cases |
| Local plugin distribution | Bundles are built from one canonical skill; actual desktop discovery and account policy remain separate checks |
| Additional jurisdictions or hosted services | Separate requirements, maintenance process and service-model review |

## Maintenance and validation

Record URLs, check dates, applicable periods and supported conclusions for material decisions. Recheck laws for the relevant period, forms before filling them and provider terms before a recommendation or contract. Release sources are starting points rather than permanent authority to apply old rules.

Keep English/Russian template roles and user guides aligned while leaving machine identifiers stable. Distinguish code tests, behavioral skill trials and live integration tests. Reproduce defects with synthetic data and add a check that catches the actual failure. See [validation](validation.md) for the work actually performed.

## Guided setup and validated records

Use the [beginner guide](quickstart.md) and [distribution guide](distribution.md). `start` resumes without changing preferences; `demo` uses a separate synthetic workspace; `doctor` checks local health. Processing assessment is a recorded, scoped review with configuration/evidence hashes, not legal certification. Profile values have field-specific validation. `entry` updates tasks/questions/decisions under the same lock with history, explicit transitions, evidence and an expected prior hash. Legacy malformed records are reported without silent migration. Proposal/operation JSON files remain instruction templates; no external execution engine or provider-state validator is implied.
