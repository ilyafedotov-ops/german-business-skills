# Resume a task across lifecycle stages

Use when a user asks to save progress, return later or continue a related task.
Read only the existing result, relevant task/question/decision entries and their
referenced evidence. Do not run a new welcome questionnaire or request an
accounting choice merely to reopen a formation plan or letter.

## With an existing workspace

1. Resolve folders and identity using [workspace](workspace.md). Inspect the
   relevant task by ID and its evidence health; reuse saved language and the
   explicitly chosen authoritative system. Do not infer facts from filenames.
2. Compare the result's source versions with current evidence. A changed original,
   new authority letter or revised user fact can invalidate a proposal or review.
   Preserve the old result and prepare a linked revision; do not silently rehash.
3. Identify the next actionable item. A supported explicit user request takes
   priority; otherwise use verified deadlines and dependencies. An unknown deadline
   needs verification, not an invented urgency ranking. A blocked field need not
   block independent factual preparation.
4. Use the existing `entry` writer with the inspected expected hash to update a
   task. Separate “prepare draft” from “send application” if the first can finish
   while the second remains open. Completion evidence must prove that task's own
   outcome. Reference question/decision IDs in notes where useful; `depends_on`
   accepts IDs in the same register only. A plan table is a view, not another queue.
5. Report the actual saved result, unresolved item and next action. Language or
   skill changes keep the same workspace, entrepreneur, authority and history.

If the writer is unavailable (including unsupported native-only operations),
preserve a readable continuation note without editing the registers directly.
State which task update was not saved. Existing overview described in the [monthly workflow](monthly-workflow.md) remains a
projection of canonical records and cannot discover promises hidden only in prose.

## Without a workspace

A saved draft or simple question does not require full workspace initialization.
Keep the relevant context in the conversation, or, when the user requests durable
files, save a versioned readable result outside Git/skill directories at the
chosen private location. A synthetic trial may use an isolated temporary folder.
Explain that a temporary location is not durable business storage.

End that result with: task and activity/period; confirmed facts and their sources;
exact output versions; unresolved questions; current external-action state;
existing authorization scope; one next step and the evidence it needs. Keep this
with the result rather than creating another profile or registry. On return, read
this note and new evidence, retain prior versions, and continue from the actual
state. Do not claim cross-session recall without an accessible saved result.

A due date or continuation note is not a scheduled notification. Use
[connections](connections.md) if the user requests actual reminders.
