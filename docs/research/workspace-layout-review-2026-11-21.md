> Dated review, not current implementation status. See [current status](../project-status.md) for delivery and remaining work.

# Private workspace folder layout: review and v2 plan

Review date: **2026-11-21**. Baseline inspected: **`9c3e5e9`** (content of the
private workspace created by `start`, `demo`, intake and the protected writers).
Legal sources were checked on **2026-11-21**. This is a maintainer review performed
inline in one Claude Code session without an independent reviewer. It is not a
legal assessment, a GoBD certification or a usability test.

## Verdict

The five visible areas, hidden internal records, month-partitioned preserved
originals and the hash index are a sound base. GoBD Rz. 117 prescribes no
particular filing system: chronological order with a traceable unique index
(Rz. 122) can satisfy the requirement to keep records in order. The gaps are
findability for a user, adviser or auditor, record classes stored in the wrong
area, inconsistent year partitions and the missing procedure documentation.

## Primary sources

| Source | Practical consequence for the layout |
| --- | --- |
| [§147 AO](https://www.gesetze-im-internet.de/ao_1977/__147.html) | Records must be kept in order. Books, records and their organizational documents: 10 years; accounting vouchers: 8 years; business letters and other relevant documents: 6 years. Periods start at the end of the calendar year and do not expire while an assessment period is open. |
| [§14b UStG](https://www.gesetze-im-internet.de/ustg_1980/__14b.html) | A copy of every issued invoice and every received invoice: 8 years. |
| [Consolidated GoBD, AO-Handbuch 2026, Anhang 33](https://ao.bundesfinanzministerium.de/ao/2026/Anhaenge/BMF-Schreiben-und-gleichlautende-Laendererlasse/Anhang-33/anhang-33.html) | Rz. 64/71/77: unique voucher number or document ID linked to entries; Rz. 68: running numbering as completeness control; Rz. 110: plain file storage regularly does not meet immutability without further measures; Rz. 117: no prescribed order, receipt and archiving logged; Rz. 122: unique index kept for the full period; Rz. 151–155: procedure documentation. |
| [BMF, GoBD 2nd amendment, 2025-07-14](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Weitere_Steuerthemen/Abgabenordnung/2025-07-14-GoBD-2-aenderung.pdf?__blob=publicationFile) | Incoming electronic documents stay in the received format; for an e-invoice the structured part suffices, the readable part only when it adds tax-relevant content; verified OCR output must also be kept (Rz. 119, 131). |
| [AWV sample procedure documentation for voucher filing](https://www.awv-net.de/publikationen-produkte/publikationen/detailseite/musterverfahrensdokumentation-zur-belegablage) | Structure for a small business's description of receipt, filing order, access, protection and adviser exchange. |

## Findings at baseline

| # | Finding | Evidence |
| --- | --- | --- |
| 1 | Assistant files were written to the user's inbox | `00_admin/inbox` maps to `01 Inbox`; `folder-scan-*.json` and documented input files landed there |
| 2 | The inbox loop did not close | `scan-folder` refuses the workspace's own inbox; an imported source stays there without a marker |
| 3 | Originals use SHA-256 filenames without a running number | `ingest_document`; `verify` and native `windows.ps1` require `stem == sha256` |
| 4 | Issued-invoice copies are stored as correspondence without a year | `invoicing.py` writes `08_correspondence/invoice-evidence/<uuid>` |
| 5 | Year partitions are inconsistent | Bank `normalized/`, one `register.json` for all years, flat correspondence writers |
| 6 | Canonical register placement is inconsistent | `04_accounting/register.json` is visible; other registers are internal |
| 7 | The readable overview is hidden | `overview.html`/`.md` under `.business-kit/admin/` |
| 8 | No procedure documentation | No source or template mentions it |
| 9 | No retention class, hold or document direction in the index | `documents.json`; `german-rules.md` asks for a retention class |
| 10 | `demo` used the legacy layout | `create_demo` called `init_workspace` with its `legacy` default |
| 11 | E-invoice parts are separate unlinked files | Each file is indexed independently by hash |

## Approved plan

Stored records use logical paths translated by longest-prefix mapping, so a
versioned mapping can relocate some files without rewriting records. Both Python
and native PowerShell reject layout descriptors other than version 1, so an older
kit fails closed on a v2 workspace.

- **Phase 0:** a new `00_admin/work` key for assistant files in every layout
  (finding 1); `demo` creates the localized layout (finding 10).
- **Phase 1:** versioned v2 mapping in Python and native Windows; root overview,
  internal accounting register, a reserved procedure-documentation folder and a
  shared year-path helper (findings 5–7).
- **Phase 2:** readable original names with a running number, issued-invoice
  copies under Documents, managed-inbox preview and post-import handling, then
  v2 as the default for new workspaces (findings 2–4).
- **Phase 3:** opt-in v1→v2 migration with a hash-listed plan, a verified full
  backup and the v2 descriptor written last as the commit point.

Retention class and direction (9), e-invoice grouping (11) and generated
procedure documentation (8) are separate data-model work. Existing workspaces are
never migrated silently.

## Method and limits

Evidence came from reading source and documentation and from synthetic workspaces
created outside the repository with `start`, `demo`, `scan-folder` and `receive`.
The review was inline; the repository's independent-review gate was not met by it.
