# Private workspace and offline utilities

On Windows without Python, use [native Windows](native-windows.md) for supported setup/intake and host tools for readable preparation. Python commands below apply only when that optional runtime is available. Do not install it by default or claim native parity for unported validated operations.

Additional offline tools and record contracts are described in [preparation](preparation.md) and [payments](payments.md). They write versioned reports without changing the workspace schema or canonical profile.

Use Python 3.9+ and the bundled `scripts/workspace.py`. It makes no network calls. The assistant's own file-reading tools and remote model are separate data flows; apply `privacy.md` before reading real third-party records into context.

Contents: [Create](#create-then-install-project-scoped-skills) · [State](#files-and-state) · [Language/mode](#language-and-working-mode) · [Facts](#profile-facts) · [Originals](#import-and-verify-documents) · [Reconcile](#reconcile-normalized-csvs) · [Templates](#templates-and-external-operations) · [Recovery](#exit-codes-and-recovery).

## Create, then install project-scoped skills

Initialize a **new or empty private directory outside Git repositories and skill directories**. Do not initialize inside the public source checkout. Example from the source repository:

```bash
python3 skills/de-business-kit/scripts/workspace.py init --root /absolute/path/to/private-workspace --year 2026 --language ru --mode bookkeeping
```

Replace the path and year; do not use the example literally. On Windows, use the installed Python 3 launcher and an absolute path such as `C:/Users/NAME/Documents/Business-private`. Symlinked paths are rejected; select the actual physical directory. The script does not configure ACLs or encryption. Protect the private folder and backups using the user's normal OS controls.

For **project-scoped installation**, initialize the private workspace first, then run the repository installer pointing to that existing workspace. Installing into an empty folder first would make it nonempty, so initialization would correctly refuse it. User-scoped installation can happen before initialization. Do not enable Git/worktree/cloud syncing for this private folder just to make a host's project UI work; select a local folder session or use the user-level skill.

All relative input paths below are relative to `--root`, not the current shell directory. Use a single writer; a `.workspace.lock` prevents concurrent script mutations. After a crash, inspect whether the process is still running before removing a stale lock. Never remove another writer's active lock.

## Files and state

New CLI `init` and `start` use five everyday folders in `en`, `ru` or `de`, plus `.business-kit` for internal records and a localized root start guide. Folder language is pinned separately in `.workspace-layout.json` and the workspace marker. Include both the internal area and descriptor in backups. `--layout legacy` explicitly selects the old layout; existing workspaces resume unchanged. No automatic migration is implemented.

The table below lists **stable logical references**, not necessarily physical paths. Before using ordinary file tools, run `workspace.py folders --root <private-folder>` (or native `-Action folders`) and translate the longest matching prefix. Under the document archive, `originals`, `derived` and `proposals` also have translated names. Prefer the actual paths returned by operations. Never create old English directories alongside a localized workspace. See `assets/folder-layouts.json` for the shared mapping. The low-level Python `init_workspace` API retains its legacy default for existing callers; `start_workspace` defaults to localized folders.

| File / directory | Meaning |
|---|---|
| `00_admin/workspace.json` | Workspace UUID, schema version, initial year, language and working mode |
| `00_admin/runtime.json` | Actual host/provider/plan/data-processing configuration |
| `00_admin/documents.json` | Index of original bytes and storage periods |
| `00_admin/tasks.json` | Task array, with dependencies and completion evidence |
| `00_admin/questions.json` | Question array, with fact blocked and requested evidence |
| `00_admin/decisions.json` | Decision array, with effective date, reviewer and evidence |
| `00_admin/inbox/` | Private intake/answer files |
| `01_profile/business.json` | Canonical profile; flat `facts` mapping |
| `02_registration/`, `05_tax/YYYY/` | Draft worksheets, official receipts and responses; tax consultations in `05_tax/YYYY/consultations/` |
| `03_banking/`, `04_accounting/` | Provider requirements, statements/normalized files, workflow agreements |
| `06_bookkeeping/YYYY/MM/originals/` | Immutable-by-workflow original copies; no legal immutability guarantee |
| `06_bookkeeping/YYYY/MM/derived/` | OCR, extracted facts and normalized data |
| `06_bookkeeping/YYYY/MM/proposals/` | Legacy proposal files; new validated records use `00_admin/casework.json` |
| `07_exports/YYYY-MM/` | Generated reconciliation and optional records archives |
| `08_correspondence/` | Relevant correspondence |
| `09_audit/events.json`, `09_audit/history/` | Local events and before/after profile snapshots |

The initializer leaves the document archive empty. Intake creates only the selected storage month; derived files and proposals get directories when an operation needs them. Existing empty month folders are preserved. A folder period is not a tax-period determination. Keep invoice, service, receipt and payment dates in extracted records. Missing values stay unknown.

The task/question/decision files start as empty arrays. Use the validated `entry` command below to preserve IDs, transitions, locks and history. Legacy untyped records are flagged for reviewed conversion; never silently clear or migrate them. A due date in a file does not create an actual reminder.

## Guided start and demonstration

```bash
python3 <skill-directory>/scripts/workspace.py start --root <private-folder> --year 2026 --language en --mode general
python3 <skill-directory>/scripts/workspace.py demo --root <new-private-demo-folder> --year 2026 --language ru
python3 <skill-directory>/scripts/workspace.py doctor --root <private-folder>
```

Use [onboarding](onboarding.md) to guide the user instead of making them type commands. `start` resumes an existing workspace without changing preferences or year; arguments select defaults only for a new workspace. `demo` requires a new/empty folder and creates synthetic CSVs, preserved originals, a real reconciliation and localized `START-HERE.md`. It never fills a real business profile. Inspect interrupted demonstrations with `start`/`doctor`; do not rerun initialization over them.

## Runtime review and diagnostics

`status` reports `setup_incomplete`, `needs_attention`, or `configured`, with separate health, assessment status, missing fields and next action. It does not display profile values. `doctor` also checks original integrity and reports local Python/platform; browser, host discovery and account capabilities remain `not_probed`. Exit zero means the diagnostic ran, not that everything is ready.

Use `00_admin/runtime.json` as the starting format. Record actual product/version, local/cloud/hybrid execution, model provider, authentication route, plan, training-policy check date (`YYYY-MM-DD`), DPA assessment, retention reference, residency scope, and connector names/references. Leave unknowns null or `unknown`. `third_party_connectors` is a string array, never account tokens.

For a recorded assessment, set `client_data_mode` to `review_recorded` and add:

```json
"review": {
  "reviewed_by": "identified reviewer",
  "reviewed_at": "2026-10-25",
  "scope": "Specific data categories and workflow assessed",
  "evidence_file": "00_admin/processing-assessment.md"
}
```

The nonempty private evidence file explains the actual assessment, sources, limitations and scope. It cannot be a mutable configuration/register file. Missing settings cannot be marked reviewed. Save the full proposed runtime object as a private input file, then run:

```bash
python3 <skill-directory>/scripts/workspace.py runtime --root <private-folder> --input 00_admin/inbox/runtime-review.json
```

The writer stores assessment/configuration hashes and history under the workspace lock. A changed evidence file or configuration edited outside the command invalidates the recorded review. A changed provider, plan, connector, purpose or data category requires reconsideration; the command cannot decide legal suitability. To proceed without an assessment, retain `synthetic_or_redacted_until_reviewed`. Follow [privacy](privacy.md) before real personal-data processing. This is not a compliance checkbox.

## Task, question and decision registers

Every entry needs `schema_version: 1`, an opaque `id` (letters/digits/underscore/hyphen, at most 64 characters), `title`, `owner`, and `status`. New tasks start `pending`, questions `open`, decisions `proposed`. Optional fields are `depends_on` (IDs in the same register), `due_date`, `deadline_source`, `evidence_file`, `reviewer`, `supersedes`, `superseded_by`, and `note`. Unknown fields are rejected. Use the active language for title/note; retain machine identifiers.

```json
{
  "schema_version": 1,
  "id": "task-check-001",
  "title": "Check the unmatched synthetic payment",
  "owner": "user",
  "status": "pending",
  "depends_on": []
}
```

```bash
python3 <skill-directory>/scripts/workspace.py entry --root <private-folder> --collection tasks --input 00_admin/inbox/task.json
python3 <skill-directory>/scripts/workspace.py entry --root <private-folder> --collection tasks --id task-check-001
python3 <skill-directory>/scripts/workspace.py entry --root <private-folder> --collection tasks --input 00_admin/inbox/task-update.json --expected-sha256 <current-entry-hash>
```

Inspection returns state, evidence health and the version hash without the title/evidence content. Updates require that exact previous hash. Writes preserve unrelated entries and history; they never schedule reminders or perform external actions.

| Register | States | Requirements |
|---|---|---|
| `tasks` | `pending`, `in_progress`, `blocked`, `completed`, `cancelled` | Completion requires evidence and completed dependencies with valid evidence. A deadline needs a source or explicit user-target reference. |
| `questions` | `open`, `deferred`, `resolved` | Resolution requires evidence. |
| `decisions` | `proposed`, `approved`, `rejected`, `superseded` | Approval requires reviewer/evidence. Supersession requires an approved replacement linked to the old decision. |

Preserve terminal entries and create linked corrections. For an approved decision, create and approve its replacement with `supersedes=<old-id>`, then change only the old state to `superseded` and add `superseded_by=<replacement-id>`. Its content and reviewer evidence remain unchanged. Dependency and supersession cycles are rejected.

Evidence paths are relative private files; mutable administration files cannot serve as evidence. Hashes detect changes, not document truth. Changed evidence stays flagged, while inspection, unrelated work and linked corrections remain possible. Never rehash just to hide a discrepancy. Preserve legacy registers with incompatible shapes/broken links and prepare a reviewed conversion before using the writer.

## Language and working mode

`workspace.json` stores `language` (`en` or `ru`; legacy `de` accepted) and `mode` (`general`, `bookkeeping` or `tax-consultant`). A v0.1 workspace without `mode` is read as `general`; its files are not rewritten during status checks and schema version stays 1. Both languages and modes share the existing profile and evidence.

```bash
python3 <skill-directory>/scripts/workspace.py configure --root /absolute/private-workspace --language en --mode tax-consultant
python3 <skill-directory>/scripts/workspace.py configure --root /absolute/private-workspace --mode bookkeeping
python3 <skill-directory>/scripts/workspace.py status --root /absolute/private-workspace
```

Supply at least one setting. An actual change records before/after marker history and a `workspace_configured` event under the workspace lock; setting the same values again returns `unchanged`. The command changes no business fact, VAT regime, original document, year or workspace identity. Status reports language and mode without printing personal profile values. Apply temporary chat overrides without changing defaults; see [language and modes](language-and-modes.md).

## Profile facts

Use the exact keys in `business.json`. Groups include legal form and activity classification; all activities; owner, residence and business location; preparation, actual business start, commercial launch and registration dates; existing VAT, history and waivers; turnover across all activities; bookkeeping method, software and work split; customer/supplier countries and banking/provider needs. Tax identifiers can be referenced rather than copied in full.

Each fact has this shape:

```json
{
  "value": null,
  "status": "unknown",
  "source": {"kind": null, "ref": null},
  "recorded_at": null,
  "effective_from": null,
  "note": null
}
```

Supported states: `unknown`, `declared`, `proposed`, `verified`, `needs_review`. A nonunknown fact needs a value and evidence source. `verified` requires an inspected private file source; the writer stores its hash, and status detects missing/changed evidence. The script cannot validate document truth or a legal conclusion. Legacy verified facts without fingerprints require review, not silent migration. Record money as decimal strings with currency and period identified, not binary floats.

New writes validate profile field types. VAT regime is `Kleinunternehmer`, `Regelbesteuerung` or `unresolved`; accounting method is `EÜR`, `Bilanzierung` or `unresolved`. Employee/cash/cross-border/existing-VAT flags are booleans. Dates use `YYYY-MM-DD`; `vat_prior_year` is an integer year. Client/country lists are string arrays. Activities are arrays with unique `activity_id`, optional text `description`, `classification` (`freiberuflich`, `gewerblich`, `mixed`, `unresolved`) and date/null `commenced_at`. VAT-history items contain `regime`, `effective_from`, and `source_ref`. Provider/bank requirements are objects; remaining text fields require nonempty strings. Unknown facts remain null.

Person-wide turnover/forecast fields use `{"amount":"1234.56","currency":"EUR","period":"2026"}` with a nonnegative decimal string and explicit year. Preserve original foreign amounts separately and substantiate conversion. This storage format does not calculate qualifying statutory turnover. Legacy values are flagged without rewriting; correct individual fields with evidence through `record`.

Save a one-field update in `00_admin/inbox/fact.json`:

```json
{
  "field": "vat_current_regime",
  "value": "Regelbesteuerung",
  "status": "declared",
  "source": {"kind": "user_statement", "ref": "intake-2026-10-25"},
  "effective_from": null,
  "note": "Declared existing treatment; authority evidence not yet reviewed."
}
```

Run:

```bash
python3 <skill-directory>/scripts/workspace.py record --root /absolute/private-workspace --input 00_admin/inbox/fact.json
```

The input file must be inside the workspace. `--input -` also accepts JSON through stdin; do not embed secrets in shell command arguments. Keep external submission dates and evidence in an operation record, not an inferred boolean in the profile. Previous profile values are preserved in snapshots.

## Import and verify documents

```bash
python3 <skill-directory>/scripts/workspace.py ingest --root /absolute/private-workspace --source /absolute/source/invoice.xml --period 2026-10
python3 <skill-directory>/scripts/workspace.py verify --root /absolute/private-workspace
python3 <skill-directory>/scripts/workspace.py status --root /absolute/private-workspace
```

Intake accepts regular PDF, XML, PNG, JPG/JPEG, TIF/TIFF and CSV files, at most 50 MiB. It reads bytes without executing, OCRing or parsing active content, gives the stored copy a SHA-256 filename, and indexes original name, size, hash, storage period and import time. Originals are not overwritten. Identical bytes reuse an indexed document only after integrity verification; this is not a conclusion about business duplicates. Different scans of the same invoice still need business-level review.

`verify` checks indexed original integrity and reports unexpected original files requiring review. It does not validate tax treatment, completeness of received documents, XML business rules, legal retention or the integrity of the audit history itself. The user can alter files and their index; this is not a tamper-proof archive. Never label a successful hash check GoBD certification.

Individual JSON replacements are atomic, but the complete multi-file workflow is not a transactional database. After an interrupted or failed operation, inspect originals, the index and history before retrying; do not blindly delete or overwrite evidence. The code preserves a changed/unrecognized copy for review when it cannot safely roll back its own incomplete import.

## Reconcile normalized CSVs

Preserve raw bank exports separately. Convert a **derivative** into UTF-8 comma-separated CSV with these headers:

```csv
transaction_id,booking_date,amount,currency
synthetic-tx-001,2026-10-03,97.00,EUR
```

Prepared ledger entries use:

```csv
entry_id,transaction_id,amount,currency
synthetic-sale,synthetic-tx-001,100.00,EUR
synthetic-fee,synthetic-tx-001,-3.00,EUR
```

Positive amounts mean inflows and negative amounts mean outflows in **both** files. `transaction_id` is a verified link to the bank record, not a guess from similar amounts. Give separate stable IDs to different transactions, including across accounts. Multiple ledger rows can share a transaction ID for a documented split. Leave an unknown ledger transaction ID empty so it is reported as unlinked.

Use a dot decimal separator, no grouping or exponent notation, and uppercase three-letter currency codes. The tool validates code syntax, not a current ISO currency catalogue or each currency's minor-unit rules. Bank booking dates must belong to the requested period. The ledger file should cover entries relevant to those payments; an invoice's document month can be different. Duplicate IDs, duplicate/missing headers, malformed rows and invalid amounts are rejected. Other columns are ignored.

Place both normalized input files in the private workspace and run:

```bash
python3 <skill-directory>/scripts/workspace.py reconcile --root /absolute/private-workspace --bank 03_banking/bank.csv --ledger 04_accounting/ledger.csv --period 2026-10
```

The report matches **transaction ID plus currency** and compares exact Decimal totals. It lists matches, differences, unmatched bank records, unmatched ledger groups, unlinked entries and currency-separated totals, with hashes of the inputs. It does not infer exchange rates, allocate unrelated amounts, classify expenses, post entries or close a period. An empty input pair requires review instead of establishing completeness.

Reports receive unique names under `07_exports/YYYY-MM/`. The CLI prints summary counts and the relative report path; it does not print the full bank statement. Exit `0` means a report was produced, including when its status is `needs_review`. A successful report is not a green accounting conclusion.

## Templates and external operations

Copy only needed templates into the private workspace:

- [localized templates](language-and-modes.md): English/Russian form worksheets, bookkeeping agreements, monthly reports and tax consultations; choose using [locales.json](../assets/locales.json).
- [proposal](../assets/proposal.json): extracted facts and unposted treatment.
- [operation](../assets/operation.json): exact payload, authorization and outcome.
- [source check](../assets/source-check.json): source, effective dates and applicability.

Create unique IDs. Do not reuse null IDs as real identifiers. Monetary fields in proposals are decimal strings; null means unknown. The templates are workflow schemas, not a provider's API request body.

External operation states may be `draft`, `ready_for_review`, `authorized`, `submitted`, `submission_unconfirmed`, `authority_response_received` or `cancelled`. Use only the state the evidence supports. Bind authorization to the exact recipient, period and payload; a significant payload change invalidates the old scope. Maintain prior linked operations when correcting. No external execution engine is shipped in v0.4.

## Exit codes and recovery

- `0`: local operation completed; read the report status for unresolved differences.
- `1`: `verify` found integrity or unexpected-original issues.
- `2`: invalid/unsafe input, schema issue or filesystem error; inspect before retry.

The utilities refuse symlink paths, path traversal, existing content during initialization and work inside Git or skill directories. They use owner-only POSIX modes where supported, without Windows ACL or encryption guarantees. Public repository files and private business files remain separate.

## Document review desk

Use [document workflow](document-workflow.md) for `desk.py` commands and additive casework schema 1. Proposal template schema 2 and source checks have validated writers; external-operation templates do not execute integrations. The complete accounting ledger and ELSTER submission remain core gaps.
