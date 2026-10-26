# Local plugin distribution — v0.5.0 preview

Windows users can start without Python using [native Windows tools](windows.md). The native entry point shares the existing workspace and covers installation, start/resume, preview, intake, integrity, real overview and full backup/restore; advanced validated automation remains an optional Python-engine capability.

[English](distribution.md) | [Русский](distribution.ru.md)

The maintained workflow lives only in `skills/de-business-kit`. Root `plugin.json` declares the portable Agent Plugins identity; `.claude-plugin/plugin.json` is its thin Claude adapter. The offline builder copies that same skill into two independent local marketplace bundles. It includes the license, manifests, authored EN/RU readmes from `packaging/` and complete skill resources; repository tests, Git history, root-level private files and machine settings are excluded. Review the canonical skill before packaging: the builder is not a secret scanner.

This preview supplies no MCP server, lifecycle hook, credential, automatic installer or updater. Installing a plugin does not grant Python execution, filesystem access, browser tools, subscriptions or access to banking, Lexware or ELSTER. Actual host tools, permissions and account policy control those capabilities.

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
  codex/plugins/de-business-kit/skills/de-business-kit/...
  claude/.claude-plugin/marketplace.json
  claude/plugins/de-business-kit/.claude-plugin/plugin.json
  claude/plugins/de-business-kit/skills/de-business-kit/...
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

Start a fresh Claude Code session and invoke `/de-business-kit:de-business-kit`. Registration and installation use the host's default scope; review its settings and intended scope first. See the [Claude marketplace procedure](https://code.claude.com/docs/en/plugin-marketplaces) and [manifest reference](https://code.claude.com/docs/en/plugins-reference), checked 2026-10-25. These commands cover the local Claude Code route; Claude Desktop/Cowork import remains a separate unperformed acceptance check.

Avoid enabling both a copied standalone skill and its plugin in one session. Keep the previous reviewed package until the replacement passes a synthetic check. Do not delete or recreate the private business workspace when upgrading a skill.

## Evidence and remaining checks

Package tests extract each archive, resolve its catalog and manifest, compare every skill file with the canonical source, and run the extracted `workspace.py` with English and Russian synthetic workspaces after deleting the source fixture. They also check reproducibility, missing resources, metadata drift, unsafe paths and overwrite refusal. These are offline utility/resource checks.

On 2026-10-25, Claude Code **2.1.310** read-only `plugin validate` passed for a generated local marketplace and its packaged plugin. Both host packages now contain mutually linked EN/RU readmes with a first-run prompt. The separate public-directory check still reports a missing icon; public submission and directory acceptance remain deferred. Codex CLI **0.164.0** exposes marketplace registration, but registration/installation were not run.

The CI workflow runs native `windows-latest` (Python 3.9/3.14) and `macos-latest` (Python 3.10/3.14) jobs. [All four jobs passed on 2026-10-25](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40229530057) after fixing an installer drive-root error found by the first Windows run. Python 3.9 is covered on Windows because [GitHub's macOS ARM64 tool builds do not provide it](https://github.com/actions/python-versions/blob/main/versions-manifest.json). These checks execute offline Python utilities, not desktop apps.

No desktop installation, discovery, permission prompt, account synchronization or complete live workflow has been tested by this packaging work. Record host/product version, OS, language, discovery, setup, resumption and synthetic-file results before claiming desktop support. Use the [validation notes](validation.md) and [scenario cases](../evals/scenarios.json).
