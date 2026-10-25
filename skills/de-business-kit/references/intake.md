# Staged intake

Collect what the current workflow needs. Do not demand a passport, every tax identifier or all customer invoices at first use. Distinguish a user's own administration from operating an accounting service for other people.

## Stage 0 — establish the workspace and data boundary

Ask/reuse: starting or existing business; country of residence and establishment; natural person or another legal form; chosen private local folder; desired language (English or Russian) and working mode; assistant product and account/plan. Infer the requested mode from a clear task rather than forcing a menu. Record model/provider and local/cloud execution separately in `00_admin/runtime.json`. Apply `privacy.md` before bringing real third-party data into context. No account credentials are required for intake.

Initialize using `workspace.py init --root <private-path> --year <year> --language ru|en --mode general|bookkeeping|tax-consultant`, selecting one value for each option. The CLI retains legacy `de` compatibility; complete user templates are supplied for English and Russian. Unknown facts stay null. Do not populate a demo with the author's or user's remembered personal data. A tax question can be answered before creating a workspace; persistent settings and records become available after initialization.

## Stage 1 — minimum business context

Gather these in small batches:

| Group | Facts | Why |
|---|---|---|
| Activity | Concrete products/services, qualifications where relevant, clients B2B/B2C, countries, employees yes/no | Classification and scope |
| Dates | Preparation, actual commencement, commercial launch, existing registrations | Identify trigger dates without conflation |
| Existing business | All activities of the same person, existing tax/VAT treatment, elections and authority letters | Avoid resetting VAT history |
| Turnover | Previous calendar year actual and current-year forecast across relevant activities; currency; source | Assess applicable questions, not just brand revenue |
| Administration | Municipality, relevant authorities, existing Gewerbe/Finanzamt/ELSTER status | Appropriate registration path |
| Operating needs | Transaction count, cash, currencies, recurring invoices, assets, mixed private use, current services and material risk/coverage needs | Needs-led banking, insurance and service shortlist |
| Work split | User-led responsibilities for categories, reconciliation and submission; existing adviser only if the user involves one | Avoid duplicated or missing work |

Use stable activity IDs and preserve effective dates. The `activities` fact is an array of objects such as `{ "activity_id": "activity-001", "description": null, "classification": "unresolved", "commenced_at": null, "prior_year_turnover_eur": null }`. This is one natural person's profile, not a multi-client database.

## Stage 2 — conditional details

Collect legal name, business address, tax identifiers, bank details and documents only when a specific form or accounting process requires them. Prefer direct user entry of sensitive identifiers in the official form. Store verified references when copying the full identifier is unnecessary. Record prior-year figures as decimal strings, not rounded conversational estimates. Make clear which forecasts are the user's assumptions.

For international trade, collect supply type, customer/supplier country, B2B/B2C and applicable VAT-ID evidence. For regulated trades, qualifications or residence-permission constraints, identify the official authority and the missing evidence; do not silently classify or infer permission. Payroll, corporations, partnerships, insolvency and complex cross-border schemes require a separate workflow.

## Record facts

Use `workspace.py record --root <path> --input <local-answer.json>` for known profile fields. Input example:

```json
{
  "field": "vat_current_regime",
  "value": "unresolved",
  "status": "declared",
  "source": {"kind": "user_statement", "ref": "intake-2026-10-25"},
  "effective_from": null,
  "note": "Need prior election or Finanzamt letter."
}
```

`verified` requires actual evidence supporting the fact, not an AI inference. Keep disputed facts with `needs_review`; never promote them silently. A chat statement can be recorded as `declared`. Do not put secrets in the `note` or `source.ref` fields.

Use `workspace.py entry` for questions/tasks with the [register contract](workspace.md#task-question-and-decision-registers). Put the blocked fact, reason and requested evidence in `title`/`note`; use stable IDs, owner, status and `depends_on`. A due date requires `deadline_source`; completion requires an evidence file. Inspect the current entry hash before updating. A task file is not a scheduled notification.

## Completion

Show a short profile summary, the top missing items and the next useful task. A partially complete profile is usable. Do not block folder setup, evidence collection or general explanations because final tax classification is unresolved.
