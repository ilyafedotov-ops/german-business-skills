# Working modes

**English** · [Русский](modes.ru.md) · [Project README](../README.md)

Version **0.2.0 preview** provides one portable skill with an explicit focus for each task. Bookkeeping and tax analysis use the same private profile, evidence index and decision history; they do not create separate versions of the business.

## Select a mode and language

| Setting | Purpose |
| --- | --- |
| `general` | Onboarding, registration, provider choice and general administration |
| `bookkeeping` | Documents, proposed entries, payment reconciliation, monthly reporting and handoff |
| `tax-consultant` | Sourced analysis of a concrete tax question, scenarios, calculations and next actions |
| `en` / `ru` | User-facing language and localized Markdown templates |

Choose the initial defaults when creating a new private workspace:

```bash
python3 skills/de-business-kit/scripts/workspace.py init --root /absolute/private-workspace --year 2026 --language en --mode bookkeeping
```

Change saved preferences without reinitializing business data:

```bash
python3 skills/de-business-kit/scripts/workspace.py configure --root /absolute/private-workspace --language en --mode tax-consultant
python3 skills/de-business-kit/scripts/workspace.py status --root /absolute/private-workspace
```

Run these commands from the source checkout or use the installed script's absolute path. On Windows use the installed Python 3 launcher. The initializer requires a new or empty directory; never use it to switch an existing workspace's mode.

Settings are stored in `00_admin/workspace.json`. A clear task request selects the task's mode, and an explicit chat language takes precedence for that task. Persist a new language when the user requests an ongoing change, such as “Use Russian from now on”, or uses `configure`. Reuse an already expressed choice without asking for it again.

Preserve official German labels in both languages. Translate their explanations, not the field identities. JSON keys, status identifiers and internal agent references stay in English for consistent processing. Use `assets/en/` or `assets/ru/` for user-facing Markdown templates; the JSON schemas in `assets/` are shared. Existing `de` settings remain accepted for compatibility.

## Bookkeeping mode

### Purpose

Turn the available receipts, invoices and payment records into an organized, reviewable monthly work package. Continue useful processing while isolating the particular transactions that need clarification.

### Workflow

1. **Establish coverage and responsibility.** Identify the entrepreneur, period, accounts, bookkeeping software, VAT profile and division of work with a bookkeeper or Steuerberater. Save the working agreement in `04_accounting/workflow.md`.
2. **Capture evidence.** Preserve originals, index their provenance and hashes, and store OCR or extracted information separately. Keep document, service and payment dates distinct.
3. **Prepare proposals.** Extract the relevant fields, identify the business purpose, propose categories/tax treatment, and show the source and reason for each uncertain item. Save proposals under `06_bookkeeping/YYYY/MM/proposals/`.
4. **Review exceptions.** Group missing receipts, conflicting information, possible duplicates and tax-sensitive cases into concrete questions. Do not silently turn an unresolved case into an approved entry.
5. **Reconcile payments.** Use verified transaction references and exact decimal arithmetic. The supplied utility compares normalized CSVs; it does not create those references, infer exchanges or post entries. Empty inputs and differences require review.
6. **Report the month.** Record account/statement coverage, reconciled totals, missing evidence, unresolved decisions and observed provider state. Save `06_bookkeeping/YYYY/MM/close.md` using the localized monthly template.
7. **Prepare the handoff.** Build the agreed package under `07_exports/YYYY-MM/`, with a manifest of included/excluded records and remaining questions. Record delivery only when there is actual evidence of delivery.

Use the localized `bookkeeping-workflow.md` and `month-close.md` templates. Keep proposals in the shared `proposal.json` schema, with explanatory text in the selected language. Apply the [bookkeeping reference](../skills/de-business-kit/references/bookkeeping.md) and provider-specific rules, including the [Lexware reference](../skills/de-business-kit/references/lexware.md).

### Example

> Use bookkeeping mode in English for October. My receipts and bank export are in the private workspace. Prepare the workflow agreement, identify missing evidence, propose categories, reconcile verified payment references and produce a monthly report. Explain any transaction that needs a tax decision and prepare a focused question about it.

### Expected result

A month report should state what was processed, what matches, what remains unresolved and what the user or adviser needs to do next. “Amounts match” is a reconciliation result; it does not establish the correctness of every tax decision or the completeness of the entire month's source records.

## Tax-consultant mode

### Purpose

Answer a concrete tax question with a reasoned conclusion grounded in the user's actual facts and current official guidance. Provide usable analysis, including alternatives and calculations where relevant. Identify professional-review needs precisely rather than substituting a general referral for the analysis.

### Workflow

1. **Frame the question.** Identify the decision, relevant tax/year, activities and jurisdiction. Read the necessary existing facts and their evidence; ask only for missing facts that could affect the result.
2. **Check the current rules.** Consult official law and administrative guidance, recording URLs, retrieval/effective dates and applicability. Separate enacted rules from proposals, provider help and assumptions.
3. **State the conclusion.** Explain the likely treatment on the established facts, the rule supporting it and any fact that could change it. Mark a provisional conclusion as provisional.
4. **Compare useful scenarios.** Show how the answer changes under realistic alternative facts or available choices. Include consequences, constraints and what is still unknown.
5. **Calculate transparently.** Define each input, period, rate, basis and rounding method before deterministic calculation. Use supported scripts or inspected calculations; never infer a tax liability from an unexplained model estimate. Do not claim that the package includes a comprehensive tax engine.
6. **Specify review flags.** Identify the actual ambiguity, missing evidence, material election, conflict or exceptional treatment needing review, and formulate a concrete question. Continue unaffected analysis.
7. **Save the consultation.** Use `assets/en/tax-consultation.md` and save a uniquely named document under `05_tax/YYYY/consultations/`. Update linked questions/tasks and record adopted decisions separately from analytical proposals.

For Russian output, use `assets/ru/tax-consultation.md`. The consultation should contain the answer, facts/evidence, source-backed reasoning, calculations or scenarios, uncertainties and next actions. It is an AI analysis workflow, not a claim of licensed Steuerberater status or a binding ruling.

### Example

> Use tax-consultant mode in English. I am adding a new business activity to an existing freelance business. Establish the relevant VAT history and figures, explain which rules apply, compare the available scenarios and document calculations with their assumptions. Save the consultation and list the specific evidence or adviser decision still needed.

## General mode and moving between modes

Use `general` when the user is setting up the business or the next task has not yet been narrowed down. It collects the initial profile, creates a registration route, prepares form worksheets and supports bank/software selection.

A bookkeeping question may reveal a tax issue. Create a linked consultation for that issue, preserve the original proposal and continue processing unaffected documents. A tax consultation may produce a reviewed treatment to apply to future matching transactions; record its scope and effective date before reusing it. Keep a historical decision when later facts change the conclusion.

## What modes do not change

Mode and language settings do not grant tools, change permissions, establish consent to publish private data or authorize filings, contracts or payments. There are no production provider connectors in this preview. Local preparation and analysis remain useful without those connectors; externally observed actions must be recorded only when they actually occur.

Use the shared [workspace](../skills/de-business-kit/references/workspace.md), [privacy](../skills/de-business-kit/references/privacy.md), [German rules](../skills/de-business-kit/references/german-rules.md) and [form workflow](../skills/de-business-kit/references/forms.md) for the relevant task.
