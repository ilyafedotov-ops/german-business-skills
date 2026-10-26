# Changelog

[English](CHANGELOG.md) | [Русский](CHANGELOG.ru.md)

Versions follow Semantic Versioning. All releases below are previews, not a
certification of accounting correctness or desktop compatibility. Historical
milestones are first published on 2026-10-26; their original commits are retained.

## Unreleased

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
