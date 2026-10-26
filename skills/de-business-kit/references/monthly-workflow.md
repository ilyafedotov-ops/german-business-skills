# One month: local cash records and manual ELSTER

Use this recipe when the user chooses local cash records and manual ELSTER. It
does not establish eligibility for EÜR, a filing obligation, or the correct form.
Check those facts against the shared profile and current official sources using
[tax estimates](tax-estimates.md) and [forms](forms.md). Do not replace the user's
self-managed workflow with an accountant handoff.

The assistant performs supported local operations; the user should not edit JSON
or remember commands. Explain results in their language, retaining German form
names. Start with the saved workspace, month and next action, not a new intake.

## Minimum inputs and runtime

- Private workspace and selected month; inspect existing records first.
- Evidence for the chosen accounting method, activity and relevant accounts.
- Documents and bank/provider exports covering the intended scope. Record missing
  sources and unknown facts rather than assuming the month is complete.
- The user's supported manual ELSTER access; authentication stays with the user.

On Windows without Python, use native `windows.ps1` for start, folders, intake,
integrity and `-Action overview -Period YYYY-MM`, and [recovery](recovery.md) for
backup/restore. Native overview inspects saved state/evidence but does not perform
the full filing preflight or protected accounting mutations. If no approved
existing runtime can perform those mutations, prepare readable worksheets and
state the exact blocked step. Never emulate them by editing canonical JSON or
silently install Python. See [native Windows](native-windows.md).

## Work through the month

1. **Resume and protect.** Refresh the real overview and inspect unresolved
   submission attempts first. Create and verify a complete backup before a
   migration or first use of a new interface for changing real records.
2. **Organize and review.** Preserve original bytes; classify the documents,
   inspect extracted values against their source, and retain uncertain questions.
   Approval of a document or proposal does not post an accounting entry.
3. **Map payments.** Preview the original bank export; review date, sign, currency,
   account and transaction-ID mapping before accepting normalized records. Check
   fees, transfers and missing receipts explicitly.
4. **Record and reconcile.** Use the selected local journal's validated writer for
   reviewed cash movements. Export its per-account CSV and reconcile explicit
   transaction links with the normalized bank data. Correct through preserved
   reversals/replacements. Reconcile again after relevant changes.
5. **Read the report.** Produce the cash report and refreshed overview in the
   user's language. Explain missing evidence, account coverage, unresolved items
   and required statutory adjustments. A balanced CSV and cash total do not prove
   a complete period or provide a tax-form calculation.
6. **Prepare the applicable return.** Select the form/year using current official
   sources. Use a suitable official/provider calculation tool where needed;
   retain the actual inputs, output and review evidence. Do not invent a result,
   field mapping or tax formula. Preserve the exact filing version and source
   documents; run `filing-check` where supported. Resolve blockers by recording a
   new version, preserving the old one, rather than changing frozen evidence.
7. **Submit manually after approval.** Present the exact recipient, form, period,
   payload and unresolved limitations. The user reviews and authorizes that
   version, authenticates to ELSTER and performs the actual send. Record the
   attempt only when it actually starts. Do not click Send on the user's behalf
   unless separately authorized for that concrete action.
8. **Record the observed result.** Inspect and preserve the real transmission
   receipt and reference before recording `submitted`. A timeout or missing
   receipt remains `submission_unconfirmed`: investigate before retrying. Keep a
   subsequent Finanzamt response, its evidence and any sourced date separate
   from the receipt. No automatic reminder exists merely because a date is saved.

## Completion and interruption

Provide a readable summary of what is recorded, what remains open and the next
step. Refresh the overview after changes; it is a generated snapshot, not another
task register. Local overview checks grant no approval. Do not call the month
closed or the return accepted without the required evidence.

When interrupted, preserve completed records and exact draft versions. On resume,
read their current state and recheck evidence; never restart a send from memory.
If a capability is unavailable, identify the saved artifact and the manual step
that remains. A synthetic test of this recipe proves local state transitions,
not tax correctness, user usability or a live ELSTER connection.
