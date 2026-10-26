# German Business Kit

**English** · [Русский](README.ru.md) · [Deutsche Startanleitung](skills/de-business-kit/guides/start.de.md)

**An AI assistant skill set for starting and running a business in Germany.** Get help with opening an activity, questions, forms, everyday documents, accounting, reports, changes and closure. Designed for Freiberufler and Einzelunternehmen/Gewerbe.

## Start here

**[First-time setup: from installing your AI app to your first answer →](skills/de-business-kit/guides/install.en.md)**

You do not need to code. The guide explains what Codex and Claude Code are, helps you choose one, and walks through installing the app, adding all seven skills and trying a fictional example. It includes expected results, diagrams and help when a step fails.

1. **Open an AI assistant:** Codex or Claude Code on your computer.
2. **Add German Business Kit:** install the complete seven-skill bundle in your assistant project.
3. **Ask for one result:** “I want to start working as a translator in Germany. Help me choose one small first step.”

![Open an assistant project, add seven skills, ask one question](skills/de-business-kit/guides/images/setup-map.en.svg)

Already installed? [Choose your first task](skills/de-business-kit/guides/start.en.md) or [continue existing work](skills/de-business-kit/guides/user-guide.en.md#continue). [Short setup checklist](docs/quickstart.md) · [All documentation](docs/index.md).

## What it helps with

| Your task | Help available |
| --- | --- |
| Start a business | Clarify the activity, research requirements, prepare a registration plan and form drafts |
| Understand a question or letter | Explain the issue, check current sources, identify missing facts and prepare a reply |
| Work with customers | Proposals, invoices, payment follow-up and correspondence |
| Organize accounts and taxes | Document review, reconciliation guidance, supported local cash records and reporting preparation |
| Choose or change services | Compare banking, insurance and software; inspect supplied exports |
| Change, hire, pause or close | Prepare the steps, documents, dependencies and outstanding obligations |

You can ask a simple question before choosing accounting software or creating a records folder. When you choose an existing accounting system, it stays authoritative. The optional local records application supports file operations; it is not needed for the first conversation.

**Preview limits:** no complete tax calculation engine, production service connectors or direct ELSTER transmission. Lexware testing currently uses local examples. Preparing a form does not submit it. See [current capabilities and remaining work](docs/project-status.md).

## Example requests

- “I want to open an activity in Germany. Help me find the next step; ask only for facts you need.”
- “Explain this Finanzamt letter in Russian and help prepare a German reply.”
- “Can a phone bought in installments be a business expense? Check the applicable sources and ask for missing facts before giving concrete accounting treatment.”
- “Continue from my saved workspace. Show what is unfinished and the next action.”

Before using real documents, establish what content the AI service and connected tools may receive. Keep private records in a separate business folder. Enter passwords, TANs and certificates only through official authentication screens.

## Install

- **New user:** [full step-by-step guide](skills/de-business-kit/guides/install.en.md).
- **Download:** [published 0.8.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.8.0-preview.1); choose the `-codex.zip` or `-claude.zip` skill bundle and `SHA256SUMS`.
- **Updating or using plugins/terminal:** [advanced installation](docs/distribution.md) and [release verification](docs/releases.md). Preserve existing installations and business records.
- **Optional records application:** [Windows/macOS application guide](gui/README.md); [standalone Windows tools](docs/windows.md).

Source version: **0.8.0-preview.1**. New guide edits in source do not change the already published archives. User guides and report templates support English/Russian; application navigation also supports German. Full German report coverage is unfinished.

## How the skills work together

`de-business-kit` helps you start or continue. Six focused skills cover **start, operations, accounting, tax, services and changes**. Install them together; they share resources and one business context. You can invoke a focused skill directly without repeating setup.

[Lifecycle and roadmap](docs/lifecycle.md) · [Architecture](docs/architecture.md) · [Ontology](docs/ontology.md) · [Accounting limits](docs/core-capabilities.md).

## Validation and contributing

The published 0.8.0-preview.1 release passed automated Windows/macOS, PowerShell 5.1, browser and package checks; its downloaded assets were verified. Ordinary-user desktop acceptance and real service operations remain separate. See [dated evidence and gaps](docs/validation.md); passing tests do not certify tax correctness.

For contributors, start with [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md). The separate [interactive prototype](docs/prototype.md) uses fictional data.

```sh
python3 -B tools/check_package.py
python3 -B -m unittest discover -s tests -v
```

[Changes](CHANGELOG.md) · [Security](SECURITY.md) · [MIT license](LICENSE). AI apps and services have their own terms. Workflow names do not confer licensed Steuerberater status.
