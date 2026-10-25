# Completing self-managed accounting and tax reporting

[English](core-capabilities.md) | [Русский](core-capabilities.ru.md)

The product goal is that an entrepreneur manages their own accounting and tax reporting. Document preparation is an implemented part of that goal. A complete ledger and ELSTER submission are **unfinished core capabilities**, not optional adviser exports. This plan describes acceptance criteria; it does not claim implementation or a certified process.

The welcome dialog now saves **local versus existing-software accounting** without a default; see [the accounting workflow](accounting.md). Implemented foundations include an evidence-linked local cash journal with duplicate checks and preserved corrections, period cash summaries/account reconciliation CSVs, and frozen filing versions with reviewed authorization, uncertain-attempt protection, manually evidenced receipts and separate authority responses. These are working local capabilities, not complete statutory accounting or live transmission. Existing software stays authoritative on the external route.

| Capability | Current evidence | Required before completion |
| --- | --- | --- |
| Document and review desk | Original catalog, proposals, reviewed bank mapping, reconciliation, generated overview | Continue format/host acceptance and technical e-invoice validation; keep substantive review distinct |
| Accounting ledger | Reviewed local cash journal for explicitly selected EÜR, splits, duplicate prevention, reversals/corrections and per-account CSV; external route blocks local postings | Complete statutory treatment, asset/noncash adjustments, balances/closing rules and complete representative periods; method eligibility is not inferred |
| Tax reporting calculation | Period-specific worksheets and sourced conditional analysis | Supported form/year mappings derived from actual accounting entries, explicit assumptions, reproducible calculations and cross-checks; omissions and unsupported cases visible before approval |
| ELSTER submission | Form worksheets; no implemented authenticated transmission | Verify official supported transport and access requirements, supported forms/year versions, user-controlled authentication, concrete payload preview/approval, technical validation, duplicate prevention, timeout/retry investigation, transmission receipt and correction workflow; test against the supported official environment before live claims |
| Finanzamt follow-up | Observed responses and supplied deadlines linked to frozen filing versions; receipt and authority outcome remain separate | Live response retrieval, complete objections/corrections workflow and separately sourced deadline calculation; reminders require an actual scheduler |

The intended lifecycle is **evidence → proposed treatment → user review/approval → actual accounting entry → return draft → separate submission approval → evidenced submission → authority response and any correction**. A user may perform the unsupported external steps in their chosen system; the assistant can help and preserve inspected results. That is an explicit interim workflow, not evidence that an integration exists.

Build the ledger and form calculations before claiming end-to-end reporting. Develop the submission adapter against a defined supported form/year and official interface, with independent security review of credentials, authorization, duplicate prevention and readback. Keep accountant consultation and archive sharing available for specific needs; neither is a required endpoint or substitutes for these capabilities.
