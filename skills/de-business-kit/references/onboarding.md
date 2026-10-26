# Guided start, demonstration and recovery

User-facing guides ship inside the skill: [Russian start](../guides/start.ru.md), [English start](../guides/start.en.md), [German start](../guides/start.de.md), [Russian manual](../guides/user-guide.ru.md), [English manual](../guides/user-guide.en.md). Offer the relevant section when helpful; keep commands and technical references behind the conversation. A simple question does not require a demo or full setup. Existing workspace guides are not overwritten by an update.

For substantial setup/source-intake work, provide a readable outcome and next step under [readable output](readable-output.md). Do not make the user choose a technical format; use an available readable document by default and explain capability gaps only when relevant.

Use for first use, “help me set this up,” “continue,” or a confused user. Offer outcomes in the active language: **Prepare/start an activity**, **Handle a customer document**, **Organize records/reporting**, **Answer a question or letter**, **Choose/connect a service**, **Change/pause/close an activity**, **Continue my work**. Infer a clear choice from the request; do not force a mode menu. Keep the `tax-consultant` machine ID for existing workspaces; show the preparation-focused label.

If the user already has email, cloud/accounting records or a nonempty folder, follow [existing-data onboarding](existing-data.md) before proposing fresh setup. Inspect source access and existing workspace markers; do not initialize over the source or reset accounting/VAT history.

Only when the requested task needs accounting records, establish where the user wants to keep their accounts: an existing exact software product or local records. Do not choose a default or infer the accounting method from that decision. Follow [accounting workflow](accounting-workflow.md) to save the evidenced choice with `desk.py accounting-configure` and inspect it with `accounting-status` on resume. The user can defer this choice while intake/research continue. Existing external books remain authoritative; a local EÜR cash journal is limited preparation, not complete statutory accounting. Once records exist, changing the authoritative system requires a separately reviewed migration.

## First useful task

First distinguish a question, a document/form preparation, persistent record work
and an external action. For a question or preparation, use the relevant direct
skill and needed facts immediately. Steps involving a private folder/runtime
below apply only when files or persistent workspace operations are required.
Do not require accounting configuration for registration or a letter. For an
existing workspace, reuse identity, preferences and task history without restarting.

1. Identify whether the user means their own business or a service for others. For the latter, apply [legal boundaries](legal-boundaries.md). Ask/reuse the language, actual host and Windows/macOS environment. Inspect available tools; do not assume Python, web research or browser control from plugin installation.
2. Explain that the assistant can organize evidence, prepare drafts and research questions. Distinguish this from professional representation, an accounting system's confirmed postings, or a tax submission. Explain the specific limits relevant to the chosen task rather than reciting every warning.
3. Ask the user to choose/open a private local folder through the host's folder picker if available. Use a local folder session without Git or worktrees. Explain a detected sync location, unsupported symlink or access problem in plain language. Do not enable sync, grant broad permissions, or weaken host controls to get past setup.
4. On Windows, prefer the native `start` route in [native Windows](native-windows.md), then continue the processing assessment below. It uses the same records but does not implement the complete Python doctor/runtime-review writer. When using the optional Python engine, run `python3 <skill-directory>/scripts/workspace.py start --root <chosen-private-folder> --language en --mode general` using the chosen language/mode/year. Use the actual Windows Python launcher where appropriate. `start` creates only a new/empty directory or resumes an existing marker. Existing preferences win on resume; use `configure` only for an explicit preference change. Never retry a failed initialization by deleting the folder.
5. Read the returned status. `setup_incomplete` means structural setup is usable while data-processing assessment is outstanding; use public rules and synthetic or appropriately redacted data. `needs_attention` requires inspection of the listed issue, without reinitializing. `configured` means an assessment was recorded, not that the host is legally certified or all tasks are authorized. Check the assessment's current scope before real data.
6. Use [privacy](privacy.md) to identify what leaves the machine, which product/plan/tools process it, and where records/logs live. Prepare the assessment with source evidence; ask only for account facts that cannot be inspected. Never make the user certify compliance through a blanket checkbox. Record agreed factual settings with `runtime`; see [workspace contracts](workspace.md#runtime-review-and-diagnostics).
7. Offer a separate synthetic demonstration. On the native Windows route demonstrate preview/intake/verification/resume as described in [native Windows](native-windows.md); do not claim reconciliation was run. With the optional Python engine use `demo --root <new-private-demo-folder> --year <chosen-year> --language en|ru`. It imports two synthetic CSV originals, runs real reconciliation, and writes localized `START-HERE.md`. Show three matched groups and the EUR 12 unmatched outflow. Explain that an arithmetic match does not establish tax treatment. Keep demo and real work in different folders.
8. End with what is done, what needs attention, and one next action. On “continue,” use `start` and inspect only relevant tasks/questions/evidence. Preserve existing VAT history, mode, language, decisions and originals.

## Missing capabilities

If Python is unavailable, do not treat it as a failed installation or ask the user to install it by default. Use the native Windows route for supported local operations and host tools for research/worksheets. Explain only the specific advanced automation gap when encountered. Do not claim that a downloadable ZIP contains a bundled Python runtime. Host installation, subscription purchases and permissions are separate user choices; the skill cannot grant them. Never run an opaque remote installer or request account secrets.

If web access is unavailable, identify which consequential rule remains unverified and prepare conditional/factual work. If browser access is unavailable, prepare a field worksheet; do not simulate entry or submission. In Claude plugin installations the invocation may be namespaced; use the host's actual skill picker.

## Recovery

- On the native route run `verify` and inspect the existing records/lock without claiming a complete diagnostic assessment. With the optional Python engine run `doctor --root <workspace>` for local integrity, setup issues and lock visibility. It does not probe the app's browser or cloud permissions. Report the actual outcome in the active language; technical JSON is for the agent.
- For an existing or nonempty folder: reopen it, choose a new folder, or inspect its marker. Never clear it to make initialization succeed.
- For a lock: check the process/operation with the user or actual host tools. Do not remove another writer's lock. Only after establishing that no writer remains should an authorized recovery preserve and remove the stale lock.
- For altered originals or evidence: preserve both versions, identify what changed, restore from a trusted backup when appropriate, or create a linked correction. Do not update hashes merely to make a warning disappear.
- For malformed legacy records: keep the existing file and history, explain affected fields, and prepare a reviewed conversion to the documented format. `status` never silently migrates them. Profile corrections use `record`; register conversion needs a separately reviewed local edit because there was no old register schema.
- For updates: install/review a fresh skill package separately, close active writers, verify a synthetic example, and reopen the same private workspace. Do not initialize business data again. Avoid duplicate standalone and plugin installations.

Use the implemented [full backup and restore workflow](recovery.md). Backup verification is a separate operation: preserve a protected copy outside the source checkout, restore into a fresh private location, then run native `-Action verify` or the optional Python `doctor` and `verify` commands as available. Native verification does not replace the full Python diagnostics. Never delete originals or backups based only on folder age. This preview does not encrypt files or configure Windows ACLs.

## Folder language during setup

For a new workspace, use the user's chosen English, Russian or German language for physical folders and the start guide. `start` defaults to the localized layout in both engines. Explain the five everyday areas through that guide; do not ask users to classify mixed invoices before inspection. Existing workspace paths and folder language stay fixed on resume, even if conversation preferences change. Before ordinary file reads/writes, obtain `workspace.py folders --root <private-folder>` or native `-Action folders` and resolve stable logical references into actual paths. Never create a parallel English folder tree. German folder/guide support does not imply full German report/prototype translation.
