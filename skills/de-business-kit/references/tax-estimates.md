# Source-led tax estimates and report checks

Use this reference with [tax questions](tax-consultant.md) for estimates and with [forms](forms.md) for return preparation. Keep tax formulas, rate tables, thresholds, rounding algorithms and year-specific field mappings out of package code and reusable templates. Retrieve the applicable rules when needed and use a suitable official calculator or the user's selected accounting/tax software. Do not create an ad hoc tax engine when a calculator is unavailable. Existing decimal totals and reconciliation check recorded money; they do not determine tax treatment.

## Choose the calculation route

Reuse the onboarding accounting choice. With existing software, inspect its exact product, edition, supported tax year and report; preserve its authoritative export instead of maintaining a second ledger. With local accounting, prepare the evidence and inputs for the relevant official form or suitable calculation tool. Choosing local records does not mean this package calculates a statutory return. Do not silently buy, connect or migrate to software. A consultation can proceed without creating a workspace.

There is no assumed universal ELSTER calculator. Inspect the actual form and help: some fields require an amount prepared elsewhere. If a field needs a calculation that the available tool cannot support, identify that gap and prepare the remaining inputs. An ordinary self-accounting task does not require an accountant handoff.

## Find the rule and the appropriate tool

Starting sources checked **2026-10-25**. Retrieve the applicable year again at use; links and current consolidated law do not establish historical applicability. This is a source map, not a stored formula or a claim that a calculator was executed.

| Task | Primary source to retrieve | What to establish before using the output |
| --- | --- | --- |
| Income-tax tariff estimate | [BMF income-tax calculator](https://www.bmf-steuerrechner.de/) and its help; [EStG §32a](https://www.gesetze-im-internet.de/estg/__32a.html) and applicable-year provisions | Select income tax, year and assessment circumstances. The tariff calculator starts with `zu versteuerndes Einkommen`; it does not establish this from business revenue or cash profit, or provide a complete personal liability. |
| UStVA or annual VAT return | [Official ELSTER forms](https://www.elster.de/eportal/formulare-leistungen/alleformulare/), the selected form/year's help; [2026 UStVA instructions](https://www.elster.de/eportal/helpGlobal?themaGlobal=help_ustva_2026) are a dated example | Verify field labels/units, taxable transactions, timing, deductible input VAT, adjustments and rounding in the applicable instructions and selected product. Do not reuse an old Kennziffer table or infer tax from bank totals. |
| Profit / Anlage EÜR | [EStG §4](https://www.gesetze-im-internet.de/estg/__4.html), [§11](https://www.gesetze-im-internet.de/estg/__11.html), selected-year Anlage EÜR and its help through the official form catalogue | Establish method eligibility, complete period coverage and tax adjustments. A cash-movement report is supporting evidence, not a statutory EÜR result. |
| Trade-tax estimate | [GewStG §11](https://www.gesetze-im-internet.de/gewstg/__11.html), [§16](https://www.gesetze-im-internet.de/gewstg/__16.html), application provisions and the actual municipality's official year-specific Hebesatz publication | Establish relevant activity, adjusted base, municipality/year and product support. Do not borrow another municipality's rate or assume current wording applies to an older period. Consider any income-tax interaction separately under its own rules. |
| Product-generated calculation | The selected provider's official help and actual product report for the chosen year | Verify what the edition calculates, data/settings used, exclusions, validation messages and report version. A help page alone does not prove an account feature or a successful calculation. Use [existing-data guidance](existing-data.md) for access. |

For every material rule, retain title, URL, section, retrieval date, effective period and applicability explanation using the existing consultation/source-check records. Read the full relevant source, not just a search snippet. If the source cannot be inspected or rounding/applicability is unclear, mark that point unresolved; do not implement a remembered or inferred formula as a fallback.

## Prepare and estimate

1. Establish the user's question and tax/period. Reuse known facts and request only decisive missing inputs. Distinguish turnover, cash movements, profit, taxable income, VAT and prepayments. Missing information is unknown, not zero.
2. Review the input population and tax treatment. Keep actual records separate from forecast assumptions. Include other relevant activities and personal circumstances only where needed. For VAT, establish Soll/Ist and its evidence separately from EÜR; inspect invoice, supply and payment dates instead of assigning every item to its cash month.
3. Choose a tool that actually supports this question/year. For a forecast, define low/base/high input scenarios only when evidence supports that range; use the same verified tool for each. Do not substitute a universal reserve percentage or model-memory answer.
4. Use nonidentifying inputs in public calculators. Apply privacy and existing authorization before accessing real records in a provider. User handles login/MFA. Record the exact tool/year, inputs, settings and observed output; retain a private export or screenshot where supported. Never say a tool ran if only its help page was read.
5. Compare the result with its input evidence and report scope. Check signs, currency, period, net/gross units, coverage, prepayments and tool warnings. Use a second suitable official/provider result when available; investigate differences in inputs, scope, year and rounding rather than averaging results. Do not claim independent verification if both displays use the same calculation engine.
6. Explain the estimate and what changes it. Separate estimated liability, already-paid amounts and the resulting planning need only when those components are evidenced. State excluded taxes/contributions and the next review trigger. A saved result is an estimate or draft, not an assessment or filing.

If the tool is unavailable, provide the sourced method, prepared inputs and exact steps to obtain the result. Ask for its relevant output if needed; do not invent a number, mark a calculation complete, or stop unrelated document work. A pasted user result is user-supplied until checked; retain that provenance.

## VAT timing example and research limits

[UStG §13](https://www.gesetze-im-internet.de/ustg_1980/__13.html) distinguishes performance and receipt timing, including advance-payment exceptions. [§20](https://www.gesetze-im-internet.de/ustg_1980/__20.html) governs permission for Istversteuerung. EÜR alone does not establish that permission. [§15](https://www.gesetze-im-internet.de/ustg_1980/__15.html) governs input VAT, including completed business supplies, compliant invoice possession, advance-payment conditions and deduction restrictions; the buyer's own Ist choice does not make all input VAT payment-based.

Practical example: a service completed in September, invoiced in October and paid in November cannot be allocated from its bank date alone. Establish the applicable output-tax timing. For a purchase, check when the supply and invoice-possession conditions were met, plus deductibility; invoice issue date is not necessarily receipt date. Preserve the decision and source in the worksheet before using the selected tool. Foreign transactions, mixed/private use, assets, advances, corrections and regime changes need their relevant rules, not a domestic shortcut.

The 2026 UStVA public instructions require whole-euro bases and describe signs and input fields, but this research did not verify exact ERiC calculation/rounding semantics for every case. Do not infer a truncation or negative-rounding algorithm. The BMF-hosted 2026 form PDF returned HTTP 503; a [BMF-issued copy hosted by IHK Ulm](https://www.ihk.de/blueprint/servlet/resource/blob/6936592/fccd966702cb382459b0ed0ecb38cd94/voranmeldung-2026-data.pdf) was visually inspected. Use current official help and the actual year's form/product to resolve calculations. No authenticated calculator, provider account or ELSTER submission was exercised by this source research.

## Preserve the review trail

Use the existing English/Russian consultation template for inputs, rule/tool references, observed result, assumptions, verification status and unresolved differences. If a private workspace exists, preserve a new version with source evidence and the actual tool export; do not replace history. No new calculation registry is needed.

For a return, carry checked values into the existing [form preparation](preparation.md) and [filing evidence workflow](accounting-workflow.md). Recheck affected values after source records or settings change. Saved worksheet/source hashes establish local integrity, not legal correctness, current provider state or a successful tax calculation. Keep submission authorization and receipt tracking separate.
