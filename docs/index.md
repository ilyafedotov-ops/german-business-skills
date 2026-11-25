# Technical documentation

[English](index.md) · [Русский](index.ru.md) · [User documentation](../README.md#start-here)

For maintainers and contributors. Users can go directly to [installation](../skills/de-business-kit/guides/install.en.md), [everyday tasks](../skills/de-business-kit/guides/user-guide.en.md) or [assisted forms and service access](../skills/de-business-kit/guides/assisted-services.en.md).

| Need | Read |
| --- | --- |
| What works and what remains | [Current status and P1–P7 roadmap](project-status.md) |
| Components, execution and trust boundaries | [Architecture](architecture.md) |
| Records, relationships and state transitions | [Ontology](ontology.md) |
| Guided setup page for beginners (EN/RU/DE) | [Guided setup page](setup-page.md) |
| Launch carousels, video scripts and their sources | [Launch materials](../presentation/README.md) |
| Build/install a complete skill bundle | [Distribution](distribution.md) |
| Publish or verify an immutable release | [Release process](releases.md) |
| Evidence, test commands and acceptance gaps | [Validation](validation.md) |
| Make a change | [Contributing](../CONTRIBUTING.md), [repository rules](../AGENTS.md), [security](../SECURITY.md) |

The installed assistant uses the self-contained [skill entry point](../skills/de-business-kit/SKILL.md) and on-demand [workflow references](../skills/de-business-kit/references/lifecycle.md). They are operational instructions, not a second user manual.

## Research

The [workspace layout review](research/workspace-layout-review-2026-11-21.md) explains the current folder structure and keeps its source-check date; recheck external claims for the current task. Superseded research lives in Git history.

## Keep this structure small

User instructions live in the portable guides; technical explanations live here. Current implementation and remaining work belong in `project-status.md`; actual test evidence belongs in `validation.md`. Update an existing owner and link to it instead of adding another status, quick-start or topic summary. Historical evidence keeps its original dates and limits.
