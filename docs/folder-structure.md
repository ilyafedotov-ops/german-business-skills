# Workspace folders and language

[English](folder-structure.md) | [Русский](folder-structure.ru.md) | [Deutsch](folder-structure.de.md)

Review date: 2026-10-25. This page distinguishes the current implementation from the proposed user-facing structure. The project supports self-managed accounting; an accountant export is optional.

## What was confusing

The current workspace has ten English-named top-level directories. Russian conversation/report preferences do not translate those names. German is accepted in some saved settings, but several entry points and generated outputs still support only English/Russian or fall back to English. Full German support must not be claimed yet.

`04_accounting` and `06_bookkeeping` represent different technical purposes, but look like competing places to put an invoice. `00_admin/inbox` is difficult to discover; `07_exports` gives an optional output more prominence than everyday work. The profile, indexes and history are implementation records, not filing decisions for users.

Previously, initialization also created a full year and twelve months with `originals`, `derived` and `proposals` below each month. New initialization now creates the archive container only. Intake creates its selected month and originals directory; other operations create their output directories when needed. That avoids 49 empty directories at setup. Existing empty folders and original files are preserved.

## Recommended everyday structure

Use one selected language for a new workspace, not duplicate English/Russian/German copies of the same records.

| Purpose | English | Русский | Deutsch |
| --- | --- | --- | --- |
| Items to bring into the workspace | `01 Inbox` | `01 Входящие` | `01 Eingang` |
| Preserved source documents and related derivatives | `02 Documents` | `02 Документы` | `02 Dokumente` |
| Statements, accounting records and reports | `03 Accounts` | `03 Учёт` | `03 Buchhaltung` |
| Returns, tax correspondence and submission evidence | `04 Taxes` | `04 Налоги` | `04 Steuern` |
| Registration, contracts and general business correspondence | `05 Business` | `05 Бизнес` | `05 Unternehmen` |

These are **proposed names**, not paths supported by the current writers. Actual folder renaming needs a versioned path-resolution contract across Python, native Windows, evidence readers, exports and generated links. A localized interface/guide could instead use these labels while keeping existing storage paths. Confirm the intended Explorer/Finder experience before changing that contract.

Create subdivisions only when needed. Under documents use `YYYY/MM` for ordering, with translated labels such as `Оригиналы` / `Originale` and `Обработанные` / `Aufbereitet`. Show month names in the interface. A storage month must not determine tax treatment. Keep source filenames and exact bytes; readable titles belong in the catalog. Do not copy a document into multiple categories just because several tasks reference it.

Keep the business profile, indexes, audit history and technical configuration in a clearly identified internal area. It is not a security boundary and must remain in backups. Avoid asking the user to choose between tax/accounting categories before the document has been inspected: the inbox accepts mixed information, and unresolved classification remains visible.

Put optional exports beneath reports rather than making “accountant handoff” the main task. An archive, report, reviewed document, accounting entry and submitted return need separate labels and completion evidence.

## Compatibility and language changes

Do not rename existing workspaces in place or silently rewrite evidence references. Existing paths remain supported. A future migration needs a preview, backup verification, collision checks, full reference mapping, original-hash verification and a recoverable completion record before it is offered.

Store folder language separately from conversation/report language. Switching the assistant to Russian must not rename an established German archive. German official terms and form identifiers stay exact; explain them in the user's chosen language. Use short portable names, preserve Unicode, avoid Windows reserved names and characters, and check actual Windows/macOS behavior.

## Acceptance for the next layout

- A Russian-speaking user can start, file a mixed document and resume without interpreting English labels.
- A German-speaking user can do the same without an English fallback.
- New folders, native Windows intake, optional Python operations and generated links use the same versioned mapping.
- Language switching leaves original bytes and existing references unchanged.
- Intake works before every business/tax fact is known; no duplicated archive is created.
- Legacy workspaces remain readable, and recovery preserves originals and user files.

Only lazy month creation is implemented by this change. Full folder localization, a migration and a translated prototype are not yet implemented.
