# Changelog

[English](CHANGELOG.md) | [Русский](CHANGELOG.ru.md)

Versions follow Semantic Versioning. All releases below are previews, not a
certification of accounting correctness or desktop compatibility. Historical
milestones are first published on 2026-10-26; their original commits are retained.

## 0.13.0-preview.1

- **Welcome wizard after installation.** A new user who has just installed the kit, or asks to start, gets a guided welcome in the chat itself (Claude Code, the Claude app or Codex): a read-only setup check, then one short step at a time for language, situation, business folder, data handling and a first task, ending with a summary and a saved task for anything unfinished. Steps use the app's multiple-choice questions where available and numbered options otherwise.
- **Setup check.** `workspace.py setup-check` and the native `windows.ps1 -Action setup-check` report the kit version, missing skills, a second installed copy, the helper runtime and whether the chosen folder is missing, empty, an existing or unsupported workspace or a folder of files, and whether it is private, synced or writable, with one next action. Both write nothing. The installed skill now knows its version (`assets/version.json`, kept equal to `VERSION` by the release check).
- The install request now ends by starting the welcome, and the first message after installing is the welcome request in English, Russian and German. Helper commands get a plain description that apps show when they ask for approval.

## 0.12.0-preview.1

- **New private-workspace folder structure** (breaking for workspaces from earlier previews, which this version refuses without changing them; create a new workspace and import the originals again). One structure in English, Russian or German, created the same way by Python, native Windows, the GUI and the demo:
  - five visible areas, a root overview page (`OVERVIEW.html` / `ОБЗОР.html` / `ÜBERSICHT.html`) refreshed by both overview engines, and internal records in `.business-kit`;
  - the inbox holds only the user's files: assistant inputs and folder previews use an internal work folder, the workspace inbox can be previewed, and a file imported from it moves to `Imported/<YYYY-MM>` without overwriting;
  - originals get a running number per storage year and a readable, Windows-safe name such as `2026-00007_invoice.pdf`, while the index keeps the SHA-256 and original name;
  - copies of issued invoices are kept in `02 Documents/<year>/<month>/Outgoing invoices`, and new bank and correspondence files under storage-year folders;
  - the accounting register is internal, and setup writes a procedure documentation (Verfahrensdokumentation) draft with retention periods (§147 AO, §14b UStG; checked 2026-11-21) for the user to complete;
  - start guides and the user guides explain every folder. The earlier layouts, the `--layout`/`-Layout` options and hash-named originals were removed. See the [dated folder-structure review](docs/research/workspace-layout-review-2026-11-21.md).
- Records accept only the current formats: a workspace marker without saved language and mode, a cash entry without `schema_version` 2 and line VAT status, or a bundle without its skill catalog is refused instead of being read with defaults. The `vat_not_recorded` report issue and the installer's single-skill fallback were removed; malformed records are still reported without being rewritten.
- Onboarding fixes from live new-user trials on 2026-11-21 (six fresh Claude Code sessions with the built plugin):
  - the helper programs `desk.py`, `workflows.py`, `payments.py` and `recovery.py` now also start under isolated Python (`python3 -I`), which assistant hosts can use for user files;
  - the records app lists files waiting in the inbox and imports selected ones in place, so each moves to `Imported` as with an assistant import; long result paths now wrap on narrow screens;
  - the synthetic demo also runs in German and keeps its bank and records files in storage-year folders;
  - instructions name the validated helpers for resuming (`start`, `verify`, `entry --id`), tasks, questions, profile facts and the runtime review instead of internal JSON files, ask assistants to run helpers as single plain commands and to mention the app's approval prompt first, and the install guides explain that prompt;
  - the start guide's inbox request now asks the assistant to wait for the user's choice; assistants choose the storage month before an import, leave a review task afterwards and remove temporary inputs whose content is saved.
- The quick start now leads with one request to the assistant in Claude Code, the Claude app or Codex. The request asks for the published release instead of a copy of the repository's current files, checks all seven skills and ends by starting a fresh session. The Claude app marketplace steps, the Claude Code commands (now in their own section) and the Codex ZIP route follow as manual installs.
- A writer waiting for the workspace lock no longer fails on Windows when another writer is still deleting the lock it just released; a lasting permission error is still reported as such after the wait.
- Add an offline EN/RU/DE guided setup page (`installer/`) for beginners: assistant choice with plan requirements, official sign-up and per-system download links, the existing Claude marketplace and Codex project-skill routes with copyable text, and four fictional first-task demos. It never downloads or runs installers and never collects credentials; provider links and plans were checked on 2026-11-20. It is not yet published at a web address or as a release asset.
- Add a "Data & risks" step to the guided setup page: what AI can get wrong, where file content goes, GDPR basics in plain words, the AI-literacy duty for staff, the provider's own training setting as a checklist, and a six-card "would you share this?" practice check. Provider privacy facts were checked on 2026-11-20. Also add a progress count and bar, checklist tick counts, an enlargeable marketplace screenshot and a compact phone layout.
- Make the guided setup page's kit-installation step start with one copyable request to Claude or Codex, the same one the README recommends; the Claude marketplace and Codex ZIP routes move into a collapsed "install manually" section.
- Shorten the guided setup page for beginners: each step shows a few short instructions with details under "More…", nothing needs ticking, the training setting moves to the app step, and the finish page offers one fictional first task with more examples on demand. The data step now reads like a licence agreement that must be answered with “I have read and understand” before the kit step; the share check becomes an optional self-test. Only paid plans are recommended (Claude Pro or ChatGPT Plus or higher), and phones are told that setup runs on a computer.
- Replace the guided setup page's translator demos with a freelance programmer, add a first step for an Instagram/YouTube content creator, offer both on the finish page, and add "What it looks like…" screenshots of the real Claude and Codex apps (EN/RU/DE, fictional examples, 2026-11-21).
- Match the current Claude app, where Chat and Cowork share one view: the setup page and install guides now say to start a new task and switch to Cowork only in older versions, and to open **Plugins** in the sidebar (**Customize → Plugins** in some versions). The install and user guides and the README use the freelance programmer example instead of the translator.

## 0.11.0-preview.1

- Add protected invoice issue/correction/delivery records, immutable evidence and exact-attempt continuation; keep provider actions, dispatch and recipient receipt distinct.
- Add an opt-in Lexware Office draft/readback API adapter with explicit cost/access checks, durable creation intent, no automatic retry after uncertain outcomes, and same-object browser finalization/sending handoff. The Office L browser route is user-accepted E2E for zero-value test documents; live API and broader nonzero acceptance remain open.
- Add saved invoice-to-receipt comparisons with prepayment exclusion, partial payments/refunds, correction/currency/coverage blockers and freshness checks. Prepare DE/EN/RU customer payment queries with separate EN/RU private reviews; no automated sending or provider payment allocation.
- Bind filing continuation to receipt-preparation source evidence and preserve revised preparation versions. Add source-led income-tax prepayment request, EU goods purchasing and customer payment workflows; these do not introduce statutory calculation or ELSTER transport.
- Preserve invoice-stated prepaid and rounding amounts in bounded UBL/CII inspection; distinguish document totals from current settlement.
- Add shared cost checks before paid setup and screenshot privacy checks before sharing. Preserve no-upgrade decisions and keep real account evidence outside public artifacts.
- Add source-grounded research/evaluation tooling and EN/RU guidance. Release/platform acceptance requires the exact tag checks and verified assets.
- Fix nested correction-family preflight: uncertain original delivery, competing corrections and corrupt ancestor evidence block new attempts while preserving outcome recording for attempts already begun.

No automatic private-workspace migration, complete statutory ledger, desktop signing or live ELSTER transmission is added. The API adapter requires existing supported access; browser operation does not require a tariff upgrade.

## 0.10.0-preview.1

- Make the assistant and private business folder the primary route; add skill invocation, installation prompts, lifecycle examples and EN/RU visual guides. The GUI remains optional.
- Apply shared prerequisites, reusable confirmed context, current primary-source research and separate arithmetic checks across workflows; document AI/provider processing, capable-model selection and task-specific browser/computer guidance.
- Remove the documentation history archive; keep current status and validation summaries, with earlier work retained in Git.

- Make the repository a Claude plugin marketplace: `.claude-plugin/marketplace.json` installs the published release pinned by tag and commit, so Cowork, chat and Claude Code users add `ilyafedotov-ops/german-business-skills` under **Customize → Plugins** in three steps. Rewrite the EN/RU README and installation guide around that route, keep Codex as a condensed project-skill route, redraw the setup diagrams and add a release step for moving the pin.
- Add recorded invoice payment allocation across periods, readable EN/RU balances and EN/RU/DE GUI details; preserve partial/overpayments, refunds and corrections, flag unresolved currencies/directions, and invalidate filing source reports when the allocation basis changes.
- Add native lock diagnosis/recovery and shared writer metadata; preserve exact raw lock bytes in Python and PowerShell audit history. Package the shared native helper explicitly.
- Reuse filing preflight within each locked GUI snapshot and add a synthetic snapshot profiler. New workspace language defaults to English; explicit and saved preferences remain unchanged.
- Add an opt-in POSIX Codex evaluation runner for ten synthetic fresh-session cases, independent state/action checks and separate rubric review. This is developer tooling, not an end-user requirement or automatic legal/quality certification.

- **Breaking for cash-entry input:** new local cash entries use `schema_version` 2. Every line records VAT as stated on its evidence (`stated`, `none_stated` or `unresolved`) and can link the current approved proposal it settles. The writer checks that net plus VAT equals the line amount, refuses unapproved, replaced or different-activity proposals and fingerprints each link. Entries without line VAT can no longer be posted; start from `accounting-template --kind entry`.
- Period reports (schema 2) group stated VAT by currency, movement kind and rate, report `vat_unresolved` and `vat_not_recorded`, and add a VAT section to the EN/RU Markdown. Reports and filing preflight stop when a linked proposal changes. The GUI entry form adds VAT fields and an approved-invoice picker in EN/RU/DE.
- Writers wait up to five seconds for a cooperating writer instead of failing at once. Locks record process, computer and time; `doctor` classifies a remaining lock as active, stale or unverifiable, and the new `workspace.py unlock` and GUI lock check remove only a lock whose writer has ended (or an unverifiable one after explicit confirmation), preserving it in history and the audit log. Native `windows.ps1` locks also record the computer.
- Linked-folder refusals now name the linked path component and its real location, in Python and native PowerShell. On macOS and Linux, atomic and exclusive writes also sync their folder so a crash cannot lose a completed rename.

The accounting register stays schema 1; existing entries remain readable, reportable and reversible without migration. Stated-VAT sums are evidence for a calculation tool, not a VAT return.

## 0.9.0-preview.1

- Add operation-specific connector/browser/desktop discovery and assisted draft/export workflows, with user-controlled login and final confirmation, EN/RU guides and synthetic browser trials.
- Add EN/RU desktop-first installation guides from choosing an AI app through seven-skill discovery and a first task; simplify README and quick starts.
- Package an original illustration and editable EN/RU setup diagrams through an exact-path allowlist, with detached-resource and rejection tests.
- Keep explicit one-small-step requests focused before full registration planning; add bilingual scenarios and record fresh Codex/Claude trials and remaining acceptance gaps.

- Consolidate user help into installation, one task manual and assisted-service guidance; separate technical documentation and the current P1–P7 roadmap from dated history. Remove 29 duplicate Markdown files while retaining original evidence.
- Preserve uncertainty after export-generation/download failures and manual submission without a receipt; avoid invented required fields or formulas in assisted form preparation.

All seven skills remain one bundle. Workspace schemas and runtime accounting behavior are unchanged. This preview has no live ELSTER transport, complete statutory tax calculator or production service connectors; Lexware remains on local examples. Browser artifact retrieval and ordinary-user desktop acceptance remain open. Publication and platform acceptance require the exact tag's checks and verified assets.

- Improve GUI browser-test startup diagnostics and wait for snapshot completion before checking refreshed tasks; preserve application behavior and existing assertion deadlines.

## 0.8.0-preview.1

Lifecycle skill bundle preview. Publication requires the matching tag checks and verified assets; previously published versions remain unchanged.

- Preserve explicitly selected legacy installation sources even when the source folder has a different name or an unrelated sibling exists.
- Deliver the router and six domain skills as one portable bundle with shared profile/evidence, complete-set installation and detached resource checks.
- Add EN/RU preparation and continuation across launch, customer work, correspondence, annual readiness, services, first hire, changes and closure.
- Show active lifecycle tasks, including undated/cross-month tasks, dependencies and evidence health, in the real overview and GUI home. GUI continuation prepares a request for the assistant without executing it.
- Inspect bounded standalone invoice/CreditNote XML references and retain correction evidence. Inspect supplied service exports with explicit route/date-basis and coverage limits; Lexware remains on local examples.
- Clarify source-led tax consultations, required date/accounting facts, and task-first user guidance without adding tax formulas.
- Record fresh synthetic trials, Codex CLI and explicit Claude Code discovery, and local runtime/package checks. Exact-ref Windows 5.1/other platform, ordinary-user and real-service acceptance remain open; see [validation](docs/validation.md).

## 0.7.0-preview.1

Version [0.7.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.7.0-preview.1). Download availability requires successful platform gates, publication and verification of the matching assets.

- Add a real local workspace GUI with English/Russian/German navigation, document
  import/review, private saved drafts and contextual assistant requests.
- Expose existing validated accounting configuration, cash entries, reversals,
  linked corrections, period reports and versioned filing/evidence actions.
  No tax calculation engine or ELSTER transmission is added.
- Add full backup/verification/restore controls and explicit recovery states.
- Protect local sessions with random credentials, same-origin/host checks,
  workspace selection identities and optimistic concurrency for saved drafts.
- Build separate Windows/macOS applications with an embedded runtime; end users
  do not install Python. Native builds and packaged smoke tests become CI gates.
  Native OS code signing/notarization and participant usability acceptance remain open.
- Refresh bilingual quick starts, diagrams, folder examples and project descriptions.

## 0.6.0-preview.4

- Retry cryptographic verification a bounded number of times when GitHub's newly
  created attestation is not yet readable. Verification never becomes optional;
  persistent failures still stop the job. Tests cover delayed success and failure.
- Preview.3 passed all test/security/build gates and published an immutable release,
  but its immediate final verification raced attestation availability. Subsequent
  release verification succeeded. No existing files or tags were replaced.
- Retain the explicit static prototype dispatch and complete CodeQL severity gate.

## 0.6.0-preview.3

- Use explicit static screen dispatch, removing indirect renderer lookup entirely.
- Retain preview.2's SARIF metadata fix and browser regressions. Its gate correctly
  blocked the remaining indirect-call alert before publication; preview.2 is an
  unpublished candidate tag, not a downloadable release. No tags are moved.
- This is the replacement for preview.1, including the complete verified-release
  and self-managed accounting workflows described below.

## 0.6.0-preview.2

- Fix the release security gate to read CodeQL rule severity from SARIF extension
  metadata and reject unresolved rules. The saved report from preview.1 now fails
  correctly at severity 7.5; the earlier gate's success was not a clean scan.
- Fix synthetic prototype routing so URL fragments cannot invoke inherited object
  methods. Add browser regressions for malicious and unknown fragments.
- Run branch-push CI on main and PR CI on feature changes, avoiding duplicate
  branch/PR runs. Tagged releases still run the full independent gates.
- Supersedes preview.1. Its downloaded skill ZIPs exclude the affected prototype,
  but its source and security-gate implementation should not be used as the current
  baseline. Existing immutable tags and assets remain unchanged.

## 0.6.0-preview.1

- Fix Windows import rollback by capturing final timestamps after the write handle closes, while preserving modified/replaced files.

- Add one checked version contract, versioned release archives, per-file manifests
  and exact source-commit metadata. Existing workspace records are not migrated.
- Gate release publishing on Windows/macOS utility, native PowerShell 5.1 and
  browser checks; pin external actions and add dependency/security scanning.
- Generate GitHub build attestations and use immutable releases. Signatures prove
  origin and unchanged bytes, not absence of bugs or legal/tax correctness.
- Carry forward the complete self-managed accounting workflow in 0.5.0-preview.

## 0.5.0-preview

Historical snapshot: `c4df69f`. Adds document catalogs/review, bank normalization,
limited local cash records, manual ELSTER evidence/preflight, localized folders,
readable reports, user guides, real overview and verified backup/restore. Native
Windows covers intake, overview and recovery; protected accounting/filing writers
still use optional Python. The graphical prototype remains synthetic.

Historical source-only release: no new build-provenance claim for this commit.
Use 0.6.0-preview.1 for the attested packages and current maintenance workflow.

## 0.4.0-preview

Historical snapshot: `17f850d`. Adds international transactions, payment-provider
reconciliation preparation, reverse-charge research, activity classification and
ELSTER form worksheets. No live payment, accounting-system or filing integration.
Historical source-only release; superseded by the current preview.

## 0.3.0-preview

Historical snapshot: `bc7f24a`. Adds guided private setup, EN/RU workflows,
reproducible offline host packages and Windows/macOS utility validation. Older
accountant-oriented wording is superseded by the self-managed accounting scope.
Historical source-only release; superseded by the current preview.
