# Verify an access route for one concrete operation

Use with [existing data](existing-data.md) and [data-source access](data-source-access.md).
The bundle contains no production banking/accounting/ELSTER connector or scheduler.
This workflow uses tools actually supplied by the host and authorized for the task.
For selecting/setup of a practical route and executing a browser/desktop draft,
use [assisted service operations](assisted-services.md). Work through available
authorized tools; missing API access does not preclude browser help. Record the
exact manual/user-held boundary and verify any later result.
Use the [EN operation note](../assets/en/connection-check.md) or
[RU operation note](../assets/ru/connection-check.md) for a durable check. Keep
provider observations distinct from user-supplied files and simulated test outcomes.

1. Identify the requested operation, exact service/product/edition, account or
   workspace, source of truth and necessary data scope. Reuse known facts.
2. Inventory available connector/API/browser/file tools before asking the user
   for information they can provide. A visible plugin or API document is not
   proof of credentials, permissions, supported write operations or current access.
   When interaction is needed but unavailable, recommend the supported task-specific
   setup under [interaction tools](assisted-services.md#recommend-interaction-tools-only-when-useful),
   including suitability limits and a useful manual/file alternative.
3. Read the provider's current official operation/format documentation. Establish
   authentication, permission scope, supported versions, limits and output format.
   Apply the [cost check before setup](assisted-services.md#check-costs-before-setup)
   before asking for API keys or opening upgrade/trial/checkout flows. Record current
   entitlement, added charges or unknowns, and the chosen included alternative.
   Use official user-controlled login; never store passwords, TANs, tokens or
   certificate contents in profile files or conversational notes.
4. For read-only access within the requested scope, perform the smallest useful
   inspection and verify account identity and returned data. Limit imported data;
   preserve original exports and record source/time. Report partial results.
5. For a requested write, prepare the exact target/account/payload and expected
   result. Resolve only missing authorization at that boundary. Read back the
   actual provider state or obtain a verifiable receipt before marking success.
6. If access expires or an attempt times out, preserve observed state and inspect
   history before retrying a potentially duplicated operation. Do not invent an
   idempotency guarantee. Keep an unconfirmed attempt unresolved when read-back
   cannot determine its result.
7. Save a readable access/operation note in the existing source map or task evidence:
   requested capability, actual tool, tested operation, observation date, result,
   limits and next step. No new credentials database or second operational ledger.

When direct access is unavailable, use an authorized export/import or a guided
manual action with the user supplying outcome evidence. Prepare useful work
without claiming that this fallback is an automatic integration. A custom adapter
requires a concrete supported operation and separate security/runtime acceptance.

For reminders, verify a real available scheduler, destination, timezone, recurrence
and authorization; inspect the created job and supported delivery evidence. A due
date, drafted message or scheduler instruction alone is not a configured reminder.

## Incomplete access and bounded retries

| Observation | Continue safely | Do not claim |
| --- | --- | --- |
| Tool absent or operation unsupported | Inspect an authorized export or prepare exact manual steps | A configured integration or completed operation |
| Authentication expired / denied | Preserve selected scope; use official reauthentication by the user | That requesting read access authorizes a write |
| Partial pages or skipped records | Record actual coverage, filters and cursor/time; fetch only the missing scope through a supported route | A complete month/year or “no documents” from a partial result |
| Write timed out / result ambiguous | Preserve payload/version and attempt; query history/readback; stop automatic retries if result remains unknown | Failure, success or permission to submit again without evidence |
| Readback disagrees | Preserve both observations, identify the exact discrepancy, prepare correction | That a successful request alone establishes the final state |

For an export fallback, preserve original bytes and provider selection details
before normalizing a derivative. Map columns only from observed headers/documentation;
check identifiers, currency, date scope, duplicate records and omitted pages or
attachments. Use existing intake/bank-mapping tools where the format is supported.
An offline inspection proves only the supplied snapshot, not current account state.

## Inspect a supplied accounting export

Use this route when the task concerns missing documents or period coverage and
no suitable live access is available. It does not select a new accounting system.
Start from the user's stated product and preserve it as authoritative; an export
is a dated snapshot. Do not require workspace setup for a factual explanation.

1. Establish the target period and the export's actual selection: document date,
   payment date or another documented basis; object types, statuses, accounts,
   filters, generation time and pages. Keep user statements separate from observed
   file contents. Unknown coverage is **unknown**, not zero or complete.
2. Preserve every supplied original before processing. Inspect only the relevant
   subset through suitable host tools. The catalog accepts PDF/XML/images/CSV;
   it does not unpack or import ZIPs. Keep an unsupported archive at its source or
   a separately assessed private evidence location. Record what was not inspected;
   do not treat a list of archive filenames as verified contents or discard the ZIP
   after extracting derivatives. See [existing data](existing-data.md).
3. Use the coverage section of the operation note. Compare observed record IDs,
   references and individual document files. Report repeated rows, exact-byte
   copies, conflicting versions and missing attachments separately; do not merge
   them just because an invoice number or amount matches. Counts describe only
   the inspected selection. A CSV row is not proof that its original is supplied.
4. Identify the smallest next action: obtain the missing page/original, inspect
   the item's actual status/date, or prepare a reviewed correction. Re-exporting
   does not repair an uncaptured record. Do not change a category, finalize, lock,
   mark sent or post records merely to make an export look complete. Verify the
   selected export route's side effects before recommending it.
5. Save a dated readable result with original references and unresolved scope.
   Reuse the source map/task evidence and preserve its earlier version. If a
   workspace exists, resolve logical paths through the folder helper before writing;
   do not create parallel English folders in a localized workspace. Use validated
   writers for canonical records. If no workspace is needed, return the explanation
   or a standalone private note without inventing register updates.

Finish with what was supplied, actually inspected, missing and still unverified,
plus one next action. Do not promote an export check into live-account readback,
period closure, accounting correctness or filing readiness. A later export is new
input: compare its scope and versions before using it to close the existing task.
