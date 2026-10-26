# German Business Kit

**English** · [Русский](README.ru.md) · [Deutsche Startanleitung](skills/de-business-kit/guides/start.de.md)

**A system of skills supporting an entrepreneur in Germany, from preparing to start through daily work, reporting, changes and closure.** German Business Kit helps Freiberufler and Einzelunternehmen/Gewerbe answer questions, prepare forms and documents, choose services and resume with shared context. Coverage is uneven: the [lifecycle map](docs/lifecycle.md) separates existing guidance, tools and gaps.

Start with a task in ordinary language in Codex or Claude Code with the skill enabled. A simple question requires neither the local GUI nor full workspace setup. The local application and utilities support record operations; available integrations and the chosen accounting software complement that route.

**Source version: 0.8.0-preview.1.** The seven-skill lifecycle changes described here are in the current source; older release archives do not acquire them automatically. See [release changes](CHANGELOG.md#080-preview1) and [release verification](docs/releases.md). The [real workspace interface](docs/gui.md) supports document import/review, cash-entry corrections, filing-evidence editing and backup/recovery with EN/RU/DE navigation. Packaged builds include their runtime; users do not install Python. Download availability depends on completed publication and verification of the matching platform archive. Platform checks and first-launch acceptance remain separate gates.

This preview includes a limited cash journal and filing-evidence tracking. It has no complete tax calculation engine or direct ELSTER transmission. The separate interactive prototype uses fictional data.

[Start guide](skills/de-business-kit/guides/start.en.md) · [User guide](skills/de-business-kit/guides/user-guide.en.md) · [All topics](docs/index.md) · [Capabilities and limits](docs/project-status.md)

## Skills in the bundle

| Skill | When to use |
| --- | --- |
| `de-business-kit` | Start, resume or choose the next action |
| `de-business-start` | Prepare launch and registration |
| `de-business-operations` | Proposals, invoices, payment follow-up and correspondence |
| `de-business-accounting` | Documents, reconciliation and authoritative records |
| `de-business-tax` | Tax questions, reporting and Finanzamt replies |
| `de-business-services` | Banking, insurance, software and service access |
| `de-business-changes` | Changes, hiring, pause and closure |

Install the complete set together: domain skills use shared resources in `de-business-kit`. Invoke a domain skill directly when appropriate. The shared profile and chosen accounting system persist; changing skills does not restart setup. These changes are in source and local builds; previously published archives remain unchanged.

## Quick start

1. **Enable the skill in your existing assistant.** Select the installed German Business Kit; for a new installation use a verified `-codex.zip` or `-claude.zip` for the matching release. Extracting a ZIP does not install a skill. [Installation options](#install).
2. **Describe the result you need.** For example: “I want to start an activity,” “Help me fill in this form,” or “Explain this letter.” The assistant asks only for facts that affect the task.
3. **Save context when useful.** For document work, choose a private folder outside the application and Git repositories. Existing accounting software stays authoritative; choose the accounting route when it becomes relevant.
4. **Use suitable tools.** The skill checks actual file, search, browser and connector access. The local GUI is an additional way to work with records: [application setup and launch](gui/README.md), [release verification](docs/releases.md).

**Copy this for setup:**

> I downloaded German Business Kit. Help me inspect and install it in this app. Explain which files will be installed and where. Use native tools on Windows; do not install Python or change security settings. Then help me choose one first task and a separate private folder. Offer a fictional example if I want to try it first.

Already installed? Select **German Business Kit** from the skills available in your app and use one of the [example requests](#example-requests). Before real personal data is processed, establish which content may reach the AI service or connected tools. Enter passwords, TANs and ELSTER certificates only through the official authentication flow.

## How it works

```mermaid
flowchart TD
    A["Entrepreneur task at any stage"] --> B["Choose a domain skill directly or use the router"]
    B --> C["Formation · forms · questions · operations · reporting"]
    C --> D["Available tools and chosen services"]
    D --> E["Readable result, evidence and next action"]
    E --> B
```

Dedicated skills now provide changes and closure preparation; actual external execution and complete acceptance remain separate. The [coverage map and roadmap](docs/lifecycle.md) distinguish that goal from current readiness.

Self-managed accounting and filing remain important parts of the product. The first developed monthly route uses local cash records and manual ELSTER; it is one journey. Existing accounting software stays authoritative when selected. Production connectors and direct ELSTER transport are absent. Preparation, approval, sending and observed confirmation remain separate stages; professional consultation is available for a specific need.

## What you can do today

| Your task | What the kit provides | Current boundary |
| --- | --- | --- |
| Prepare to start an activity | Guidance for facts, classification, registration plans and form worksheets | Current requirements depend on the case; no automatic registration |
| Get an answer or prepare a form | Task modules, source research, readable answers and reviewable drafts | Portal access and actual submission are verified separately |
| Organize a mixed folder | Preview, selected intake, preserved originals and integrity checks | Copying a file does not review or post it |
| Review documents and payments | Catalog, proposed fields, reviewed bank mappings and reconciliation | Catalog review is in the bundled GUI; bank mapping/reconciliation use standalone utilities with an existing Python runtime |
| Manage local cash records | Reviewed entries, splits, reversals and period reports | Limited journal, not a complete statutory ledger or tax engine |
| Prepare taxes and letters | Source-based analysis, form worksheets, readable reports and recipient documents | Official forms/calculations must be checked for the actual year; submission is separate |
| Track a filing | Versioned drafts, checks, authorization and observed receipt/response records | GUI uses the bundled protected engine; standalone utilities need their runtime. No direct ELSTER transmission |
| Continue or recover work | Active tasks across months, undated tasks, dependencies, evidence status and verified full backup/restore | Overview is a snapshot; GUI continuation prepares a copyable request, not an AI session |
| Follow an invoice correction | Bounded standalone XML inspection, prior-invoice references and reviewed evidence links | No complete e-invoice validation, automatic refund or accounting correction |
| Inspect a supplied service export | Export route/date basis, originals, inspected scope and missing evidence | Lexware trials use local examples; no live connector or automatic archive importer |
| Prepare a change, first hire or closure | A before/after plan, dependencies, materials and unresolved obligations | No automatic registration, payroll calculation or cancellation |
| Compare business services | Needs-based banking, insurance and software research using current sources | No automatic account opening, purchase or policy selection |

**Windows application:** the packaged GUI includes its engine for supported document, cash-entry, filing-evidence and recovery operations. **Standalone PowerShell without Python:** native tools cover installation, start/resume, folder preview, intake, integrity, real overview and full backup/restore. Protected journal/filing writes, catalog updates and full filing preflight are not yet native. The assistant must identify an unavailable operation instead of claiming it succeeded. See [Windows guidance](docs/windows.md).

**macOS:** choose the application archive for your Mac architecture; its engine is bundled. Standalone Python utilities require an existing Python 3.9+ runtime; macOS does not guarantee it is installed. Node and Playwright are developer tools, not onboarding requirements.

**Languages:** application navigation supports English/Russian/German; user guides and report templates are English/Russian. Folder names and the short start guide also support German. Official form labels remain in German; full German report coverage is unfinished.

## Example requests

| What you need | What to say |
| --- | --- |
| Existing folder or email | “My invoices are in this folder and Gmail. First show which sources you can access and what you found. Help me choose what to import; do not change the source or send anything.” |
| This month's work | “Continue October in my existing workspace. Show missing receipts, unmatched payments, accounting work and filing issues. Open a readable overview and suggest the next action.” |
| A tax question | “This invoice is from another country and mentions reverse charge. Check my actual business facts and the applicable period against official sources. Explain what is known and what still needs checking.” |
| A letter or report | “Explain this Finanzamt letter in English. Identify any deadline with its source, prepare a German reply draft if needed, and keep my private notes separate.” |
| Starting an activity | “Help me clarify Freiberufler or Gewerbe for this activity, including my existing activities. Ask only what affects the next step and prepare a registration plan.” |
| Banking or insurance | “Compare suitable services for my activity, countries, currencies and expected payments. Show current costs, exclusions, eligibility and sources before recommending anything.” |
| Resume or back up | “Save where we stopped and the next action. Create and verify a complete backup at the location I choose.” |

**Illustrative result, using fictional records:** two invoices and a bank export are preserved; one payment matches an invoice and another lacks a receipt. The readable result links the originals, explains the missing receipt and leaves the unresolved item open. It does not label the month complete or a return submitted.

[Russian examples](README.ru.md#примеры-запросов) · [Detailed working modes](docs/modes.md) · [Documents and reports](docs/documents.md)

## Your private workspace

New workspaces use five everyday areas. This English example shows the main folders; year/month folders are created when needed.

```text
My business/
├── START-HERE.md
├── 01 Inbox/
├── 02 Documents/
│   └── 2026/10/
│       ├── Originals/
│       ├── Processed/
│       └── Proposals/
├── 03 Accounts/
│   ├── Bank/
│   ├── Records/
│   └── Reports/
├── 04 Taxes/
├── 05 Business/
│   ├── Registration/
│   └── Correspondence/
├── .business-kit/          ← internal records and history
└── .workspace-layout.json  ← folder mapping
```

**Reports have a home:** accounting/reconciliation outputs use the mapped Accounts areas; tax materials use Taxes. Ask the assistant for the actual link to each generated result. The real overview is stored in the internal admin area and can be opened as HTML or Markdown. See [folder names in EN/RU/DE](docs/folder-structure.md) and [report types](docs/documents.md).

Changing the conversation language does not rename folders. Existing workspaces retain their earlier layout. Include internal records and the folder mapping in a full backup; a selected-document archive is not a complete backup. Originals and hashes support traceability, but do not certify GoBD compliance, encrypt files or establish tax correctness.

## Install

The quick start uses skills in your assistant. The local application is optional and has its own launch instructions. Choose the route you need:

| Situation | Guide |
| --- | --- |
| Local Windows/macOS application | [Application instructions](gui/README.md), [scope and delivery](docs/gui.md) |
| Standalone Windows tools, no Python | [Native Windows setup and limits](docs/windows.md) |
| Downloaded Codex/Claude release package | [Verify the download](docs/releases.md), then [register/install the extracted marketplace](docs/distribution.md#optional-host-installation-after-review) |
| Start from source or maintain the project | [Distribution and build instructions](docs/distribution.md), [Contributing](CONTRIBUTING.md) |
| Understand host differences | [Platform compatibility](skills/de-business-kit/references/platforms.md) |

The application runs from its extracted folder; no desktop installer is supplied. The skill bundle uses the host's permitted local skill/plugin mechanism; there is no public one-click marketplace listing. Avoid enabling both the standalone skill and the same plugin in one session.

**Updating:** preserve the previous skill and any customizations, verify the new package in a separate folder, then replace the installed skill through the documented host route. The standalone installer refuses to overwrite an existing installation. Keep the private business workspace in place; do not initialize it again or rename managed folders as part of an update. See [updates](docs/distribution.md) and [backup/recovery](skills/de-business-kit/references/recovery.md).

## Interface, validation and development

The **[local GUI](docs/gui.md)** connects those records to controlled actions. The generated **real workspace overview** reads your saved records and shows issues and next steps. The separate **[interactive prototype](docs/prototype.md)** demonstrates onboarding, document review, unmatched payments and resuming work with fictional data in browser storage. It is not connected to your real accounts.

**Release acceptance (2026-10-26):** [0.8.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.8.0-preview.1) passed Windows/macOS utility checks, native Windows PowerShell 5.1, Chromium/WebKit journeys, all three application package checks and security gates. All eight downloaded assets passed checksum, immutable-release and build-provenance verification. Codex CLI and explicit Claude added-directory discovery remain separate macOS evidence. Ordinary-user first launch, other host discovery routes and real service operations remain open. See the [dated validation record](docs/validation.md) for exact commits, checks and limits.

Historical evidence: the [0.6.0-preview.4 release workflow](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40288755911) passed Windows/macOS utility checks, native Windows PowerShell 5.1 checks, browser/document checks, security gates and release verification. That run covers the earlier skill baseline, not the 0.7 GUI. It does not establish nontechnical-user usability, live service integration or tax correctness. [Validation records](docs/validation.md) preserve the exact scope and remaining acceptance work.

The named release assets include checksums and signed build provenance. A verified signature establishes origin and integrity; it does not certify accounting results. [Release history](CHANGELOG.md) · [Verification instructions](docs/releases.md).

For contributors:

```bash
python3 -B tools/check_package.py
python3 -B -m unittest discover -s tests -v
```

[Architecture](docs/architecture.md) · [Repository rules](AGENTS.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md). Use fictional data in public examples and issues. The project is [MIT-licensed](LICENSE); AI apps and third-party services have their own terms. The `tax-consultant` workflow name does not confer licensed Steuerberater status.
