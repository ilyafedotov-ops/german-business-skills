# Platforms and local installation

Documentation checked: **2026-10-25**. These are documented capabilities, not
completed integration tests. Record the user's product, app version, account
plan, local/cloud execution mode, and available tools before using an adapter.

## Portable core

This package contains one self-contained skill, `de-business-kit`, with task
modules under `references/`. Keep `name` and `description` in `SKILL.md` and use
relative resource paths. OpenAI and Claude Code support the Agent Skills format.
Keep provider-specific tool names and settings out of the common workflow.
`agents/openai.yaml` supplies optional OpenAI UI metadata. A skill describes a
workflow; it does not grant permissions or install tools.

| Local host | Project discovery directory | User discovery directory | Invocation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/de-business-kit/` | `~/.agents/skills/de-business-kit/` | `$de-business-kit` in CLI/IDE; use the available desktop skill picker |
| Claude Code, including Desktop Code tab local sessions | `.claude/skills/de-business-kit/` | `~/.claude/skills/de-business-kit/` | `/de-business-kit` |

The canonical distribution source is `skills/de-business-kit/`. Copy it with
the repository's `tools/install.py`; do not store private business files in that
source tree. The installer supports project or user scope, validates both
destinations before writing, and refuses existing installations. It does not
change host settings, install browser integrations, or enable permissions.

Current Codex documentation recommends `.agents/skills`, rather than older
`.codex/skills` examples. Claude Cowork and cloud sessions do not automatically
read the local user skills folder; account-enabled skills and cloud project
behavior are separate deployment paths. Do not promise Cowork support from
this local installer. Test each intended surface separately.

Sources:

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)

## Browser and computer capabilities

Prefer a supported connector or documented API for suitable operations, then
dedicated Browser/Chrome tools. Use native screen control only when the actual
host supports it. Otherwise produce a field worksheet for manual entry.

| Host capability | Documented behavior and limitation |
| --- | --- |
| Codex desktop built-in Browser | Can open pages, inspect rendered state, click and type. It uses its own profile. The documentation currently says automated file uploads are unavailable; provide a manual upload step. |
| Claude Code Desktop Browser | Can interact with external sites subject to site permissions. Its profile is separate from the user's normal browser. |
| Claude in Chrome | Uses a supported Chromium browser and extension; current prerequisites include extension 1.0.36+, direct Anthropic Pro/Max/Team/Enterprise plan and `/login`. API-key, long-lived-token and exclusive third-party-provider authentication do not enable this route. Current docs exclude WSL. |
| Claude native Computer Use | Preview on macOS/Windows, currently Pro/Max only. Native screen-control access to browser apps is view-only; use the dedicated browser tool for form entry. |

Detect capabilities from the current session; never infer them from a skill
being installed. Native Computer Use, a built-in Browser, and a Chrome extension
are different tools with different permission and account requirements.

For ELSTER and other portals, prepare an answer sheet containing the observed
field label, proposed value, source, rationale and unresolved questions. Enter
confirmed values into a draft if supported. Authentication, certificates,
passwords, TAN, CAPTCHA and MFA stay in the official user authentication flow.
Do not place them in business profile files or chat. Review the completed form
before any separately authorized submission. A button click alone is not proof
of a successful filing; verify the official receipt.

Sources:

- [OpenAI: Browser](https://learn.chatgpt.com/docs/browser)
- [Claude Code: Desktop application](https://code.claude.com/docs/en/desktop)
- [Claude Code: Chrome integration](https://code.claude.com/docs/en/chrome)

## Data processing configuration

Local file operations do not imply local model inference. Treat selected file
contents, screenshots, tool responses and chat transcripts as potentially sent
to the configured provider. Capture the actual product, execution location,
authentication type, plan, retention/training settings, DPA status, relevant
regional controls and third-party connectors before handling client data.

Anthropic distinguishes consumer and commercial terms; its DPA is incorporated
into commercial terms. Claude Code may retain local plaintext transcripts.
OpenAI Business and API offer no training by default, but API retention or EU
residency features must not be assumed to cover a desktop subscription. Remote
MCP services have their own processing policies. An opt-out or DPA alone does
not establish GDPR compliance; use the data-protection task module.

Sources:

- [Claude Code: Data usage](https://code.claude.com/docs/en/data-usage)
- [Anthropic: DPA incorporation](https://privacy.claude.com/en/articles/7996862-how-do-i-view-and-sign-your-data-processing-addendum-dpa)
- [OpenAI: Plan features](https://learn.chatgpt.com/docs/pricing)
- [OpenAI API: Data controls](https://developers.openai.com/api/docs/guides/your-data)

## Verification status

Python installer tests cover destination paths, preservation of existing files,
preflight of both targets, dry-run behavior and symlink rejection. They do not
exercise either desktop application. **Desktop skill discovery, browser login,
form filling, ELSTER submission and account-specific data controls have not
been integration-tested for this release.** Run a local smoke test with synthetic
data and record host/version/results before claiming support for a workflow.
