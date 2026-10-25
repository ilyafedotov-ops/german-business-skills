# Payment systems and statement reconciliation

Use for Stripe, PayPal, Wise, bank/PSP statements, payout batches, refunds, disputes, FX and owned-account movements. The executable tools are offline CSV readers. Naming a provider does not imply a connector, eligibility, fee recommendation or known contractual seller.

## Preserve and normalize

Preserve original exports with `workspace.py ingest`; make a separately named normalized derivative. Record the export account, covered period/timezone, whether balances are total/available/reserve, and every source mapping. Use explicit IDs and document links, never amount-only inferred allocation. A payout is a movement from provider to bank, not new revenue. Verify whether the user or a documented Merchant of Record is the contractual seller/invoice issuer. For a MoR, gross end-customer collections are not automatically the user's revenue.

`payments.py template` returns the request contract. Fill `account_id`, `period` (`YYYY-MM`), `balance_basis`, `provider_role`, `coverage_confirmed`, `sources`, optional `bank_path`, and per-currency `balances` with opening/closing decimal strings. `coverage_confirmed` records the operator's statement coverage assessment, not independent verification. Opening/closing values are recorded inputs; preserve their statement evidence. Include all activity and payout sources once. Keep each account and balance basis in a separate run. Never mix available and total balances or count a reserve movement twice.

Supported `sources[].format`:

- `normalized`: CSV columns `event_id,booking_date,kind,amount,currency,related_id,transfer_id,bank_transaction_id`. Amount is a signed effect on the declared balance basis, decimal major units with a dot, no exponent/grouping. Dates are `YYYY-MM-DD`; currencies uppercase. IDs must be unique across all source files.
- `stripe_activity`: a narrow reader for the **itemized balance-change activity** report. Require `balance_transaction_id,created_utc,currency,gross,fee,net,reporting_category,is_managed_payments,withheld_tax`. Accept explicit UTC seconds `YYYY-MM-DD HH:MM:SS`, `YYYY-MM-DDTHH:MM:SS` or the latter with `Z`; the report month is UTC, not automatically the German tax month. Require explicit `is_managed_payments` = `false`/`0` and `withheld_tax` = zero (never blank); request these columns when exporting. Extra columns are retained in the fingerprinted raw source. Optional `source_id`, `charge_id`, `automatic_payout_id` are carried into normalized events. `gross − fee = net` must hold. CSV amounts are major units, not API minor units. Fees become separate balance events; no expense/VAT treatment is assigned.

The Stripe adapter supports only `charge`, `refund`, `refund_failure`, `dispute`, `dispute_reversal`, `fee`. Unknown categories fail with a normalization-review instruction. Managed payments/nonzero withheld tax fail: the report's `fee` can include withheld tax and cannot silently become a processing expense. Preserve the export and prepare a reviewed normalized derivative for such cases. The strict timestamp subset is tested synthetically, not against every live export variant.

**Stripe activity excludes payouts.** Import the separate payout section through a reviewed normalized derivative; its effective date is not the activity creation date. Do not assume `automatic_payout_id` is a bank transaction ID. For automatic payouts inspect the batch report, including earlier activity. Manual/instant payout allocation may not be available; retain balance reconciliation and open allocation questions. No live export fetching or automated payout-section adapter is included.

## Event meanings and checks

| Kinds | Balance sign and follow-up |
|---|---|
| `charge` | Positive; invoice/revenue recognition remains separate |
| `fee`, `refund`, `dispute` | Negative; link `related_id` to event/document evidence (possibly an older period) |
| `fee_reversal`, `refund_reversal`, `dispute_reversal`, `payout_reversal` | Positive; preserve original relationship and reason, never delete the original |
| `payout` | Negative; `bank_transaction_id` must explicitly identify the bank receipt |
| `reserve_hold`, `reserve_release` | Negative/positive only where these affect the chosen statement basis; review separate reserve balances |
| `transfer`, `fx` | Signed legs; retain shared `transfer_id`, account/currency evidence and fees; review both sides |
| `adjustment` | Explicit review required; never an automatic balancing plug |

The report checks only bank rows explicitly referenced by payouts and reports supplied/referenced/unreferenced row counts. It does not reconcile unrelated bank activity; use the existing bank/ledger workflow for that. Bank CSV uses the existing `transaction_id,booking_date,amount,currency` contract. Multiple payout events may group to one explicitly referenced bank receipt. A bank booking can fall in the next month; confirm actual timing and retain unmatched payouts. Unknown links, duplicate IDs, wrong signs, unbalanced currencies and empty/unconfirmed coverage do not become a completed match.

For each currency the report checks **opening + signed events = reported closing**. It then checks explicitly linked payouts against bank amounts/currencies. `arithmetic_matched` describes these numbers only; refund/dispute evidence may still be open. FX, transfers, reserves and adjustments remain review items. FX legs never produce a tax conversion rate automatically. `workflows.py verify` can recheck saved source fingerprints.

Refunds/chargebacks are not the same as VAT reverse charge. Determine actual changes to consideration, collectibility, cancelled supply, correction document and applicable period before a §17 correction. A processor event name does not itself settle VAT, EÜR timing or loss recognition.

## Primary source snapshot

Checked **2026-10-25**, valid as a navigation/format snapshot; recheck changed report schemas and the applicable legal period.

- [Stripe balance report](https://docs.stripe.com/reports/balance): separate activity/payout exports, major units, UTC option and withheld-tax caveat.
- [Stripe balance transaction](https://docs.stripe.com/api/balance_transactions/object), [reporting categories](https://docs.stripe.com/reports/reporting-categories), [report options](https://docs.stripe.com/reports/options) and [payout reconciliation](https://docs.stripe.com/reports/payout-reconciliation): signs, categories, time basis and payout scope.
- [UStG §17](https://www.gesetze-im-internet.de/ustg_1980/__17.html): tax correction depends on underlying facts, not just a chargeback label.
- [UStG §16(6)](https://www.gesetze-im-internet.de/ustg_1980/__16.html): VAT conversion can differ from settlement FX.
