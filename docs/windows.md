# Windows: start without installing Python

[English](windows.md) | [Русский](windows.ru.md) | [Quick start](quickstart.md)

For the local application, download and verify the Windows x64 GUI archive for
[0.7.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.7.0-preview.1)
when published. Extract the whole folder and open `GermanBusinessKit.exe`; its
bundled engine supports document review, protected cash entries, filing evidence,
drafts and recovery without a user-installed Python. Keep the launcher running.
See [application instructions](../gui/README.md) and [download verification](releases.md).
No Authenticode signature is supplied; follow device policy if launch is blocked.

## Optional standalone PowerShell route

Use the Codex or Claude Code app you already have. **Python, Git, WSL and PowerShell 7 are not prerequisites for the native Windows start and document-intake path.** The assistant uses available host tools and Windows PowerShell 5.1. You do not need to type commands or edit JSON yourself.

1. Open a local folder session in the app. Obtain the reviewed skill/plugin; a source ZIP can be extracted with Explorer's **Extract All**. Keep it separate from business files. The assistant can install the standalone skill using its native installer; no package manager is needed.
2. Say: “I use Windows and have no Python. Use native Windows tools. Help me organize my existing records in a separate private folder, show a synthetic intake example, and continue without installing developer tools.”
3. The assistant checks available tools and permissions, then creates or resumes the private workspace. It previews the chosen source folder before importing selected supported files, preserves originals and checks their hashes.
4. Ask “Show my real October overview” or “Create and verify a complete backup at this protected location.” The assistant generates readable views or uses [full recovery](../skills/de-business-kit/references/recovery.md), then reports what was actually checked. The native overview inspects saved state and local evidence; it does not run full filing preflight. Existing business facts and VAT history stay in the same shared workspace.

Research, tax explanations, service comparisons and form worksheets need no Python. Native commands cover installation, start/resume, folder preview, original-file intake, duplicate detection, integrity checks, the real read-only overview and full verified backup/restore. They do not create protected accounting entries or filing transitions and do not submit returns.

Outside the packaged GUI, some advanced automation still uses the optional Python engine: validated profile/register changes, document catalog/proposals, reviewed bank mappings/reconciliation, XML inspection, full filing preflight, protected cash-journal/filing writes and selected-record archives. If that runtime is unavailable, the assistant continues useful preparation and identifies the exact unfinished operation. It must not install Python automatically or present manually edited records as validated results. An existing approved runtime can be used where appropriate; any extra tool or remote processing needs its own concrete assessment.

A script blocked by Windows or organizational policy should remain blocked until an approved route is available. The assistant must not disable protections to finish setup. Local file operations also do not mean the AI model runs locally; review the actual data flow before processing real personal data.

The assistant's [native command reference](../skills/de-business-kit/references/native-windows.md) describes commands and limits. [Validation](validation.md) distinguishes executed checks from pending Windows/desktop acceptance. The native path is preview functionality, not a claim that every existing automation has been ported.
