# Choose where you keep your accounts

[English](accounting.md) | [Русский](accounting.ru.md) | [Documentation](index.md)

The welcome dialog establishes your accounting setup instead of choosing it for you. If you already use accounting software, identify the exact product and edition and continue using it as the authoritative system. If you want local records, the assistant explains the supported scope and collects the necessary accounting-method facts. You can postpone this decision and still organize documents or ask questions.

Your choice is saved and reused when you return. Choosing a system does not change your VAT treatment or rewrite business facts. Changing systems after records exist requires a separate migration; the assistant cannot silently start a second set of books.

| Route | What works now | What remains outside this implementation |
| --- | --- | --- |
| Local records | Reviewed cash movements for an explicitly selected EÜR workflow; split income/expense/transfer lines; duplicate checks; preserved reversals/corrections; period summaries and account CSVs for reconciliation | Complete statutory EÜR, double-entry accounting, asset/depreciation and other tax adjustments, official return calculations and transmission |
| Existing accounting software | Preserve authoritative exports and their evidence; prepare and track exact report versions, user approval, observed submission receipts and Finanzamt responses | A bundled provider connector, automatic retrieval/posting, or independent verification of the provider's books |

Try: “Help me choose where to keep my accounts during setup. If my existing software fits, continue from there.” Or: “Use the local cash records, show unresolved classifications, and reconcile them against my statement.”

## Period review

The local report separates recorded income, expenses, transfers and unresolved movements for each currency. Its cash difference is not taxable profit. An internal bank transfer or payment-provider payout must not become another sale. Reports also export one CSV per account for the existing reconciliation workflow. Original entries and corrections remain available; generated reports are snapshots, not locked books or proof that every transaction was supplied.

English/Russian Markdown reports and machine-readable JSON are saved together. Missing coverage and statutory calculations remain visible. The assistant must review the real reporting period's rules and form before preparing an actual return.

## Filing and Finanzamt follow-up

Either route can preserve a specific return draft and supporting evidence. Review and authorization are tied to that version. A changed payload or a changed underlying local JSON cash report blocks further preflight until a new version is prepared and reviewed.

The filing tracker records an uncertain attempt **before** a separately authorized external submission. It sends nothing. If the result is unclear, it blocks blind retry. After actual inspection, a retained transmission receipt and reference can support a locally recorded submitted status. A later Finanzamt letter is a separate record; receipt is not acceptance of tax treatment. The assistant can record a sourced deadline and create a follow-up task, but the tracker does not schedule reminders or calculate legal deadlines.

The exact commands and safeguards are in the [agent workflow](../skills/de-business-kit/references/accounting-workflow.md). [Integration research](../skills/de-business-kit/references/submission-integration-sources.md) explains ERiC prerequisites and the remaining transport/form-calculation gaps. These commands use the optional Python engine; the native Windows-only entry point does not yet implement them.
