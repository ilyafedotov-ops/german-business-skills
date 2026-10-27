---
name: de-business-operations
description: >-
  Handle daily work for a German sole trader: customer proposals, invoice preparation, payment follow-up, corrections, purchasing and business correspondence. Русский: предложение клиенту, счёт, оплата, переписка. Accounting postings belong to de-business-accounting; tax treatment and Finanzamt letters to de-business-tax.
---

# Business Operations

Read the [shared context and execution contract](../de-business-kit/references/shared-context.md)
on direct entry. This skill ships with the complete German Business Kit bundle;
shared resources remain in the sibling `de-business-kit` directory. Read only
references relevant to the task. Use the user's language and saved context.

Use [daily operations](../de-business-kit/references/operations.md) for the
customer-to-payment or purchasing journey. Identify which result is requested:
a draft, review, payment follow-up, correction or reply. Do not turn it into a
full month-close task.
For actual issue, invoice corrections, sending and delivery confirmation, use the
[invoicing workflow](../de-business-kit/references/invoicing-workflow.md). It combines
the chosen service route with protected local attempts and outcome evidence.
For an EU goods purchase, apply the [before-order and received-invoice VAT checks](../de-business-kit/references/international.md#before-ordering-goods-from-another-eu-country),
including the Kleinunternehmer branch, before suggesting VAT-ID use or recovery.
For an invoice/correction with a partial payment, use the
[saved customer payment reply](../de-business-kit/references/operations.md#save-and-resume-a-customer-payment-reply)
to distinguish invoice-stated prepayments from later receipts and save a resumable case.
For entering or editing a customer document in the chosen software, use
[assisted service operations](../de-business-kit/references/assisted-services.md).
A supported browser draft route can complement a read-only connector; do not
issue/finalize/send an invoice merely to save or preview it.

- Preserve agreed scope, evidence, dates, currency, recipient and document version.
  Unknown price, identifier, tax treatment or delivery fact stays unresolved.
- Research applicable invoice rules through current official sources before
  asserting completeness. Technical e-invoice validation is separate from a
  readable render; inspect actual structured data when supplied.
- Use [document authoring](../de-business-kit/references/document-authoring.md)
  for readable user/recipient outputs, and [payments](../de-business-kit/references/payments.md)
  for evidence-linked matches. A payment match does not post or settle a tax choice.
- Keep private notes separate from recipient documents. Prepare an exact outgoing
  draft and reuse applicable sending authorization; never infer sending from a file.
- For a disputed contract or debt, use [legal boundaries](../de-business-kit/references/legal-boundaries.md).
  Preserve a factual chronology; do not invent late fees, interest or legal claims.

Pass posting/reconciliation to `de-business-accounting` and unresolved tax
questions to `de-business-tax`, with only relevant evidence. Continue the
independent document work and report what is ready, blocked and next.
