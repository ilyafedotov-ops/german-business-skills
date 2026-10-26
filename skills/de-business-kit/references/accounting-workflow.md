# Accounting choice, cash records and filing evidence

During welcome/onboarding, establish the authoritative accounting route from the user's existing setup and intended work. Do not preselect local accounting or a vendor. Reuse an explicit existing choice. Ask one practical question: **Do you already keep your accounts in software, or do you want to maintain local records here?** Identify the exact product/edition if external. Explain the relevant capability limits before the user chooses.

This is independent of conversation mode, language, accounting method and VAT treatment. Do not infer EÜR eligibility from a local choice. A user can defer the choice and continue intake, research and document review. Read `desk.py accounting-status` on resume. It returns `undecided` without creating a record when no choice exists. After a choice, use `accounting-configure` with preserved evidence of the user's instruction; never invent consent. Existing software remains authoritative on the external route and `entry-post` is blocked. A choice cannot be switched after cash/filing records exist: prepare a separately reviewed migration instead of creating parallel books.

## One command interface

All commands use `scripts/desk.py`. Input and evidence paths are relative to the private workspace. The assistant prepares JSON behind the conversation; the user need not edit it. Use `accounting-template --kind configuration|entry|filing|filing-action` to obtain the exact current contract.

| Command | Purpose |
| --- | --- |
| `accounting-status --root <private>` | Saved route, configuration hash, entry count, filing states and unavailable capabilities |
| `accounting-configure --root <private> --input <choice.json>` | Record local/external, exact product where relevant, account alias, method, reviewer and evidence |
| `entry-post --root <private> --input <entry.json>` | Record an explicitly reviewed local cash movement with split lines and evidence |
| `entry-reverse --root <private> --entry-id <id> --reversal-id <new-id> --evidence <file> --actor <reviewer> --note <reason>` | Preserve the original and add an equal opposite correction on its original date |
| `period-report --root <private> --period YYYY[-MM or -Qn]` | Unique JSON, localized Markdown and account-specific CSV for reconciliation |
| `filing-create --root <private> --input <draft.json>` | Freeze a report/portal-summary version and supporting sources for either accounting route |
| `filing-show --root <private> --id <id>` | Inspect frozen record and its current hash |
| `filing-action --root <private> --input <action.json> --expected-sha256 <current-hash>` | Record the next evidenced review, authorization or observed result |

Updating a configuration before records exist also needs `--expected-sha256` from `accounting-status`. No source-account credentials belong in `account_reference`, product names, evidence or command arguments. An account alias identifies the business/accounting context; it is not an authentication token. One workspace still belongs to one entrepreneur.

## Local cash records: supported boundary

Local writes require an explicitly selected `local` / `EÜR` workflow and no conflicting known profile method. This records a workflow choice, not a legal determination that the person qualifies. The configuration does not rewrite profile facts. `Bilanzierung` and unresolved methods do not enable this cash journal.

Each entry has a stable ID, payment date, account alias, source transaction ID, signed decimal amount, currency, reviewed split lines, reviewer, reason and a preserved evidence file. Account aliases are normalized to lower case; native transaction IDs retain their exact case. Evidence should link the bank/payment source and supporting original documents. The writer verifies the evidence bytes and split sum; it cannot verify the truth of a human-supplied category or retrieve missing source records. Use `unresolved` for unsettled classification instead of guessing.

Split lines use `income`, `expense`, `transfer` or `unresolved`, plus an explicit category and activity reference. Positive means inflow; negative means outflow. Refunds can reverse the sign of an income/expense category. Internal account transfers and PSP payouts are movements of existing funds, not a second sale; retain both account legs. Use specific category text to distinguish owner contributions/drawings, loans/principal and internal transfers; do not infer tax treatment from the broad movement kind. Activity references are textual, not a fully validated activity registry.

Example: a sale `100.00`, fee `-3.00`, PSP payout `-97.00` and receiving bank transfer `97.00` produce recorded income `100.00`, expenses `-3.00`, transfer net `0.00` and operating cash difference `97.00`. The payout must not create another `97.00` income entry. Keep USD and EUR totals separate; no exchange rate is invented.

An account/transaction pair cannot be posted twice. Correct it by reversing the original and creating a new entry with `replaces` pointing to the reversed entry. Originals remain unchanged, each original can be reversed once, and a correction retains account/transaction/currency. Reversal on the original date restates that period's cash report; it is a correction of recorded data, not a claimed current-period statutory adjustment. Reports are versioned snapshots, not locked/closed books. Reconcile the generated account CSV against an independent statement through `workspace.py reconcile`.

Reports always retain `needs_review` / `not_calculated`: account coverage, year-end timing, assets/depreciation, private-use adjustments, VAT, deductibility and official form mappings are not solved by cash arithmetic. Do not call `operating_cash_net` taxable profit or a complete EÜR. See [official-source research](submission-integration-sources.md). The report contains entry/configuration fingerprints; a filing that uses its JSON as source evidence cannot pass review/authorization/attempt preflight after the underlying entries change. Supply the machine-readable JSON alongside human-readable versions to retain that check.

## Filing lifecycle for either route

The user can prepare the real return in their existing accounting software or official portal. Follow [source-led estimates and report checks](tax-estimates.md) to find the current calculation rules and appropriate tool; local accounting does not authorize inventing a tax formula. Save the exact reviewed export/summary and relevant source files. A filing draft names form, observed version, period, actual recipient, unresolved items and optional `supersedes`. The tool copies the payload and sources into `05_tax/YYYY/filing-evidence/`; it does not generate an ERiC payload or validate official fields. Never use an incomplete cash report as a submission-ready tax return.

Use `workflows.py catalog` or [the form catalogue](../assets/form-catalog.json) for the machine `form` ID: for example `ustva` for Umsatzsteuer-Voranmeldung, `ust` for annual VAT and `euer` for Anlage EÜR. Keep the German display label in user-facing explanations, not in the `form` field. The catalogue is routing information, not proof of the obligation or an inspected current schema.

1. Create a `draft`; all material unresolved items must be settled in a replacement before review.
2. `review` records inspected content and recipient/form/period against the frozen version. It is not official technical validation.
3. `authorize` records an actual user instruction covering that exact version, account, recipient and operation. Do not fabricate authorization evidence. This command records authorization; it grants no external tool permissions.
4. Immediately before a separately authorized manual/provider submission, use `begin` to record `submission_unconfirmed`. This **does not send anything**. Preserve this state after a timeout/crash; do not blindly resubmit.
5. `receipt` records an inspected transmission reference plus preserved portal/provider receipt evidence and changes the local record to `submitted`. The tool validates file integrity, not receipt authenticity or server state. Use it only after real readback. If evidence instead establishes that no transmission occurred, use `not-submitted`; it returns to `reviewed`, retaining the attempt and requiring fresh authorization before another attempt.
6. `response` appends an observed acknowledgement, information request, assessment, rejection or other letter to the submitted record. A sourced `due_date` may be recorded with the response evidence and explanatory note. It is not calculated automatically and creates no reminder. Use the existing task register for follow-up actions/reminders. An authority response never silently changes the record into “tax treatment accepted.”

Each action requires actor, preserved evidence and explanatory note. Use the note to record observed dates, receipt origin, checked reference and deadline basis; `recorded_at` only records when this utility saved the event. Names are supplied metadata, not authenticated signatures. No evidence from the mutable accounting register is accepted.

`cancel` is allowed only before an attempted submission. It cannot erase an uncertain result. A changed report or correction needs a new linked draft and new review/authorization; it cannot bypass an unresolved attempt for the same account/form/period. Preserve source JSON files for preflight: original payload/source fingerprints must still match before review, authorization and attempt. Afterwards, receipt/response recording uses the frozen copies, so later accounting work does not prevent saving the outcome of an earlier submission.

## Storage, recovery and unavailable integrations

`04_accounting/register.json` is additive; existing workspaces are not reinitialized or automatically migrated. Shared locks, expected hashes and snapshots coordinate writers. The register checksum is checked against its latest audited history checkpoint to detect a missing file or isolated rollback. It is not a digital signature or protection against replacing the whole workspace/history. A mismatch or interrupted multi-file write requires inspection and recovery; never delete state or rewrite hashes to make an attempted filing look new.

The Python engine is required for these validated commands. On the native Windows-only path, continue evidence gathering and supported existing-software work; do not substitute manual register edits or install dependencies implicitly.

No banking/provider API adapter, ERiC library, certificate management, tax-form calculation engine or live submission is bundled. Official developer access, current SDK/interface/licence review and test-environment acceptance are still required for a future transport. This local workflow prepares and records work; it is not evidence that an external action occurred merely because a command returned success.
