# Daily customer and purchasing work

Use the shared contract, [document authoring](document-authoring.md) and
[lifecycle sources](lifecycle-sources.md). Support preparation and available
verified actions; this reference does not implement invoicing software or debt collection.
For a multi-step customer case use the private [EN worksheet](../assets/en/customer-case.md)
or [RU worksheet](../assets/ru/customer-case.md) alongside recipient documents.
For an ordinary question or letter use [correspondence](correspondence.md).
The worksheet links actual records; it neither issues invoices nor replaces books.
For issue/correction and delivery execution, load the
[invoicing workflow](invoicing-workflow.md): inspect existing cases, prepare the
actual chosen-system operation, retain distinct attempts and record observed results.

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

Before an EU goods order, apply the [pre-order VAT check](international.md#before-ordering-goods-from-another-eu-country),
including the Kleinunternehmer ID-use election risk. If a VAT invoice has already
arrived, use the [received-invoice route](international.md#when-an-eu-goods-invoice-already-includes-vat).
Bring unresolved treatment to `de-business-tax` while continuing factual preparation.

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

## Save and resume a customer payment reply

For a supplied invoice/correction and payment query, prepare the factual reply
and a versioned private case worksheet in the existing customer correspondence
folder. Resolve its physical path through `folders`; reuse the chosen case and
authoritative system. Save useful local drafts under the existing authorization,
even when a settlement question prevents a definitive payment request.

1. Read the preserved originals and exact inspection reports. Keep gross,
   invoice-stated prepaid amount, rounding and invoice-stated amount due in
   separate rows with currency, source location and date. The inspector exposes
   optional `prepaid_amount` and `rounding_amount`; absent fields remain unknown
   source values, not observed zero payments. Old reports may lack these keys;
   inspect the original again into a new report when needed, preserving the old one.
2. Read explicit bank/payment references and distinguish receipts already included
   in the invoice's prepaid total from later receipts. An invoice's amount due is
   a document-time amount, not today's receivable. Do not subtract the same receipt
   again from an amount due that already includes it. Never identify payments by
   amount alone. If allocation or coverage is uncertain, show the alternatives as
   conditional and ask for the decisive reference/system record.
3. Treat a correction as a separate document with its own totals and relationship.
   Preserve its sign; do not automatically net it against the original balance or
   infer cash refund. Separate a proposed correction, an actually issued correction,
   customer acceptance/dispute and observed money movement. Reuse the chosen
   system's correction route; no new final number or shadow posting.
4. Calculate only the supported factual comparison with independently checked
   decimal arithmetic. Invoice total checks and a current settlement comparison
   are separate. State included/excluded receipts and the as-of date. No claim of
   complete balance, tax adjustment, default, fees or legal entitlement follows
   from matching arithmetic or XML extraction.
5. Save the recipient-language reply separately from the user's EN/RU private
   review, with the actual source/version links and one concrete next action.
   Inspect the saved output. Keep local paths, internal calculations and unresolved
   alternatives out of the recipient message unless relevant and intentionally
   expressed. A factual request for clarification can be prepared while the
   payment demand remains unresolved; delivery is a separate action.
6. On continuation, read the last worksheet and its sources before asking again.
   New payment or corrected allocation evidence requires a linked new worksheet
   and reply version. Preserve earlier reviewed/sent artifacts, reuse the existing
   open task through its writer, and identify exactly which conclusion changed.
   A Russian explanation or language switch does not change numbers or authority.
