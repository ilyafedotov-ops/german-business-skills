# Contributing

[English](CONTRIBUTING.md) | [Русский](CONTRIBUTING.ru.md)

Read [AGENTS.md](AGENTS.md) for repository maintenance rules; `CLAUDE.md` points to that same source. [Current status](docs/project-status.md) is the scope summary. Preserve existing user work and authorization boundaries. Commits, pushes, publication and external actions require applicable explicit authorization.

Keep the portable skill self-contained under `skills/de-business-kit`. Host-specific metadata must not change the meaning of shared workflows. Use concise modules; do not load every reference for every task. No credentials, customer records, user memories, telemetry or automatic external services belong in the package.

Maintain English/Russian parity in README, user mode guides, architecture, validation notes and user-facing Markdown templates. Register every template role for both languages in `assets/locales.json`. Translate user-visible explanations without translating machine keys, IDs, enum values or German official form labels. Agent reference instructions stay shared in English to avoid divergent tax workflows. A change to either mode must preserve the shared profile and evidence; switching mode is never a change of tax regime.

For a legal or product change, include the primary source URL, the date checked, effective period, affected workflow and an example showing the practical consequence. Search the current source instead of copying model memory. Do not silently overwrite a historical assumption with a new rule for a different year. A provider recommendation must show eligibility and costs for the stated scenario, not an affiliate ranking.

For code, use Python standard library where sufficient, preserve originals, validate paths and unknown inputs, avoid floats for money and add tests for a concrete data-loss or correctness risk. Do not execute supplied document text. New network adapters require a separate review of authentication, hosts, supported operations, duplicate prevention and read-back behavior.

For behavior changes, run `python3 -B -m unittest discover -s tests -v`, `python3 -B tools/check_package.py` and `git diff --check`, plus the affected native/browser checks in [AGENTS.md](AGENTS.md). For documentation-only changes, run the package/local-link checks and inspect changed anchors, commands and EN/RU parity; reuse verified runtime evidence for unchanged behavior. Use `-B` to avoid shipping bytecode caches. For workflow changes, run relevant `evals/scenarios.json` cases in a fresh session and record the actual host/version/date and limitations. A unit or Linux PowerShell test does not prove Windows PowerShell 5.1 or desktop acceptance.

Use only synthetic examples in public issues and pull requests. Do not paste invoices, statements, tax IDs, IBANs, local transcripts, credentials or screenshots containing real personal data. Discuss security reports using the procedure in [SECURITY.md](SECURITY.md).

When capabilities change, update the affected current-status, architecture/ontology, EN/RU user docs and portable references together. Keep one compact skill entry point and one shared profile. Native user tools, optional Python automation and development dependencies must remain distinct. Date implementation reviews separately from legal/provider research; preserve historical validation, never relabel it as a new run. Treat plugin descriptions as capability claims and keep Codex/Claude metadata aligned.

Contributions are licensed under this repository's MIT licence. Linked external laws and provider documents retain their own status and rights; link and summarize them instead of copying entire manuals.
