# Invoice issue, correction and delivery

Use for actual invoicing work in the user's chosen system or established manual
process, together with [assisted services](assisted-services.md),
[document authoring](document-authoring.md) and [daily operations](operations.md).
The optional Python writer below protects local evidence and continuation. It
does not create a legal invoice, assign numbers, contact a provider or send mail.
Use available authorized host tools for those operations; use guided manual
execution when the tool cannot perform the exact operation. Do useful preparation
without installing a runtime or changing the chosen invoicing/accounting system.
For Lexware Office, use the [provider draft/readback and browser sending route](lexware.md#provider-invoice-draft-readback-and-sending).
Its opt-in API adapter creates an external draft; this local evidence writer alone
does not. Keep the provider attempt and invoice issue/delivery states separate.

## Prepare the concrete invoice or correction

Read existing case facts and inspect the actual system/account, customer, activity,
scope of supply, dates, price/currency, tax treatment and required format. Reuse
known facts and authorizations. Research missing tax/form requirements before
claiming completeness; an incomplete draft may still be saved. Do not finalize
merely to get a PDF, assign a parallel final number or infer issuance from a number.

For a correction, preserve the original issued artifact and exact provider ID.
Identify the requested effect: missing/incorrect particulars, amount reduction,
cancellation or replacement. Inspect current sent/locked/payment-allocation state
and the provider's supported route before choosing the action. A provider's
"Gutschrift" label, statutory self-billing, refund and actual cash movement are
different concepts. A linked correction need not always cancel/reissue the whole
invoice; its permitted form depends on the transaction and applicable transition.
See [dated sources and provider limits](assisted-services-sources.md#invoice-correction-and-delivery-check--2026-10-27).

Prepare exact fields/files in the authorized draft, read them back, inspect the
exported artifact and save a separate private review. Record checks of customer,
amounts, dates, tax/format, correction relationship and material side effects in
the review evidence. If a cancellation unlinks payments or reverses a booking,
include those effects in the concrete action scope. No local status grants that
authority or changes the actual books.

## Protected local records

The assistant uses `scripts/desk.py` from the shared core. Resolve the workspace
with `workspace.py folders`; input/evidence paths are inside that workspace.
Inspect `invoice-list` without a period filter before creating a case or resuming
an uncertain attempt. It includes all invoice periods; the general GUI/native
overview does not display this new lifecycle. Keep a linked open task in the
existing task register, backed by a saved readable status and case note.

| Command | Purpose |
| --- | --- |
| `invoice-template --kind invoice` | Input contract for an immutable draft |
| `invoice-create --root <private> --input <relative-json>` | Freeze draft and source files |
| `invoice-template --kind action` | Exact action contract; unused optional fields stay null/empty |
| `invoice-show --root <private> --id <id> --language en` | Current record/hash, preflight issues, allowed actions and readable status |
| `invoice-action --root <private> --input <relative-json> --expected-sha256 <inspected-hash>` | Protected evidence transition |
| `invoice-list --root <private> --language ru` | All-period continuation, including unknown outcomes |
| `invoice-report --root <private> --id <id> --language en` | New private Markdown status with evidence history |

A draft records `invoice_id`, stable `business_reference`, organizational `period`,
issuing `system` and `account_reference`, `customer_reference`, `currency`,
`document_file`, 1–64 `source_files`, `unresolved_items`, optional `corrects`,
`correction_kind` and `replaces`. Sources must include the chosen system/account
and business facts; keep an existing accounting choice authoritative. An explicitly
different invoicing service can coexist with accounting; document that choice.
Do not require unrelated EÜR onboarding. Unknown facts belong in unresolved items.

`business_reference` identifies the same business operation across attempts and
draft replacements. Do not invent another reference to bypass an uncertain result.
For an erroneous unissued draft, `cancel` locally, then create `replaces=<old-id>`
with the same business reference and corrected facts. This resets review/authority
and preserves history. Local cancel does not cancel anything at the provider.

An issued correction uses `corrects=<issued-id>` and `correction_kind`:
`amendment`, `amount_credit`, `cancellation` or `replacement`. This bounded writer
requires the same system/account, customer and currency; wrong-recipient/currency
corrections need the actual provider's separately reviewed process. Competing
unfinished corrections and uncertain original delivery block new correction work.
The original record stays preserved; the correction does not silently rewrite it.

## Issue or record an existing result

1. `review-issue` records actual review evidence; `authorize-issue` records the
   existing matching authorization for this exact issue/correction scope. The
   actor and evidence are operator-supplied records, not authenticated identity.
2. Immediately before the external action, `begin-issue` freezes an attempt ID
   and makes the outcome `issue_unconfirmed`. Use the selected host tool or have
   the user perform the exact reviewed operation. The CLI itself does nothing
   externally. For a correction, "issue" here means the selected correction action,
   including a provider cancellation that creates no separately numbered invoice.
3. Read back actual provider state and export the resulting recipient artifact.
   `confirm-issued` requires that attempt ID, actual `external_id`, `invoice_number`,
   `document_file`, evidence, actor, note and observed date. Keep the original draft
   AND actual issued bytes: final numbering/rendering may legitimately differ.
   Review any material difference before delivery. Amendments/cancellations may
   reuse the original identifiers or have null `invoice_number` when none was
   assigned; never invent one. The resulting `issued` state on a correction means
   its observed completed outcome, not an extra invoice or automatic posting.
4. After a timeout, query the authoritative object/history. Missing search results
   or generic errors do not prove failure. Keep unknown results open; never repeat
   creation/finalization/cancellation automatically. `confirm-not-issued` requires
   affirmative evidence and `outcome_kind=confirmed_not_issued`; retry then needs
   fresh review/authorization and a new attempt. Late results cannot resolve a
   different attempt. Safe reads/downloads are separate from consequential retries.

For an already issued invoice/correction supplied from outside this workflow,
create its evidence draft and use `adopt-issued` with the actual artifact/reference
and readback evidence. It records history without fabricating an earlier approval
or local attempt. A supplied document alone does not prove issue state: retain its
authoritative provenance and any limits in the note. Both outcome routes require
inspection; the utility does not verify the truth of operator-supplied evidence.

## Review, send and confirm delivery

`review-delivery` records review of the ACTUAL final issued artifact, required
format, exact `recipient={channel,address}` and optional `attachment_files` (up to
32). Channels are `email`, `portal`, `post`, `other`; the address is the precise
destination/account/address for that route, not an inferred customer email.
Only intentional recipient files go in the package. Private review notes stay out.
Review correction history and whether sending an historical document is still
appropriate. A recorded cancellation/replacement blocks sending its original;
new parent/sibling corrections invalidate previous delivery review/authorization.

`authorize-delivery` records authority for these exact frozen bytes and destination.
Use the frozen package, not a regenerated attachment or changed working file.
`begin-delivery` records a new attempt before the external send/share/post action.
Use the actual supported route; record readback, not a success guess:

| Action | Evidence and meaning |
| --- | --- |
| `confirm-dispatched` | Active `attempt_id` + actual `external_id` correlation reference + dispatch evidence; not customer receipt |
| `confirm-delivered` | Same attempt/reference + `outcome_kind=delivery_receipt` or `recipient_acknowledgement` + inspected receipt evidence identifying the document/destination; not agreement or payment |
| `confirm-delivery-failed` | Same attempt/reference + affirmative `confirmed_not_dispatched` for an uncertain attempt, or `delivery_failure` after dispatch (for example a bounce); preserve earlier dispatch history |

A sent-folder entry, provider "Gesendet", file download or share-link creation is
not delivery confirmation. If receipt evidence is unavailable, leave `dispatched`
or `delivery_unconfirmed` visible. After confirmed failure, review destination and
files again and obtain/reuse authority that actually covers the retry. Changing a
recipient requires a new delivery review and authorization. No blanket resend
from a timeout, silence or absence of a read receipt is supported.

If the user already sent the issued artifact outside this workflow, use
`adopt-dispatched` with its actual recipient, sent attachment files, observed date,
dispatch reference and evidence. It creates an `observed-...` attempt reference
without inventing an earlier local review, authorization or begin event. Later
receipt/failure observations target that reference. It cannot replace an existing
uncertain attempt; resolve that attempt instead. This records a past fact, never
authorizes a new send or proves customer receipt.

## Compare an issued invoice with customer receipts

After issue/delivery, use the existing private bank export and invoice evidence
to prepare a factual payment comparison. Keep Lexware or the user's other chosen
system authoritative. This route saves an actual EN/RU report and frozen inputs;
it does not allocate a payment, mark an invoice paid or send a reminder.

The optional Python commands in `desk.py` are:

| Command | Purpose |
| --- | --- |
| `invoice-payment-template` | Input contract for a comparison |
| `invoice-payment-prepare --root <private> --input <relative-json> --expected-sha256 <invoice-hash> --language en` | Save a new immutable comparison and readable report |
| `invoice-payment-check --root <private> --report <saved-json>` | Verify report/artifact integrity, working-source freshness and invoice/correction context before reuse |

1. Reuse the issued record from `invoice-show`; inspect its frozen final document.
   Record the **invoice-stated amount due**, already accounting for stated prepaid
   amounts and rounding, as `amount_due`. This is a reviewed input, not an amount
   the utility extracts or a provider's current balance. Save `review_file` naming
   the exact document/field, account, receipt references, inclusion decisions and
   coverage through `as_of`; record `reviewer` and `bank_account` without secrets.
2. Supply one account's normalized CSV as `bank_file`, with
   `transaction_id,booking_date,amount,currency` (ISO dates, signed dot decimals).
   Reuse the existing reviewed bank-import route if normalization is needed.
   Export dates may span periods. Never infer an invoice match from equal amounts.
3. Each selected `payments` item contains `transaction_id`, signed `amount`,
   `treatment` and `evidence_file` supporting the invoice allocation. A partial
   amount must fit inside that bank movement. Duplicate/missing IDs and wrong
   signs are refused. This is a comparison of selected amounts, not a reservation
   of those funds against other invoices or a check of all account allocations.
4. Use `included_prepaid` for receipts already included in the stated amount due;
   they are not subtracted again. `later_receipt` and `later_refund` mean movements
   **not included in that document amount**, not merely a booking-date ordering.
   Refunds are signed negative. Use `uncertain` when the relationship is unresolved.
   Set `coverage_confirmed=true` only after checking all relevant receipts and
   refunds through `as_of`, including other accounts where applicable. A single
   supplied CSV does not itself establish complete coverage.
5. The calculation is stated due minus selected later receipts/refunds. Uncertain
   allocation, currency mismatch, future selected transactions, unconfirmed
   coverage, an as-of date before recorded issuance, or a noncancelled correction
   in the invoice family leave the remainder
   unresolved. Inspect the authoritative system to resolve correction effects;
   never net correction totals automatically. A zero difference, including a
   zero-value test invoice with no receipts, is not payment evidence.
6. Inspect the actual saved Markdown and retain its JSON/evidence snapshots. Before
   resuming, run `invoice-payment-check`: `current` means unchanged inputs/context,
   not correct allocations or a settled invoice; inspect `comparison_issues` too.
   Changed working inputs or invoice/correction history require a new report.
   Preserve previous reports. Corrupted frozen evidence fails closed. Outputs are
   private reviews; prepare any customer reply separately under
   [payment follow-up](operations.md#save-and-resume-a-customer-payment-reply).

If Python is unavailable, perform and save the same source-led comparison with
available host tools; do not claim these protected checks were executed or require
a runtime installation. This route needs no API key, provider upgrade or bank write.

## Prepare a customer payment follow-up

Use the saved comparison to prepare a neutral customer query, with its private
review kept separate. This optional Python route writes actual recipient text in
German, English or Russian, an EN/RU private review, frozen input/review evidence
and an audit-bound manifest. It neither sends nor changes provider/payment state.

| Command in `desk.py` | Purpose |
| --- | --- |
| `payment-followup-template` | Request fields for a new draft |
| `payment-followup-prepare --root <private> --input <relative-json> --expected-sha256 <comparison-hash> --language en` | Save a new recipient draft and separate private review |
| `payment-followup-check --root <private> --report <manifest-json>` | Check the exact saved files and underlying comparison before reuse |

Run `invoice-payment-check` first and use its `report_sha256`. Fill
`comparison_file`, `mode`, `recipient={channel:"email",address:<exact destination>}`,
`customer_name`, `sender_name`, `recipient_language` (`de`, `en`, `ru`),
`prepared_on` and a separate `review_file`. The review must support the destination,
customer/invoice identity, names/signature, inclusion facts and requested wording.
These are operator-supplied reviewed facts, not authenticated customer identity.
Recipient and private-review languages are independent.

- `balance_query` requires a current, positive comparison with no unresolved
  comparison issues. Its text asks about an unexplained difference; it makes no
  assertion of overdue debt or legal entitlement and adds no fee or deadline.
- `clarification` omits all amounts and asks which payments relate to the invoice.
  Use it when coverage, allocation, currency or corrections remain unresolved,
  or when a zero/negative comparison needs clarification rather than a demand.
  Stale inputs are blocked for both modes: prepare a fresh comparison first.

Inspect the actual `recipient_path` and `review_path`. Only the recipient text is
customer material; never attach the private review, manifest, statement or source
snapshots. The template body includes only invoice number, customer/sender names,
and, for a balance query, comparison date/difference/currency. Check that the supplied
names and invoice number are themselves suitable for the recipient. No account,
receipt IDs, local paths, source notes or hashes are copied into the message.

Before external delivery, run `payment-followup-check`, inspect `current` and
`comparison_issues`, and review the exact destination/text under the user's
authorization. `delivery_state=not_sent` means this preparation workflow has not
sent anything; it does not inspect an external mailbox. There is no automated
dispatch/receipt tracking for these letters. Preserve actual later dispatch/receipt
evidence separately using the existing correspondence/task workflow. Do not use
invoice-delivery actions to claim this letter was delivered.

Each preparation creates a new version. Changed input, review, comparison or invoice
history invalidates reuse; corrupted frozen evidence or edited recipient/review
artifacts fail closed. Revise inputs and create a new version, preserving the old
files. If the runtime is unavailable, prepare the same separate files with available
host tools and state which protected checks were not executed.

## Save and resume

Every action needs `actor`, `evidence_file`, `note`, `occurred_on` and the freshly
inspected record hash. Evidence is copied into immutable snapshots; working-file
drift blocks issue preparation but does not prevent recording what happened after
an attempt started. Corrupt frozen evidence blocks transitions. Preserve partial
files after interruption; the shared lock/checkpoints are not a database transaction.
The mutable register is not acceptable as evidence for itself or another task.

Save `invoice-report` and the private case note, then update the existing task via
its writer. Separate "prepare", "issue", "dispatch" and "confirm receipt" tasks
when their outcomes differ. On return, read `invoice-list`/`invoice-show` and the
evidence before acting; a previously exported status can be stale. Retain earlier
recipient artifacts, reviewed versions, attempts, receipts and corrections.
If Python/protected writers are unavailable, save a readable continuation without
editing the register directly or claiming protected status. Standalone native
Windows and the current GUI have no invoicing controls for this module.
