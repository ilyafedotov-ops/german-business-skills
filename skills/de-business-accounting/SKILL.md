---
name: de-business-accounting
description: >-
  Review and organize German sole-trader receipts, bank/payment evidence, reconciliation, accounting entries and period close in the chosen system. Русский: бухгалтерия, документы, сверка, учёт за месяц. Tax interpretations/returns use de-business-tax; service selection uses de-business-services.
---

# Business Accounting

Read the [shared context and execution contract](../de-business-kit/references/shared-context.md)
on direct entry. This skill ships with the complete German Business Kit bundle;
shared resources remain in the sibling `de-business-kit` directory. Read only
references relevant to the task. Use the user's language and saved context.

Read [accounting workflow](../de-business-kit/references/accounting-workflow.md)
and reuse the saved authoritative system. If undecided, ask local versus exact
existing software only when accounting work requires it. No default, shadow ledger
or inference of EÜR eligibility from choosing local records.

For work in that software use [assisted service operations](../de-business-kit/references/assisted-services.md):
discover existing connectors and browser/desktop tools, inspect the chosen
account, and carry out the authorized draft/import/export scope. Verify side
effects and actual results; document a manual handoff for unsupported actions.
Ask `de-business-services` for access setup when needed, preserving this task.

1. Inspect the relevant period, originals and unresolved tasks through
   [document workflow](../de-business-kit/references/document-workflow.md) and
   [bookkeeping](../de-business-kit/references/bookkeeping.md).
   For a batch of receipts use [receipt-to-period preparation](../de-business-kit/references/bookkeeping.md#prepare-receipts-for-the-requested-period):
   preserve originals, separate cash/profit and VAT timing, save draft proposals
   and a readable review, and carry unresolved items into continuation.
2. Separate extraction, proposals, user review, actual posting and reconciliation.
   Use existing validated writers, locks, expected hashes and evidence. External
   books remain authoritative; inspect actual service state before claiming posting.
3. Use [payments](../de-business-kit/references/payments.md) for gross/fee/refund/
   payout reconciliation; do not treat a bank payout as additional revenue.
4. For local cash records follow [monthly workflow](../de-business-kit/references/monthly-workflow.md).
   Its cash arithmetic is not a statutory tax return. For year-end preparation use
   [annual workflow](../de-business-kit/references/annual-workflow.md).
5. For derived amounts and estimates use [source-led calculations and checks](../de-business-kit/references/tax-estimates.md).
   Confirm prerequisites, research applicable rules, execute reproducibly and
   independently check; ordinary totals do not establish tax treatment.
6. Produce a readable period summary with linked evidence, missing documents,
   unmatched payments and unresolved treatment. Preserve corrections and history.

Pass tax treatment, estimates, return preparation and authority letters to
`de-business-tax`; include the chosen system, period and input versions. An open
question must not be silently converted into a final category or completed month.
