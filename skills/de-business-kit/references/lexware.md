# Work with Lexware Office

## Identify the product and available access

Ask whether the product is **Lexware Office** in the browser or an installed product such as **Lexware buchhaltung / financial office**. Do not reuse Office API assumptions for desktop products. Record the exact product, edition, adviser workflow and currently available access in `04_accounting/workflow.md` and the runtime register.

**Version 0.2 has no production Lexware connector.** These are preparation instructions and design constraints for a future adapter. Use supplied local utilities for evidence and reconciliation. Provide reviewed entry instructions or handoff files; never claim that this package uploaded, posted or submitted anything.

## Diagnose missing documents correctly

Distinguish document status from booking category:

| Lexware item | Meaning | Export consequence |
| --- | --- | --- |
| Status `Zu prüfen` or `Entwurf` | Not fully captured; no corresponding posting | Not exported |
| Category `Zu prüfen` | Captured with an interim-account posting | Included in export |

The documented interim accounts are **1590 (SKR03)** and **1370 (SKR04)**. Use this temporary category only within a treatment agreed with the tax adviser; it is not a universal correct expense category. Keep the unresolved question and required follow-up visible after export.

For a missing receipt:

1. Compare the document date with the selected export month. Lexware exports receipts by document date, independently of payment date.
2. Check the actual status and whether required capture fields and category were saved.
3. Check whether the document was captured after the export; inspect transfer logs and errors.
4. Check relevant bank allocations and the agreed division of work. Unassigned transactions can make a posting export incomplete.
5. Record the cause, evidence and next action in `06_bookkeeping/YYYY/MM/close.md` and the task register.

Do not infer that the adviser cannot see an uncaptured document anywhere. The adviser cockpit also provides access to the client's live Lexware view; live access and transfer into the adviser's own software are different workflows. Establish which view or transfer is missing the document.

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

## Required outputs

- `04_accounting/workflow.md`: product/edition, access, authoritative system, adviser responsibilities, export format and lock-on-export setting if known.
- `06_bookkeeping/YYYY/MM/proposals`: reviewed category/tax proposals and unresolved cases, without fabricated provider IDs.
- `06_bookkeeping/YYYY/MM/close.md`: receipt/export coverage and exceptions; distinguish local preparation from actual provider state.
- `07_exports/YYYY-MM`: handoff package with an inclusion/exclusion manifest and transfer evidence only when a transfer actually occurred.

## Official sources

Checked **2026-10-25**; product capabilities and plan conditions can change.

- [Product distinction: Lexware Office versus Lexware buchhaltung](https://shop.lexware.de/buchhaltungssoftware-vergleich).
- [Lexware Office Public API and plan eligibility](https://www.lexware.de/funktionen/public-api/).
- [API documentation: files, invoices, vouchers, payments and rate limits](https://developers.lexware.io/docs/).
- [Missing receipts: status versus category, document date and transfer checks](https://help.lexware.de/de-form/articles/548692-belege-fehlen-im-export-oder-wurden-nicht-ubertragen-ursachen-und-losungen).
- [Unassigned transactions and export troubleshooting](https://help.lexware.de/de-form/articles/548872-fehlermeldungen-und-probleme-beim-export-von-belegen-und-buchungsdaten-losen).
- [Adviser cockpit and access to the live client view](https://office.lexware.de/steuerberater/funktionen/steuerberater-cockpit/).
- [Adviser export configuration, including locking postings](https://steuerberater.help.lexware.de/de/articles/603461-export-der-daten-uber-den-steuerkanzlei-zugang).
