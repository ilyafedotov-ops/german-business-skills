# German Business Kit — local preview 0.7.0-preview.1

**Start here:** `skills/de-business-kit/guides/start.en.md` · `skills/de-business-kit/guides/user-guide.en.md`. These files ship inside the extracted package; the source checkout is not needed.

Windows users can start without Python using native Windows tools (see `skills/de-business-kit/references/native-windows.md`). The native entry point shares the existing workspace and covers installation, start/resume, preview, intake, integrity, real overview and full backup/restore; advanced validated automation remains an optional Python-engine capability.

[English](README.md) | [Русский](README.ru.md)

German Business Kit contains seven skills for the entrepreneur lifecycle: formation, daily operations, accounting, taxes, services, changes and closure. Shared context and evidence connect tasks; guidance is supported by validated local tools. English and Russian are supported, with official German form labels retained. Real connections, sending and exact-host acceptance are verified separately.

## Bundle contents

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

## Start with a small guided setup

After reviewing and installing the plugin through your host, open a fresh chat and send:

> Use German Business Kit to help me get started. Use the language of my request and clarify the result I need. Select a suitable skill; introduce private-folder setup when the task needs it. Use synthetic data for a demonstration.

The shared workflow and references are in `skills/de-business-kit/SKILL.md`. Setup should preserve unknown facts and distinguish creating a workspace from completing business or tax setup. Keep real records outside this plugin and public source repositories. Do not recreate an existing private workspace to change its language or working mode.

A useful first task is a focused answer, a launch plan, a reply draft or a selected document check. For ongoing work, save a readable result and the next action. Continue the same private workspace later; use your existing accounting program as authoritative when selected. Reviewing a document, recording an entry and submitting a return are separate steps.

## What the package requires

The advanced optional utilities require **Python 3.9+**, with no additional Python packages. The host must separately provide and permit file access and code execution. Browser tools, paid accounts, banking access and external connectors are not supplied by this plugin. If a required tool is unavailable, ask for manual steps instead of treating an operation as completed.

Published release ZIPs are named `de-business-kit-<version>-codex.zip` and `de-business-kit-<version>-claude.zip`; local development builds use `codex.zip` and `claude.zip`. Both contain local marketplace folders. **Extract the archive into a new folder before registering the marketplace directory.** These transport ZIPs are not direct plugin-upload files, and building or extracting them does not install anything. Follow the source project's [verification](https://github.com/ilyafedotov-ops/german-business-skills/blob/main/docs/releases.md) and [installation guide](https://github.com/ilyafedotov-ops/german-business-skills/blob/main/docs/distribution.md) for host-specific steps; ask the assistant to explain them before execution. No background hook, MCP server, credential or automatic updater is included.

Use synthetic data to verify discovery, guided setup, language, continuation and file operations in your exact app/OS version. This preview cannot submit filings or certify bookkeeping, legal compliance or account readiness. External actions still require the user's authorization and the host's actual capabilities.


The installed skill also includes `references/monthly-workflow.md` for local cash records and manual ELSTER, and `references/recovery.md` for verified complete backups. Native overview inspects saved records and local evidence; it does not run full filing preflight or enable protected accounting writes. The separate interactive prototype is not included as a production GUI.
