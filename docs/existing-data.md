# Start with data you already have

[English](existing-data.md) | [Русский](existing-data.ru.md) | [Documentation](index.md)

You can start with invoices in Gmail, records in an accounting service, or a folder of mixed files. You do not need to start a new business profile from scratch, migrate software or hire an accountant. The assistant first identifies the relevant source and the tools actually available in your session.

Try one of these requests:

- “My October invoices are in Gmail and some also exist in Lexware Office. Find the relevant records, keep their origins and avoid duplicate entries.”
- “I already use sevdesk. Help me continue my own bookkeeping from the existing documents and records.”
- “I use WISO, but I am not sure which integration is available. Identify my product and help me use the data already there.”
- “This folder contains invoices, bank statements, contracts and old exports. Show what can be imported before changing anything.”

## How access is chosen

| What you have | What happens next |
| --- | --- |
| A connected plugin | The assistant checks the account and actual search/read/download capabilities with a small relevant read. Search access alone may not include attachment downloads. |
| A supported API | The assistant checks the exact product, edition, permissions and operation. Existing authorized credentials stay in supported secret storage. This package does not include production service adapters. |
| A website or desktop application | Available browser or computer-control tools may support inspection/export. You authenticate in the official interface; do not paste passwords, tokens or ELSTER certificates into chat. Windows/macOS capabilities are checked in the current host. |
| No suitable connection | The assistant gives specific manual export steps and continues from the files. Installing a plugin or seeing a login screen is not a successful connection/import. |
| An existing local or synchronized folder | A metadata-only preview lists candidates and exclusions. A separate private destination keeps source files unchanged. Online-only files and unsupported formats need a suitable download/export or review step. |

“Lexware” needs clarification between Office and desktop products. “WISO” needs clarification between Steuer and MeinBüro, cloud/Desktop and the relevant year/version. Available plans and API behavior change; the assistant checks [official provider sources](../skills/de-business-kit/references/data-source-access.md) for the operation rather than promising a universal connector.

## Review and continue

The assistant saves a private source map with account aliases, periods, access evidence, retrieved source IDs, original file links and missing items. It checks pagination and explains partial results. Email dates, file modification dates and invoice/payment dates stay distinct. The same invoice in several sources does not automatically become several accounting entries.

For a folder, the preview normally visits up to 1,000 entries and ten directory levels. It skips hidden entries, links/reparse points, key/certificate files and nested workspaces; reports limits/errors; and does not read file contents, import, unpack or modify anything at the source. Supported intake formats are PDF, XML, common images and CSV. EML/MBOX, ZIP, office documents and native accounting files are preserved separately and need appropriate tools; the assistant must not silently discard or claim to have parsed them. After reviewing the scope, selected files are copied with original-byte verification through the [document workflow](document-workflow.md).

Read/import work does not authorize sending or deleting email, posting transactions, locking books, transferring money or filing taxes. Some provider export/download actions change state; the assistant checks that behavior and uses existing authorization only for its actual scope. Your current accounting system stays authoritative until you explicitly choose and verify a migration.

On your next visit, say “Continue from my source map and show what has not been retrieved or reviewed.” Existing history and unresolved items remain in the same private workspace.
