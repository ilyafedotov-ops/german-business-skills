# Guided start, demonstration and recovery

Use for first use, “help me set this up,” “continue,” or a confused user. Offer outcomes in the active language: **Set up my business**, **Organize this month**, **Tax questions and preparation**, **Continue my work**. Infer a clear choice from the request; do not force a mode menu. Keep the `tax-consultant` machine ID for existing workspaces; show the preparation-focused label.

## First useful task

1. Identify whether the user means their own business or a service for others. For the latter, apply [legal boundaries](legal-boundaries.md). Ask/reuse the language, actual host and Windows/macOS environment. Inspect available tools; do not assume Python, web research or browser control from plugin installation.
2. Explain that the assistant can organize evidence, prepare drafts and research questions. Distinguish this from professional representation, an accounting system's confirmed postings, or a tax submission. Explain the specific limits relevant to the chosen task rather than reciting every warning.
3. Ask the user to choose/open a private local folder through the host's folder picker if available. Use a local folder session without Git or worktrees. Explain a detected sync location, unsupported symlink or access problem in plain language. Do not enable sync, grant broad permissions, or weaken host controls to get past setup.
4. If Python is available, run `python3 <skill-directory>/scripts/workspace.py start --root <chosen-private-folder> --language en --mode general` using the chosen language/mode/year. Use the actual Windows Python launcher where appropriate. `start` creates only a new/empty directory or resumes an existing marker. Existing preferences win on resume; use `configure` only for an explicit preference change. Never retry a failed initialization by deleting the folder.
5. Read the returned status. `setup_incomplete` means structural setup is usable while data-processing assessment is outstanding; use public rules and synthetic or appropriately redacted data. `needs_attention` requires inspection of the listed issue, without reinitializing. `configured` means an assessment was recorded, not that the host is legally certified or all tasks are authorized. Check the assessment's current scope before real data.
6. Use [privacy](privacy.md) to identify what leaves the machine, which product/plan/tools process it, and where records/logs live. Prepare the assessment with source evidence; ask only for account facts that cannot be inspected. Never make the user certify compliance through a blanket checkbox. Record agreed factual settings with `runtime`; see [workspace contracts](workspace.md#runtime-review-and-diagnostics).
7. Offer a separate synthetic demonstration. Use `demo --root <new-private-demo-folder> --year <chosen-year> --language en|ru`. It imports two synthetic CSV originals, runs real reconciliation, and writes localized `START-HERE.md`. Show three matched groups and the EUR 12 unmatched outflow. Explain that an arithmetic match does not establish tax treatment. Keep demo and real work in different folders.
8. End with what is done, what needs attention, and one next action. On “continue,” use `start` and inspect only relevant tasks/questions/evidence. Preserve existing VAT history, mode, language, decisions and originals.

## Missing capabilities

If Python is unavailable, explain the missing local dependency and offer public-information planning or a manual worksheet. Do not claim that a downloadable ZIP contains a bundled Python runtime. Host installation, subscription purchases and permissions are separate user choices; the skill cannot grant them. Never run an opaque remote installer or request account secrets.

If web access is unavailable, identify which consequential rule remains unverified and prepare conditional/factual work. If browser access is unavailable, prepare a field worksheet; do not simulate entry or submission. In Claude plugin installations the invocation may be namespaced; use the host's actual skill picker.

## Recovery

- Run `doctor --root <workspace>` for local integrity, setup issues and lock visibility. It does not probe the app's browser or cloud permissions. Report the actual outcome in the active language; technical JSON is for the agent.
- For an existing or nonempty folder: reopen it, choose a new folder, or inspect its marker. Never clear it to make initialization succeed.
- For a lock: check the process/operation with the user or actual host tools. Do not remove another writer's lock. Only after establishing that no writer remains should an authorized recovery preserve and remove the stale lock.
- For altered originals or evidence: preserve both versions, identify what changed, restore from a trusted backup when appropriate, or create a linked correction. Do not update hashes merely to make a warning disappear.
- For malformed legacy records: keep the existing file and history, explain affected fields, and prepare a reviewed conversion to the documented format. `status` never silently migrates them. Profile corrections use `record`; register conversion needs a separately reviewed local edit because there was no old register schema.
- For updates: install/review a fresh skill package separately, close active writers, verify a synthetic example, and reopen the same private workspace. Do not initialize business data again. Avoid duplicate standalone and plugin installations.

Backup verification is a separate operation: preserve a protected copy outside the source checkout, restore into a fresh private location, then run `doctor` and `verify`. Never delete originals or backups based only on folder age. This preview does not encrypt files or configure Windows ACLs.
