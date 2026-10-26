# User guide

**English** · [Русский](user-guide.ru.md)

Choose a concrete outcome in the [task guide](tasks.en.md).

New here? Follow the [short start guide](start.en.md). Read this manual by task; you do not need to learn technical commands.

[Lifecycle tasks](#launch-annual-preparation-and-business-changes) · [Service exports](#inspect-a-service-export) · [Invoice corrections](#invoice-corrections-and-partial-payments) · [Documents](#documents) · [Accounts and payments](#accounts-and-payments) · [Taxes and letters](#taxes-and-letters) · [Reports](#reports) · [Continue](#continue) · [States](#states) · [Help](#help) · [Backups](#backups)


You can directly select `de-business-start`, `de-business-operations`, `de-business-accounting`, `de-business-tax`, `de-business-services` or `de-business-changes`. The general `de-business-kit` helps select the next action. See the [map and shared resources](../references/lifecycle.md). Install the complete bundle; keep one profile.

## What this assistant is

German Business Kit is a set of instructions and tools for Codex and Claude Code. It helps you handle business tasks and records independently throughout your activity in Germany. The app, file access, AI subscription and service connections are provided separately. The skill alone does not grant access to email or banking.

This manual describes existing document, payment, reporting and recovery tasks within the wider entrepreneur skill system. Formation, questions and service selection also have dedicated modules; change and closure guidance is available. See the [portable lifecycle map](../references/lifecycle.md). A complete accounting/tax engine and ELSTER transmission integration are not implemented. Existing accounting software remains authoritative. Professional consultation is optional for a specific issue.

## Ask for a result

Specify the result, period and source where relevant. For example:

> Organize October 2026 documents from this folder. Show the list first. I want to see which invoices need review and which evidence is missing. Do not send anything.

The assistant should reuse known facts, ask only what matters and retain uncertainty. Say “I don't know” when a fact is unresolved. A simple explanation does not require a workspace, full questionnaire or mode selection.

## Launch, annual preparation and business changes

Start with the outcome in the [task guide](tasks.en.md). For example: “Prepare a launch plan for this activity,” “Show what is missing before annual reporting,” or “Plan closing one activity while keeping my other work running.”

The relevant skill reuses your profile and prepares a readable plan or worksheet with known facts, dependencies, sources and open decisions. Formation, customer work, annual readiness, service access and changes have dedicated worksheets. First-hire preparation covers the required questions and next steps; payroll calculations and registrations need their actual tools and evidence. A saved plan does not establish a completed registration, hire or closure.

## Find your files

| New English workspace folder | What to find |
| --- | --- |
| `01 Inbox` | Files awaiting processing; placing a file here does not itself import it |
| `02 Documents` | Preserved originals and derivatives by year/month |
| `03 Accounts` | Bank records, accounting records and internal reports |
| `04 Taxes` | Form materials and filing/authority-response evidence for the year |
| `05 Business` | Registration and business correspondence |

Originals may have hash-based filenames; the source filename is retained in the index. Ask the assistant to find a document by name, period, contents or linked payment. Do not manually rename stored originals or managed folders.

Older workspaces may use different English technical names. This is not an error or a reason to create another workspace. Profile, history and other internal records live in the technical area; you do not need to edit them, but they belong in backups.

## Documents

> Show what is in this folder. Suggest what to import. Preserve selected originals unchanged and show extracted facts separately for review.

For email or a service, identify the source, period and exact product/edition if known. The assistant checks available tools. Preferring a plugin/API does not establish that a connection exists. Alternatives may include permitted browser work or a selected export. Do not put passwords or keys in chat.

Compare suggestions against the original: amount, currency, date, supplier/customer and purpose. Correct individual fields and leave uncertain categories open. OCR and extraction do not establish tax correctness. Receiving the same file again does not necessarily mean a duplicate business transaction.

**Result:** preserved originals, a readable account of processed/skipped items, questions and the next action. A single-file failure must not be concealed by a blanket “done.”

## Accounts and payments

> Prepare October for my review. Show matched payments, missing receipts, fees, refunds and unresolved transactions separately by currency.

If your accounts are in Lexware, sevdesk, WISO or another product, identify the exact version. The assistant must not create parallel accounts or treat an uploaded document as a confirmed posting. The local route includes a limited cash journal for an explicitly selected EÜR workflow; that neither establishes eligibility nor calculates all statutory returns.

Before importing a bank export, review column mapping, signs, dates, currencies and account. For international payments and payment services, identify available statements and payouts; a processor payout is not automatically another sale. Missing amounts and exchange rates must not be invented.

**Result:** a readable report of the actual evidence checked. Matching amounts does not prove a complete month or correct tax treatment.

## Inspect a service export

> Check this supplied export for the requested period. Explain how its date selection works, which originals are present and what evidence is still missing. Keep my existing accounting system authoritative.

The assistant records the export route, date basis, supplied files, inspected pages and gaps. A CSV row or matching count does not prove that every original or an entire month is present. Lexware Office guidance distinguishes document/PDF selection from DATEV posting exports; current project trials use local examples. A live connection or import is confirmed only by an actual service result. See [services and access](../references/connections.md).

## Taxes and letters

> Explain this letter, what it asks and the next action. Distinguish its stated date from a verified deadline. Prepare a German draft response and a separate English explanation. Do not send yet.

For a conceptual tax question, ask for the rule and its source first. For example: “Does buying a phone in installments change its depreciation period?” Before concrete entries or amounts, the assistant needs the relevant date, accounting method and other decisive facts. It checks applicable primary sources and uses a suitable official or selected accounting tool for calculations; the skill does not supply its own tax formula engine.

For a form identify the purpose and year/period. Form applicability, deadlines and elections depend on your circumstances and current official sources. Exact German field names remain visible so you can find them in the interface.

A draft comes first, followed by review of facts, values and attachments. Before an external submission you see the exact recipient, form, file versions and material decisions. If authorization is missing, it is requested for that specific action. After sending, actual evidence is preserved; an unclear result must be checked before retrying.

**Limit:** this project has no working ELSTER adapter. The assistant may use available permitted host tools or provide step-by-step actions. A polished PDF does not replace the official form, and a plan does not prove a filing.

## Reports

> Prepare a readable report with the result, sources, open issues and next action. Link the file. If a recipient document is needed, keep it separate from my private review sheet.

HTML opens in an ordinary browser without Python. PDF uses an available export tool and must be checked after saving; otherwise the assistant provides the readable source and names the unfinished step. DOCX/XLSX are options when suitable tools exist. Technical JSON or CSV must not be the only explanation of the result.

A German recipient document can have a separate English or Russian explanation for you. Private questions, internal paths and notes are not automatically sent. Revisions preserve older versions; a corrected document does not inherit approval just because its predecessor was approved.

## Banking, insurance and other services

> Compare options for these needs: … Account for current services, normal prices after promotions, restrictions and terms. Do not buy or connect anything without my decision.

The result includes sources and check dates, reasons for the comparison and decision-relevant questions. A recommendation does not establish supplier approval, a contract or a working connection.

## Continue

At the end ask to save the result, open questions and next step. Return to the same folder:

> Continue here. Show the latest saved state, changes in the sources and what needs to happen next.

The overview also shows active business tasks without dates and tasks from other months. It shows unresolved dependencies and changed or missing evidence; an independent task can still continue. Completed and cancelled tasks stay in history. Ask the assistant to inspect the saved task before continuing. In the GUI, the continuation button prepares a request to copy to your assistant; it does not start an AI session or complete work automatically.

Change language naturally: “Respond in German from now on; do not rename my folders.” New folder names support EN/RU/DE; complete report templates currently cover English and Russian. Switching tasks does not change your tax regime. A dated task is not an automatic notification.

## States

| State | Meaning |
| --- | --- |
| Unknown | Insufficient evidence; not zero or “no” |
| Proposed / draft | A version is prepared for review |
| Document reviewed | Particular facts were checked within the stated scope; a posting may still be absent |
| Entry recorded | Evidence of a record in the chosen system; not proof of complete tax correctness |
| Authorized to send | A specific action and version are authorized; transmission is not yet confirmed |
| Transmission confirmed | An observed transmission result is saved; not substantive acceptance by Finanzamt |
| Response received | An actual authority response exists and needs reading and assessment |

## Help

| Problem | What to ask |
| --- | --- |
| Skill is missing | “Check installation and discovery in my app version. Explain what is missing.” |
| Folder or file is inaccessible | Identify the selected location and request an access check. Do not grant whole-disk access unnecessarily. |
| Python is mentioned | “Check native Windows and available tools. Continue preparation without installing Python; explain which automation is unavailable.” |
| Setup is incomplete | “What exactly is unrecorded or unchecked? Continue available work with fictional/redacted data.” |
| File changed, integrity error or lock | “Diagnose without deleting originals, resetting data or removing another writer's lock.” |
| Service access is unavailable | “Show an allowed route or explain which selected export I should prepare.” |
| Sending result is unclear | “Check status and evidence in the actual service first. Do not blindly resend.” |

For support collect the app/version, OS, step, expected result and redacted error. Remove names, tax IDs, bank details, keys and real documents. Do not publish the workspace.

## Backups

Keep a protected copy of the entire workspace, including hidden internal records and `.workspace-layout.json`. A selected reports archive is not a full backup. Test restoration in a separate folder, not over the current one.

Skill updates and business data are separate. The installer refuses to overwrite an existing installation; ask to compare versions and preserve custom changes first. Never delete business data to update the skill. Automatic migration of the older folder layout is unavailable.

## Check your own environment

Capabilities depend on the app version, permissions and tools. Basic Windows operations use native PowerShell without mandatory Python; some advanced validated operations still need an available additional engine. macOS does not guarantee Python either. Try a small fictional example in your environment before relying on an entire process. The project's demo interface uses fictional records and is not connected accounting software.


## One month with your own cash journal and manual ELSTER

Ask: “Continue October in my local cash journal, show unresolved items, and help me prepare the applicable return for manual ELSTER.” The assistant should organize documents, review bank mapping, record supported reviewed cash movements, reconcile and give you a readable report. Cash totals are not a calculated tax return. The form/year and any calculation tool require their own evidence and review.

The real workspace overview now shows your accounting choice, period entries, open questions, saved filing versions and their blockers. It is a snapshot: ask to refresh it after changes. A submission with an unknown outcome remains visible even when you switch months. You authenticate and send in ELSTER after reviewing the exact version; preserve the actual receipt. A receipt and a Finanzamt decision are different records.

Ask: “Create and verify a complete backup at this protected location”, or “Restore this backup into a new folder and check it.” [Full backup and restore](../references/recovery.md) includes originals, records, evidence and history, and is available through native Windows tools without installing Python. An existing folder is never overwritten. Keep both the backup and original until you have checked the restored workspace.

The native Windows overview reads saved records and checks local evidence hashes; it does not run the full filing preflight. Advanced protected accounting/filing writes still need a supported existing execution environment. It does not silently install Python. [Monthly workflow and exact limits](../references/monthly-workflow.md).

## Invoice corrections and partial payments

You can supply an original invoice, a later CreditNote and relevant payment
records. The assistant can preserve and inspect supported standalone XML, explain
its reference to the earlier invoice, and save a reviewed document link. The
issued originals and earlier drafts remain available. Missing or ambiguous links
stay open. A partial payment or CreditNote does not automatically mean the invoice
is settled, money was refunded or accounting was corrected. Existing software
remains authoritative; ask to continue the saved case when new evidence arrives.
This is bounded evidence preparation, not technical e-invoice validation or sending.
