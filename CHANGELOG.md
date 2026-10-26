# Changelog

[English](CHANGELOG.md) | [Русский](CHANGELOG.ru.md)

Versions follow Semantic Versioning. All releases below are previews, not a
certification of accounting correctness or desktop compatibility. Historical
milestones are first published on 2026-10-26; their original commits are retained.

## 0.6.0-preview.1

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
