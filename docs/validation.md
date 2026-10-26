# Validation summary

[English](validation.md) · [Русский](validation.ru.md) · [Technical documentation](index.md)

Evidence index updated **2026-10-26**. Tests and public examples use synthetic data. [Current status](project-status.md) owns the capability matrix and remaining P1–P7 work; this page records what was checked. Old results do not validate newer source automatically.

## Evidence by scope

| Scope | Observed result | Limits and detailed record |
| --- | --- | --- |
| Published `0.8.0-preview.1`, source `04bcd80a008d48fcd4cdc635988440e17291c5a1` | Tag run [40342363902](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40342363902): 16 jobs passed, PR-only dependency-review skipped; all eight downloaded assets verified against checksums, exact repository/workflow/tag/commit provenance and immutable release proof | Automated Windows/macOS, PowerShell 5.1, browser and package evidence; not tax certification, ordinary-user desktop acceptance or live service operations. [Release record](history/validation-2026-10-26.md#published-080-preview1-verification-2026-10-26) |
| Beginner onboarding at `325a04e824600b428f4f544881ecd1808b4f3daf` | Local Python: 277 tests, 272 passed/5 native skips; detached packaging: 14 passed. Codex CLI 0.164.0 EN/RU and constrained Claude Code 2.1.310 discovery/first-answer trials on macOS; initial Claude scope regression fixed and retested | Conversations are not desktop download/sign-in/install acceptance. [Trial conditions and evidence](history/validation-2026-10-26.md#beginner-installation-guides-and-live-first-use-trials-2026-10-26) |
| Assisted-service source through `9f37d8106b64e961aadf181158b79704e1e2dea7` | Local Python: 277 tests, 272 passed/5 native skips; package checks/builds and synthetic browser-fixture smoke passed. Russian draft trial saved/reviewed known fields, final-send count 0. Fresh export retest generated once, lock count 0 | Agent-tool download retrieval remains unverified after timeout/policy block; fixture CSV success does not repair that gap. Claude unknown-field/formula regression fixed and retested; manual “done” without a receipt remained unconfirmed. [Full conditions and failures](history/validation-2026-10-26.md#assisted-service-discovery-draft-entry-and-manual-confirmation-2026-10-26) |

The [complete dated chronology](history/validation-2026-10-26.md) preserves earlier results, failures, corrections and prototype evidence. Temporary local paths in it identify evidence captured during those runs; they are not distributed artifacts or guaranteed durable links. The [original correction plan](history/lifecycle-plan-2026-10-26.md) is historical, not the current task queue.

## Run the relevant checks

From the checkout, using an existing development runtime:

```sh
python3 -B tools/check_package.py
python3 -B -m unittest discover -s tests -v
git diff --check
```

Choose additional checks by the changed area in [AGENTS.md](../AGENTS.md#validation-and-delivery): native Windows contracts, overview, recovery, GUI, printable documents, skill trials or packaging. Documentation-only work needs package/link/anchor/parity checks; resource moves also need detached-package verification. Build into a new absolute directory outside the checkout. Node/Playwright and Python development tools are not user prerequisites.

Native Windows acceptance requires Windows PowerShell 5.1 on Windows; a macOS/Linux PowerShell run is not equivalent. A fresh-session skill trial must record host/version, actual tools and observable outcomes without exposing evaluation criteria. A successful test, CI upload, health endpoint or polished file is not evidence of an external action.

## Open validation gaps

- Ordinary-user desktop install, sign-in, first launch, continuation and recovery on supported Windows/macOS hosts; other discovery routes and real installation screenshots/video.
- Real service-specific access, draft/export/submission and readback; Lexware remains local by user choice. No real ELSTER authentication or transmission was tested by the synthetic portal.
- Complete browser artifact retrieval in the assisted export journey; generation confirmation alone is insufficient.
- Representative complete accounting/reporting periods and actual selected calculation/form-tool results, beyond local cash arithmetic.
- Intermittent local PowerShell timeouts remain unexplained in historical runs. Later successful checks do not establish their cause or universal host reliability.

GitHub provenance does not supply Windows Authenticode or Apple notarization. No hosted production service was deployed. New source/package checks do not alter published archives.

## Documentation consolidation — 2026-10-26

Changes start from `9f37d8106b64e961aadf181158b79704e1e2dea7`. User help now has installation, one task manual and assisted-service guidance; `docs/index.md` is the technical entry point. Current scope/roadmap lives in `project-status.md`. Duplicate topic/start/task pages were merged, and original plans/validation moved to labelled history. Markdown file count fell from **161 to 132**; top-level `docs/` pages from **46 to 16**. Six original EN/RU plan/validation/prototype-validation documents were compared after normalizing relocated link targets: all original narrative retained. No runtime behavior, workspace schema or tax rules changed.

- `python3 -B tools/check_package.py`: passed, including EN/RU template coverage and portable links.
- All authored Markdown local file/anchor check: **883 links/anchors across 132 files passed**. EN/RU guide sections/tables and current technical pages were independently reviewed.
- `python3 -B -m unittest discover -s tests -p test_packaging.py -v`: **14 passed** (4.922 s), including detached resource/link checks.
- `python3 -B -m unittest discover -s tests -p test_skill_bundle.py -v`: **4 passed** (37.012 s); `test_package_check_scope.py`: **1 passed** (0.003 s), on macOS 27.0.1 arm64. Native-bundle cases here use local PowerShell; this is not fresh Windows PowerShell 5.1 acceptance.
- `python3 -B tools/build_package.py --output /private/tmp/gbk-docs-consolidated-package-20261026`: both host packages built; not installed or published.
- `python3 -B tools/release.py check` and `git diff --check`: passed. Independent read-only review found no blockers; a historical language-switch link was corrected and confirmed.
- Hosted checks inspected for the **prior** source: [PR #12](https://github.com/ilyafedotov-ops/german-business-skills/pull/12) at `325a04e` and [PR #13](https://github.com/ilyafedotov-ops/german-business-skills/pull/13) at `9f37d81` each show **17 successful checks**. These do not validate the documentation-cleanup commit.

The earlier full-suite/runtime evidence is reused only for unchanged behavior. No new browser journey, user study, live provider action, native desktop acceptance or release verification was performed for this documentation change.

## 0.9.0-preview.1 release preparation — 2026-10-26

Release preparation `ed74f64` versions the beginner onboarding, assisted-service workflows and documentation consolidation as `0.9.0-preview.1`. `VERSION`, both manifests, EN/RU changelogs and current download instructions agree. Independent release review found that packaged documentation links followed moving `main`; they now pin `v0.9.0-preview.1`, and the reviewer confirmed the fix. Earlier published tags/assets are unchanged; workspace schemas and accounting runtime behavior are unchanged.

- `python3 -B -m unittest discover -s tests -v`: **277 tests, 272 passed and 5 native Windows/interoperability skips**, 126.846 s on macOS 27.0.1 arm64. Includes release, packaging and security-policy tests. Log: `/private/tmp/gbk-090-full-tests.log`. Final documentation-only link pins were subsequently checked in the built packages and link checks.
- `npm test`: **8 passed**; `npm audit --audit-level=high`: **0 vulnerabilities**. Logs: `/private/tmp/gbk-090-npm-tests.log` and `/private/tmp/gbk-090-npm-audit.log`.
- `python3 -B tools/check_package.py`, all **883** local Markdown links/anchors, `python3 -B tools/release.py check` and `git diff --check`: passed. Both host packages built into `/private/tmp/gbk-090-preflight-package-20261026` without installation or publication.

These are prepublication checks. The exact release PR/tag must still pass its platform/security gates, and the immutable release plus all eight downloaded assets require exact repository/workflow/tag/commit verification. Prior PR evidence does not replace those gates. Real provider operations, ordinary-user desktop acceptance and complete browser artifact retrieval remain open.

### Release CI investigation and browser diagnostics — 2026-10-26

At release PR head `dc05b32`, Python and JavaScript CodeQL exported SARIF but failed during upload without an explanatory error; the unchanged failed-job rerun passed. The Actions-language scan passed the local SARIF policy with zero findings, but GitHub timed out processing its upload and had not registered that analysis. A neutral aggregate check is not treated as complete scan acceptance.

The Windows Chromium job also timed out at the saved-document reload (`tests/gui-browser.cjs:416`). Its previous write/recovery requests succeeded, then no browser API request appeared after reload; the busy attribute was absent. Existing logs could not distinguish a failed static script from a synchronous bootstrap exception. This is an unresolved initial CI failure, not evidence of a broken accounting write or permission to lengthen deadlines.

Test-only diagnostics now report bounded static-path outcomes, page readiness/translation availability, browser errors and server stderr with the known session token redacted, plus a synthetic failure screenshot. No application code, assertions or timeouts changed. An independent read-only review found no blockers. A temporary controlled probe blocked `i18n.js`: it exited with the expected failure and reported the failed script, undefined translations and the bootstrap TypeError. That validates the reporter, not the cause of the original Windows failure. Static response status means headers arrived, not that a script executed.

`npm run test:gui -- --browser=chromium` and `--browser=webkit` both passed locally: real-record/recovery/stale-tab journeys, 54 localized route/width checks and six task-home checks per browser. WebKit reported 17 existing screenshot-only CSP diagnostics under the narrowly scoped screenshot filter; Chromium reported none. Logs: `/private/tmp/gbk-090-gui-{chromium,webkit}.log`, `/private/tmp/gbk-090-missing-script.log`; initial CI logs: `/private/tmp/gbk-090-{windows-browser,codeql-python,codeql-js,codeql-actions}.log`. Fresh exact-head Windows and security checks remain required before merge/publication.
