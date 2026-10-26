# German Business Kit — local workspace interface

[English](README.md) | [Русский](README.ru.md)

This application opens a real private workspace. It is separate from the fictional
prototype. Keep the whole extracted application folder together. Start
`GermanBusinessKit.exe` on Windows or `GermanBusinessKit` on macOS. Your normal
browser opens the interface; keep the launcher running while you work. Closing the
launcher stops its local service. No Python, Node, account or cloud service needs
to be installed for the packaged application.

1. Choose English, Russian or German for navigation. Open an existing business
   workspace, or create one in a new/empty private folder outside the application
   and Git repositories. Changing navigation language does not rename folders.
2. Start with the task you want to work on. Home shows saved active tasks across
   months, including tasks without dates, their dependencies and evidence status.
   Continue with your assistant prepares a request to copy into your assistant;
   it does not open an AI session or mark the task complete. For a document task,
   add a small batch of PDF, XML, image or CSV documents (up to 30 files and 12 MiB
   per batch) and inspect the per-file results.
3. When the task involves accounting, choose where authoritative accounts are kept. Existing software remains
   authoritative; local entry posting requires an explicit local EÜR choice.
4. For document/accounting work, review documents, save unfinished forms as drafts,
   and record reviewed cash
   movements with their evidence. Correct posted entries using a reversal and
   linked replacement; previous records remain intact.
5. For a filing task, prepare versioned filing records. Check blockers before
   review/authorization.
   Record manual submission attempts, actual receipts and Finanzamt responses.
   The interface sends no return and calculates no statutory tax forms.
6. Use Settings to create/verify a full backup and restore only to a new folder.
   A restored workspace is not opened automatically. Open it explicitly to inspect
   the recovered result.

The browser communicates only with a session-protected service on your own
computer. No analytics, remote fonts or automatic AI calls are included. Business
form drafts are saved in the private workspace when you choose Save draft; browser
storage holds only session/preferences, not the accounting records. Save before
closing. A second tab changing the workspace invalidates old forms instead of
saving them into the wrong business folder.

Evidence is downloaded or previewed as text/images; untrusted HTML is not rendered
as part of the application. Technical validation messages and source evidence may
remain English/German. Generated report templates are English/Russian; German
navigation does not imply German tax calculations or a full German report set.

This is a release candidate until the corresponding platform checks and release
verification pass. Native Windows Authenticode signing and macOS notarization are
not supplied. Follow your device's policy if execution is blocked; do not disable
protections. Verify the exact published archive and its provenance before use.
A locally built binary is not a published signed release.
