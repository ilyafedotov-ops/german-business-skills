# Select banking and accounting providers

Use a requirements-led comparison. This skill prepares recommendations and opening/setup checklists; **v0.2 does not open accounts, buy subscriptions or provide production bank/accounting connectors**. Do not create an application or transmit identity documents as a side effect of comparison.

## Collect requirements before selecting candidates

Read `01_profile/business.json` and the existing accounting workflow. Ask only for missing details that could change the shortlist. Start with eligibility categories, not copies of passports, complete tax identifiers or banking credentials.

| Area | Questions that affect selection |
| --- | --- |
| Business | Legal form, business activity, country of residence/establishment, personal-name versus business-name account |
| Payments | Monthly incoming/outgoing transactions, cards and users, cash, foreign currencies/transfers, direct debits and payment providers |
| Accounting | Bookkeeping method, VAT treatment, typical foreign transactions, e-invoicing, assets, cash, payroll and multiple activities |
| Cooperation | Adviser's preferred product/export, responsibility for capture/posting/submissions, required access roles |
| Integration | Existing banks, required bank feed, CSV fallback, actual API operations, plan eligibility and quotas |
| Practical limits | Budget, contract term, language, support, credit needs, expected growth and migration/export requirements |

Add unresolved eligibility or tax questions to `00_admin/questions.json`. Do not turn an uncertain answer into an assumed eligibility result.

## Bank/account shortlist

Consider these candidates only where the user's needs fit; this is not a ranking:

| Candidate | Current official evidence and check to perform |
| --- | --- |
| N26 Business | Official support describes self-employed/freelance customers operating under their own name. Verify accepted legal form, account-name needs, existing-account rules and current residency/identity-document eligibility. |
| DKB-Business | Product page addresses free professions, healthcare professions, property management and self-employed users. Verify acceptance of the specific business and current application requirements. |
| Qonto | German legal centre identifies a regulated payment institution. Check the actual contract, permitted activities, safeguarding arrangements, fees and integrations for the proposed plan. |
| Finom | German legal page identifies Finom Payments BV as the licensed e-money provider. Check the current German contract and actual entity rather than relying on older partner-bank marketing. |

Distinguish a bank deposit from a payment/e-money account. Describe the actual protection mechanism and any applicable limits using the product's current legal disclosures; do not label every account with a generic deposit-insurance promise. Inspect the German/current-country documents where those govern the account.

Calculate ordinary annual cost from the user's expected volumes: base fee, additional transfers/cards/users, cash, foreign transfers/FX and relevant add-ons. Show introductory offers separately with their expiry and post-offer price. Check VAT treatment of quoted fees rather than applying one blanket assumption.

Do not retain KYC documents in this project. Provide a provider-specific checklist and let the user submit the required identity evidence directly through the legitimate provider process. Keep passwords, TANs and account-opening authentication outside workspace files.

## Accounting shortlist

Start with Lexware Office, sevdesk and Papierkram when appropriate. Retain the user's existing product unless a concrete missing capability justifies comparing migration costs.

| Candidate | Verified API consideration to recheck |
| --- | --- |
| Lexware Office | Current feature page lists Public API from XL. Confirm needed endpoints and exact write semantics; read `lexware.md`. |
| sevdesk | Official help lists REST API in Buchhaltung Pro for German system version 2.0. Confirm the user's version and required operations. |
| Papierkram | Current help documents read/write REST access, beta status and package-dependent credit quotas. Check endpoint coverage and quota costs. |

Compare the actual required workflow, not the presence of a marketing checkbox:

1. Validate representative domestic and foreign transaction types, correction invoices, partial payments, assets and mixed-use items where relevant.
2. Check incoming/outgoing e-invoice formats, validation and export of original XML/hybrid files.
3. Check bank-feed compatibility, reconciliation and a documented fallback for missing feeds.
4. Confirm the adviser's exact export format and responsibilities; a PDF export may not be the required accounting export.
5. Verify API access, quotas, credential model, current product/version and supported draft/final states separately.
6. Examine complete export, cancellation access, migration and retention arrangements.
7. Review the applicable data-processing terms, relevant subprocessors and the proposed data flow.
8. Calculate ordinary total cost including API-eligible tiers, adviser-transfer extras and contract duration. Do not equate a free skills package with free third-party services.

Use synthetic representative transactions to assess a candidate before proposing migration. Do not upload live client invoices merely to compare products.

## Deliver a reviewable decision

Save banking results in `03_banking/comparison.md` and accounting results in `04_accounting/comparison.md`. Include:

- Requirements and user-specific priorities; identify assumptions.
- A candidate matrix with `confirmed`, `not supported` or `not verified` for each material criterion.
- Official source URLs, retrieval date, exact applicable plan/entity and ordinary cost calculation.
- A recommendation with reasons, unresolved blockers and the consequence of choosing each alternative.
- A setup/migration checklist and the next authorized action. Do not claim that opening, purchase, integration or migration has occurred.

Record the selected option and decision date only after the user chooses it or an existing explicit instruction establishes that choice. Keep factual profile values separate from recommendations.

## Official source directory

Checked **2026-10-25**. Revisit these pages at the time of recommendation; do not hardcode prices or permanent eligibility rules.

- [N26 Business eligibility and account name](https://support.n26.com/en-de/memberships-and-account-types/business-accounts/how-does-n26-business-work).
- [DKB-Business product](https://www.dkb.de/geschaeftskunden/konto-anlage/geschaeftskonto).
- [Qonto German legal centre](https://legal.qonto.com/de).
- [Finom German legal documents and provider identity](https://finom.co/de-de/legal-documents/).
- [Lexware Office API eligibility](https://www.lexware.de/funktionen/public-api/).
- [sevdesk API availability](https://hilfe.sevdesk.de/de/articles/9374668-sevdesk-api).
- [sevdesk API reference](https://api.sevdesk.de/).
- [Papierkram REST API, quotas and documentation](https://www.papierkram.de/hilfe/api/).
