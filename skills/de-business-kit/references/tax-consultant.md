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
| Expense / asset / mixed use | Actual business purpose; purchase/financing versus rental contract; full acquisition cost and invoice VAT; delivery/acquisition year and month; business/private use; profit-determination method; prior treatment; VAT deduction question separately |
| Foreign invoice or sale | Type of supply; supplier/customer establishment; B2B/B2C; relevant VAT-ID evidence; invoice tax; service and payment dates |
| Income-tax estimate / reserve | Profit basis, other relevant income, deductions and assessment circumstances; period; prepayments; which taxes and social contributions are included or excluded |
| Trade tax / classification | Actual activity, legal form, municipality, year and existing authority treatment; avoid deciding from a job title or brand alone |
| Letter / deadline / correction | Exact document, notification and receipt evidence, affected period, action requested and any prior submissions; inspect the specific deadline rule |

Do not request a complete personal financial history for a narrow VAT question. Read only necessary evidence and apply `privacy.md` before processing real third-party personal data.

## Research the rule that applies

Read `german-rules.md` as a source map, then retrieve the relevant official source for this task. Prefer the statute and its application provisions, BMF or state tax-administration guidance, current ELSTER help and the competent authority's current procedure. Use provider documentation for product behavior. Apply its [source recovery sequence](german-rules.md#recover-an-unavailable-primary-source) before leaving a failed link unresolved. A search snippet alone does not establish a material tax conclusion.

Record the source title, URL, precise provision or section, retrieval date, publication/update date if available, effective period and why it applies. Use `assets/source-check.json` for reusable checks. A new publication date does not necessarily mean that the rule applies to an older tax year. If current and historic wording differ, identify the relevant version explicitly.

Distinguish what the source states from the application or inference made from the user's facts. Cite the source near the supported claim. If authoritative information cannot be retrieved, state which point remains unverified, offer conditional scenarios and continue factual preparation. Do not invent quotations, paragraph numbers, deadlines or successful source checks.

## Explain, compare and estimate

Lead with the answer or the narrow unresolved decision. Explain the rule in plain language, show how it applies to the known facts, and identify the decisive assumption. Give a recommendation when the evidence supports it; do not substitute an unranked list of every theoretical option.

For an ordinary first question, give the direct answer, a short practical explanation and only the exceptions that could materially change it. Keep citations next to the supported claims. Do not expand into an exhaustive catalogue of elections or a full report unless requested. End with at most three grouped questions needed for the next concrete step; a conceptual answer can proceed conditionally before those details are known. Before choosing dated rules, preparing entries or calculating an amount, confirm the transaction year/month and accounting method rather than silently using the current year or assuming EÜR. For financed assets, distinguish the acquisition from repayments, financing costs and any bundled service; retrieve the applicable asset and VAT rules instead of deriving the treatment from the payment schedule.

For choices, compare eligibility, expected tax effect, cash flow, administrative work, evidence requirements and any binding period or reversal consequences. Keep lawful planning separate from an election: a recommendation is not a filed waiver or approved change. Explain which fact would change the recommendation.

Follow [source-led calculations and checks](tax-estimates.md). Once the prerequisites
are sufficient, use a suitable official/provider tool or a bounded local calculation
based on newly inspected applicable rules. Record the case-specific formula,
inputs, currency, year, rule source, actual execution, rounding and independent
check. Keep year-specific tax formulas out of reusable package code/templates;
this is not a general tax engine. Existing decimal totals check recorded money,
not tax treatment. Revenue, bank receipts, profit, `zu versteuerndes Einkommen`
and VAT remain distinct; cash totals alone do not establish EÜR or taxable income.

For income tax, use the applicable year's rules and assessment circumstances. The BMF income-tax calculator derives tariff tax from an entered `zu versteuerndes Einkommen`; it does not establish that input or a complete personal liability. Separate income tax, VAT, trade tax, surcharges, prepayments and social contributions as relevant. Do not add them twice or assume that a business-only profit figure is the person's taxable income. Avoid a universal “save X%” rule; a cash reserve can be a labelled scenario based on stated assumptions, with exclusions and a review trigger.

Do not upload identifying financial details to a public calculator. Use nonidentifying scenarios or the selected software within its verified scope. Do not claim a calculator or tool was run unless it actually was. When an official/provider tool is unavailable, assess the bounded local route in `tax-estimates.md`. Leave amounts unresolved when necessary inputs, applicable rules or executable arithmetic are unavailable; label missing independent verification explicitly. This package bundles no tax calculation engine.

## Apply the outcome to bookkeeping or forms

For a receipt, link the consultation ID, source checks and necessary factual conditions in the existing proposal. Keep extracted amounts separate from proposed category and tax treatment. Leave review state unapproved until there is an actual reviewer decision; do not mark the provider record posted or change historical evidence. A reusable treatment rule needs a defined scope, effective period, evidence and reviewer reference, and must be reconsidered for materially different facts.

For a form, hand over to `forms.md` with proposed field values and evidence. Preserve exact German field labels. Check the scope of existing authorization for the concrete recipient, period, action and payload before any external mutation. Finish the reviewable draft first; resolve only missing authorization at the action boundary. Do not repeat a confirmation already supplied for that exact operation. Record transmission evidence separately from substantive authority acceptance.

## Prepare or revise an income-tax prepayment request

For “reduce my tax prepayments”, first identify the tax and year. This route covers
preparation of an **Einkommensteuer-Vorauszahlungen** adjustment; do not apply it
unchanged to VAT, trade tax or other taxes. Use [correspondence](correspondence.md)
for recipient/private separation and [continuation](continuation.md) for saving.

1. **Read the existing case.** Inspect the current notice (or label the user's
   summary), its instalments and dates, actual credited payments/refunds, relevant
   forecast and prior requests/responses. Establish whether a changed notice,
   deferral or suspension exists. Reuse known facts; identity placeholders do not
   block preparing a draft. A request for preparation does not authorize sending.
2. **Establish the forecast's basis.** Separate expected annual income tax after
   creditable withholding but before prepayments from profit, revenue and the
   amount still payable. If that annual tax is already supplied, retain its
   provenance and uncertainty; do not invent a tariff derivation or ask for a full
   tax history just to subtract known credits. If it must be derived, use the
   source-led calculation workflow first. Keep other taxes separate.
3. **Inspect applicable rules and route.** Retrieve EStG §37, AO §124 and current
   ELSTER help linked below using the source-recovery sequence. Check the specific
   year and requested adjustment. Prefer the dedicated **Antrag auf Anpassung von
   Vorauszahlungen** when appropriate. A German explanation is draft text for that
   route, not an official payload or proof that portal fields were inspected.
4. **Compute a proposal, not an assessment.** Execute the bounded reconciliation
   of the supported annual forecast and credited prepayments. Show the current
   assessed instalment alongside the requested change and its assumptions. Apply
   the independent-check requirements in `tax-estimates.md`; retain actual code or
   tool output. Do not automatically spread a difference across several remaining
   dates, round an amount, request a negative instalment or promise a refund.
   Overpayments, missing credits and multiple remaining instalments need their
   specific treatment checked. The current notice remains the basis for payment
   unless effective changed assessment or other applicable relief is evidenced.
5. **Save and inspect the actual package.** When durable files are requested, use
   the already selected private location. In a managed workspace resolve logical
   tax/correspondence folders with `folders`; otherwise use the selected private
   folder without forcing initialization. Create a new case/version directory
   without symlinks or overwriting existing files. Save:
   - German recipient draft with period, proposed adjustment, supported reason and
     explicit missing identity/reference fields; no private paths or review notes;
   - separate EN/RU private review with current versus requested amounts, input and
     source references, actual arithmetic/check status, missing facts, selected
     route and exact external-action state;
   - calculation evidence and source/input versions needed to reproduce it, plus
     continuation details in that review: case ID, output filenames, prior version
     if any, open items, authorization scope and one next action.
   Link preserved originals instead of copying unrelated records. List only actual
   selected attachments; never attach the private review by default. Reopen saved
   files and compare their amounts, period, audience and draft status before
   reporting success. If a write fails, report the unsaved part explicitly.
6. **Resume from files.** Read the saved review and referenced evidence in a fresh
   session. A corrected forecast invalidates the affected draft, calculation and
   check. Preserve their bytes, create a linked revision, recompute and inspect its
   actual files. The new review identifies which earlier proposal it supersedes;
   keep submission/authority state separate. A changed estimate or transmission
   receipt never becomes an amended notice. Update an existing task only through
   its validated writer and current expected hash; if unavailable, state the
   unsaved task update in the readable continuation note. No parallel register.

Primary starting sources checked **2026-10-27** for this preparation route:
[EStG §37](https://www.gesetze-im-internet.de/estg/__37.html),
[AO §124](https://www.gesetze-im-internet.de/ao_1977/__124.html),
[ELSTER request](https://www.elster.de/eportal/formulare-leistungen/alleformulare/eingvorauszlg)
and [public help](https://www.elster.de/elsterweb/helpGlobal?themaGlobal=help_eing_vorauszlg).
Recheck at use. Synthetic example: an annual forecast of €2,000 after withholding
and before prepayments, €1,800 credited and one remaining assessed instalment of
€600 gives a requested remainder of €200. A corrected €2,300 forecast gives €500;
both remain proposals while the unchanged notice calls for €600. These figures
illustrate reconciliation, not a reusable tax formula or a guaranteed decision.

## Resolve uncertainty without stopping useful work

Name the specific review issue and the evidence needed. For example: a prior VAT waiver cannot be located; mixed activity classification is disputed; a foreign establishment affects tax residence; a material correction concerns already filed returns; an objection deadline is near; payroll, a corporation or a partnership falls outside this release's scope. Prepare the relevant facts, document references and precise questions for the appropriate Steuerberater or authority. Continue unaffected extraction, arithmetic, draft preparation and organization.

Do not redirect every ordinary tax explanation to a professional. Do not imply that a disclaimer, a free licence or the mode name establishes permission to offer individual tax services to other people. If the user intends to operate a service for third parties, distinguish that operating model from using the software for their own affairs and route its professional-law question for qualified review.

## Save and finish

Use [English consultation template](../assets/en/tax-consultation.md) or [Russian consultation template](../assets/ru/tax-consultation.md). Fill only applicable sections; remove irrelevant empty tables. In a managed workspace, resolve the logical `05_tax/YYYY/consultations/` destination with `folders` before saving a new `YYYY-MM-DD-<opaque-id>.md` report or case directory. For a selected private folder without managed records, follow [standalone continuation](continuation.md#without-a-workspace). Create directories as needed without following symlinks or overwriting existing files. Do not write private reports into the skill installation or source repository.

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
