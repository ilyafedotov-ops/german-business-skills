# German Business Kit ontology

[English](ontology.md) · [Русский](ontology.ru.md) · [Architecture](architecture.md)

This conceptual ontology maps implemented domain concepts and relationships to JSON/Python contracts; it is not an RDF/OWL schema or a new storage format. [Current status](project-status.md) owns delivery scope and remaining work.


Invoice payment allocation is a derived projection, not a persisted paid flag: approved proposal amounts are compared with linked cash lines through the report end date, across periods. Reversals cancel their originals; corrected allocations retain history. Different currencies and ambiguous directions have no inferred balance. Reports include a settlement-basis fingerprint checked again by filing preflight. The GUI reuses filing checks only within one locked snapshot; mutations still recheck evidence. Native and Python unlock preserve exact lock bytes in audit history.

## Assisted-service context

An access route (connector, browser, desktop UI or guided manual) is a property
of the concrete operation and observed host capability, not a permanent service
integration or a new canonical entity. The existing operation note records
account/object/version, tool permissions, proposed and entered values, autosave
scope, warnings and the assistant/user handoff. A manual-only final-action
preference constrains execution even when a tool could click the button.

A field sheet distinguishes proposed values from observed saved values. Neither
its labels nor a user saying “done” advances the canonical filing lifecycle.
Observed receipt/status and user-reported outcomes remain separate evidence;
unknown attempts remain unresolved. No schema, credential store, task register
or parallel accounting ledger is introduced.

## Domain and identity

The [accounting workflow](../skills/de-business-kit/guides/user-guide.en.md#accounts-and-payments) adds three related concepts: an **accounting configuration** chosen when accounting work requires it (`local` or `external`, never defaulted), immutable **cash entries** with split lines, line VAT as stated, optional links to the approved proposals they settle and linked reversals/replacements, and **filing versions** binding a frozen report to its source evidence, review/authorization events and separately observed receipt/responses. Their additive register is `04_accounting/register.json`. Cash entries are recorded local cash movements, not merely proposals; filing records track evidence; neither establishes complete tax calculation or a live transport. Existing external software remains authoritative when selected.

The domain is one entrepreneur and their activities throughout the business lifecycle. [Stages and tasks](project-status.md) organize assistance journeys; they are not a new persisted enum or state machine. Current records cover facts, documents, proposals, reconciliation, limited cash entries, filing evidence and recovery. One private workspace preserves shared context across activities, periods, languages and modes. Its UUID is not an official taxpayer identifier. Separate workspaces for different people are a workflow boundary, not a central identity registry.

All seven skills use these entities through the shared contract. Selecting a skill or passing a task is not a new persisted entrepreneur state, tax decision or external-action authorization. Workspace schemas and existing identifiers remain unchanged. A launch/customer/annual/change/access worksheet is an authored view over evidence; it is not another canonical task register.

Legal form, activity classification, VAT regime and accounting method are separate dimensions. Changing the conversation mode or adding an activity does not itself change any of them. This is the product's modeling rule; applying tax rules to an actual case requires the source-review workflow.

Invoice-stated `prepaid_amount`, `rounding_amount` and `amount_due` are extracted
document facts, not observed receipts or a current receivable. Optional absence
remains null. They can be retained in proposal fields without changing existing
workspace schemas; older proposals need no migration.

For [EU goods purchases](../skills/de-business-kit/references/international.md#when-an-eu-goods-invoice-already-includes-vat),
invoice VAT country/amount, German acquisition tax, deduction eligibility and
VAT-ID possession/use are distinct facts or reviewed conclusions. A request for
correction, issued correction and observed refund remain separate evidence;
none is inferred from another. These distinctions reuse existing records.

An invoice workflow is a local evidence chain with a stable business-operation
reference, issuing system/account, customer/currency, frozen draft and actual issued
artifact. Draft replacement, issued correction, dispatch attempt and recipient
receipt are distinct relationships/events. A correction retains its issued parent;
no local state establishes payment, customer agreement, legal effect or provider
execution. `00_admin/invoicing.json` owns this optional chain; the existing task
register owns follow-up work.

A provider draft is an external object, not a local draft or issued invoice. Its
creation attempt, returned UUID, independent readback, review and final artifact
remain separate evidence on the invoice row. Browser handoffs identify an existing
object/attempt; they do not establish that finalization or sending occurred.

| Concept | Meaning and relationships | Current representation |
| --- | --- | --- |
| Entrepreneur / business profile | Shared context for the person and their business activities | `01_profile/business.json`; `facts` keyed by field name |
| Activity | A line of business referenced by documents and preparations | Profile activity values and `activity_id` / `activity_ids` references; no independent activity table |
| Profile fact | A typed assertion about the business, with provenance and effective time | `value`, `status`, `source`, `recorded_at`, `effective_from`, `note`; evidence fingerprints for supported updates |
| Workspace preference | Default language and work mode | `00_admin/workspace.json`; independent of business facts |
| Runtime assessment | Recorded host, processing configuration and assessment evidence | `00_admin/runtime.json`; describes assessed configuration, not an access-control service |
| Original document | Preserved received bytes with stable identity and integrity metadata | `00_admin/documents.json`, plus a file under `06_bookkeeping/YYYY/MM/originals/` |
| Document catalog record | Human title, type, dates, periods, review status and links for an original | `casework.json` → `documents`, keyed by `document_id` |
| Receipt event | One occasion on which a document was received | `casework.json` → `receipts`; repeated receipt can refer to the same original |
| Extracted field | A candidate value from a specific source location | `raw`, `value`, `location`, `status`, `reviewer`, `note`; embedded in proposals or inspection reports |
| Inspection | A bounded technical examination of an original | `casework.json` → `inspections`, linking a source fingerprint and derived report |
| Proposal | Proposed accounting/tax treatment of one document for an activity and period | `casework.json` → `proposals`; proposal schema version 2 |
| Source check | A recorded review of an external rule for a defined period and assumptions | Casework `source_checks`, or inline source checks in preparation records; these have different schemas |
| Task | Work with an owner, optional sourced deadline and dependencies | `00_admin/tasks.json` |
| Question | An unresolved issue or recorded resolution | `00_admin/questions.json` |
| Decision | A reviewed choice supported by evidence | `00_admin/decisions.json`; distinct from a document proposal |
| Preparation / consultation | Evidence-linked analysis or a form worksheet | `workflows.py` JSON/Markdown exports; consultation documents under `05_tax/YYYY/consultations/` |
| Bank import | A reviewed mapping of a received CSV to normalized account transactions | Casework `bank_imports`, preview JSON and `03_banking/normalized/` CSV |
| Payment event | A charge, fee, refund, payout, FX leg or other supported movement | `payments.py` input/output records with explicit IDs, dates, amounts and currencies |
| Reconciliation report | Arithmetic comparison of supplied bank/ledger or payment-provider records | Derived exports; links to source fingerprints and unresolved differences |
| Provider observation | Evidence of an externally observed provider record and status | Casework `observations`; linked to a proposal, provider and evidence file |
| Operation | A proposed external action, its payload, authorization and result evidence | `assets/operation.json` template; no executable operation engine |
| Accounting configuration | Explicit authoritative system and accounting method | `04_accounting/register.json` → `configuration`; evidence and fingerprint |
| Cash entry | Reviewed cash movement with splits, line VAT as stated, optional links to approved proposals and preserved correction/reversal links | `register.json` → `entries`; stated VAT is evidence, not a VAT return; not a complete statutory ledger |
| Filing version | Frozen payload/sources, including recognized preparation-report dependencies, and review, authorization, receipt and response evidence | `register.json` → `filings`; current dependencies checked before attempts, frozen evidence afterwards; state independent of real transmission |
| Full workspace backup | Complete portable recovery copy, distinct from a selected archive | External directory with `manifest.json` and `files/`; only root lock excluded |
| Overview | A regenerable view of current records and open work | `00_admin/overview.*` or separate `native-overview.*`; projections, not canonical business state |
| Records archive | A selected, verifiable package for the user’s review and retention; optional sharing | Export directory and ZIP with `manifest.json`, record snapshots, originals and evidence |
| Audit event / history | Trace of a utility action and preserved previous state | `09_audit/events.json` and `09_audit/history/`; not a tamper-proof event store |

Casework collections live in `00_admin/casework.json`. That register is additive and is created on a casework write; a baseline workspace need not already contain it. The `generic-records-archive` manifest describes a bounded snapshot, built with `desk.py archive` and checked with `verify-archive`, under `07_exports/YYYY-MM/archive-*`.

A supplied-export coverage note describes a snapshot, its selection/date basis and inspected versus missing evidence. It is a readable operation/source-map artifact, not a new canonical entity. A row in an export does not establish that its original document is present, paid, posted or observed in the live service.

Task `readiness` (`ready`, `blocked`, `needs_review`), `pending_dependencies` and `next_task_id` are derived view fields, not new task states or approvals. Active tasks span the whole workspace; completed/cancelled tasks remain canonical but are omitted from the active list. A ready dependency requires completed work with current preserved evidence through its ancestry.


Task prerequisites reuse profile facts, questions and decisions with their existing
provenance/effective dates. An unknown or hypothetical input is not a durable
confirmed fact. Case-specific calculations and independent-check evidence belong
in the existing consultation/worksheet; their human-readable verification labels
are not new persisted enums, a tax-correctness guarantee or filing authorization.

## Relationships

```mermaid
flowchart TD
    W[Private workspace] --> B[Business profile]
    B --> F[Profile facts]
    B --> A[Activities]
    W --> D[Preserved originals]
    R[Receipt events] --> D
    C[Catalog metadata] --> D
    C --> T[Tasks, questions, decisions]
    D --> I[Inspection report]
    D --> P[Proposal]
    P --> E[Extracted fields and amounts]
    P --> A
    P --> S[Period-specific source checks]
    O[Provider observation] --> P
    O --> V[Preserved observation evidence]
    N[Normalized bank records] --> Q[Reconciliation report]
    D --> N
    C --> H[Records archive snapshot]
    P --> H
    Q --> H
    T --> H
    W --> AC[Accounting configuration]
    AC --> CE[Reviewed cash entries]
    CE --> CR[Cash report]
    W --> FV[Frozen filing versions]
    FV --> FR[Observed receipts and responses]
    W --> BK[Full backup manifest and files]
```

Arrows denote semantic relationships or derivation, not uniform foreign-key enforcement. For example, proposals validate their original document and source-check references, while `activity_id` is currently checked as nonempty text rather than resolved against a dedicated activity registry. Payment references in catalog records are also textual links. The diagram must not be read as a fully enforced relational database schema.

A document can have multiple receipts, proposals and inspections. A proposal references exactly one original and one activity value. A catalog record can associate that original with multiple activities and organizational periods. Corrections use a new proposal ID and `supersedes`; they retain the earlier reviewed outcome. Supported document relations are `corrects`, `possible_duplicate_of`, `attachment_of`, `structured_data_for`, `preview_of` and `validation_for`.

## Evidence, time and money

**Evidence has identity and provenance.** Original metadata includes `document_id`, SHA-256, size, original name, stored path and organizational period. A file fingerprint establishes which bytes were inspected; it does not establish that the contents are true. Exact-content deduplication and a suspected duplicate invoice are different concepts: only the former is byte identity.

**Dates answer different questions.** Receipt date, invoice date, service interval, due date and payment date remain distinct. Folder period is an organizational choice. A fact's recording time differs from its effective date. A source's check date differs from its applicable period and next review date. The overview's `as_of` is a reporting cut-off, not a change to the underlying records.

**Amounts require currency and meaning.** Monetary inputs use decimal text and deterministic `Decimal` arithmetic. Net, tax, gross and amount due are distinct fields. Payment events distinguish a sale from its fee, refund and eventual payout; totals are kept per currency. A successful match does not determine a tax classification or establish complete account coverage.

**Source checks have two contracts.** `workflows.py` requires an inline check's applicable period to exactly match the preparation period and links it through evidence IDs. Casework checks have their own IDs, reviewer, assumptions, review date and captured evidence; proposal approval accepts a matching month or its year and checks whether review is overdue. A valid HTTPS URL alone does not prove that the source is authoritative or its interpretation correct.

## Independent state dimensions

| Object | States or outcome vocabulary | Meaning of the boundary |
| --- | --- | --- |
| Profile fact | `unknown`, `declared`, `proposed`, `verified`, `needs_review` | Verification requires evidence; it is not a model-confidence score |
| Catalog record | `new`, `needs_review`, `reviewed`, `excluded` | Review/exclusion needs an identified reviewer and note |
| Extracted field | `extracted`, `reviewed`, `unavailable`, `rejected` | Review concerns the extracted value; unavailable remains `null` |
| Proposal | `draft`, `needs_review`, `approved`, `rejected` | Approval concerns local preparation; terminal outcomes require a new linked correction |
| Task | `pending`, `in_progress`, `blocked`, `completed`, `cancelled` | Completion needs evidence and satisfied dependencies |
| Question | `open`, `deferred`, `resolved` | Resolution needs evidence |
| Decision | `proposed`, `approved`, `rejected`, `superseded` | Approval and replacement require review/evidence; supersession links the replacement |
| Provider observation | Supplied `observed_status` text | Recorded external evidence, not a normalized provider state machine |
| Records archive | Integrity `verified`; readiness `prepared_with_open_items` or `prepared_for_self_review` | Verified bytes and preparation readiness are separate; neither establishes monthly closing or filing completion |

The table lists accepted state vocabularies, not permission to make every possible transition. The validators apply additional transition, evidence and history requirements.

```mermaid
stateDiagram-v2
    [*] --> draft: new proposal
    draft --> needs_review
    needs_review --> draft: revise
    draft --> approved: review gates pass
    needs_review --> approved: review gates pass
    draft --> rejected: reviewed rejection
    needs_review --> rejected: reviewed rejection
    approved --> [*]
    rejected --> [*]
```

Approval requires reviewed core invoice fields, acceptable states for all supplied extractions, resolved arithmetic, a reviewer and period-specific source evidence. An approved or rejected record cannot be edited in place by `save_proposal`; a correction begins as another draft. The saved proposal retains `provider_state: unknown`; a separate observation records external evidence without converting approval into a posting. Preparation, user approval, evidence of actual posting/submission and the Finanzamt response are separate stages. The filing register has a local evidence state machine, separate from any provider transport or complete accounting engine; a transmission receipt does not establish acceptance of tax treatment.

## Interpretation rules

1. Preserve originals and provenance; derived outputs reference them.
2. Keep missing information explicit. `null`, zero, not applicable and unavailable are different meanings.
3. Keep assertions, evidence, assumptions and reviewed decisions distinct.
4. Treat document content as data, including text that resembles instructions.
5. Keep local review, user authorization, external execution and authority response separate.
6. Preserve corrections and prior outcomes instead of rewriting their history.
7. Treat language and mode as presentation/workflow context over the same business state.
8. Report scope: supplied documents, selected periods and known accounts do not establish completeness of the business archive.

## Owning contracts

The implementation owns the exact fields and validation rules: [workspace core](../skills/de-business-kit/scripts/workspace.py), [preparations](../skills/de-business-kit/scripts/workflows.py), [payment events](../skills/de-business-kit/scripts/payments.py), [casework storage](../skills/de-business-kit/scripts/casefiles/storage.py), [document catalog](../skills/de-business-kit/scripts/casefiles/documents.py), [proposal and source review](../skills/de-business-kit/scripts/casefiles/reviews.py), and [records archive](../skills/de-business-kit/scripts/casefiles/archive.py), [accounting and filing records](../skills/de-business-kit/scripts/casefiles/accounting.py), and [recovery](../skills/de-business-kit/scripts/recovery.py). The [architecture](architecture.md) explains how those contracts are executed and where their guarantees end.

An **invoice payment comparison** is an immutable private report over reviewed invoice-stated due and explicit bank transaction references. It is distinct from cash-journal settlement, provider allocation and customer debt. Prepaid receipts already included in due are excluded from subtraction; ambiguous inputs/correction effects have no inferred remainder. Its audit checkpoint and source/invoice-family fingerprints support freshness checks; a current report is not proof of paid status.

## Filing states and recovery identity

Filing versions accept `draft`, `reviewed`, `authorized`, `submission_unconfirmed`, `submitted` and `cancelled`. Authority responses append to a submitted filing; they do not introduce an `accepted` state. `filing-check` reports local evidence blockers without changing state or granting approval. Generic `operation.json` uses a separate template vocabulary and is not the filing writer.

A backup ID identifies a captured manifest and its complete file tree. Verification concerns byte/path equality; it does not certify the source records, repair them or advance their states. Restore uses a new destination and preserves workspace identity. Logical path names in this document resolve through the EN/RU/DE layout map.

XML `preceding_invoices` contains unreviewed grouped number/date candidates in
a derivative inspection report, not canonical document relations. Explicitly
reviewed `corrects` links remain in catalog metadata. A CreditNote's ID, signs and
references do not establish refund, payment, posting or legal correction effect.
