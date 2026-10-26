# Local plugin distribution — v0.10.0-preview.1

**New users:** follow the [illustrated setup](../skills/de-business-kit/guides/install.en.md). It covers the Claude plugin marketplace (Cowork, chat and Claude Code) and a project-local Codex copy, without terminal commands. This page covers the marketplace contract and advanced source, plugin and update routes.

The [local GUI application](gui.md) bundles its engine for document review, cash entries, filing evidence and recovery on Windows/macOS; users do not install Python. Download availability requires publication and verification of the matching platform archive. Optional [standalone Windows tools](../skills/de-business-kit/guides/user-guide.en.md#check-your-own-environment) cover installation, start/resume, preview, intake, integrity, real overview and full backup/restore; their advanced protected writers still require an existing supported engine.

[English](distribution.md) | [Русский](distribution.ru.md)

The maintained bundle lives in `skills/` and contains seven skills listed in `skills/de-business-kit/assets/skill-set.json`. Shared instructions, templates and utilities remain in `de-business-kit`; sibling domain skills reference them directly. Python/PowerShell installers preflight the complete set and destination conflicts before writing. The builder creates independent Codex/Claude marketplace bundles with all resources, readmes and manifests. Do not install a dependent skill alone; private business data is not migrated. Installer safety checks do not replace source review for secrets.

This preview supplies no MCP server, lifecycle hook, credential, automatic installer or updater. Installing a plugin does not grant Python execution, filesystem access, browser tools, subscriptions or access to banking, Lexware or ELSTER. Actual host tools, permissions and account policy control those capabilities.


Install the complete set together: domain skills use shared resources in `de-business-kit`. Invoke a domain skill directly when appropriate. The shared profile and chosen accounting system persist; changing skills does not restart setup. These changes are in source and local builds; previously published archives remain unchanged.

## GitHub marketplace for Claude

The repository root is also a Claude plugin marketplace. `.claude-plugin/marketplace.json` lists one plugin, `de-business-kit`, whose `github` source pins the latest published release tag **and** its commit SHA. Users add `ilyafedotov-ops/german-business-skills` under Claude **Customize → Plugins → Add → Add marketplace**, or run `claude plugin marketplace add ilyafedotov-ops/german-business-skills` and `claude plugin install de-business-kit@german-business-kit`. A plugin added in claude.ai or the desktop app is saved to the account and reaches Cowork, chat and signed-in Claude Code sessions.

Claude fetches the plugin from the pinned commit, so changes on the default branch are never installed before release. At that commit the plugin root is the repository root (`.claude-plugin/plugin.json` plus `skills/`); Claude loads only the seven skills, and the root contains no `bin/`, hooks, agents or MCP configuration. The marketplace name `german-business-kit` differs from `de-business-kit-preview` used by local review bundles, so both can be registered. Anthropic's directory review does not cover marketplaces added by address.

The marketplace file is read from the default branch; the address works only after this file is merged there. Move the pin only after publication and asset verification, as described in [maintainer publication](releases.md#maintainer-publication). `tests/test_packaging.py` checks the entry name, the tag and commit formats and, where the tag is fetched, that the tag resolves to the pinned commit and its plugin manifest.

## Use a published package

For the standalone application, use [application downloads and instructions](gui.md).
The rest of this page covers the primary skill/plugin bundle. Users do not need
to build the project. Once published, download the named Codex or Claude ZIP from
[release 0.10.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.10.0-preview.1),
follow [download verification](releases.md), and extract it into a new folder using
Explorer or Finder. Published filenames include the version, for example
`de-business-kit-0.10.0-preview.1-codex.zip`.

Inside the extracted folder, `codex` or `claude` is the marketplace root. Skip the
build section and go to [host installation](#optional-host-installation-after-review).
In those examples replace `/absolute/path/to/new-review-bundle/codex` or
`/absolute/path/to/new-review-bundle/claude` with that actual extracted directory.
Ask the assistant to resolve the path and explain the installation before running
it. The [start guide](../skills/de-business-kit/guides/user-guide.en.md#first-task) covers your first
useful task. Published archives stay unchanged; source documentation edits appear
in packages only after a new release.

## Build and review without installing

Maintainers build packages from a reviewed source checkout, with Python 3.9+ and no extra packages:

```bash
python3 -B -m unittest discover -s tests -v
python3 -B tools/check_package.py
python3 -B tools/build_package.py --output /absolute/path/to/new-review-bundle
```

On Windows, replace `python3` with `py -3` or the installed Python 3 command and use an absolute Windows output path. The output's parent must already exist. The builder rejects an existing output, parent traversal, symlinked paths and an output inside the source checkout. Choose a new directory for every build; no existing installation is overwritten.

The result contains:

```text
new-review-bundle/
  codex/.agents/plugins/marketplace.json
  codex/plugins/de-business-kit/plugin.json
  codex/plugins/de-business-kit/skills/{de-business-kit,de-business-start,de-business-operations,...}/...
  claude/.claude-plugin/marketplace.json
  claude/plugins/de-business-kit/.claude-plugin/plugin.json
  claude/plugins/de-business-kit/skills/{de-business-kit,de-business-start,de-business-operations,...}/...
  codex.zip
  claude.zip
  SHA256SUMS
```

Both ZIPs are reproducible **marketplace transport archives**, not direct plugin-upload files. Extract into a fresh folder before using a marketplace path. For example:

```bash
python3 -m zipfile -l /absolute/path/to/new-review-bundle/codex.zip
python3 -m zipfile -e /absolute/path/to/new-review-bundle/codex.zip /absolute/path/to/new-extraction
```

The resulting marketplace root is `/absolute/path/to/new-extraction/codex`. The already-built `codex` and `claude` directories also work as the intended marketplace roots. `SHA256SUMS` detects changed archive bytes; it does not authenticate a publisher. Keep packages separate from private business workspaces.

## Optional host installation after review

The following commands change host configuration; the builder never runs them.

For Codex, register the reviewed local marketplace directory:

```bash
codex plugin marketplace add /absolute/path/to/new-review-bundle/codex
```

Restart the ChatGPT desktop app, open the Plugins Directory, select **German Business Kit Preview**, and install **German Business Kit**. Start a new chat and request the `de-business-kit` guided setup. Local marketplace availability depends on the surface and policy. This follows [official OpenAI packaging and local marketplace guidance](https://developers.openai.com/plugins/build/plugins), checked 2026-10-25.

For Claude Code, validate the marketplace and plugin before registration:

```bash
claude plugin validate /absolute/path/to/new-review-bundle/claude
claude plugin validate /absolute/path/to/new-review-bundle/claude/plugins/de-business-kit
claude plugin marketplace add /absolute/path/to/new-review-bundle/claude
claude plugin install de-business-kit@de-business-kit-preview
```

Start a fresh Claude Code session and invoke `/de-business-kit:de-business-kit`. Registration and installation use the host's default scope; review its settings and intended scope first. See the [Claude marketplace procedure](https://code.claude.com/docs/en/plugin-marketplaces) and [manifest reference](https://code.claude.com/docs/en/plugins-reference), checked 2026-10-25. These commands cover a local review bundle. Ordinary users install through the [GitHub marketplace](#github-marketplace-for-claude); a Cowork desktop installation trial remains open.

Avoid enabling both a copied standalone skill and its plugin in one session. Keep the previous reviewed package until the replacement passes a synthetic check. Do not delete or recreate the private business workspace when upgrading a skill.

## Evidence and remaining checks

Package tests extract each archive, resolve its catalog and manifest, compare every skill file with the canonical source, and run the extracted `workspace.py` with English and Russian synthetic workspaces after deleting the source fixture. They also check reproducibility, missing resources, metadata drift, unsafe paths and overwrite refusal. These are offline utility/resource checks.

On 2026-10-25, Claude Code **2.1.310** read-only `plugin validate` passed for a generated local marketplace and its packaged plugin. Both host packages now contain mutually linked EN/RU readmes with a first-run prompt. The separate public-directory check still reports a missing icon; public submission and directory acceptance remain deferred. Codex CLI **0.164.0** exposes marketplace registration, but registration/installation were not run.

On **2026-10-26**, project-scoped standalone installation was checked through actual **Codex CLI 0.164.0** discovery on macOS arm64. Two fresh app-server processes found all seven enabled catalog skills at their installed paths, with no project errors; 128 files and installed sibling links were verified. This covers CLI discovery after process restart, not model invocation, marketplace installation or desktop UI. See the [dated evidence](validation.md).

The CI workflow runs native `windows-latest` (Python 3.9/3.14) and `macos-latest` (Python 3.10/3.14) jobs. [All four jobs passed on 2026-10-25](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40229530057) after fixing an installer drive-root error found by the first Windows run. Python 3.9 is covered on Windows because [GitHub's macOS ARM64 tool builds do not provide it](https://github.com/actions/python-versions/blob/main/versions-manifest.json). These checks execute offline Python utilities, not desktop apps.

No desktop installation, discovery, permission prompt, account synchronization or complete live workflow has been tested by this packaging work. Record host/product version, OS, language, discovery, setup, resumption and synthetic-file results before claiming desktop support. Use the [validation notes](validation.md) and [scenario cases](../evals/scenarios.json).

On **2026-10-26**, Claude Code **2.1.310** also discovered all seven standalone project skills in two fresh control-initialize processes using explicit `--add-dir`. No model turn was sent. This is a separate bounded CLI result, not automatic discovery or desktop acceptance; see the [validation record](validation.md).

On **2026-10-26**, Claude Code **2.1.310** `plugin validate` passed for the root marketplace, with warnings only about the repository-root plugin (no icon, root `CLAUDE.md` not loaded, an untracked ignored `.DS_Store`). In an isolated configuration directory, adding the local checkout as a marketplace and installing `de-business-kit@german-business-kit` fetched commit `b7f85c0422429f94159a6cc6352f8b83ab4b5d63` from GitHub; `plugin details` listed seven skills, and the installed `skills/` tree was byte-identical to that commit. This proves the pinned source, not the `owner/repo` address before merge or installation in Cowork, chat or the desktop UI.

[Versions, signatures and release verification](releases.md)
