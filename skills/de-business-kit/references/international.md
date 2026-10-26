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
