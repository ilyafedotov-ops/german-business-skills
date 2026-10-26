# Verify an access route for one concrete operation

Use with [existing data](existing-data.md) and [data-source access](data-source-access.md).
The bundle contains no production banking/accounting/ELSTER connector or scheduler.
This workflow uses tools actually supplied by the host and authorized for the task.

1. Identify the requested operation, exact service/product/edition, account or
   workspace, source of truth and necessary data scope. Reuse known facts.
2. Inventory available connector/API/browser/file tools before asking the user
   for information they can provide. A visible plugin or API document is not
   proof of credentials, permissions, supported write operations or current access.
3. Read the provider's current official operation/format documentation. Establish
   authentication, permission scope, supported versions, limits and output format.
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
