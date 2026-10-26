# Lexware Office document export: source findings

Checked **2026-10-26** against public, first-party Lexware documentation.
Applies to inspection of an October export; record the actual year and selected
date basis. This is provider-documentation evidence, not authenticated account
access, a tested integration, an export receipt or a tax calculation. Self-managed
work remains a valid route; an adviser is not a prerequisite for local inspection.

## Product and access boundaries

These findings concern browser-based **Lexware Office**. Installed **Lexware
buchhaltung / financial office** have separate commands and contracts; do not
reuse their manuals for Office. The [official product comparison](https://shop.lexware.de/buchhaltungssoftware-vergleich)
is a product-identification pointer carried from the existing reference; its
content could not be reverified in this check because the server returned 403.

The [Office edition page](https://www.lexware.de/preise/) labels S as receipt
capture/archive, L as accounting/EÜR/VAT and XL as including API. Its extracted
comparison table does not preserve all availability indicators, so it does not
prove the exact document-export entitlement of every edition. The [Public API
page](https://www.lexware.de/funktionen/public-api/) explicitly places that API in
XL. This is not evidence that manual document downloads require XL. Inspect the
actual edition, account permissions and available controls; do not upgrade,
create credentials or invite an adviser merely to inspect an export.

## Choose the export before interpreting its period

The [manual-export FAQ](https://help.lexware.de/de-form/articles/709771-haufige-fragen-zu-den-manuellen-exporten-an-die-steuerkanzlei)
documents a separate document/PDF route under `Einstellungen > Export > Meine
Lexware Office-Daten herunterladen > weitere Exporte > Belege`. It permits
incoming/outgoing invoice filters and **Rechnungsdatum or Zahldatum**. The same
FAQ says DATEV-format exports cover the selected period rather than individually
selected documents; they do not offer an outgoing-only selection. Do not apply
the DATEV date rule to every document export. Record the selected control and
period in the inspection manifest. For example, an invoice issued in September
and paid in October can differ between invoice-date and payment-date selections.

The [manual-export instructions](https://help.lexware.de/de-form/articles/548755-manuelle-exporte-fur-den-datentransfer-an-die-steuerkanzlei)
describe three DATEV-compatible choices: document images with posting proposals,
posting batches, or both. Period selection may be annual, monthly or individual.
Completed ZIPs appear below the export overview. The article says an adviser
connection changes which tab is visible; it does not require adding one.
Its general FAQ about adviser/client numbers must be read alongside its specific
statement that the images-with-proposals export needs neither. Never invent
real identifiers for inspection.

## Status, category and missing coverage

The [missing-document article](https://help.lexware.de/de-form/articles/548692-belege-fehlen-im-export-oder-wurden-nicht-ubertragen-ursachen-und-losungen)
distinguishes **status** `Zu prüfen`/`Entwurf` (not fully captured, no posting,
excluded from the documented posting-based export) from **category** `Zu prüfen`
(captured and posted to an interim account, included). It names 1590/SKR03 and
1370/SKR04 and presents that category as an adviser-agreed temporary treatment.
This is not a reason to categorize unresolved documents merely to make an export
appear complete. Record exclusions and resolve treatment separately.

For the documented posting/transfer routes, receipts enter by **Belegdatum**,
independent of payment or performance date. A later payment can produce only a
payment posting in its month. Capture after an earlier export also creates a
coverage gap. This source does not establish whether the separate original/PDF
download includes every unreviewed document; inspect the actual result and list
uncertainties rather than promising coverage.

## Exports can change provider records

[Festschreibung documentation](https://help.lexware.de/de-form/articles/548165-festschreibung-richtig-gemacht)
lists obligatory locking for the audit export, DATEV Buchungsdatenservice and
ADDISON OneClick, among other triggers. Manual DATEV-format export and DATEV
Rechnungsdatenservice can optionally lock records. Locking cannot be reversed;
the lock's date logic can differ from export inclusion (performance date, with
document-date fallback and advance-payment exceptions).
The [adviser export settings](https://steuerberater.help.lexware.de/de/articles/603461-export-der-daten-uber-den-steuerkanzlei-zugang)
also allow automatic locking to be configured. Inspect the selected route and
effective locking option before starting anything; stop for concrete
authorization if the proposed action would lock, transmit or otherwise change
records. Viewing controls alone is not authorization to finalize October.

## Preserve originals separately from readable views

The [local-download article](https://help.lexware.de/de-form/articles/548791-erklarvideo-einzelne-belege-lokal-abspeichern)
documents image exports in PDF or original format. The [E-Rechnung capture
article](https://help.lexware.de/de-form/articles/548951-so-einfach-erfasst-du-e-rechnungen-in-lexware-office)
explains that XML is visualized for reading and that `<>` downloads the attached
XML. Preserve the source XML or original hybrid file alongside any readable
rendering. A printed PDF does not demonstrate preservation of the structured
payload. The [DATEV image-import example](https://help.lexware.de/de-form/articles/548356-manueller-export-belegbilder-wie-importiere-ich-belegbilder-mit-den-zugehorigen-belegdaten-in-datev)
also contains generated XML metadata; an `.xml` filename alone does not identify
the original e-invoice. Inspect formats and contents without modifying originals.

## Unverified account facts

No live account, edition-specific control, selected lock setting, October file,
export completeness, original-byte identity or bank reconciliation was tested.
Public help pages can change and contain adviser-oriented examples. Preserve
these limits when giving account-specific steps; ask only for the missing
product/edition, period basis or export evidence needed for the next step.
