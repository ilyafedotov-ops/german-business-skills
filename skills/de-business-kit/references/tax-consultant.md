# Tax questions and preparation

Use mode ID `tax-consultant` for sourced tax explanations, comparisons, estimates and proposed treatment of the user's own German sole-trader business. Give a useful answer to the actual question, with a clear conclusion and the facts that could change it. This workflow provides decision support; it does not confer the professional status of a Steuerberater or authority to represent the user.

Use the active English or Russian language for the answer and saved report. Preserve official German legal terms and form labels, explaining them on first use. Switching language or mode changes the workflow preference, never the entrepreneur's tax status, facts or existing decisions.

## Establish the question and minimum facts

1. Identify the exact question, tax year or transaction period, entrepreneur and affected activity. Reuse the private profile, previous decisions and relevant questions. A consultation can proceed in chat without creating a workspace when no storage location has been selected.
2. Gather only missing facts that can change the answer; ask at most three related questions at once. Separate `declared`, evidence-confirmed and assumed inputs. Do not turn a conversational estimate into a verified amount.
3. Keep legal form, activity classification, VAT regime and profit determination separate. For a second business or brand, inspect the same person's existing VAT history and other activities before considering a new choice.
4. Identify the practical outcome: understand an obligation, compare permitted options, estimate an amount, assess a particular receipt, prepare a form, or formulate a question for a Steuerberater. Permission to analyse does not itself authorize an election, posting, filing or payment.

| Question | Facts to establish before an individual conclusion |
|---|---|
| Kleinunternehmer / Regelbesteuerung | Existing treatment and elections; dates; relevant turnover across the entrepreneur's activities; applicable year; planned customers and input costs |
| Expense / asset / mixed use | Actual business purpose; invoice and payment evidence; business/private use; acquisition and use dates; prior treatment; VAT deduction question separately |
| Foreign invoice or sale | Type of supply; supplier/customer establishment; B2B/B2C; relevant VAT-ID evidence; invoice tax; service and payment dates |
| Income-tax estimate / reserve | Profit basis, other relevant income, deductions and assessment circumstances; period; prepayments; which taxes and social contributions are included or excluded |
| Trade tax / classification | Actual activity, legal form, municipality, year and existing authority treatment; avoid deciding from a job title or brand alone |
| Letter / deadline / correction | Exact document, notification and receipt evidence, affected period, action requested and any prior submissions; inspect the specific deadline rule |

Do not request a complete personal financial history for a narrow VAT question. Read only necessary evidence and apply `privacy.md` before processing real third-party personal data.

## Research the rule that applies

Read `german-rules.md` as a source map, then retrieve the relevant official source for this task. Prefer the statute and its application provisions, BMF or state tax-administration guidance, current ELSTER help and the competent authority's current procedure. Use provider documentation for product behavior. A search snippet alone is insufficient for a material tax conclusion when the full source is available.

Record the source title, URL, precise provision or section, retrieval date, publication/update date if available, effective period and why it applies. Use `assets/source-check.json` for reusable checks. A new publication date does not necessarily mean that the rule applies to an older tax year. If current and historic wording differ, identify the relevant version explicitly.

Distinguish what the source states from the application or inference made from the user's facts. Cite the source near the supported claim. If authoritative information cannot be retrieved, state which point remains unverified, offer conditional scenarios and continue factual preparation. Do not invent quotations, paragraph numbers, deadlines or successful source checks.

## Explain, compare and calculate

Lead with the answer or the narrow unresolved decision. Explain the rule in plain language, show how it applies to the known facts, and identify the decisive assumption. Give a recommendation when the evidence supports it; do not substitute an unranked list of every theoretical option.

For choices, compare eligibility, expected tax effect, cash flow, administrative work, evidence requirements and any binding period or reversal consequences. Keep lawful planning separate from an election: a recommendation is not a filed waiver or approved change. Explain which fact would change the recommendation.

Calculate amounts with deterministic decimal arithmetic or an appropriate verified official calculator. Record inputs, currency, year, formula/rule version, rounding and output. Use the actual relevant tax base. Revenue, bank receipts, business profit, `zu versteuerndes Einkommen` and VAT are distinct. EÜR eligibility and adjustments require their own assessment; a bank total is not an EÜR.

For income tax, use the applicable year's rules and assessment circumstances. The BMF income-tax calculator derives tariff tax from an entered `zu versteuerndes Einkommen`; it does not establish that input or a complete personal liability. Separate income tax, VAT, trade tax, surcharges, prepayments and social contributions as relevant. Do not add them twice or assume that a business-only profit figure is the person's taxable income. Avoid a universal “save X%” rule; a cash reserve can be a labelled scenario based on stated assumptions, with exclusions and a review trigger.

Do not upload identifying financial details to a public calculator. An available local implementation or nonidentifying scenario can establish the arithmetic. Do not claim an official calculator or tool was run unless it actually was. This package bundles no income-tax engine.

## Apply the outcome to bookkeeping or forms

For a receipt, link the consultation ID, source checks and necessary factual conditions in the existing proposal. Keep extracted amounts separate from proposed category and tax treatment. Leave review state unapproved until there is an actual reviewer decision; do not mark the provider record posted or change historical evidence. A reusable treatment rule needs a defined scope, effective period, evidence and reviewer reference, and must be reconsidered for materially different facts.

For a form, hand over to `forms.md` with proposed field values and evidence. Preserve exact German field labels. Check the scope of existing authorization for the concrete recipient, period, action and payload before any external mutation. Finish the reviewable draft first; resolve only missing authorization at the action boundary. Do not repeat a confirmation already supplied for that exact operation. Record transmission evidence separately from substantive authority acceptance.

## Resolve uncertainty without stopping useful work

Name the specific review issue and the evidence needed. For example: a prior VAT waiver cannot be located; mixed activity classification is disputed; a foreign establishment affects tax residence; a material correction concerns already filed returns; an objection deadline is near; payroll, a corporation or a partnership falls outside this release's scope. Prepare the relevant facts, document references and precise questions for the appropriate Steuerberater or authority. Continue unaffected extraction, arithmetic, draft preparation and organization.

Do not redirect every ordinary tax explanation to a professional. Do not imply that a disclaimer, a free licence or the mode name establishes permission to offer individual tax services to other people. If the user intends to operate a service for third parties, distinguish that operating model from using the software for their own affairs and route its professional-law question for qualified review.

## Save and finish

Use [English consultation template](../assets/en/tax-consultation.md) or [Russian consultation template](../assets/ru/tax-consultation.md). Fill only applicable sections; remove irrelevant empty tables. Save a material consultation as `05_tax/YYYY/consultations/YYYY-MM-DD-<opaque-id>.md` inside the selected private workspace. Create directories as needed without following symlinks or overwriting existing files. Do not write private reports into the skill installation or source repository.

Include the question, known facts and evidence, assumptions, conclusion, sources and dates, any calculation, options, precise review issues and next action. Preserve consultation IDs when changing language. A translated copy is another rendering of the same analysis, not a new tax decision. A later substantive correction should reference the earlier report instead of erasing it.

Link unresolved questions or an actual decision with the `entry` command and [register contract](workspace.md#task-question-and-decision-registers). Preserve existing records and use the current entry hash for updates. Store concise user-facing conclusions and evidence, not hidden reasoning or complete chats. A draft conclusion must not silently become a `verified` profile fact or an approved decision.

End the chat with the result, its practical effect, what remains unresolved and the next concrete action. If a saved report exists, identify it. If no report was saved or no external operation occurred, do not imply otherwise.

## Verified primary starting sources

Checked **2026-10-25**. Recheck the rule and applicable period when using it; the check date is not a guarantee for future consultations.

- [UStG §2](https://www.gesetze-im-internet.de/ustg_1980/__2.html): the VAT enterprise includes the entrepreneur's entire commercial and professional activity.
- [EStG §4](https://www.gesetze-im-internet.de/estg/__4.html): profit determination, conditional EÜR eligibility and business-expense rules; payment arithmetic alone does not settle them.
- [EStG §32a](https://www.gesetze-im-internet.de/estg/__32a.html): year-specific income-tax tariff, assessment and rounding rules; check application provisions for the actual year.
- [BMF tax calculator](https://www.bmf-steuerrechner.de/): distinguish tariff tax on taxable income from establishing a person's full tax liability.
- [StBerG §2](https://www.gesetze-im-internet.de/stberg/__2.html) and [§6](https://www.gesetze-im-internet.de/stberg/__6.html): current professional-law framework, including paid/unpaid assistance, the limited mechanical-work exclusion and conditional exceptions. Assess any service to others under its actual operating model; the software's label or price does not resolve that question.
