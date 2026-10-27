# Assisted service routes: checked source findings

Checked **2026-10-26**, using public official/provider sources. Applies to route
selection on that date; choose the actual form version, business facts, period,
account edition and permissions before acting. These findings support assisted
preparation; they are **not** authenticated UI acceptance, a connector, tax
calculations, successful drafts, exports or submission receipts. Earlier dated
research remains historical evidence. Shared agent reference; EN/RU explanations
belong in the affected user guides.

## ELSTER: initial tax registration

The official [Einzelunternehmen questionnaire](https://www.elster.de/eportal/formulare-leistungen/alleformulare/fseeun)
covers commencement of commercial, self-employed/freelance and agricultural or
forestry activity. Its public start page offers a version selection and
`Weiter`; the tax-office selection depends on the place of business management.
Practical consequence: a freelancer need not find a separate freelancer-only
questionnaire. Observe the available version and labels instead of copying
field numbers from an old worksheet.

The [ELSTER business-start page](https://www.elster.de/elsterweb/infoseite/unternehmensgruendung)
states that the electronic questionnaire requests the new business tax number,
is due within one month of commencing activity, and requires registration.
The [Rheinland-Pfalz tax-authority startup leaflet](https://lfst.rlp.de/fileadmin/lfst.rlp.de/Service/Existenzgruender/Merkblatt_fuer_Existenzgruender__Stand_06.03.2025_.pdf)
expressly permits an existing account and describes `Formulare & Leistungen >
Alle Formulare` as the start path. Reuse an eligible existing account; do not
create a second account as a routine prerequisite.

The [current registration help](https://www.elster.de/eportal/helpGlobal?themaGlobal=help_registrierung)
restricts email-only registration to the stated missing-ID/tax-number situation
and to completing/transmitting the questionnaire. It documents email activation,
CAPTCHA, password and certificate steps. An email-only startup account is not
proof that later VAT returns are available. Have the user handle credentials,
activation messages, certificate selection, CAPTCHA and any MFA in the official
UI; never obtain certificate bytes or secrets in chat.

Tax registration and municipal trade registration have different purposes.
The federal [business-registration guidance](https://www.existenzgruendungsportal.de/Navigation/DE/So-gehts/Unternehmensanmeldung/unternehmensanmeldung)
distinguishes trade registration from the freelancer route to the Finanzamt.
There can nevertheless be a combined digital front door: the
[Niedersachsen tax authority](https://lstn.niedersachsen.de/steuer/steuervordrucke/betriebseroeffnung_aufgabe/betriebseroeffnung-67695.html)
links a combined tax/trade application. Practical consequence: identify the
municipality and actual supported route; ordinary ELSTER questionnaire work does
not demonstrate completion of a Gewerbeanmeldung, and a combined route must show
evidence of each relevant procedure.

### Recommended assisted route and boundary

With a permitted browser/computer tool, open the official start page, let the
user authenticate, inspect the live form, and actively enter evidence-backed
draft answers within the user's scope. Explain German labels in the user's
language and ask only for unresolved facts or consequential elections. Save a
draft where the live UI provides that action, read back values and warnings, and
prepare a readable review before the user performs final confirmation. A
worksheet is a useful fallback when tool access is absent, not a reason to
decline available draft assistance.

This is an operating recommendation under the package's authorization rules,
not a claim that every current questionnaire screen was inspected. Public
sources do not establish its complete authenticated fields or save/validation
controls. Observe them live. Keep draft, validation, final transmission and
authority response separate. The [ELSTER FAQ](https://www.elster.de/eportal/helpGlobal?themaGlobal=help_eop)
also warns that its inbox confirms filings made directly through Mein ELSTER;
do not infer failure of a different software route from an empty ELSTER inbox.

## Lexware Office: read, draft and export

This section concerns browser-based **Lexware Office**, formerly **lexoffice**,
not installed Lexware buchhaltung/financial office. The
[API documentation](https://developers.lexware.io/docs/)
records the rebranding and current `api.lexware.io` gateway. Its invoices section
documents creation, retrieval, rendering/download and browser view/edit links;
it does not document an invoice-update endpoint. Creation defaults to `draft`;
`finalize=true` creates an open invoice. Draft invoices have no downloadable
document file; requests return 409. An XRechnung PDF is a preview, while the XML
is the electronic invoice. Practical consequence: use the supported browser
editor for existing draft changes and preview; **do not finalize an invoice
merely to obtain a draft file**. General API write permission is not proof of an
operation-specific update contract.

The [invoice product page](https://www.lexware.de/funktionen/rechnungen/)
documents preview, returning to edit, saving a draft and later completion. The
[current creation instructions](https://help.lexware.de/de-form/articles/547986-rechnung-oder-teilrechnung-erstellen-schritt-fur-schritt)
give `+ > Rechnung erstellen`, alternatively `Belegliste > Neuer Beleg > Rechnung`.
They distinguish preview from `Abschließen und Speichern`, which finalizes and
assigns the final number, and subsequent email sending. Invoice creation is
documented from version M. Practical consequence: fill and read back a draft in
the existing browser session; have the user confirm finalization and sending
after review. Neither a preview nor an `Offen` status proves delivery.

The [Public API help](https://help.lexware.de/de-form/articles/548863-alles-rund-um-public-api)
requires XL and documents individually scoped keys. The
[feature page](https://www.lexware.de/funktionen/public-api/)
states no additional API usage charge. These are provider conditions, not a
purchase recommendation or proof of manual-export eligibility. Existing browser
access can be enough; do not request a plan upgrade or new key merely to help
with an available draft. Key creation and integration setup are separate scoped
actions, with secrets retained in an appropriate runtime credential mechanism.

### Export selection is part of the answer

The [manual-export FAQ](https://help.lexware.de/de-form/articles/709771-haufige-fragen-zu-den-manuellen-exporten-an-die-steuerkanzlei)
documents the PDF route: `Einstellungen > Export > Meine Lexware Office-Daten
herunterladen > weitere Exporte > Belege`, filtered by incoming/outgoing invoices
and **Rechnungsdatum or Zahldatum**. Selected documents can also be printed from
the document list with a PDF printer. DATEV exports instead cover the whole
selected period, without an outgoing-only selection, and use document date for
the described inclusion. Practical consequence: September invoices paid in
October can produce different selections. Record route, year, period, date
basis, status filters and observed output before diagnosing a missing document.
PDF printing alone does not preserve original structured invoice bytes.

The [locking documentation](https://help.lexware.de/de-form/articles/548165-festschreibung-richtig-gemacht)
lists obligatory locking for audit exports, DATEV Buchungsdatenservice and
ADDISON OneClick; manual DATEV exports and DATEV Rechnungsdatenservice can lock
optionally. Adviser configuration can also enable automatic locking. Locking
cannot be reversed and its date basis can differ from export inclusion.
Practical consequence: inspect the effective option before starting an export;
authorization to inspect a month does not authorize locking or transmission.
Continue reading available records while a consequential action awaits the
user's final confirmation. See the more detailed dated
[export findings](lexware-export-sources.md) for original-file and coverage gaps.

## Other providers: verify the operation, not just the brand

Prefer an already available supported connector for its documented operation,
then an authorized browser/computer session, then supplied exports or guided
steps. Check the actual product, account, permissions, draft/final status,
period basis, originals and side effects. Do not require an API or technical
installation when browser assistance can complete the requested preparation.

For contrast, the official [sevdesk API documentation](https://api.sevdesk.de/)
states that invoices are created as draft and that operation endpoints change
their status; its `enshrine` action is irreversible. It also documents distinct
CSV and ZIP invoice exports. Practical consequence: do not transplant Lexware's
status model or export assumptions into sevdesk. This bounded check establishes
no sevdesk edition entitlement, complete operation matrix or tested connector.

## Evidence still needed for service acceptance

No live accounts or authentication were used. No account-specific permissions,
form field maps, draft saving, invoice editing, receipt/original downloads,
exports, locking settings or transmission were tested. A later acceptance check
must name the actual host/tool, account scope and operation, use synthetic
fixtures where possible, and inspect read-back/artifacts and any confirmation.
Public documentation supports a route proposal; observed service state supports
claims about what happened.

## Invoice correction and delivery check — 2026-10-27

Checked **2026-10-27** for the protected [invoicing workflow](invoicing-workflow.md).
These public sources establish documented routes, not access or acceptance in a
particular account. Recheck the applicable transaction period and actual UI before
execution; preserve the selected product and its existing books.

- Lexware's [creation help](https://help.lexware.de/de-form/articles/547986-rechnung-oder-teilrechnung-erstellen-schritt-fur-schritt)
  separates finalization from sending. Its [numbering help](https://help.lexware.de/de-form/articles/548053-nummernkreise-einstellen-und-rechnungsnummern-vergeben)
  says drafts receive numbers, while the creation article associates final numbering
  with completion. This inconsistency remains unresolved without actual route
  observation: a number alone cannot prove issuance, and no local number is assigned.
- [Correction/amount help](https://help.lexware.de/de-form/articles/640615-rechnung-korrigieren-oder-rechnungsbetrag-korrigieren-so-gehst-du-vor)
  distinguishes amount corrections from content errors; [cancellation/reissue](https://help.lexware.de/de-form/articles/548199-abgeschlossene-rechnungen-stornieren-und-neu-ausstellen)
  and [locked-document correction](https://help.lexware.de/de-form/articles/548776-wie-berichtige-ich-einen-beleg)
  describe different effects on originals, numbers, bookings and payment links.
  Inspect sent/locked/paid state and the exact supported branch. A provider's
  automatic paid/refunded label does not independently prove a bank movement.
- The [official API](https://developers.lexware.io/docs/) documents draft creation,
  `finalize=true` for open invoices, no invoice update/status-transition endpoint,
  and unavailable draft files (409; corrected in the adapter check below). A 504 may follow successful processing. Use
  supported UI/manual editing where needed; read back after timeouts and do not
  finalize just to download a preview. No idempotency guarantee or automatic
  invoice-send capability is inferred from a create endpoint.
- [Sent-attachment history](https://help.lexware.de/de-form/articles/548518-wie-kann-ich-dateien-aus-dem-kundenmanager-mit-der-rechnung-oder-dem-angebot-versenden)
  and [email logging](https://help.lexware.de/de-form/articles/548812-lexware-ios-app-belege-per-e-mail-versenden-und-im-kundencenter-teilen)
  support inspecting dispatch evidence. They do not establish customer receipt,
  reading, agreement or payment. [E-invoice sending](https://help.lexware.de/de-form/articles/547942-e-rechnungen-versenden-und-empfangen)
  also permits downloaded files sent separately; preserve the actual destination,
  final files and route's receipt evidence. If unavailable, delivery stays unconfirmed.
- [UStDV §31(5)](https://www.gesetze-im-internet.de/ustdv_1980/__31.html)
  permits specifically linked correction of missing/incorrect particulars; full
  cancellation/reissue is not the universal rule. [UStG §14](https://www.gesetze-im-internet.de/ustg_1980/__14.html)
  distinguishes statutory self-billing (`Gutschrift`) from a provider's credit-note
  label. No automated legal classification is implemented.
- For the **2026** transition, [UStG §27(38)](https://www.gesetze-im-internet.de/ustg_1980/__27.html)
  and the [BMF UStAE snapshot dated 2025-12-31, section 14.11](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/Umsatzsteuer-Anwendungserlass/Umsatzsteuer-Anwendungserlass-31-12-2025.pdf?__blob=publicationFile&v=2)
  require checking the actual format duty and available transition. Do not claim
  every 2026 correction must be XML, or that an email always suffices. This dated
  BMF snapshot is navigation evidence, not a claim to be the latest consolidated
  guidance; research the actual case before asserting compliance.

Example consequence: an issued document with a wrong description may need a
linked content correction or a provider-supported cancellation/replacement. A
partial amount credit is a different route. A saved PDF, number or "Gesendet"
label alone establishes none of those legal effects or customer receipt.

## Lexware API and browser route — 2026-10-27

Implementation-specific recheck for the [actual invoice route](lexware.md#provider-invoice-draft-readback-and-sending):

- [API reference](https://developers.lexware.io/docs/#invoices-endpoint): fixed
  `api.lexware.io`; Bearer credentials; `/v1/profile` identifies the organization.
  POST `/v1/invoices` defaults to draft; GET by UUID supplies independent readback.
  No documented invoice update, existing-draft finalization or sending endpoint.
  `finalize=true` creates a new invoice, so it cannot safely finalize a saved draft.
- [Invoice cookbook](https://developers.lexware.io/cookbooks/invoices/) explicitly
  states that draft creation consumes a number, consistent with the
  [number-circle help](https://help.lexware.de/de-form/articles/548053-nummernkreise-einstellen-und-rechnungsnummern-vergeben).
  Some other cookbook claims are stale; the endpoint reference owns field/format
  contracts. The adapter labels number consumption before draft authorization.
- [File endpoint](https://developers.lexware.io/docs/#download-an-invoice-file):
  draft has no downloadable artifact and returns 409, refining the earlier 406
  note. Readback and download must refer to the same stable provider version.
  A PDF rendering of XRechnung is a preview; preserve required structured originals.
- [HTTP statuses](https://developers.lexware.io/docs/#http-status-codes): a 504 may
  follow successful processing. No idempotency guarantee was established. The
  adapter records intent before POST, never replays writes automatically and
  recovers known objects by GET. Sequential requests within each client are spaced by 550 ms; concurrent
  clients can still encounter the documented two/second limit. HTTP failures do not prove that creation failed.
- [Invoice creation help](https://help.lexware.de/de-form/articles/547986-rechnung-oder-teilrechnung-erstellen-schritt-fur-schritt)
  separates preview, finalization/save, open status and later email sending.
  [Attachment history help](https://help.lexware.de/de-form/articles/548518-wie-kann-ich-dateien-aus-dem-kundenmanager-mit-der-rechnung-oder-dem-angebot-versenden)
  supports inspection of sent files. Exact save/send controls and history fields
  must be observed in the actual account; documentation alone is not UI acceptance.

No live account, credential, provider draft, finalization or email was used for
this implementation check. A supported API contract, local HTTP fixture and
browser handoff do not establish production compatibility or recipient delivery.
