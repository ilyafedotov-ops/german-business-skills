# Daily customer and purchasing work

Use the shared contract, [document authoring](document-authoring.md) and
[lifecycle sources](lifecycle-sources.md). Support preparation and available
verified actions; this reference does not implement invoicing software or debt collection.
For a multi-step customer case use the private [EN worksheet](../assets/en/customer-case.md)
or [RU worksheet](../assets/ru/customer-case.md) alongside recipient documents.
For an ordinary question or letter use [correspondence](correspondence.md).
The worksheet links actual records; it neither issues invoices nor replaces books.

## Customer request to payment

1. Establish the requested outcome, customer and activity, agreed scope, actual
   performance, relevant dates, price/currency and existing document versions.
   Ask for decisive missing facts; do not invent a contract or delivered work.
2. Prepare a proposal or invoice draft using confirmed terms. Before calling an
   invoice complete, verify the applicable current rules, tax treatment, recipient
   and format. Send unresolved VAT/exemption/reverse-charge questions to the tax
   skill. Continue a factual draft without implying that it is ready to issue.
3. Use the selected authoritative invoicing/accounting system where it exists.
   Inspect its actual numbering and correction behavior; do not assign a parallel
   final invoice number. A local preview is a draft until that system or a reviewed
   actual process issues it. Preserve issued versions and original structured data.
4. Produce separate user-language review notes and the recipient document. Inspect
   the actual exported format; a PDF view is not an e-invoice validation. Reuse
   existing sending authorization only for the exact reviewed document/recipient.
5. Record actual delivery outcome separately from preparation. Match later payments
   using [payments](payments.md) and explicit evidence. Partial payments, refunds,
   fees and disputed amounts remain visible; do not mark paid from a filename.
6. For a correction, preserve the earlier issued document and link the replacement
   through the chosen system's supported process. The accounting skill handles
   actual postings/reversals; a new letter does not alter the ledger.

## Unpaid or disputed invoice

Inspect agreed terms, performance, delivery evidence, amounts actually received,
previous reminders and the customer's stated dispute. Recheck legal grounds before
asserting default, a deadline, interest, fees or enforceability. Do not supply
formula-based penalties from memory. Use [legal boundaries](legal-boundaries.md)
for disputed claims. Prepare a factual, reviewable reminder or clarification and
its next action; do not threaten proceedings or send it without matching authority.

## Purchasing and expenses

Keep order/contract, delivery, invoice, payment and potential refund distinct.
Preserve original documents; prepare receipt proposals and explicit payment links.
Question missing business purpose, mixed use, currencies or tax treatment rather
than forcing a category. Accounting approval and posting belong to the accounting
workflow; contractual acceptance, cancellation and payment are separate actions.

## Completion and continuation

Deliver the document or factual result, its status, unresolved items and the next
step. Save only necessary task/evidence references in an existing workspace;
respect [privacy](privacy.md). A question or draft does not require creating a
workspace, running month-close or buying invoicing software.

## Supplied correction XML and payment evidence

When the user supplies an issued document and later correction, preserve both
originals and inspect standalone XML through [document workflow](document-workflow.md).
The inspector recognizes UBL CreditNote and selected UBL/CII preceding-invoice
references; it does not issue, validate or post a correction. A positive or negative
CreditNote amount stays exactly as supplied. See [source bindings](correction-xml-sources.md).

Compare the reference ID/date with actual originals, seller/customer, currency and
available authoritative-system evidence. A matching number alone is insufficient
when multiple issuers or periods can share it. Missing/duplicate/malformed references
remain unresolved. Save an explicit reviewed `corrects` relation through the
catalog writer only after establishing which preserved original it concerns.
Keep the document's overall review state unresolved while tax/format questions remain.

Link actual payment evidence separately using the existing catalog payment references
and the preserved bank original. `payment_refs` are evidence pointers, not a
verified balance calculation. Do not populate `dates.paid` from a partial receipt,
a credit-note issue date or an inferred net balance. A CreditNote is not proof of
cash refund, customer agreement or resolved dispute. Preserve earlier drafts,
write a new readable case summary, and keep a sourced follow-up task for settlement
or correction questions. Resume it using [continuation](continuation.md), with the
chosen external system still authoritative and without local shadow postings.
