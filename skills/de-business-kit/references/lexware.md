# Work with Lexware Office

## Identify the product and available access

Identify **Lexware Office** in the browser versus an installed product such as
**Lexware buchhaltung / financial office**. Reuse known facts; do not apply the
Office API or export menus to desktop products. Keep the user's chosen system
and self-managed accounting route. An adviser is an optional participant.

**This package has no production Lexware connector.** Use
[existing-data onboarding](existing-data.md) to inspect available host tools or
supplied files. A missing connector does not require an API subscription or a
migration. See [connection verification](connections.md) for the shared operation
note and supplied-export coverage procedure. Do not claim access, posting or
submission from a saved configuration or a help page.

For a factual question, answer without requiring a workspace. For saved work,
reuse the existing source map/task evidence. Paths below are **logical**: resolve
them with `workspace.py folders` or native `-Action folders` before ordinary file
access. Do not create parallel folders or rewrite canonical records directly.

## Assisted drafts and exports

Use [assisted service operations](assisted-services.md) for nontechnical users
who need practical help in the actual account, and the dated
[current source record](assisted-services-sources.md) for route constraints.
An existing suitable connector is useful for supported reads; use an available
browser for unsupported draft edits or UI export steps rather than demanding API
setup. Confirm the observed edition, company, document and current UI controls.

The current documented invoices API has no invoice-update operation, and a draft
invoice has no downloadable invoice file. Do not infer editing support from a
create/read endpoint or finalize an invoice to make a PDF download work. Use
supported browser draft editing/preview; explain an unavailable export precisely.
`Abschließen und Speichern` finalizes/assigns the invoice number in the documented
creation route—it is not merely saving a draft. Read back the resulting draft and
leave finalization/sending to the user when that is their chosen boundary.

For an export, set the requested period/date basis and output, inspect any locking
or transfer option before execution, and verify the downloaded original file.
Preserve a task-specific handoff if download/upload or a final action is unsupported.
These are agent workflows; only local Lexware examples have been tested. Live acceptance remains unperformed
until an explicitly available test account and operation are actually checked.

## First bounded document read

For the selected Lexware Office acceptance route, start with a user-designated
test account containing synthetic documents and a specified period. Use an
already available suitable connector first; otherwise use an actual supported
browser session. Do not configure API credentials or install an adapter merely
to run this check. If only the login screen is available, let the user authenticate
in the official flow; no secrets go into chat or notes.

Verify the intended account before opening documents. Inspect the visible document
list and selected date/status filters; then read one relevant document's ID, type,
dates and status without editing it. Record the observed scope and retrieval time.
If original download is available and within scope, preserve that original and
compare its identity with the displayed record. A successful preview alone proves
neither original retrieval nor all pages. Report list access, document read and
original download separately. Stop at unavailable access or an operation with
unapproved side effects; an export fallback remains a separate snapshot check.

Save the result in the existing operation note, including partial/unknown scope
and the next action. Use this small read as service acceptance only for the
observed account/operation. It does not establish a production connector, continuing
access, posting, complete-month coverage or readiness to file. Real business data
requires the shared privacy assessment before model processing.

## Identify the export before diagnosing missing documents

Export findings were checked **2026-10-26**; the dated
[primary-source findings](lexware-export-sources.md) record scope and uncertainties.
First establish the exact export route, year, period and selected date basis.
If the route is unknown, give conditional explanations and obtain the existing
export/settings evidence before concluding why a document is absent.

| Route | Inspect | Limit |
| --- | --- | --- |
| Document/PDF download | Incoming/outgoing selection and **Rechnungsdatum or Zahldatum** filter | Not the same selection as DATEV; a PDF rendering does not establish original XML preservation |
| DATEV posting/document export | **Belegdatum**, capture status/time, selected period and document links | A later payment posting need not include the original document again |
| Existing supplied files | Observed headers, IDs, document originals, pages and filters | Snapshot only; absent files or unknown totals cannot establish live-account completeness |

For the **documented posting-based export**, distinguish status from category:

| Lexware item | Meaning | Export consequence for that route |
| --- | --- | --- |
| Status `Zu prüfen` or `Entwurf` | Not fully captured; no corresponding posting | Excluded |
| Category `Zu prüfen` | Captured with an interim-account posting | Category alone does not exclude it |

Do not apply this table as a guarantee about the separate original/PDF download.
Do not assign the interim category merely to include a document in an export.
Keep the treatment unresolved until supported; consultation is optional rather
than a required handoff for investigating coverage.

For a missing receipt, compare its date with the **actual selected date basis**,
then capture/status at export time, original availability and export diagnostics.
A document entered later cannot be assumed present in an earlier snapshot. Keep
user-reported values distinct from inspected files/provider state. Inspect bank
allocations separately when relevant; they do not prove document completeness.
If a user has an adviser, distinguish their live view from a transfer to their
separate software; do not infer one from the other.

## Preserve evidence without closing or changing the period

For the documented PDF route, current help points to `Einstellungen > Export >
Meine Lexware Office-Daten herunterladen > weitere Exporte > Belege`. Verify the
actual account controls and edition; API eligibility does not establish manual
export eligibility. Prefer an existing supplied export for inspection.

Before initiating any new export, check its effect: manual DATEV export may lock
records depending on the option/settings; audit export, DATEV Buchungsdatenservice
and ADDISON transfer have documented locking effects. A request to inspect missing
documents does not authorize these mutations. Match concrete authorization before
locking/transferring; otherwise continue with available evidence. Re-exporting,
changing a category or finalizing a draft is not a substitute for diagnosis.

Preserve source XML or the original hybrid file as well as readable views.
Generated DATEV XML metadata is not necessarily an original e-invoice. The local
catalog does not unpack/import ZIPs: retain them at source or in a separately
assessed private evidence location, and disclose uninspected contents. Use the
shared export procedure for supported files; never silently discard unsupported
originals or treat a CSV row as its attached document.

## Design constraints for a future API adapter

Verify these details against the current API documentation before implementing or using a connector:

- Use the current gateway `https://api.lexware.io`; do not build against the former `api.lexoffice.io` address.
- Invoice creation defaults to draft; `finalize=true` creates an open invoice. Do not assume later arbitrary status changes are supported.
- Uploaded vouchers can be `blank` during asynchronous OCR before becoming `unchecked`. Wait for a usable state.
- Bookkeeping voucher writes accept `open` or `unchecked`; unchecked net vouchers are unsupported.
- Preserve every existing attachment ID on voucher updates: omitting IDs can permanently delete attachments. Read the current object and version first.
- Payment endpoints expose payment status; do not mistake them for a bank-payment API.
- Handle rate limiting, version conflicts and ambiguous timeouts; read back before retrying creation.
- Download the required original XML or hybrid document, not only a rendered PDF.

Check the user's current plan. The official feature page currently lists Public API from **XL**, without a separate API fee. Do not promise these conditions indefinitely or infer that all integrations have identical eligibility.

Keep credentials in the runtime's credential mechanism, never in company JSON, proposals, public Git or audit text. A future adapter must restrict hosts and operations independently of document contents. Present concrete proposed mutations before using existing or newly granted authorization, then verify the resulting provider state.

## Required result and continuation

Return a readable explanation or dated operation note: selected route/date basis,
observed versus reported scope, original references, missing/unknown documents,
possible cause with evidence, and one next action. Do not mark the month closed.
For persisted work, use the existing logical `00_admin/source-map.md` and linked
period evidence under `07_exports/YYYY-MM`; preserve previous versions. Update
existing tasks only through validated writers and only when the task warrants it.
No new provider registry, local shadow ledger or adviser package is required.
An optional transfer package records inclusion/exclusion and actual transfer
evidence only when that separate operation is requested and performed.

## Official sources

The API/design pointers below retain their **2026-10-25** check date; reverify
before implementation. Export-route findings were separately checked on
**2026-10-26** in [the source note](lexware-export-sources.md). Product capabilities
and plan conditions can change.

- [Product distinction: Lexware Office versus Lexware buchhaltung](https://shop.lexware.de/buchhaltungssoftware-vergleich).
- [Lexware Office Public API and plan eligibility](https://www.lexware.de/funktionen/public-api/).
- [API documentation: files, invoices, vouchers, payments and rate limits](https://developers.lexware.io/docs/).
- [Missing receipts: status versus category, document date and transfer checks](https://help.lexware.de/de-form/articles/548692-belege-fehlen-im-export-oder-wurden-nicht-ubertragen-ursachen-und-losungen).
- [Unassigned transactions and export troubleshooting](https://help.lexware.de/de-form/articles/548872-fehlermeldungen-und-probleme-beim-export-von-belegen-und-buchungsdaten-losen).
- [Adviser cockpit and access to the live client view](https://office.lexware.de/steuerberater/funktionen/steuerberater-cockpit/).
- [Adviser export configuration, including locking postings](https://steuerberater.help.lexware.de/de/articles/603461-export-der-daten-uber-den-steuerkanzlei-zugang).
