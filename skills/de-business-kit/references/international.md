# International transactions and reverse charge

Use this module for cross-border purchases/sales, foreign SaaS, reverse charge (including a user's phrase “reverse charges”), foreign customers or payment reporting. Payment reversals/chargebacks also use [payments](payments.md); they are a different question from VAT reverse charge.

## Prepare a transaction, not a country guess

1. Identify the entrepreneur/activity, relevant invoice/service/payment dates and reporting period. Preserve the invoice, contract and any correction. Separate supplier, customer, actual establishment involved, contractual seller, invoice issuer and payment processor. A foreign IBAN, currency, brand or server location does not establish place of supply.
2. Establish goods/services/mixed supply, exact service category, B2B/B2C evidence and intended use, recipient and supplier establishments, own VAT regime and person-wide history. Obtain net/tax/gross and currency from evidence; the worksheet's net amount is not an automatic tax base calculation.
3. For services, test §3a UStG and its exceptions before a general B2B/B2C rule. Property, events/admission, transport, short-term hire, electronic services and certain non-EU consumer services can need different treatment. Goods need separate intra-EU acquisition/distance sale, import/export, customs and import-VAT analysis. Foreign establishments or mixed supplies need focused review.
4. For a qualifying taxable German incoming foreign service, assess §13b and the supplier establishment route. **Kleinunternehmer status does not itself remove recipient liability**, and liability does not establish input-tax deduction. Prepare the calculation only after date, tax base, rate and deduction eligibility are supported.
5. For EU B2B service sales, check recipient status, relevant VAT IDs, invoice requirements and conditional ZM. Check §18a(4) for an entrepreneur applying §19(1); do not automatically demand ZM from every Kleinunternehmer. Non-EU B2B services need place-of-supply and foreign-obligation review, not automatic German tax-free categorization.
6. For consumer sales, identify the service category/location evidence and applicable thresholds or exceptions before evaluating OSS. The foreign EU small-enterprise procedure under §19a is distinct from domestic Kleinunternehmer treatment; do not assume automatic foreign exemption.
7. Record VAT-ID queries as dated evidence: queried IDs, submitted name/address, simple validity vs qualified field results, response/reference and preserved result. `unavailable` is not `invalid`; format checks do not establish validity. Do not copy tax IDs into public fixtures.
8. Assess AWV/Bundesbank reporting separately using resident/nonresident status, transaction purpose, amount, date and exceptions. Under the current §67 snapshot the general threshold is **over EUR 50,000 or equivalent**, with exceptions including specified goods and short-term credit/deposit payments. Netting can matter. Own-account transfers alone do not settle reporting for underlying transactions. Verify the rule and conversion basis for the actual period; do not auto-file from a foreign bank line.

Use `workflows.py template --kind international` and the [preparation contract](preparation.md). Routes are review prompts, not tax classifications. A source check needs the applicable period and local evidence of inspected wording; retrieval date alone does not determine effective law. Keep unresolved treatment open while completing factual work. Separate payment-system FX from VAT conversion under §16(6).

## Before ordering goods from another EU country

Use this check during purchasing, not only at month-end. Give the relevant warning
and next step first; ask only for missing decisive facts. A general question needs
no workspace. These are ordinary-goods checks, not the service/SaaS §13b route.

1. Establish the actual seller, dispatch/destination countries, business use,
   purchaser's VAT regime, dates and any special supply regime. A foreign shop or
   IBAN does not prove cross-border movement or the country of invoice VAT.
2. For an ordinary qualifying acquisition by a German business on
   Regelbesteuerung, check business invoice details and communicate the valid
   German USt-IdNr. to the supplier before the order is finalized. Confirm the
   supplier's intended treatment and retain the order/ID/transport evidence.
   The ID alone does not establish every condition for an exempt
   innergemeinschaftliche Lieferung. Do not invent a completed validity check.
3. Warn that omitting the ID can produce supplier-country VAT that cannot simply
   be deducted in a German USt-Voranmeldung. The German innergemeinschaftlicher
   Erwerb must still be assessed separately; supplier VAT does not remove that
   obligation. Any deduction of German acquisition tax is a different question.
4. **For Kleinunternehmer, do not recommend using the ID merely to buy without
   VAT.** Check eligible status, aggregate relevant EU goods acquisitions in the
   preceding year and expected current year, and any earlier threshold waiver/ID
   use. Under the checked §1a(3)–(4) rules the Erwerbsschwelle is EUR 12,500 in
   each of those tests; use of an issued ID with the supplier counts as a waiver
   binding for at least two calendar years. Merely possessing the ID is different.
   This election is distinct from opting out of the domestic §19 exemption.
   German acquisition VAT can then be due without corresponding input deduction
   for the exempt activity. State this financial consequence even in a short
   warning; mentioning only the threshold or waiver does not explain the risk.
   New vehicles and excise goods have separate rules;
   do not apply this threshold to services or all purchases indiscriminately.
5. For a below-threshold eligible buyer without a waiver, supplier-country VAT
   or German destination VAT under distance-sale rules may apply. Inspect the
   actual facts before challenging it; OSS is a reporting route, not proof of
   an invoice error or a right to deduct. Do not silently make a tax election.

## When an EU goods invoice already includes VAT

1. Preserve the order, original invoice, delivery and payment evidence. Identify
   whose VAT is actually stated, its rate/amount, buyer and seller status, business
   use, transport, relevant dates and whether/when an ID was supplied or obtained.
   Reuse known facts; an invoice rate or seller country alone is not conclusive.
2. Keep **foreign invoice VAT**, **German acquisition VAT** and **deduction
   eligibility** separate. Never copy foreign VAT into ordinary German Vorsteuer
   merely because the purchase is for business or paid. Check German acquisition
   obligations promptly instead of waiting for a supplier correction to settle
   every reporting question. Route services back to the service analysis.
3. For a missing-ID qualifying business acquisition, check correction with the
   supplier under the relevant country's rules. Later communication can permit
   correction with evidence of business capacity/use at acquisition and the other
   supply conditions. Prepare a factual supplier-language request if asked, using
   placeholders for missing invoice/ID details; request review of the correction
   and refund if already paid. Do not promise repayment, invent an issued credit
   note or treat a corrected invoice as observed cash reimbursement.
4. Foreign **Vorsteuervergütung** is a separate conditional procedure, not a cure
   for every no-ID invoice. Check eligibility and exclusions for incorrectly
   invoiced VAT and supplies that qualify/could qualify for intra-EU exemption
   before suggesting an application. The Austrian guidance below expressly
   addresses the missing-ID problem. Do not turn an access failure into a promise
   of reimbursement or a blanket assertion that recovery is forever impossible.
5. Recheck the Kleinunternehmer branch above before advising later ID use or a
   VAT-free correction. German VAT on an eligible distance sale is not foreign
   VAT simply because the seller is abroad; §19 does not confer input deduction.
   If facts change, explicitly replace the earlier recommendation and any draft
   based on it. Preserve old versions and keep the chosen accounting system.
6. End with a useful next action and the unresolved treatment. A proposed
   correction, an issued correction, a refund, an accounting adjustment and a
   filing are distinct events. Save requested notes/drafts through the existing
   document/continuation workflow; no automatic posting, sending or submission.

### EU goods sources and applicability

Checked **2026-10-27** for ordinary goods acquired for a German business in 2026;
refresh for the transaction period, seller country, special regimes and any
subsequent legal developments. These instructions add no tax engine or election.

| Source | Scope and practical consequence |
| --- | --- |
| [UStG §1a](https://www.gesetze-im-internet.de/ustg_1980/__1a.html) | Acquisition conditions, eligible threshold buyers, prior/current-year tests, ID-use election and exceptions |
| [UStG §15](https://www.gesetze-im-internet.de/ustg_1980/__15.html) and [full act fallback](https://www.gesetze-im-internet.de/ustg_1980/BJNR119530979.html#BJNR119530979BJNG001902301) | German acquisition-tax deduction is separate from foreign invoice VAT; deductions for exempt activities are restricted |
| [UStG §3c](https://www.gesetze-im-internet.de/ustg_1980/__3c.html) | Destination VAT and eligible distance-sale recipients; supplier location does not identify invoice VAT |
| [European Commission 2020 Quick Fixes, §§4.3.2–4.3.3](https://taxation-customs.ec.europa.eu/system/files/2021-08/explanatory_notes_2020_quick_fixes_en.pdf#page=73) | Nonbinding guidance for the rules from 2020: omitted ID, separate acquisition taxation and later national invoice correction |
| [Austrian BMF/USP: intra-Community supplies](https://www.usp.gv.at/themen/steuern-finanzen/umsatzsteuer-ueberblick/weitere-informationen-zur-umsatzsteuer/umsaetze-mit-auslandsbezug/ausfuhr-innergemeinschaftliche-lieferung.html) | Austrian administrative guidance, updated 2026-01-01: missing UID prevents exemption/input deduction; later correction needs evidence of business capacity at acquisition; pointers to UStR 2839/3992a |
| [BZSt: foreign EU input-VAT refund](https://online.portal.bzst.de/SharedDocs/Leistungsbeschreibung/DE/weiterleitung_vorsteuerverguetungsantraegen_inlaendischer_antragsteller.html) | Separate application with recipient eligibility; Kleinunternehmer exemption excludes forwarding; not automatic recovery of a missing-ID invoice |

Example: an ordinary Austrian seller dispatches a business monitor to Germany
in October 2026. A Regelbesteuerung buyer omitted an existing valid DE ID and
received Austrian VAT. Do not propose German deduction of that foreign amount;
check supplier correction and German acquisition taxation separately. If the
buyer is instead an eligible Kleinunternehmer below the threshold with no waiver,
do not copy that recommendation into advice to use the ID. First explain the
election and check whether the invoice instead carries German destination VAT.

## Primary sources and applicability

Checked **2026-10-25**. These links support the review framework and current snapshot, not automatic applicability to historical periods. Inspect wording/application provisions for each transaction before recording a conclusion.

| Source | Use and practical consequence |
|---|---|
| [UStG §3a](https://www.gesetze-im-internet.de/ustg_1980/__3a.html) | Place of service and exceptions; an EU address alone does not decide VAT |
| [UStG §13b](https://www.gesetze-im-internet.de/ustg_1980/__13b.html) | Recipient liability; a foreign SaaS purchase by a Kleinunternehmer still needs assessment |
| [UStG §18a](https://www.gesetze-im-internet.de/ustg_1980/__18a.html) | ZM scope including subsection 4; avoid outdated thresholds on explanatory portals |
| [UStG §19a](https://www.gesetze-im-internet.de/ustg_1980/__19a.html) and [BZSt OSS](https://www.bzst.de/DE/Unternehmen/Umsatzsteuer/One-Stop-Shop_EU/one_stop_shop_eu.html) | Separate procedures and eligibility; an EU consumer sale does not automatically select a scheme |
| [BZSt VAT-ID checks](https://online.portal.bzst.de/SharedDocs/Leistungsbeschreibung/DE/gueltigkeit_einer_umsatzsteuer-identifikationsnummer_nach_18_e_UStG.html) | Preserve the actual dated query result, not an invented verified flag |
| [AWV §67](https://www.gesetze-im-internet.de/awv_2013/__67.html) and [Bundesbank payment-reporting FAQ](https://www.bundesbank.de/resource/blob/611818/91551718a7066e282189b917027a4b8b/mL/faqs-zur-awv-zahlungsmeldungen-data.pdf) | Reporting assessment separate from tax and payment processing |
| [UStG §16](https://www.gesetze-im-internet.de/ustg_1980/__16.html) | VAT conversion requires its own supported basis |
