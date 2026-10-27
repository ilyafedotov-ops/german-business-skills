# Source-led calculations, estimates and report checks

Use this reference with [tax questions](tax-consultant.md), accounting work and
[forms](forms.md). Apply the shared prerequisite checks first: establish the
requested amount, applicable period, relevant confirmed facts and missing inputs.
Calculations are allowed when their rules, inputs and scope are established.
There is no bundled complete statutory tax engine. Keep year-specific formulas,
rates, thresholds and field mappings out of reusable package code/templates;
research them for the particular case and retain the method in its private record.
Local decimal totals alone do not determine tax treatment.

## Choose the calculation route

Reuse the onboarding accounting choice. With existing software, inspect its exact product, edition, supported tax year and report; preserve its authoritative export instead of maintaining a second ledger. With local accounting, prepare the evidence and inputs for the relevant official form or a supported calculation route below. Choosing local records does not mean this package calculates a statutory return. Do not silently buy, connect or migrate to software. A consultation can proceed without creating a workspace.

Prefer an appropriate official calculator or the user's selected software when it
covers the question and year. A **bounded local calculation** is also allowed:
retrieve and check the applicable formula, conditions, units and rounding; execute
it with available arithmetic tools; independently verify it as below. This can
support an estimate, a component calculation or a check of another result. Do not
turn a case-specific script into a maintained general tax engine, silently replace
the chosen ledger or claim that one component proves a complete return.

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

For every material rule, retain title, URL, section, retrieval date, effective period and applicability explanation using the existing consultation/source-check records. Read the full relevant source, not just a search snippet. Use the [primary-source recovery sequence](german-rules.md#recover-an-unavailable-primary-source) when a page fails. If the relevant text still cannot be inspected or rounding/applicability is unclear, mark that point unresolved; do not implement a remembered or inferred formula as a fallback.

## Research, calculate and independently check

1. **Establish sufficient inputs.** Identify the question, tax/transaction period,
   currency, units, basis and scope. Reuse confirmed facts and ask only decisive
   follow-ups. Distinguish turnover, gross/net receipts, profit, taxable income,
   VAT and prepayments. Missing information is unknown, not zero. Identify whether
   the user wants a factual result or a scenario. A scenario may use explicitly
   stated assumptions; it must not become a confirmed profile fact.
2. **Validate applicability before arithmetic.** Review source coverage, treatment,
   other relevant activities and necessary assessment circumstances. For VAT,
   establish Soll/Ist separately from EÜR and inspect invoice, supply and payment
   dates. Research current primary sources for the **applicable period**, including
   historical provisions, exceptions, thresholds, units, intermediate operations
   and rounding. Record exact sections and dates. Do not calculate a tax amount from
   remembered rules, a snippet, user assertions about the law or a current-year
   formula applied to another year. Where a condition is unknown, ask or label a
   conditional illustration; do not imply the condition was established.
3. **Specify the method.** Name the actual official/provider tool and supported
   year/settings, or derive a bounded formula from the inspected rules. Map every
   input to its source or explicit assumption. Distinguish a formula stated in law
   from algebra derived from it. For piecewise rules, show the selected branch and
   boundary conditions. Keep the method and any small script with the case evidence,
   outside installed skills; no new ledger, calculation service or registry.
4. **Execute reproducibly.** Use an available calculator or deterministic executable
   arithmetic, with decimal or exact rational values and the sourced rounding order.
   Avoid binary-float money arithmetic and mental/model-only numerical answers.
   Save inputs, tool/code and version where available, settings, execution output,
   intermediate values and final result. Never say a tool ran when only its help
   page was read. Use nonidentifying inputs in public tools; privacy, account access
   and external-action authorization still apply.
5. **Check separately before calling it checked.** Check both legal applicability
   and numerical execution. When supported, use a separate reviewer agent for a
   bounded read-only check of sources, effective period, input completeness and
   independently derived result. Give the reviewer the question, source evidence
   and inputs, withhold the first numerical answer until it has derived its own,
   then compare. An agent's agreement alone is not mathematical verification:
   require actual execution or a suitable independent published/tool result.
   Alternatives include an independently operated appropriate official/provider
   calculator, or a separately derived and executed method plus published known
   answers and boundary/reverse checks appropriate to the calculation. Record who
   or what checked which aspect, actual results and evidence. Re-running the same
   script, displaying the same engine twice or saying “double-checked” is not an
   independent check. If no independent route is available, label the calculation
   **computed, independently unverified**, explain the missing check and do not
   present it as filing-ready. Never fabricate a second reviewer or tool execution.
6. **Investigate discrepancies.** Compare year, source version, inputs, signs,
   gross/net units, scope, piecewise boundaries and rounding. Use exact agreement
   where required; any tolerance needs a sourced rounding explanation, not a
   convenient default. Do not average answers. A disagreement or unverified
   material rule blocks a checked conclusion for the affected amount, not unrelated
   preparation. Preserve the differing outputs and next diagnostic step.
7. **Report and preserve.** Give the answer with its scope, assumptions, sources,
   execution and check status. Separate estimated liability, prepayments and cash
   planning; state exclusions and what would change the result. Preserve inputs and
   effective dates in the existing consultation/task record through validated
   writers where required. Changed facts, sources or settings invalidate affected
   calculations and checks; recalculate a new version without erasing the old one.

When a rule, necessary input or executable tool is unavailable, prepare the sourced
method and missing-information questions; leave the dependent amount unresolved.
If only the independent check is unavailable, an actually computed provisional
amount may be shown with that limitation. A pasted user result remains
user-supplied until checked. Useful preparation continues without compulsory
software purchases, a GUI or an accountant handoff. A checked component or estimate
is not a tax assessment, complete statutory return, posting or submission.

## VAT timing example and research limits

[UStG §13](https://www.gesetze-im-internet.de/ustg_1980/__13.html) distinguishes performance and receipt timing, including advance-payment exceptions. [§20](https://www.gesetze-im-internet.de/ustg_1980/__20.html) governs permission for Istversteuerung. EÜR alone does not establish that permission. [§15](https://www.gesetze-im-internet.de/ustg_1980/__15.html) governs input VAT, including completed business supplies, compliant invoice possession, advance-payment conditions and deduction restrictions; the buyer's own Ist choice does not make all input VAT payment-based.

Practical example: a service completed in September, invoiced in October and paid in November cannot be allocated from its bank date alone. Establish the applicable output-tax timing. For a purchase, check when the supply and invoice-possession conditions were met, plus deductibility; invoice issue date is not necessarily receipt date. Preserve the decision and source in the worksheet before using the selected tool. Foreign transactions, mixed/private use, assets, advances, corrections and regime changes need their relevant rules, not a domestic shortcut.

The 2026 UStVA public instructions require whole-euro bases and describe signs and input fields, but this research did not verify exact ERiC calculation/rounding semantics for every case. Do not infer a truncation or negative-rounding algorithm. The BMF-hosted 2026 form PDF returned HTTP 503; a [BMF-issued copy hosted by IHK Ulm](https://www.ihk.de/blueprint/servlet/resource/blob/6936592/fccd966702cb382459b0ed0ecb38cd94/voranmeldung-2026-data.pdf) was visually inspected. Use current official help and the actual year's form/product to resolve calculations. No authenticated calculator, provider account or ELSTER submission was exercised by this source research.

## Preserve the review trail

Use the existing English/Russian consultation template for input readiness, rule/method/tool references, actual execution, assumptions, independent check evidence and unresolved differences. If a private workspace exists, preserve a new version with source evidence and the actual tool export; do not replace history. No new calculation registry is needed.

For a return, carry checked values into the existing [form preparation](preparation.md) and [filing evidence workflow](accounting-workflow.md). Recheck affected values after source records or settings change. Saved worksheet/source hashes establish local integrity, not legal correctness, current provider state or a successful tax calculation. Keep submission authorization and receipt tracking separate.

## Calculation-validation source examples — 2026-10-26

The following inspected sources support synthetic validation of the workflow,
not permanent package constants. Recheck applicability and current wording at use.

- [Rheinland-Pfalz Finance Ministry FAQ, Umsatzsteuer question 2](https://fm.rlp.de/themen/steuerrecht/fragen-und-antworten/seite)
  supplies a gross/net VAT example and a published expected answer for comparison.
- [UStG §§10, 12 and 28](https://www.gesetze-im-internet.de/ustg_1980/BJNR119530979.html)
  distinguish consideration, applicable rates and the temporary 2020 period. The
  practical test is that a historical transaction must not inherit today's rate.
- [BMF current UStAE, section 14.5(20)](https://www.bundesfinanzministerium.de/UStAE),
  inspected in its [official consolidated PDF](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/Umsatzsteuer-Anwendungserlass/Umsatzsteuer-Anwendungserlass-aktuell.pdf?__blob=publicationFile&v=52)
  headed **Stand 2. Juni 2026**, specifies invoice-tax cent rounding. If the HTML
  handbook is inaccessible, inspect this official alternative with available PDF
  tools and check its actual version; an indexed snippet or older edition alone
  cannot establish the requested period. Test both sides of a rounding boundary. This source
  does not establish all UStVA field, negative-correction or intermediate rounding.

Source/arithmetic examples are not desktop acceptance, live provider verification,
complete tax correctness or a substitute for the actual case's independent check.
