# Welcome wizard after installation

Run this when a new user has just installed the kit or asks to start, set up,
be welcomed or shown around, and has no concrete task yet. The conversation in
Claude Code, the Claude app or the Codex app is the interface; there is no
separate setup program. A concrete question or document comes first: help with
it, then offer the welcome in one sentence. Follow [onboarding](onboarding.md)
for the policies behind each step.

## How each step looks

- One step per message, one decision per step, in the user's language.
- Start the message with a short progress line, for example **Step 2 of 6 · Setup check**.
- Keep the text to a few lines, then the choices. Put the recommended choice
  first and mark it. Use the host's structured question tool when it has one
  (for example Claude Code's multiple-choice questions); otherwise show numbered
  options and accept a number or the user's own words.
- The user can say **skip**, **back**, **later** or **stop** at any point. Never
  repeat a question the user already answered, and skip a question whose answer
  is already clear from the conversation or the saved workspace. The Step 1
  opening text is never skipped: every first reply starts with it.
- Show plain words, never JSON, command output or internal IDs. Use ✓ for done,
  ! for something to know and ✗ for something that blocks the next step.

## Step 1 · Welcome

Never skip this step. Your first visible reply opens with this text in the
user's language, close to these words and as plain text, not a quotation. Text written before a tool call may not
be shown to the user, so put it in the reply that follows the setup check,
above the checklist:

> Welcome to German Business Kit. It helps you run a sole-trader business in
> Germany, from the first idea to invoices, accounting, tax and later changes,
> and keeps everything in one private folder. It is AI assistance, not
> professional tax advice, so check important results.

In Russian:

> Добро пожаловать в German Business Kit. Он помогает вести бизнес
> индивидуального предпринимателя в Германии: от первой идеи до счетов, учёта,
> налогов и последующих изменений, и хранит всё в одной личной папке. Это помощь
> ИИ, а не профессиональная налоговая консультация, поэтому проверяйте важные
> результаты.

In German:

> Willkommen bei German Business Kit. Es hilft Ihnen, als Einzelunternehmer in
> Deutschland von der ersten Idee über Rechnungen, Buchhaltung und Steuern bis zu
> späteren Änderungen zu arbeiten, und bewahrt alles in einem privaten Ordner auf.
> Es ist KI-Unterstützung, keine professionelle Steuerberatung; prüfen Sie
> wichtige Ergebnisse.

Then settle the language: English, Русский or Deutsch. When the user's message
already shows the language, do not ask; name it and offer the other two in one line.

## Step 2 · Setup check

Give the check a plain command description, such as "German Business Kit:
read-only setup check of this folder"; apps show it when they ask the user to
approve a command. Below the welcome, add one line: if the app asked to approve
the kit's local helper, that helper only reads this folder and contacts no
service. Run the read-only check on the current folder:

- Python: `python3 -I <skill-directory>/scripts/workspace.py setup-check --folder <current-folder>`
- Windows without Python: `windows.ps1 -Action setup-check -Root <current-folder>` (see [native Windows](native-windows.md))
- Neither: check with file tools that the seven `de-business-*` skill folders
  sit next to this one, look at the folder's contents, and say that the local
  helpers are unavailable, so saving records is limited.

Show a short checklist from the report: kit version and all seven skills; one
installation only; the local helper; the folder (empty, existing workspace,
holds files, or unsafe because it is inside a Git repository, the kit or a
synced cloud folder); web search if your own tools include it; and the model.
For the model, name the one you know you are running on only if the host shows
it, then give the [recommendation](shared-context.md#model-and-reasoning-recommendation)
without making it a requirement. When nothing is ✗, show the checklist in the same message as Step 3 so the user
does not spend a turn on it. For each ✗, give the exact fix in the user's
app and stop the wizard there: reinstall the complete kit, remove a second copy
after the user confirms which one, or choose another folder. Never install a
runtime, change settings or delete files to make a check pass.

## Step 3 · Your situation

Ask where the user stands, with these choices:

1. Planning to start a business in Germany
2. Already working as a sole trader
3. My records are in accounting software, email or folders
4. Just exploring with made-up details

This only chooses the next steps. Do not ask for accounting software, tax facts
or documents here.

## Step 4 · Your business folder

Offer choices that fit the setup check:

- **Empty or new folder:** use this folder (recommended), choose another one,
  or not now (questions only, nothing is saved).
- **Existing workspace:** continue it (recommended). Reopen it with `start`,
  never initialize again, and jump to the summary.
- **Folder with files:** keep these files as a source and create the workspace
  in a new empty folder (recommended), or not now. Preview the files later with
  [existing-data onboarding](existing-data.md); do not import yet.
- **Unsafe or unsupported folder:** explain why in one sentence; choose another
  folder or not now.
- **Exploring (situation 4):** offer a separate practice folder with the
  synthetic `demo` instead of a real workspace.

When the user chooses a folder, run `start` with the chosen language and the
`general` mode (use `bookkeeping` only when they asked for accounting help now),
then name the five visible folders and `START-HERE.md` in one line. The folder
list is in the [user guide](../guides/user-guide.en.md#your-folders).

## Step 5 · Your data

In three lines: files stay in the folder, but what the assistant reads is sent
to the AI provider; a synced folder may be less private; nothing is sent to an
authority or service without the user's explicit request. Ask:

1. Made-up details for now (recommended for a first try)
2. Real documents: then ask which app and plan they use, check what you can see
   yourself, and record only the agreed facts with the `runtime` writer as
   described in [privacy](privacy.md). Never ask for a blanket confirmation.

## Step 6 · First task

Offer three tasks that fit the situation, each in one line with what the user
gets, plus "something else". Examples: plan the first registration step,
prepare an invoice draft, sort this month's receipts, explain a letter from the
Finanzamt, try the practice demo. Start the chosen task with its skill.

## Finish

End with a short card: ✓ what is set up, ! what still needs attention, → the
one next action, and how to continue later: open the same folder and say
**"Use de-business-kit. Continue in this workspace."** When a workspace exists,
save open setup items (for example the data review) as one task with
`workspace.py entry`, so a later session can offer to finish the welcome. If the
user stops early, save that task with the steps still open, and say how to
resume.
