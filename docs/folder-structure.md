# Workspace folders and language

[English](folder-structure.md) | [Русский](folder-structure.ru.md) | [Deutsch](folder-structure.de.md)

New workspaces created with `start` or CLI `init` now use real folder names in English, Russian or German. Choose the language once at creation. Existing workspaces keep their paths. Self-managed accounting remains the main workflow; exports are optional.

## Five everyday areas

| Purpose | English | Русский | Deutsch |
| --- | --- | --- | --- |
| Mixed files awaiting intake | `01 Inbox` | `01 Входящие` | `01 Eingang` |
| Preserved documents and derivatives | `02 Documents` | `02 Документы` | `02 Dokumente` |
| Statements, accounting records and reports | `03 Accounts` | `03 Учёт` | `03 Buchhaltung` |
| Tax preparation and submission evidence | `04 Taxes` | `04 Налоги` | `04 Steuern` |
| Registration and correspondence | `05 Business` | `05 Бизнес` | `05 Unternehmen` |

The root includes a start guide in the chosen language: `START-HERE.md`, `НАЧНИТЕ-ЗДЕСЬ.md` or `HIER-STARTEN.md`. Put mixed incoming files in the first folder; the assistant can inspect and organize them without requiring a tax category in advance. Dropping a file there does not itself import or review it.

Months are created only when used. For example, a Russian original is stored under `02 Документы/2026/10/Оригиналы/`. Intake preserves source bytes and records the source filename; archived copies retain the existing hash-based naming convention. A storage month does not determine the tax period. Several tasks can reference one original without making copies in multiple folders.

Profile, indexes and history live in `.business-kit`. The versioned `.workspace-layout.json` identifies the folder language. Include both in backups; hiding technical files is not access protection. Do not edit these files or rename the folders manually.

## Stable references and compatibility

Folder language is separate from conversation/report preferences. Switching the assistant language does not rename folders or originals. The tools resolve stable internal references such as `06_bookkeeping/...` into the selected physical paths. Assistants using ordinary file tools must first inspect `workspace.py folders --root <private-folder>` or native `windows.ps1 -Action folders -Root <private-folder>`; the technical reference table is not a literal Explorer/Finder path list.

New CLI workspaces default to this layout. `--layout legacy` / `-Layout legacy` explicitly selects the older layout. The low-level Python `init_workspace` API keeps its legacy default for existing callers; `start_workspace` defaults to localized folders. Existing workspaces resume without migration. Migration would require a preview, verified backup, collision checks, reference mapping and original-hash verification; no migration is supplied now.

Native Windows setup, scan, intake and integrity checks use the same mapping as the optional Python workflows, accounting reports and archives. This does not add native Windows support for Python-only advanced operations. German folder names and the start guide are implemented; the prototype and all generated report templates are not fully translated. Native runtime validation on Linux is not Windows PowerShell 5.1 acceptance; see [validation](validation.md).
