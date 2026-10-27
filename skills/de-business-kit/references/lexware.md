# Work with Lexware Office

## Identify the product and available access

Identify **Lexware Office** in the browser versus an installed product such as
**Lexware buchhaltung / financial office**. Reuse known facts; do not apply the
Office API or export menus to desktop products. Keep the user's chosen system
and self-managed accounting route. An adviser is an optional participant.

The optional Python [invoice route below](#provider-invoice-draft-readback-and-sending)
implements bounded draft creation/readback through the public API. It is opt-in,
has synthetic transport coverage and has not been accepted in a live account. Use
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
`Abschließen und Speichern` finalizes the invoice; a number may already have been
assigned when saving the draft and does not establish issue. Read back the resulting draft and
leave finalization/sending to the user when that is their chosen boundary.

For an export, set the requested period/date basis and output, inspect any locking
or transfer option before execution, and verify the downloaded original file.
Preserve a task-specific handoff if download/upload or a final action is unsupported.
On **2026-10-27**, one authorized zero-value browser journey in an existing
business company completed draft creation/readback, finalization, PDF inspection,
sending and recipient acknowledgement. This was not a provider sandbox. The sent
PDF matched the reviewed final file byte-for-byte. The API adapter remains tested
with synthetic transport only; broader invoices, corrections and unattended
operation are not established by this bounded run. A separate browser check on
the same date saved/reopened a zero-value draft, corrected its introduction,
verified the same UUID/number, VAT setting and total, and left it unissued/unsent.
This establishes draft-text editing only, not correction of an issued invoice.

Before preparing API access, apply the shared [cost check](assisted-services.md#check-costs-before-setup).
In the authenticated [Public API settings](https://app.lexware.de/addons/public-api)
checked **2026-10-27**, key creation was disabled on the tested Office L account;
the UI stated that Public API requires Office XL. This is a dated account
observation, not a price quote or proof of another account's entitlement. The user
kept the existing plan. Continue included browser operations; do not request an
upgrade or API key merely to run tests. Live API acceptance remains blocked for
that route, independently of successful browser checks.

## Provider invoice draft, readback and sending

Pair this route with [protected invoicing](invoicing-workflow.md). It targets
**Lexware Office**, not desktop Lexware. API draft creation changes the account
and consumes an invoice number; it is not local preparation. Do not call the
provider during setup, discovery or a local demonstration. Use already authorized
account access and matching authority for the concrete creation. Do not create a
new API key, subscribe or send test invoices merely to validate installation.

Use an existing suitable host connector when available. The optional bundled
adapter requires an existing Python runtime and `LEXWARE_API_KEY` supplied by the
invoking process through an appropriate secret mechanism. Never request the key
in chat or put it in a command argument, JSON file, profile, screenshot or report.
It uses fixed `https://api.lexware.io`, normal TLS verification, bounded requests,
no redirects and no automatic retries. There is no arbitrary URL, proxy, shell or
provider-response `resourceUri` execution. If access is unavailable, continue
through the authorized browser/manual route without requiring API setup.

### Prepare and create the provider draft

1. Inspect `invoice-list` across periods before creating anything. Use the existing
   local invoice and provider ID. Record `system=Lexware Office`, the actual
   organization UUID as `account_reference` and existing contact UUID as
   `customer_reference`; inspect the correct company and recipient. An invoice
   number is not the object UUID or proof of issue.
2. Prepare a local reviewed request. This first adapter supports ordinary invoice
   creation with an existing contact, EUR and 1–100 custom items. It does not create
   contacts, update drafts, calculate tax or create correction documents. Provider
   correction/editing uses the separately reviewed web-app route. Required fields:
   `voucherDate`, `address={contactId}`, `lineItems`, `totalPrice={currency}`,
   `taxConditions`, `shippingConditions`. Optional supported fields: `language`,
   `title`, `introduction`, `remark`, `paymentConditions`, `deliveryTerms`. Use
   actual agreed dates, quantities/prices and independently established tax facts;
   minimum accepted fields do not establish legal completeness.
3. Run `desk.py lexware-template` for the action contract. Every action supplies
   `invoice_id`, `action`, `actor`, `evidence_file`, `note`, `occurred_on`; unused
   `payload_file`, `external_id`, `media_type` stay null. Execute with
   `desk.py lexware-action --root <private> --input <workspace-relative-json>
   --expected-sha256 <fresh-invoice-show-hash>`.
4. `prepare` additionally supplies `payload_file` and freezes exact request bytes.
   `authorize-draft` records the user's existing authority to create that exact
   external draft, including number consumption and account scope. These local
   records are attestations, not authenticated identity or a fresh permission gate
   when the user already authorized the same concrete operation.
5. `create-draft` checks the credential's `/v1/profile` organization, durably records
   intent, POSTs the frozen request once, preserves the returned ID, then GETs that
   object independently. It never adds `finalize=true`. API success leaves the
   local invoice unissued. Save a readable status and task after the operation.
6. Inspect preserved readback, not only the POST response. `differences` compares
   supplied fields; also inspect provider-added defaults, recipient address,
   introduction/payment/closing text, totals, tax conditions, dates and number.
   `review-readback` needs actual review evidence explaining differences and their
   accepted effect. Any fresh readback invalidates prior issue review/authority;
   material changes require fresh matching issue scope and authorization.

After timeout or HTTP error, do not repeat POST. If an ID was saved, `readback`
performs GET only. If no ID is known, inspect the actual account/history; only
`reconcile` with a reviewed `external_id` and correlation evidence can bind the
existing attempt. It requires matching requested fields and the correct company/
contact/currency. Similar fields alone do not prove it is the right operation;
verify creation time, business reference and history. A missing search match does
not prove absence. No blind reset/retry or local cancellation of an existing
provider draft is supported; unresolved cases remain visible for reconciliation.

### Finalize the same draft and read back the actual artifact

The API cannot finalize an existing invoice draft. Never create another invoice
with `finalize=true` as a substitute. Use the exact saved provider object in the
actual authorized browser session, or guide the user through it:

1. After reviewed readback, record `review-issue` and `authorize-issue` through the
   invoice writer. Inspect the live company, customer, UUID, version/content and
   editable draft again. If the UI differs from saved evidence, stop the external
   action, refresh readback and repeat the affected review.
2. Record `begin-issue` immediately before finalization. `desk.py lexware-handoff
   --root <private> --id <id> --kind finalize` returns the documented permalink,
   exact company/object and attempt. This is a handoff, not a browser action.
3. In the same draft, use **Weiter zur Vorschau**, then the separate finalization/
   save choice. The live 2026-10-27 UI exposed **Abschließen + speichern** in the
   split-button menu; selecting it executed finalization. Inspect current controls before
   using them; do not create a new draft or select a combined finalize-and-send
   operation. A combined action is unsupported by this separate review sequence.
   Honor a user-reserved final click; otherwise execute within existing concrete
   authorization using the host's supported browser tool.
4. Re-select the invoice and inspect the actual finalized status, identity and
   final content. Ordinary unpaid invoices may show **Offen**; the live zero-value
   test immediately showed **bezahlt** without a payment action. Do not infer a
   cash movement or sending from that label. Use
   `readback`, then `download` with explicit `media_type=application/pdf` or
   `application/xml`, then `review-readback`. The adapter checks readback before
   and after download; drift blocks using the artifact. Preserve required original
   structured files: a PDF representation of XRechnung is a preview. This is not
   technical e-invoice validation. Draft file retrieval is unavailable (409).
5. Record `confirm-issued` against the existing attempt, actual provider ID/number
   and exact downloaded artifact. Inspect format/content before delivery. Unknown
   finalization remains open; GET/readback does not authorize a repeated click.

### Send and verify dispatch in the provider

Use `review-delivery` for the actual final artifact, exact recipient/channel and
intentional attachments; preserve the exact subject/body and permitted To/Cc/Bcc
in its private review evidence. That frozen file is returned as the package's
`scope_evidence`; message fields are not separate structured package fields.
Keep private notes out of the recipient attachments. Record matching
`authorize-delivery`. Inspect the provider's **Per E-Mail senden** dialog against
the frozen package and its scope evidence: company/invoice, To/Cc/Bcc,
subject/body and every attachment.
This first route supports the single exact email destination in the local package;
remove unintended extra recipients only within authorized draft-editing scope.
If the service regenerates a different document or the envelope differs, stop
and re-review the actual final scope. Do not send merely because the dialog opened.

Record `begin-delivery` just before the external send. `desk.py lexware-handoff
--root <private> --id <id> --kind send` supplies the same provider UUID, attempt
and frozen package. The assistant then uses the observed final send control in
the supported browser (or the user performs it if reserved). No invented public
API endpoint or private browser API is used. Reopening an unknown attempt is an
investigation, never permission to click send again.

Re-select the invoice and inspect the actual sent history (**versendet am ...**
in the live 2026-10-27 UI) and sent files. Preserve the observed recipient, date/time
with only the precision exposed, artifact set and dispatch
reference, then `confirm-dispatched` against the same attempt. If no message ID
is exposed, use a documented correlation reference from the actual provider
history; do not invent a provider-issued ID. An API status of `open` or `paid`
does not prove sending. An unclear result stays `delivery_unconfirmed`.
Only separately inspected receipt/customer acknowledgement supports
`confirm-delivered`; sending, receipt, agreement and payment remain distinct.

Official documentation was checked on **2026-10-27**. The live browser run on the
same date observed **Senden**, the date-only sent-history entry, recipient/message
and a downloadable sent attachment. Download that actual attachment and compare
with the reviewed file when available; do not infer byte equality from a name.
The composer enabled an extra copy by default: inspect it against the authorized
recipient scope. A browser title longer than 25 characters was rejected; keep a
long test/business reference in the introduction or line description. If a provider
iframe stays blank, an exact observed same-origin UI URL may be opened separately;
never guess a private endpoint or replay the send. A standalone composer can remain
open after sending, so inspect refreshed history before deciding the outcome.
Native Save dialogs must complete before claiming an original download. See
[provider source details](assisted-services-sources.md#lexware-api-and-browser-route--2026-10-27).
Save versioned EN/RU explanations and existing follow-up tasks. The GUI and
standalone native Windows tools have no controls for this adapter.

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
