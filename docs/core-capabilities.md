# Completing self-managed accounting and tax reporting

[English](core-capabilities.md) | [Русский](core-capabilities.ru.md)

The product goal is that an entrepreneur manages their own accounting and tax reporting. Document preparation is an implemented part of that goal. A complete ledger and ELSTER submission are **unfinished core capabilities**, not optional adviser exports. This plan describes acceptance criteria; it does not claim implementation or a certified process.

| Capability | Current evidence | Required before completion |
| --- | --- | --- |
| Document and review desk | Original catalog, proposals, reviewed bank mapping, reconciliation, generated overview | Continue format/host acceptance and technical e-invoice validation; keep substantive review distinct |
| Accounting ledger | Proposals and comparisons against supplied ledger CSV; no complete posting engine | Define supported bookkeeping methods from the user's facts; stable entries linked to evidence and approval, period/date/currency rules, tax treatment, corrections/reversals without destructive overwrite, balances/totals and year/month controls; prove own-account transfers and PSP payouts do not double-count income; test complete representative periods |
| Tax reporting calculation | Period-specific worksheets and sourced conditional analysis | Supported form/year mappings derived from actual accounting entries, explicit assumptions, reproducible calculations and cross-checks; omissions and unsupported cases visible before approval |
| ELSTER submission | Form worksheets; no implemented authenticated transmission | Verify official supported transport and access requirements, supported forms/year versions, user-controlled authentication, concrete payload preview/approval, technical validation, duplicate prevention, timeout/retry investigation, transmission receipt and correction workflow; test against the supported official environment before live claims |
| Finanzamt follow-up | Preserved letters and tasks; no complete response lifecycle | Link each real response to its submission/period, distinguish receipt from assessment, track objections/corrections and sourced deadlines without inventing legal conclusions or automatic acceptance |

The intended lifecycle is **evidence → proposed treatment → user review/approval → actual accounting entry → return draft → separate submission approval → evidenced submission → authority response and any correction**. A user may perform the unsupported external steps in their chosen system; the assistant can help and preserve inspected results. That is an explicit interim workflow, not evidence that an integration exists.

Build the ledger and form calculations before claiming end-to-end reporting. Develop the submission adapter against a defined supported form/year and official interface, with independent security review of credentials, authorization, duplicate prevention and readback. Keep accountant consultation and archive sharing available for specific needs; neither is a required endpoint or substitutes for these capabilities.
