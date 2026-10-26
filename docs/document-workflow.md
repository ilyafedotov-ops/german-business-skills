# Your documents, bookkeeping and tax reporting

[English](document-workflow.md) | [Русский](document-workflow.ru.md) | [Documentation](index.md)

The main workflow is managing your own accounts and tax reporting. You can use Codex or Claude to organize documents, review proposed treatment, reconcile supplied records and prepare tax worksheets without editing JSON. Accountant consultation and sharing an archive are optional.

**This preview is not yet a complete accounting system.** It has a limited reviewed local cash journal and filing-evidence tracker, alongside document preparation and reconciliation. Complete statutory accounting and ELSTER transmission remain unfinished. Use the chosen local or external accounting route. Reviewing a proposal does not post it; preparing a form does not file it; a receipt does not establish the Finanzamt’s substantive decision.

## Start with your task

> I manage my accounting myself. Organize these documents for October 2026, preserve the originals, show what needs review and help me prepare my own accounting and tax reporting. Use my existing workspace. Do not submit anything.

For a first workspace, follow [quickstart](quickstart.md). Choose a private directory outside the project and other Git repositories. The assistant checks actual tools and data processing before using personal data. Windows can perform intake, integrity, real overview and full recovery through native tools without Python. Advanced protected writes and casework operations use an already available supported Python runtime; otherwise identify the specific blocked step. See [runtime limits](project-status.md).

1. **Organize the documents.** Supply the chosen files and period. Invoices, bank statements, contracts, registration receipts and authority letters receive readable catalog entries. A document may appear in several views while its original stays unchanged. Identical files are not stored repeatedly, but repeated receipt is recorded. Possible business duplicates and corrections need review.
2. **Review facts and treatment.** The assistant shows amounts, dates, source locations, uncertainties and proposed categories. You can correct or approve through the conversation. Original wording and earlier decisions remain traceable. XML inspection extracts a limited set of candidate fields; it does not certify an e-invoice. Embedded PDF XML and OCR require separate tools.
3. **Review the bank mapping.** Check the source columns, date format, decimal commas, signs, currencies and sample rows before normalization. Reconciliation uses explicit links to your actual accounting records. If those records are missing, the assistant must report that gap, not create a matching ledger from the statement and call it reconciled.
4. **Open the real overview.** Ask “Show my October overview.” The assistant returns the actual localized file path. Python creates `overview.html`/`.md`/`.json`; native Windows creates separate `native-overview.*` files under the mapped admin directory. They show open questions, accounting choice, period entries, saved filings and the next action. Python includes full local filing preflight; native output inspects saved state and hashes only. Unknown submission outcomes and dated authority responses stay visible across months. Ask to refresh after changes; editing a page does not update records. This is separate from the synthetic interactive prototype.
5. **Continue your accounting and reporting.** Review remaining treatment questions, actual postings and applicable form worksheets. Keep preparation, your approval, actual submission evidence and the Finanzamt's response separate. A stated letter date is not automatically a verified legal deadline.
6. **Resume later.** Say “Continue my October bookkeeping from this workspace.” Saved records remain the source of truth; the assistant should not repeat setup or invent previous approvals.

## Optional archive

Ask for an archive only when useful for your own records or later consultation. It contains selected originals, linked records, evidence, unresolved questions and an inclusion/exclusion manifest. The assistant checks the directory and ZIP against the manifest. `prepared_with_open_items` means unresolved work remains; `prepared_for_self_review` concerns the selected snapshot only. Neither status means accounts closed or taxes filed. This is not a full backup or DATEV export. Sending it to anyone requires a separate instruction.

## What still needs implementation

The [core capability plan](core-capabilities.md) defines the remaining ledger and ELSTER work and the evidence needed before claiming support. Updated [validation notes](validation.md) distinguish local utility tests, browser rendering and native desktop acceptance. For exact record/command contracts see the [portable workflow reference](../skills/de-business-kit/references/document-workflow.md).
