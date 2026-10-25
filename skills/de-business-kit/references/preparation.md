# Structured preparation commands

The assistant handles these commands behind the conversation. Ask for the user's business task and only the next missing facts, not for hand-edited JSON. Use a suitable existing private workspace; privacy/runtime assessment still applies. Scripts are Python 3.9+ standard library and install with the shared skill on Windows/macOS. Use the actual launcher (`python3` or `py -3`) available on the host.

```text
python3 <skill>/scripts/workflows.py template --kind international
python3 <skill>/scripts/workflows.py template --kind classification
python3 <skill>/scripts/workflows.py template --kind elster
python3 <skill>/scripts/workflows.py catalog
python3 <skill>/scripts/workflows.py prepare --root <private-workspace> --kind international --input 00_admin/inbox/case.json
python3 <skill>/scripts/payments.py template
python3 <skill>/scripts/payments.py prepare --root <private-workspace> --input 00_admin/inbox/payments.json
python3 <skill>/scripts/workflows.py verify --root <private-workspace> --report <returned-json-path>
```

Replace placeholders; do not run them literally. Optional `--language en|ru` overrides only that report, otherwise saved preference applies (`de` falls back to English). `template`/`catalog` print public metadata without creating a workspace. Input paths resolve inside the private workspace; parent traversal and symlinks are rejected. Create a new input filename for a revised case instead of overwriting the prior evidence.

## Preparation contract

The generated template is the executable field contract. Keep every key; missing facts are `null`. Provide `record_id`, `period` (`YYYY`, `YYYY-MM`, `YYYY-Q1` through `YYYY-Q4`) and relevant `activity_ids`. These IDs link the case conceptually to the entrepreneur's activities; the command does not certify their registration. `evidence` entries have `id` and a private-workspace `path`. References must resolve to nonempty regular files; mutable profile/register files are not evidence (use a preserved snapshot). Reports save path and SHA-256, raw input, routes and open checks. Originals and the canonical profile remain unchanged.

`source_checks` contains objects with `url`, `checked_on` (`YYYY-MM-DD`), `applicable_period` (exactly the case period), `conclusion` and `evidence_ids`. Preserve the inspected wording/version and applicability note in a local evidence file. A valid URL/date is not independent legal validation; the agent must inspect current/historical primary sources. No silent substitution of today's rules for 2024 facts.

International and classification facts follow their focused references. For an inapplicable text field, record a reason; leave unsupported dates/amounts null and explain the open item. The system does not invent data to make a worksheet complete.

For ELSTER, select a candidate ID from [form-catalog.json](../assets/form-catalog.json), confirm eligibility, live version, recipient, account capability and deadline basis, then enter `fields`:

```json
{"label":"Exact observed German section / field label","value":null,"status":"empty","evidence_ids":[],"reviewer":null,"note":"Why unresolved"}
```

Allowed field states are `empty`, `proposed`, `reviewed`. A reviewed value needs a named reviewer and linked evidence; repeated labels need their observed section/row context. Field values stay strings, including amounts. Record calculations, inputs, rounding and assumptions in `calculation_notes` with evidence references; no automatic complete income/VAT calculation is supplied. Never invent line/Kennziffer numbers. Browser instructions remain in [forms](forms.md).

## Outputs and limits

Each run writes new UUID-named JSON and English/Russian Markdown under `07_exports/<period>/`, plus an audit event. The human report shows facts/form fields or balance arithmetic, review routes and remaining checks; the adjacent JSON retains exact data. `needs_review` identifies missing facts/checks. `ready_for_review` only means supplied preparation fields passed structural checks; the script cannot establish that all legal questions or form fields were supplied. There is **no approved/submitted input state**. `filing_status` is always `not_submitted`.

Payment arithmetic has its own `arithmetic_matched` result, always `tax_status: not_assessed`. No matching result approves revenue recognition, expense deductions or a tax period. Source fingerprint verification detects changed/missing input bytes; it does not certify authenticity, report integrity, archival compliance or continuing legal validity. JSON/report/audit writes are separate, not one filesystem transaction. No live connector, browser control or scheduler is added.
