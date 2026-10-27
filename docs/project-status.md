# Current project status and roadmap

[English](project-status.md) · [Русский](project-status.ru.md) · [Technical documentation](index.md)

Reviewed against source on **2026-10-26**. German Business Kit is a seven-skill system for a natural-person entrepreneur in Germany: preparation, formation, everyday work, accounting, reporting, changes and closure. Users can ask a question before creating a workspace or choosing accounting software. Self-managed accounting remains a supported goal; consultation and sharing with an accountant are optional.

All seven skills now share a [cost check before setup](../skills/de-business-kit/references/assisted-services.md#check-costs-before-setup):
verify current-plan entitlement, explain added costs/unknowns before paid setup,
and preserve no-upgrade decisions while continuing available work. This is a
portable instruction safeguard, not a billing-enforcement mechanism.

All seven also require a [screenshot privacy check](../skills/de-business-kit/references/privacy.md#check-screenshots-before-sharing)
before sharing, including owner chat: minimized text by default, a separately
redacted and verified image when needed, and private preservation of necessary
original evidence. This is an instruction safeguard, not an automatic redactor.

## Primary user journey

Use Claude Desktop/Cowork or Codex as the interface, and one private business
folder for records, confirmed facts, open questions and continuation. The separate
GUI is an optional adapter for existing local operations; it is not a prerequisite
for onboarding, daily work or self-managed reporting. Keep its existing safeguards;
prioritize observed assistant journeys before adding GUI scope. The README starts with an assistant-led installation request and offers lifecycle, document, integration and edge-case examples. Requested usage help provides relevant copyable prompts; installation and connection success still require actual observation.

All seven skills share task-specific prerequisite checks, targeted follow-ups,
reuse of relevant saved facts and explicit persistence through existing writers.
Tax/accounting instructions now allow bounded calculations from inspected
applicable rules, executable arithmetic and separately evidenced checks. These
are instruction-level capabilities over available host tools, not a bundled
complete tax engine, guaranteed independent reviewer or new filing approval gate.
See [source-led calculations](../skills/de-business-kit/references/tax-estimates.md)
and [validation](validation.md) for actual trials and remaining limits.

Local implementation on **2026-10-27** adds primary-source recovery and a
[saved income-tax prepayment request workflow](../skills/de-business-kit/references/tax-consultant.md#prepare-or-revise-an-income-tax-prepayment-request)
to the product skills. It prepares a German recipient draft, separate EN/RU
review, calculation evidence and a continuation point; corrected forecasts retain
earlier versions. This is host-executed preparation, with no new tax engine,
protected writer or ELSTER transport. Receipt-to-period preparation now also has
an explicit saved workflow, separating payment/profit and VAT timing while keeping
unknown treatment open. Filing continuation uses the existing writers with added
preparation-source dependency freezing and freshness/readiness checks. These
changes preserve the chosen accounting system and filing history. Further FAQ
expansion is not the current priority; actual acceptance is in validation.

Customer payment continuation now preserves invoice-stated prepaid and rounding
amounts in UBL/CII inspection and draft proposals. The operations skill saves
separate recipient replies and private comparisons, distinguishing already included
receipts from later payments and retaining revised versions. This adds no invoice
issuance, settlement engine, payment allocation or technical e-invoice validation.

Local EU goods guidance now includes [checks before ordering and after a VAT invoice arrives](../skills/de-business-kit/references/international.md#before-ordering-goods-from-another-eu-country),
including Kleinunternehmer ID-use consequences, conditional supplier correction
and the distinction between foreign VAT and German acquisition/destination VAT.
Operations, accounting and tax skills share this source. It adds no tax engine,
election, refund or filing operation; [validation](validation.md) records live acceptance.

The optional Python invoicing workflow now records reviewed drafts, issue/correction
attempts, actual issued artifacts, dispatch and receipt evidence through protected
writers. It supports historical issued/sent documents, linked corrections, explicit
failure/retry and all-period continuation. The opt-in Lexware Office adapter now
creates a provider draft, preserves its ID and reads it back; final artifact
downloads check provider version stability. It binds browser finalization/sending
to that same object and protected attempt. No API finalization/send endpoint is
invented; those actions require the actual authorized host/browser/manual route.
One authorized live browser journey now covers zero-value draft creation/readback,
same-object finalization, PDF inspection, sending and recipient acknowledgement.
The sent-history PDF matched the reviewed file byte-for-byte. This used an existing
business company, not an isolated sandbox. A separate current-plan browser test
also verified saving/reopening a zero-value draft, correcting its introduction and retaining its UUID, number, VAT setting
and total while leaving it unissued/unsent. Live API adapter acceptance, nonzero
invoices, provider-linked/nonzero corrections, native-only and GUI invoicing controls remain open.
The current-plan browser route also exported a draft PDF using the explicit
**Als Entwurf drucken** option and verified the same object remained a draft.
The default **Fertigstellen + drucken** must not be used for draft-only export.
A separate manual zero-value correction draft now has live save/reopen, persisted
text-edit, preview and draft-PDF checks. Its original reference is textual; local
linkage does not establish provider linkage. With explicit authorization, the same
correction was finalized, independently read back as **offen**, and its final PDF
verified; it remains unsent. The original stayed sent and not cancelled. Nonzero
credit/refund, provider-linked correction and cancellation acceptance remain open.

**Lexware browser integration: E2E validated and accepted by the user on
2026-10-27**, on the existing Office L tariff with zero-value test documents.
Accepted scope: draft creation/readback, finalization, final PDF retrieval, sending
and acknowledged email/PDF receipt; draft correction/export; manual correction
finalization and final PDF retrieval with the correction deliberately unsent.
This accepts the browser route; the API adapter and nonzero/provider-linked
correction, refund and cancellation journeys remain outside this acceptance.

Local customer-payment reconciliation now saves a protected, readable EN/RU comparison of an issued invoice with explicitly identified bank receipts. It excludes already-included prepayments, handles partial receipts/refunds across periods, preserves frozen sources and checks report freshness against invoice/correction history. Uncertain coverage, currency or correction effects leave the comparison unresolved. It performs no provider allocation, paid-status update or collection action; live nonzero settlement acceptance remains open.

Customer payment follow-up now produces a DE/EN/RU recipient query and separate EN/RU private review from the saved comparison. Positive, current and unblocked comparisons support a factual difference query; unresolved comparisons support amount-free clarification. Protected freshness/integrity checks bind each draft to its evidence. No automated sending, legal reminder/default claim, fee or provider mutation is implemented.

## Source and published release

`VERSION` and the verified immutable [release](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.11.0-preview.1) are **0.11.0-preview.1**, from `9e2bc4c2dfd19ecac88b5433d40adbdb403d8547`. Published on **2026-10-27**, this release adds protected invoice issue/correction/delivery workflows, the accepted Lexware browser route, local receipt reconciliation and customer follow-up drafts, receipt-bound filing preparation, and cost/privacy safeguards. All eight downloaded assets passed checksum, release-attestation and exact-source provenance checks before the marketplace pin was advanced. It provides Codex/Claude skill bundles and Windows x64/macOS arm64/macOS x86_64 application archives. See [validation](validation.md) for results and remaining limits. Earlier tags/assets are preserved. This repository distributes skills and local applications; it has no hosted production application.

## Implemented scope

| Area | Available now | Boundary |
| --- | --- | --- |
| Skills and lifecycle | Optional router plus six directly usable domain skills; shared profile, EN/RU worksheets and continuation | Guidance/preparation does not establish registration, contract, hire or closure |
| Access and assisted services | Host connector/browser/manual discovery; bounded opt-in Lexware draft/readback API and exact-object browser handoff; authorized draft entry and export checks | Lexware Office L browser integration E2E validated and user-accepted (2026-10-27), within the scope above; API adapter remains synthetic-only. Nonzero invoices/corrections and ELSTER acceptance remain open |
| Intake and documents | Preserved originals, hashes, catalog, reviewed proposals, bank mapping/reconciliation and bounded standalone UBL Invoice/CreditNote/CII inspection | No complete OCR, embedded-PDF XML or technical e-invoice validation pipeline |
| Accounting | Explicit local/external choice; limited reviewed EÜR cash entries, splits, line VAT as stated with links to approved proposals, reversals/corrections, period reports and account CSVs | Existing software stays authoritative when selected. No complete statutory ledger or bundled tax formulas; stated-VAT sums are not a Voranmeldung; eligibility is not inferred |
| Filing evidence | Frozen versions, preflight, review/authorization, uncertain attempts, observed receipts and authority responses | Tracks local evidence; calculates no statutory return and sends nothing to ELSTER |
| Continuation and overview | Active tasks across periods, undated work, dependencies and changed evidence; EN/RU HTML/Markdown/JSON | Read-only projection, not approval, task completion or automatic reminder |
| Recovery | Full directory backup, manifest/hash verification and restore into a new destination; shared Python/PowerShell format | No overwrite, encryption, off-site service or scheduled backups |
| Real local GUI | EN/RU/DE interface for validated intake/review, cash records, filing evidence, drafts and recovery; bundled runtime | No automatic AI call or filing transport; ordinary-user desktop acceptance remains open |
| Standalone native Windows | PowerShell 5.1 installation, start/resume, intake, integrity, overview and full recovery without Python installation | Protected journal/filing writers and full filing preflight are not native PowerShell operations; the GUI bundles its separate engine |

Physical folder names support EN/RU/DE; full user manuals and report templates cover EN/RU. German navigation and the short German guide do not imply complete German reporting. Users need neither JSON editing nor development dependencies. Native applications, assistant tools and standalone scripts have different capability sets; see [architecture](architecture.md) and [GUI](gui.md).

The published source also projects invoice payment allocations across periods, exposes discrepancies in the GUI/report and checks settlement-basis freshness before filing actions. Native PowerShell supports lock diagnosis/recovery, including exact raw evidence. An opt-in [evaluation runner](../evals/README.md) executes selected fresh-session cases on supported POSIX developer hosts; it does not certify behavior from a passing utility test. The repository root is a Claude plugin [marketplace](distribution.md#github-marketplace-for-claude) that installs the verified preview pinned by tag and commit; the README and installation guides lead with that three-step Cowork route. A Cowork desktop installation has not been observed. Desktop signing and provider journeys outside the accepted Lexware browser scope remain open.

## Roadmap

P1–P7 are **partially accepted**, not a completed end-to-end lifecycle. This table owns the remaining work.

| Package | Delivered foundation | Remaining acceptance or implementation |
| --- | --- | --- |
| P1 — Welcome and routing | Task-first onboarding, direct domain skills, shared continuation; fresh Codex/Claude trials | Ordinary-user first conversation and continuation across supported hosts; avoid forced setup |
| P2 — Preparation and formation | Launch/classification research, form worksheets and assisted draft workflow | Verify selected authority/form/year, real authentication, field review and separately evidenced registration outcomes |
| P3 — Daily work and questions | Proposals, invoices, letters, saved receipt comparisons, correction/partial-payment evidence and follow-up | Lexware browser issue/delivery/download accepted above; next: live customer-payment allocation/readback and representative nonzero/correction journeys |
| P4 — Accounting and reporting | Limited local cash journal, external-system route, monthly/annual preparation and filing evidence | Representative complete period through selected calculation/form tools and manual ELSTER; criteria below |
| P5 — Change, hire, pause and close | Before/after plans, dependencies, first-hire preparation and history/access retention | Real selected service/authority outcomes; payroll and legal filings require their own supported tools |
| P6 — Service access | Needs-led comparison, supplied-export inspection and capability/setup discovery | Real operation-scoped access/readback in selected products; account/edition permissions and source coverage. Lexware Office L browser E2E is user-accepted within the scope above; broader operations and live API acceptance remain open |
| P7 — Delivery and usability | Illustrated installation, complete-bundle packaging, local GUI and verified preview release | Nontechnical Windows/macOS first launch, install/update/continuation and error-recovery trials, starting with Cowork and Codex skill invocation, useful result and same-folder continuation; ambiguous requests, saved-fact reuse and calculation checks; other host routes; real installation screenshots/video after those journeys are observed |

The [FAQ evaluation map](../evals/faq-coverage.json), reviewed on **2026-10-27**,
links 60 external question numbers to task owners and existing cases. At baseline
`085489d`, central-concern coverage is 2 covered, 29 partial, 24 missing dedicated
cases and 5 complete outcomes outside current scope. Twenty-nine new synthetic cases
and nine changed-fact follow-ups are defined; [validation](validation.md) owns their
observed results. This does not expand legal, insurance or residence capabilities.
The separate opt-in [research runner](../tools/run_research_evals.py) now captures
visible arithmetic and source metadata, freezes complete review criteria and binds
independent assessments to exact artifacts. Its thirty-two-case/forty-three-session selection
has fake-host regression coverage; live outcomes are recorded in validation.
The second batch covers family cover, pension contribution options, parental and
child benefits, work permission and startup support, with dated official sources.
The third batch adds small-invoice boundaries, ordinary invoice fields and the
2026 e-invoice transition, home-working expense arithmetic and quarterly VAT
deadlines with an extension correction. The fourth batch adds GWG/computer
asset treatment, mixed phone/car costs and ordinary EU consultancy with a consumer
correction. The fifth batch covers US business/consumer advice, French property
services and automated digital sales crossing the EU threshold, with a consumer
location correction. The sixth batch covers no-sales VAT returns, annual loss/return
duties and income-tax prepayment adjustment, with a private-expense correction.
Those six FAQ batches left the original ten-case runner and product skills unchanged. Remaining FAQ
priorities include record retention, business banking, contracts and other
country/service variants; other expense and asset variants remain
bounded gaps rather than inferred support.
These bounded cases do not cover all benefit variants, residence titles or individual
insurer/authority decisions. Specialized entity/residence outcomes remain preparation and
routing tasks. Acceptance requires criterion-level source/action evidence and
retests of demonstrated failures, not agreement with a secondary FAQ answer.

Automatic reminders require a defined authorized scheduler and verified delivery; no such service exists. Additional connectors, statutory ledger features and e-invoice validation should be selected for a concrete journey, not required for every user. Do not replace the chosen accounting system just to complete the roadmap.

## Accounting acceptance

The first developed monthly route is **explicitly chosen local cash records plus manual ELSTER**, not a default for everyone. Follow the [monthly](../skills/de-business-kit/references/monthly-workflow.md) and [annual](../skills/de-business-kit/references/annual-workflow.md) workflows. Full backup/restore and the real overview are implemented; they do not establish complete statutory accounting.

| Area | Evidence still needed before an end-to-end claim |
| --- | --- |
| Documents and ledger | Complete source/account/period coverage; reviewed treatment, assets/noncash adjustments, closing rules and verified reports in the authoritative system; format/host and technical e-invoice validation where applicable |
| Tax estimates and returns | Applicable official rules and form/year support; evidenced inputs and actual selected official/provider tool output; reconcile differences. Bounded case calculations need applicable sourced methods, sufficient inputs, executed output and independent check evidence; no reusable package tax constants or invented amounts |
| Submission | Supported official route/access; user-controlled authentication; exact payload preview and matching authorization; technical validation, duplicate prevention, timeout/retry investigation, actual receipt and correction workflow. A new adapter needs a supported official test environment and independent credential/authorization review |
| Authority follow-up | Observed response linked to the exact filing version; separately sourced deadline checks and objections/corrections. A transmission receipt is not substantive acceptance |

The evidence chain remains **source → proposal → review → actual accounting entry → return draft → submission authorization → observed submission → authority response**. A verified manual step can complete part of a supported assistance journey; it is not evidence of automated integration. See [validation](validation.md) for what has actually been tested.
