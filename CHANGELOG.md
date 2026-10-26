# Changelog

[English](CHANGELOG.md) | [Русский](CHANGELOG.ru.md)

Versions follow Semantic Versioning. All releases below are previews, not a
certification of accounting correctness or desktop compatibility. Historical
milestones are first published on 2026-10-26; their original commits are retained.

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
