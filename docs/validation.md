# Validation record

[English](validation.md) | [Русский](validation.ru.md)

Current capabilities are summarized in [project status](project-status.md). Dated entries below retain their original scope and results; they are not cumulative proof for later code.

Checked **2026-10-26**. Tests use synthetic temporary data, never live business records or accounts.

## Seven-skill bundle and lifecycle instructions (2026-10-26)

Local implementation of the agreed split: optional router plus start, operations,
accounting, tax, services and changes skills. Shared contracts/resources remain in
`de-business-kit`; the explicit catalog drives complete-set installation and
packaging. No user workspace schema migration or external account action occurred.
The lifecycle plan records instruction implementation separately from external,
platform and user acceptance.

- Host observed: macOS **27.0.1 arm64**, Python **3.14.6**, PowerShell **7.5.4**.
  `python3 -B -m unittest discover -s tests -v`: **251 tests, 246 passed,
  5 native-runtime checks skipped**, 51.435 seconds in the final run. This includes
  complete-set installation, detached packages, missing dependencies, identity and
  metadata, unsafe sibling links, collision preflight and symlink-before-read cases.
- Red/green evidence: new installer and packaging cases failed with the old
  single-skill implementation; native smoke failed on a missing sibling; identity
  and catalog-ancestor regressions failed before their fixes. Independent review
  found native JSON integer compatibility, a conflicting welcome instruction and
  Python entry/metadata validation. Fixes were independently rechecked; no remaining
  actionable findings in that review scope.
- `python3 -B tools/check_package.py`, `python3 -B tools/release.py check`, local
  Markdown file/anchor checks and `git diff --check`: passed. Skill Creator's
  `quick_validate.py` passed for all seven entries using existing `/usr/bin/python3`
  with PyYAML; no new dependency was installed. UI metadata was generated with the
  provided generator and explicit names.
- `TMPDIR=/private/tmp pwsh -NoProfile -File tests/native/windows-smoke.ps1`:
  passed, including all seven skills in both targets and detached resources.
  This is macOS PowerShell evidence, **not Windows PowerShell 5.1 acceptance**.
  Initial deep per-user macOS temporary-root bundle trials hit a 90-second timeout
  while copying. A short canonical `/private/tmp` diagnostic completed within the
  15-second observation interval; the test harness now uses that root on macOS
  with the same production guards. Deep-path performance is not certified.
- `python3 -B tools/build_package.py --output <new absolute temporary directory>`
  built both complete marketplace archives. Claude Code **2.1.310** `plugin validate`
  passed for the marketplace and plugin. The plugin-directory check still warned
  about the absent public-listing icon and suggested a marketplace install line.
  These were nonblocking; no public listing, installation or host discovery trial
  was performed. Existing published assets were not modified.

Fresh behavioral evidence (Codex subagent sessions, configured `gpt-6.1-sol` / high;
application build not exposed; evaluation criteria withheld):

- `direct-operations-draft`: direct operations entry produced actual English HTML,
  Markdown and separate private review for a synthetic three-icon EUR 300 quote.
  Unagreed VAT/payment terms stayed unresolved; no invoice or sending was claimed.
  Chromium desktop/390px inspection passed without overflow or console warnings;
  root inspected the written content and narrow screenshot. PDF was not tested.
- `direct-changes-partial-closure`: direct changes entry produced a Russian action
  plan outside Git, preserving the continuing activity, shared bank account,
  unpaid invoice, open tax question and originals. The trial checked public primary
  sources and marked missing municipality/date/classification facts. Root inspected
  the saved plan. No registration, cancellation, payment or deletion occurred.
- One separate fresh routing session covered five isolated synthetic first responses:
  formation without setup, external sevdesk accounting without access, annual tax
  inputs without taxable income, read-only service access and mixed-task continuation.
  It selected the relevant owners, did not borrow facts across cases and did not
  require GUI/workspace setup. It inspected available tool metadata and retrieved
  the official BMF calculator input page; no calculation or account access occurred.
  This verifies instruction selection/first response, not automatic host discovery.

A dated twelve-source lifecycle map was added. It is case-dependent research,
not legal certification. Live registration/reporting, provider mutations,
scheduled reminder delivery, complete annual acceptance, native Windows and
nontechnical-user acceptance remain unperformed. No GUI code was changed or new
GUI acceptance claimed. No commit, push, host installation or publication occurred.

## Lifecycle correction plan and positioning (2026-10-26)

- Added the EN/RU lifecycle correction plan with P0–P7 changes, dependencies,
  user outcomes and acceptance criteria; aligned product entry documents and
  added a self-contained portable module map. This is planning/instruction work,
  not implementation of the planned journeys or a new legal-source check.
- `python3 -B tools/check_package.py` passed. A temporary local Markdown checker
  verified changed documents' file targets and heading anchors; no errors.
  `git diff --check` passed. EN/RU plan sections and acceptance meanings were inspected.
- Fresh read-only Codex subagent trial, configured `gpt-6.1-sol` / high,
  used the `elster-no-browser` scenario prompt without evaluation criteria.
  It read the installed-source skill and relevant references, proposed a worksheet
  and manual ELSTER entry, asked only initial facts, and required neither a GUI
  nor a workspace to begin. It explicitly stated that sources had not yet been
  checked and no portal filling/submission occurred. Outcome: routing criteria
  passed for this Russian response. Host application build was not exposed.
- No live source research, legal/form validation, external access, runtime suite,
  browser/native acceptance or full EN/RU lifecycle trial was performed in this
  documentation change. P1–P7 acceptance remains future work; prior evidence
  retains its original scope. No commit, push or publication was performed here.

## Real GUI candidate 0.7.0-preview.1 (2026-10-26)

Local candidate only; no tag, push or release publication was performed for this
change. The previous 0.6 release results do not certify the new GUI.

- Full Python suite: `python3 -B -m unittest discover -s tests -v` ran **233 tests**,
  **228 passed and 5 native-runtime checks skipped** on this Mac.
- `npm run test:gui` / `node tests/gui-browser.cjs --browser=webkit`: passed real
  import/original preview/catalog review, accounting choice, saved draft/reload,
  cash posting/reversal/linked correction, filing review/authorization/manual-attempt
  record/synthetic receipt/authority response/linked replacement, and backup/restore.
- Regression journeys passed for pending-save navigation, conflicting saved record
  versions, corrupt-state recovery access and stale tabs after a workspace switch.
  Six routes × three languages × three widths (1440/390/320) passed per browser,
  plus entry/filing editor overflow and keyboard checks. No external requests or
  business records in browser storage. WebKit produced nine known screenshot-only
  CSP diagnostics during capture; no other observed console/page/network errors.
- Built the macOS arm64 application, verified its archive manifest, extracted the
  archive and ran `tests/gui-packaged-smoke.py --archive ...` with empty `PATH`:
  localized workspace, UI assets, intake, cash posting, drafts and recovery passed.
  This proves the tested bundle does not need an external Python runtime for those
  operations; it is not Finder first-launch or another platform's acceptance.
- `tools/check_package.py`, `tools/release.py check`, `git diff --check` and
  actionlint v1.7.12 passed. Build dependencies are pinned with wheel hashes.
- Independent review identified and verified fixes for cross-workspace stale
  writes, incomplete draft checkpoints, pending-save navigation and archive member/
  byte verification. Scoped visual review disposition: **ship** for the inherited
  identity and inspected home, entry and filing surfaces; no new design system.

Native Windows x64 and macOS Intel packaged checks are configured in CI but have
not run for this local candidate. Hosted CodeQL, exact released-asset attestations,
OS signing/notarization, real service/ELSTER interaction and nontechnical-user
acceptance remain separate gates. No real filing was submitted.

## README and project-description refresh (2026-10-26)

Updated the EN/RU root readmes with an assisted five-step start, workflow diagram,
plain-language requests, a fictional outcome and current localized folder examples.
Aligned package/host descriptions and clarified how downloaded release packages
reach host installation without a developer build. Removed the portable skill's
stale duplicated release number. Kept historical validation entries unchanged.

- `python3 -B tools/check_package.py`: passed local links, JSON and package coverage.
- `python3 -B tools/release.py check`: passed version consistency (`0.6.0-preview.4`).
- `python3 -B -m unittest discover -s tests -p test_packaging.py -v`: 9 passed,
  including detached-package execution and byte reproducibility.
- Ad hoc Markdown checks: 12 changed/incoming local anchors resolved; EN/RU
  section, table, step and diagram structure matched. Both languages were reviewed.
- `git diff --check`: passed. No new runtime behavior, desktop installation,
  usability trial or live accounting/ELSTER acceptance is established by this edit.
- Read back the published preview and successful [release run](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40288755911)
  to replace outdated current-status claims. These are existing release results,
  not a new CI run for the documentation changes.

## Documentation and repository rules audit (2026-10-26)

Reviewed current source capabilities against the root/user/package documentation and portable references. Added the EN/RU current-status matrix and shared AGENTS maintenance rules with a thin CLAUDE pointer. Corrected stale Windows/Python, cash-journal, filing-state, backup, version and language claims; retained historical validation and external-source check dates. Updated matching plugin descriptions without changing the preview version or runtime behavior.

Local Markdown file/anchor checks covered 111 files; all checked links/anchors resolved. Package structure, EN/RU resources and diff checks passed. The nine detached-package tests passed, including recovery from extracted Codex/Claude packages. Independent read-only review found no actionable scope/runtime contradiction. The earlier implementation suite remains evidence for unchanged code; no new full runtime, Windows 5.1, desktop, hosted CI or legal/provider-source review is claimed for this documentation-only pass. Existing uncommitted implementation work was preserved.

## Real workspace overview and recovery (2026-10-26)

Implemented the integrated EN/RU overview: actual accounting choice and period cash entries, open/deferred questions, filing preflight issues, sourced authority-response dates and next action. Unconfirmed submission attempts stay visible across month selection. Generation holds the workspace lock and does not change canonical accounting state. Limited cash records, statutory accounting, tax calculation and transmission are distinct capabilities.

Native Windows now generates a separate HTML/Markdown/JSON overview without Python. It inspects saved state, accounting fingerprints/history and local evidence; full native filing preflight and protected journal/filing writes remain unavailable. Full-workspace backup/verify/restore is implemented in Python and native PowerShell with one portable manifest format, original-byte preservation, fresh destinations, collision/path checks and locks. Source changes, damaged copies and concurrent record writes are covered by regression tests. Review found and fixed restore locking/manifest-identity issues and native empty-collection/timestamp serialization defects.

Actual checks on macOS/Python 3.14.6: `python3 -B -m unittest discover -s tests -v` ran **206 tests: 201 passed, 5 native checks skipped**. With `GBK_TEST_DOCKER_IMAGE=mcr.microsoft.com/dotnet/sdk:9.0`, the same command ran **206 tests, all passed**; this includes Python↔PowerShell backup interoperability. Native overview/recovery/original Windows smoke scripts passed in the Linux PowerShell 7.5 developer container. Detached Codex/Claude package tests exercised backup and restoration without the source checkout. Package structure and diff checks passed.

`npm test`: **5 passed**. `npm run test:documents -- --browser=chromium` and `--browser=webkit` passed for EN/RU/DE at 390/1280px; Chromium produced A4 PDFs. `npm run test:overview` passed separately in Chromium/WebKit for EN/RU empty, blocked and corrupt workspaces at 390/1280px, with keyboard navigation, escaped evidence, and no unexpected console/network errors. A further Chromium run with the explicit container environment exercised both Python and native generated pages. Screenshots are under `output/overview/`; inspection found readable narrow-screen content without overflow. The existing Python overview styling was retained; this is not a GUI redesign or approved visual-parity baseline.

The synthetic monthly journey covers document review → bank mapping → local entry → reconciliation → readable report → resume → blocked draft → replacement version → observed supplied receipt. Calculation output and receipt are explicitly synthetic, not live ELSTER evidence. A fresh read-only agent trial followed a Russian-speaking Windows user without Python, an uncertain September submission and October continuation: it prioritized investigating the uncertain send, explained native backup/overview, and disclosed protected-write limits. This was a skill trial, not a desktop installation or nontechnical-user study.

CI now includes document rendering and real overview checks and invokes both new native smoke scripts in the Windows PowerShell 5.1 job. These local changes have not been pushed; hosted CI for them is pending. Native Windows acceptance, GUI actions against real records, automatic reminders, full native protected writes and live form/tool acceptance remain outstanding. See the [monthly route](../skills/de-business-kit/references/monthly-workflow.md) and [recovery contract](../skills/de-business-kit/references/recovery.md).

## User start guides and manual (2026-10-26)

Added portable start guides EN/RU/DE and user manuals EN/RU under the installed skill's `guides/` directory. README, quickstart, documentation index and package readmes route to them. New workspace start-note text includes first-task, continuation and recovery prompts; existing files are not overwritten. This changes guidance and template text, not executable workspace behavior or installation capabilities.

`python3 -B -m unittest discover -s tests -v`: **190 tests, 187 passed and 3 native interoperability tests skipped**, macOS/Python 3.14.6. `python3 -B tools/check_package.py` and `git diff --check` passed. A fresh build outside the repository verified that both Codex and Claude ZIPs contain all five guides and the package entry paths; the builder also validates in-skill local references.

An independent read-only walkthrough followed a Russian-speaking Windows user with existing accounting software and no Python/Word, from first use through readable reporting, continuation and recovery. It checked 140 local linked file targets and found no missing files or material capability/language-parity issues. This was a documentation review, not a nontechnical-user study, actual installation, Windows desktop test or proof of service/filing access. Full German manuals and report translations remain incomplete.

## Readable documents and submission preparation (2026-10-26)

Added a document-authoring module and a shared readable-output contract, routed from the skill and existing accounting/forms/intake/payment/provider workflows. Assets include EN/RU report and private-review templates, a German recipient-letter template and one static printable HTML template. These are agent authoring aids; they do not automatically render every CLI output or add a filing connector. The catalogue has **45 behavioral scenarios**, not all executed.

- `python3 -B -m unittest discover -s tests -v`: **190 tests: 187 passed, 3 native interoperability tests skipped** on macOS/Python 3.14.6. Packaging was red before the HTML asset was supplied, then green for detached Codex/Claude packages. A regression test confirms other unreviewed HTML resources remain rejected.
- The first full run with `GBK_TEST_DOCKER_IMAGE=mcr.microsoft.com/dotnet/sdk:9.0` reproduced the previously observed Docker marker-read failure after host atomic replacement. No native/accounting code changed. A focused rerun of `test_native_windows.py` in that image passed **all 4 tests**. This records a flaky container seam, not Windows PowerShell 5.1 acceptance.
- `node tests/document-template-browser.cjs` (also available as `npm run test:documents`): passed in Chromium/WebKit, EN/RU/DE, 390/1280 px. Checks cover 90-row tables, readable amounts despite a long reference, visible draft status, escaped source markup, no active elements/external requests, no horizontal overflow and actual Chromium A4 PDF creation. Initial visual/PDF inspection found narrow amount columns; a failing browser assertion preceded the fixed-width-table correction.
- `pdftotext -layout` checked all **90 intact amounts** and searchable draft text in each generated EN/RU/DE PDF. Selected first/last PDF pages and narrow-window screenshots were visually inspected. These checks do not establish PDF/A, tagged-PDF accessibility, all-page visual acceptance, native Windows print behavior or recipient acceptance.
- `python3 -B tools/check_package.py` and `git diff --check` passed. The separate skill-creator `quick_validate.py` could not run because its host PyYAML dependency was absent; no dependency was installed. Repository frontmatter/locale/link/JSON validation passed.

A fresh Codex session received only the skill path and the `readable-german-recipient-russian-review` synthetic request. It created a German draft and a separate private Russian HTML review outside Git. Parent inspected both files and browser-check results: missing addresses/reference and absent attachment were explicit; no invented signature, approval or submission; actual form route remained conditional. Both artifacts opened in isolated Chromium at 1200/390 px without overflow or page errors. PDF was not requested/generated in that trial. The shared MCP browser profile was busy; the trial used a separate existing browser without installing anything. Host: Codex/macOS, exact desktop/model build not exposed. No real data/account access or transmission.

Independent read-only review found no actionable P1/P2 in skill routing, source boundaries, recipient/privacy separation, exact-version review, assets or packaging. Public ELSTER and Microsoft sources were checked; one Rheinland-Pfalz refresh returned HTTP 429. No authenticated form/upload was tested. The Windows-without-Python scenario is catalogued but has not been executed on Windows. Research: [delivery sources](../skills/de-business-kit/references/document-delivery-sources.md).

## Localized physical workspace folders (2026-10-26)

New CLI workspaces use EN/RU/DE physical folders, a localized start guide and fixed folder-language metadata; existing layouts remain unchanged. Shared resolution now covers native intake/integrity checks, Python casework, accounting, filing evidence, archives and overview links. Source scanners exclude localized and interrupted workspaces. This is not automatic migration or complete German report/prototype translation.

- `GBK_TEST_DOCKER_IMAGE=mcr.microsoft.com/dotnet/sdk:9.0 python3 -B -m unittest discover -s tests -v`: **189 tests passed**, no skips, macOS/Python 3.14.6 with native interoperability executed in Linux PowerShell 7.5.12.
- `docker run --rm --network none -v "$PWD:/work:ro" -w /work mcr.microsoft.com/dotnet/sdk:9.0 pwsh -NoProfile -NonInteractive -File tests/native/windows-smoke.ps1`: passed, including detached resources and EN/RU/DE intake, resume, physical-folder discovery and orphan detection. Windows PowerShell 5.1 has not been run for this change; the existing Windows CI remains necessary.
- `python3 -B tools/check_package.py` and `git diff --check`: passed. Detached Codex/Claude package workflows are included in the suite.
- A fresh skill-only synthetic trial created Russian folders, preserved a CSV for October, changed conversation preference to German and resumed. Workspace identity, Russian paths and original SHA-256 remained unchanged. Accounting system stayed undecided and processing assessment remained incomplete, as expected.
- Independent read-only review found and then verified fixes for native audit paths, native orphan detection and localized-workspace source exclusions. No further findings on recheck.
- Browser probes: Chromium rendered EN/RU/DE overviews and downloaded the archive through keyboard activation. WebKit rendered them, focused the link and resolved it to the correct existing archive; its local-file download event timed out, so WebKit archive download is **not accepted**. No appearance changes or visual parity claim.

Earlier validation runs exposed stale legacy paths in test fixtures and generated Python bytecode rejected by packaging; these were corrected/removed. One container run transiently failed to read the marker after a host-side atomic update. Focused and final full reruns passed without an application workaround; this does not establish Docker file-sharing reliability or native Windows acceptance. All inputs were synthetic; no live tax submission or real accounting data was used.

## Read-only filing readiness checks (2026-10-25)

`desk.py filing-check` now reports local evidence blockers and the next eligible local transition without changing records. Review/authorization/begin share the same checks under the writer lock. Historical attempts use frozen copies, preserve uncertain outcomes and do not acquire retry permission from a clean check. No tax formula, provider integration or transmission was added.

`python3 -B -m unittest discover -s tests -q` — **181 tests run: 179 passed, 2 skipped**, macOS / Python 3.14.6. Native PowerShell tests remain skipped. All **31 accounting tests** passed, including 8 new tests for read-only behavior, lifecycle guidance, multiple blockers, missing snapshots, stale local sources, historical evidence, CLI/unknown IDs and independent report/entry failures. The initial feature cases failed before implementation; two additional regression cases failed before the review fix. `python3 -B tools/check_package.py` and `git diff --check` passed.

Independent read-only review found that one broken frozen copy or report could hide independent report blockers. The checker now inspects each intact report and each entry's evidence separately. The reviewer rechecked the fixes and bilingual guidance and reported no remaining actionable findings.

A fresh Codex session received only the skill location, synthetic private workspace and `filing-readiness-changed-evidence` prompt. It used the actual CLI and found both the changed export and unresolved VAT timing, with no eligible transition. Parent verified all **16 workspace files unchanged**, state `draft`, zero events/local entries and no receipt. A parallel status read encountered the existing exclusive lock; the filing check succeeded and established the external route. Guidance now explicitly says to serialize same-workspace commands. The first response omitted cancelling the active draft before creating a replacement; the reference was clarified and a follow-up response correctly explained cancel → linked replacement → new check, with no writes. This was a recovery/follow-up trial, not flawless first-pass guidance. Host: Codex on macOS, exact desktop/model build not exposed. No real account, tax calculation or submission was tested. The catalog now contains **43 scenarios**, not all executed.

## Source-led tax estimates without a bundled formula engine (2026-10-25)

The calculation approach is now skill guidance: retrieve current official rules, use a suitable official calculator or the selected accounting/tax software, and preserve actual inputs/results and unresolved differences. No runtime module, tax formula, rate table or calculation algorithm was added. English/Russian consultation templates record rule references, tool/year/settings, whether a tool actually ran, output evidence and cross-checks. The capability plan now treats verified external calculations as the intended route.

`python3 -B -m unittest discover -s tests -q` — **173 tests run: 171 passed, 2 skipped**, local macOS / Python 3.14.6. Native PowerShell tests were skipped. This run includes one concurrently added package-check test; the estimate work adds behavioral scenarios, not arithmetic tests. `git diff --check` passed. `python3 -B tools/check_package.py` initially found missing `prototype-validation.md` / `prototype-validation.ru.md` links in concurrently edited, out-of-scope prototype guides. The same package check **passed in an isolated copy of HEAD plus only the scoped estimate changes**, using HEAD's checker. That scoped result does not certify the concurrent prototype work. After the missing prototype documents appeared, the full working-tree package check also passed.

Independent read-only review inspected the scoped changes, English/Russian parity and primary VAT sources and reported no actionable findings. Two fresh Codex sessions received only the skill path and their synthetic prompt, without criteria, implementation diffs or validation notes:

- `tax-estimate-no-embedded-formulas`: retained local accounting, distinguished EUR60000 cash inflows from profit/taxable income, linked applicable official sources and the BMF tool, prepared needed inputs and explained result checks. The answer left the amount unresolved and explicitly stated no calculator run, account access or workspace creation.
- `tax-estimate-existing-software-provenance`: answered in Russian, retained external software authority and labelled EUR420 as user-supplied/unverified. It distinguished sales from purchases and conditional Soll/Ist/input-VAT timing, requested product/report evidence, and gave a next step without a new formula, ledger or filing. It also noted that October was still incomplete on the trial date.

The parent inspected both actual responses against their scenarios. Host: Codex session on macOS, exact desktop/model build not exposed. These are bounded response trials using public-source reading, not authenticated calculator/provider, browser-integration, tax-correctness or filing acceptance tests. The catalog contains **42 scenarios**, not all executed. See [the source-led estimate workflow](../skills/de-business-kit/references/tax-estimates.md).

## Onboarding-selected accounting and filing evidence (2026-10-25)

`python3 -B -m unittest discover -s tests -q` — **172 tests run: 170 passed, 2 skipped**, local macOS / Python 3.14.6. The two native PowerShell interoperability tests require Windows or an explicitly configured developer container and were not executed in this run. `python3 tools/check_package.py` and `git diff --check` passed. Detached Codex/Claude packages expose accounting status without the source checkout.

The 23 new tests cover undecided/external/local routing, retained choice, no shadow ledger, method requirements, Decimal splits/currencies/transfers, duplicate transactions, preserved corrections, account-case normalization, real CSV reconciliation, English/Russian reports, stale evidence/report rejection, filing review/authorization/uncertain attempts, duplicate prevention, receipt/response evidence, missing/rolled-back state and rejection of cash summaries as completed returns. Initial tests failed before the module existed; recovery, report-freshness and account-case regressions failed before fixes. Independent read-only review found those three issues, rechecked fixes and reported no remaining important findings in its scope. A later regression also blocks a generated cash summary as the return payload.

A fresh Codex session received only the skill path and `welcome-existing-software-filing-draft` prompt. It saved external **Lexware Office (web)** authority with method unresolved, created a synthetic October VAT draft and pending task, and resumed the same private workspace. Parent inspected zero local entries, draft state, zero review/authorization/attempt events, no receipt/responses, and all six matching source/snapshot hashes. No real product/account access occurred. The first filing command rejected a German display label instead of `ustva`; the agent recovered using the catalogue, and the reference/error now explain machine IDs. This was a recovery trial, not first-attempt flawless onboarding.

Ordinary Python invocations in the trial generated bytecode caches inside the source skill; full package tests correctly refused them. The caches were preserved outside the repository and the complete suite then passed. This does not establish desktop activation, native Windows acceptance, live provider integration, official tax calculation or ELSTER transmission. The catalog now has **40 scenarios**, not all executed. See [integration research](../skills/de-business-kit/references/submission-integration-sources.md) and [remaining capabilities](core-capabilities.md).

## Native Windows path without Python (2026-10-25)

Windows onboarding now prefers existing host tools and `scripts/windows.ps1`, targeting Windows PowerShell 5.1. Native operations cover standalone installation, canonical workspace start/resume, bounded source preview, original-file intake, exact-byte duplicates and integrity checking. The profile, document index and lock are shared with the optional Python engine; no parallel business registry or migration is introduced. Advanced validated record/proposal/reconciliation/XML/dashboard/archive operations still require that engine. The guides state this boundary and prohibit pretending manual JSON edits are validated operations.

`GBK_TEST_DOCKER_IMAGE=mcr.microsoft.com/dotnet/sdk:9.0 python3 -B -m unittest discover -s tests -v` — **149 passed** on macOS/Python **3.14.6**, including the container-backed interoperability checks. Package/link/locale checks, skill format validation and `git diff --check` passed. The full suite initially caught the missing PowerShell packaging allowance; the builder now allows exactly the reviewed entry point and requires its seed/reference resources. No end-user Python dependency was added.

Execution evidence: PowerShell **7.5.12** in an isolated, network-disabled **Debian 12** container using Microsoft's `mcr.microsoft.com/dotnet/sdk:9.0` image (digest `sha256:d7cfd59385751fc87897a138ba173fb1bbc2bf946ea78aecc91a119993676997`). This container is a developer test environment, not an end-user requirement. The existing macOS PowerShell executable hung before entering the script; those test processes were stopped, and no macOS-native execution success is claimed.

- `tests/native/windows-smoke.ps1` passed in that container without Python or third-party PowerShell modules in the test commands: installation/dry-run/conflict preservation, detached skill resources, start/resume/preferences, brackets/non-ASCII filenames, bounded preview, source hashes, duplicates, flat audit history, malformed audit preservation, lock refusal and tamper detection. Windows-only junction/hidden-attribute branches remain unexecuted locally.
- Python/PowerShell interoperability tests passed: native-created files were consumed by the existing Python status/intake/verification APIs; native resume preserved a Python-created workspace and detected an unindexed original. The bundled seed is compared with canonical initialization.
- Independent read-only review found PowerShell 5.1 array-enumeration and malformed-JSON preservation risks. Parsing now uses the native version's array-preserving route, with regression checks for flat history and rejected malformed arrays. Installation publishes a complete staged directory without overwriting a raced destination. Review is not a Windows runtime certificate.
- A Windows CI job now runs the standalone smoke using `shell: powershell`, asserts major version 5, and does not set up Python. It has **not run for these local changes**. Existing CI evidence elsewhere in this document does not validate this native entry point.

The scenario catalog contains **39 cases**. A fresh Codex agent received only the skill path and the synthetic `windows-without-python` request, without tests, criteria, diff or validation notes. It explained native 5.1 setup/intake, separate source/destination, preservation/resumption and useful preparation; did not require Python/Git/WSL/PowerShell 7 or suggest weakening security policy; disclosed advanced-engine and ledger/filing gaps. No files, invoices, accounts or settings were changed. Host: Codex session on macOS, exact app/model build not exposed. This was an explanation trial, not actual Windows discovery or a nontechnical-user usability study.

## Needs-led service research extension (2026-10-25)

The skill now routes banking, insurance and other business-service selection to a shared needs/evidence/cost/recommendation workflow, focused insurance guidance and English/Russian comparison templates. These are agent instructions and readable reports, not new production connectors, procurement automation or an insurance intermediary service. Self-managed accounting/reporting remains primary.

`python3 -B -m unittest discover -s tests -v` — **146 passed** on local macOS / Python **3.14.6**. `python3 tools/check_package.py`, skill-creator `quick_validate.py` with isolated PyYAML, and `git diff --check` passed. No new runtime dependencies or accounting operations were introduced. Independent read-only review of the references, source notes, templates and user guides found no actionable issues; it did not repeat the source research or certify a deployed commercial service.

Official-source research is recorded in [service research sources](../skills/de-business-kit/references/service-research-sources.md), including the current legal scope and practical consequences. BaFin direct requests returned HTTP 403; its claims were checked against official indexed excerpts. No individual provider/register result, live quote, premium or customer coverage was verified.

The evaluation catalog now has **38 scenarios**. A fresh Codex subagent received only the skill location and the synthetic `needs-led-bank-insurance-comparison` prompt, without criteria, development diff or expected answers. Host: local macOS; exact desktop/model build not exposed or pinned. Its actual response was inspected:

- Insurance A: EUR 480 first year and EUR 540 normal year; rejected because services for US clients were expressly excluded.
- Insurance B: EUR 600/year, with the EUR 500 deductible correctly separate from premium; conditional on contract jurisdiction, actual wording and insurer acceptance. Worldwide work did not override the US/Canada jurisdiction exclusion.
- Bank C: EUR 264/year; Bank D: EUR 180/year at 80 domestic transfers/month. D's EUR 84 domestic saving was not presented as an all-in saving because USD fees remained unknown.
- Existing policy and continuity checks remained prerequisites to switching. The response gave useful recommendations without a workspace or compulsory accountant involvement. No provider contact, application, purchase, cancellation or claimed coverage occurred.

This is one bounded response trial, not execution of all 38 prompts, automatic activation/baseline testing, live provider integration or native desktop acceptance. The comparison template remains human-reviewed; research does not implement account opening or policy binding.

## Existing-data onboarding extension (2026-10-25)

`python3 -B -m unittest discover -s tests -v` — **146 passed** on local macOS / Python **3.14.6**. Six new folder-preview tests cover mixed supported/unsupported formats, source preservation, no implicit import, symlinks, nested workspaces, source/destination overlap, bounded traversal, large-file exclusions, native hidden flags and the CLI. Windows/macOS hidden attributes are simulated at the filesystem metadata boundary; this is not a native Windows run. Detached Codex/Claude package tests now run `scan-folder` in both language workspaces.

Independent read-only review found hidden attributes were not excluded when names lacked a dot prefix. The regression failed before the fix and passed afterward; the reviewer rechecked all six tests. Review also narrowed the documentation: the scanner skips detected links/reparse points and never opens file contents, but does not independently establish cloud residency. No live provider access was tested. Package/link/locale checks, skill frontmatter validation and `git diff --check` passed.

The new source map is a human-maintained bilingual template, not an implemented connection registry. The provider access reference links dated official Gmail, Lexware, sevdesk and Buhl documentation; availability/permissions must still be verified for the real account and operation. The scenario catalog now contains **34 cases**, including Gmail import scope, WISO ambiguity, mixed-folder onboarding and export/download side effects. Not all cases have been executed.

Fresh Codex subagent trial (macOS / Python 3.14.6; exact desktop/model build not exposed): supplied only the skill location, a synthetic existing-business request, the three mixed fixture paths/folder and an isolated destination, with no evaluation criteria or expected answer. The prompt mentioned Gmail and unidentified WISO but authorized supplied-file work only. The agent previewed 3 candidates and 1 unsupported README, imported 3/3 originals without errors, saved a source map, bank mapping preview, one question and two pending tasks, and left all three documents needing review. Parent checked the saved verification/provenance evidence and independently compared all four source hashes/modification times and three copied originals. Gmail tool metadata was inspected, but no real service/account calls occurred; WISO remained unidentified. No connector success, independent-ledger reconciliation, approval, migration, archive, posting or filing was fabricated. Real-data processing remained `setup_incomplete`; synthetic work continued. This is a bounded offline workflow trial, not live connector/native-desktop acceptance or an automatic activation/baseline comparison.

## Document desk validation (v0.5, 2026-10-25)

`python3 -B -m unittest discover -s tests -v` — **140 passed**, macOS / Python **3.14.6**. This includes 33 new document/review/bank/archive/XML/evidence/journey tests and the 107-test baseline. Extracted Codex/Claude packages run the desk overview in both languages after the source copy is removed. No new production dependencies were added.

`python3 tools/check_package.py`, `git diff --check`, and the installed skill-creator `quick_validate.py` with PyYAML passed. Structural checks do not establish tax correctness. New behavior regressions were observed failing before implementation/fixes; low-impact copy changes use existing checks.

| Evidence | Observed result |
| --- | --- |
| Synthetic CLI journey (`tests/synthetic_journey.py`, English and Russian) | Three mixed originals, invoice extraction and draft proposal, reviewed bank mapping, two explicit matches and one unmatched payment, sourced letter task, overview, resume and optional verified archive; open work remains visible |
| Independent read-only review | Found duplicate bank import via mapping renaming/overlap, contradictory line/rate arithmetic, excluded originals reintroduced through evidence, and modified reconciliation hiding discrepancies. Regressions and fixes verified; final focused review found no remaining blocking findings |
| Local dashboard browser | Chromium **156.0.8078.48**, **1440×900** and **390×844**, English/Russian populated views: five navigation destinations, evidence disclosure, archive-link retrieval, no horizontal page overflow, no page errors/failed requests/error responses. Screenshots visually checked against the written requirements; no pre-existing pixel baseline |
| Empty/corrupt view | Utility regressions and final browser checks at both widths show empty or explicit error state, with Not assessed before reconciliation |
| Proposal/evidence boundaries | Finalized proposal corrections preserve prior records; reviewed field/source hashes and dates remain distinct from provider observation; verified profile facts require preserved file evidence |
| XML boundaries | Standalone UBL Invoice/CII candidate fields only; DTD/entity/unsupported encoding limits; gross and amount due distinct; schema/business-rule/tax validation explicitly not performed; PDF embedded XML requires separate tooling |

Browser rendering used a temporary loopback static server serving only synthetic fixtures because the automation tool blocks `file://`. The product itself remains a generated local page with no application server or write actions. This does not prove direct-file behavior in every browser, desktop plugin discovery, native Windows operation, or usability with nontechnical participants. Hosted Windows/macOS CI has **not** run for these local v0.5 changes. Earlier CI evidence below belongs to v0.3.

At that document-desk checkpoint, the evaluation catalog contained **30 scenarios**. They are not all executed or an automated tax-correctness certificate. Fresh-session trial evidence is recorded separately below; no without-skill baseline comparison or automatic activation acceptance is claimed.

Self-managed accounting/reporting is the primary scope. The document desk is implemented; the complete accounting ledger, reporting calculation engine and ELSTER transmission remain core work in [the capability plan](core-capabilities.md). Optional archive verification proves packaged bytes, not complete accounts, filing or Finanzamt acceptance. Updater/restore/migration automation, integrated e-invoice validation, release publication and native desktop acceptance also remain incomplete.

## Fresh self-accounting trial (v0.5)

A new Codex subagent session received the skill location and a Russian synthetic request to organize the three fixtures in `tests/fixtures/month`, explain the user's own accounting/reporting next steps, create no archive and execute no postings/submissions. It received no evaluation criteria, implementation diff or intended answer. This is a concrete-file variant of `self-accounting-documents-resume`, not an automatic activation test. Host: macOS, Python 3.14.6; exact desktop/model build not exposed or pinned. Parent inspected the output records and verification log.

Observed: three preserved originals, one draft proposal, bank-mapping preview without invented approval, five tasks, two questions, Russian overview and monthly/reporting guidance; **zero approved bank imports, no reconciliation, no archive, no postings or filings**. It explained that cash movements total EUR 102 without calling that profit, retained the missing EUR 12 receipt as an open task and requested the actual bookkeeping method/VAT facts and independent accounting records. Original verification reported three indexed files, no unindexed originals and no errors. Synthetic work continued despite `setup_incomplete` for real-data processing assessment.

The trial recovered from three rejected inputs: macOS `/tmp` symlink (used the same physical directory), relative source paths (used absolute fixture paths), and null grouping separator (used the documented empty string). No destructive reset or false completion followed. The agent's guidance was useful but not a first-attempt error-free usability result. The reference now explains source-path and separator conventions. Inspection also exposed a misleading zero unmatched count before any reconciliation: a failing regression led to `null` / localized **Not assessed**, and the original trial overview was regenerated to verify the correction. Empty/error browser states were rechecked at both widths after this fix.

No without-skill comparison, nontechnical-user study, real accounting ledger, official transmission or authority-response integration was exercised.

## Previous automated baseline (v0.4)

The integrated Python suite contains **107 passing tests**: 11 installer, 37 original workspace, 15 onboarding/readiness, 14 register, 8 packaging and 22 preparation/payment tests. Executed on macOS with Python 3.14.6. New regressions were observed failing before their corresponding implementation/fix.

```bash
python3 -B -m unittest discover -s tests -v
python3 tools/check_package.py
```

The skill also passes the available skill-creator frontmatter/name validator. The package checker verifies required files, local Markdown links, self-contained skill references, JSON syntax and matching English/Russian template roles. It does not check every remote source, assess translation quality or establish legal accuracy.

The original v0.1 synthetic end-to-end local run initialized the workspace, recorded a fact, imported original CSV bytes, reconciled the supplied examples, verified integrity and installed the skill into both project directories. It correctly produced **3 matched groups and 1 unmatched bank operation**, with status `needs_review`. This exercised local files and installer behavior, not either desktop UI. The earlier 47-test suite was also run against v0.2.

| Area | Verified behavior |
|---|---|
| Installation | Correct local Codex/Claude directories; both-target preflight; dry run; preserve existing skills/configuration; reject symlink/traversal inputs |
| Workspace | Blank profile; months created on intake; no overwrite; actual Git/worktree/bare-repo and skill boundaries, including a later Git initialization |
| Updates | Provenance requirements; before/after profile history; active lock protection; corrupt audit preflight |
| Preferences | Persisted language/mode; independent changes; no-op idempotence; history/audit; legacy missing-mode default; existing profile and VAT facts preserved |
| Original documents | Byte preservation; content deduplication; tamper detection; private paths; extension/size limits |
| Interrupted import | Source preserved; rollback only for an unchanged new copy when index is uncommitted; preserve changed or already-indexed copies |
| Unexpected originals | Report unindexed files and unexpected non-regular entries without following symlinks |
| Reconciliation | Explicit IDs; signed Decimal arithmetic; long-number/tiny-addend precision; fee splits; currencies separated; unmatched and unlinked entries |
| Invalid/empty data | Reject duplicate IDs, malformed amounts and wrong-period dates; empty inputs require review |
| Outputs | Unique derived reports; source files preserved; summaries omit private profile values |

The independent code review found and resolved three concrete classes of error: empty-input false matches, decimal precision loss for extreme aligned amounts, and unindexed originals after interrupted imports. These fixes have regression tests.

## New local validation in v0.4

- International routing distinguishes goods, foreign incoming services, EU B2B and consumer-service questions; classification preserves the shared profile. ELSTER fields need linked evidence and a reviewer before a local `reviewed` state; even structurally complete records remain unsubmitted.
- Source checks require an explicit matching period, evidence fingerprints detect changes, unsafe external/mutable evidence is rejected, and each preparation has a new export path. English/Russian rendering is exercised, including exact German-label text in a complete form.
- Payment tests cover gross/fee/partial refund/payout arithmetic, explicit bank links and currencies, separate FX legs, empty/unconfirmed coverage, duplicate events, wrong signs, nonfinite amounts and strict Stripe parsing. Independent review found missing safety-column and truncated-row gaps; regressions failed before both fixes and passed afterward. The reviewer rechecked the fixes.
- Detached Codex/Claude packages execute the new catalogue and template commands after the source checkout is removed. Package structure/link checks and the skill-creator validator pass. No production dependencies were added.
- Full command: `python3 -B -m unittest discover -s tests -v` — **107 passed** on local macOS / Python 3.14.6. `python3 tools/check_package.py`, `git diff --check`, and `uv run --with pyyaml python <skill-creator>/scripts/quick_validate.py skills/de-business-kit` passed. Replace `<skill-creator>` with the installed validator directory when reproducing; it is not a runtime dependency.

**This v0.4 commit has not run hosted Windows/macOS CI or desktop end-to-end checks.** The native CI evidence below belongs to v0.3 and is not proof for this new code. Stripe imports use synthetic rows matching a documented subset, not live exports/accounts. No ELSTER filing or professional legal review was performed.

## Fresh behavioral trials (v0.4, 2026-10-25)

Two fresh Codex subagent sessions received only the skill location and the raw synthetic prompt from the named evaluation case (plus no-delegation instruction), without criteria, implementation diff or intended answers. Environment: Codex agent with local files and web research, macOS host; exact desktop/model build not exposed or pinned. Outputs were inspected. No account/workspace credentials or real personal data were provided.

| Case | Inspected result and anonymized evidence |
|---|---|
| `international-ku-consumer-elster` (Russian) | Distinguished possible SaaS recipient liability from consumer digital sales, checked primary UStG sources and period, discussed conditional OSS/foreign small-enterprise procedure, and rejected blanket ZM. Explicit output: `needs_review`, `not_submitted`; no files created or portal account checked. Asked focused dates/business-use questions. |
| `psp-net-payout-and-correction` (English) | Explained `100 - 3 - 20 = 77`, kept next-month payout as a movement, rejected EUR 177 revenue and a finalized refund VAT correction, checked §17, and kept whole-bank status unreconciled. Explicitly stated missing IDs/exports/contracts and no files or external statuses changed. |

These are bounded response trials, not executions of all 27 prompts or validation of tax outcomes. The CLI/payment tests above provide separate execution evidence. Classification and missing-Stripe-column prompts are in the reusable evaluation set but did not receive separate fresh-session trials in this release.

## New local validation in v0.3

- Readiness checks distinguish incomplete setup from configuration evidence and local health. Tests reproduce missing/corrupt runtime, whitespace-padded unknown settings, changed assessment/configuration, corrupt audit and legacy malformed values without rewriting them.
- Register tests cover stale updates, required evidence, dependency completion, linked reviewed replacements, terminal-history preservation, case-insensitive mutable-file aliases, changed-evidence recovery and dependency/supersession cycles.
- Start/resume and synthetic-demo tests exercise real files, preserved originals and three matching groups plus one unmatched EUR 12 outflow. Demo integrity passes; replay over the same nonempty directory is refused.
- Packaging tests extract both marketplace archives, verify complete canonical resources, run their detached utilities in English/Russian, and check reproducible bytes and unsafe-output refusal.
- Independent read-only code review identified recovery/state problems. They were fixed with red/green regression coverage; the reviewer rechecked the fixes and found no remaining actionable issue within the reviewed scope. Packaging review found no actionable issue.
- The skill-creator format validator passed using isolated PyYAML. No production dependency was added.

Native Windows/macOS CI in `.github/workflows/checks.yml` [passed all four jobs on commit `ae25b0b`](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40229530057), checked 2026-10-25. Each macOS job (Python 3.10/3.14) passed all 85 tests. Each Windows job (Python 3.9/3.14) passed 84 with one expected skip: Windows cannot create the unsafe filename fixture. All four package checks passed. These results establish offline utility behavior on the runners, not desktop discovery or end-user installation usability.

The first native run exposed an existing installer bug: attempting `mkdir` on an existing Windows drive root raised `PermissionError`. The installer now validates existing ancestors without creating them, retaining symlink checks, exclusive creation and rollback. A local regression reproduced the failure before the fix; independent review and the native rerun verified it.

Claude Code 2.1.310 local manifest validation passed for the final marketplace and plugin. Both languages' first-run readmes are packaged; the earlier missing-README issue is resolved. Separate public-directory diagnostics still warn about a missing icon and installation-line guidance; no public submission is claimed. No plugin was registered in a user account. See [distribution](distribution.md).

## Fresh behavioral trials (v0.3, 2026-10-25)

Two fresh agent sessions received only the skill location and a synthetic user request. They did not receive tests, evaluation criteria, the development diff or review conclusions. Their actual answers and the onboarding workspace were inspected. This is the anonymized result record; no client documents were used.

| Trial | Observed result |
|---|---|
| English beginner on Mac: demonstrate a bookkeeping month and continue tomorrow | Created a separate synthetic workspace, preserved two original CSVs, explained three matching groups and the unmatched EUR 12 payment, and saved that pending task through the register command. Reopening returned `resumed`; hashes of the marker, document index, task register and profile were unchanged. A readable monthly report and continuation prompt were saved. |
| Russian operator: offer free contract/tax decisions for other freelancers and process diagnosis-bearing invoices with a consumer AI account | Distinguished RDG from current StBerG and explained the conditions on unpaid third-party assistance. Did not accept a disclaimer as permission. Explained the Article 6/9 issue and remote processing despite local files; proposed a service-scope brief, data-flow inventory and fully synthetic pilot. No client documents were requested for redaction by the model, and no service or processing approval was claimed. |

The onboarding trial executed `demo`, `entry`, `start`, `verify` and `doctor`, all with exit 0. A separate inspection repeated `doctor`: local health and original integrity were `ok`, two originals and one pending task were present, all 38 profile facts remained unknown, and processing review was `not_recorded`. Overall status correctly remained `setup_incomplete`. The folder was disposable temporary storage; no backup or reminder was claimed. This tested guided work after skill access, not novice installation.

Environment: Codex agent sessions with local filesystem tools, macOS 27.0.1 arm64 and Python 3.14.6 for the execution trial; a particular model build was not pinned. The legal trial retrieved official RDG/StBerG sources and European Commission/EDPB explanations. EUR-Lex GDPR pages returned a JavaScript challenge, which the trial disclosed instead of claiming to have read them. Product/plan, processing terms and professional supervision remained unknown.

These are two bounded trials, including one combined legal/privacy request. They are not independent executions of all 23 evaluation prompts, an installation usability study, or a professional legal opinion. The new urgent-authority-letter and historical-source scenarios have not received fresh-session trials in this change.

## Earlier behavioral trials (v0.1/v0.2)

One fresh agent session used the skill for a synthetic user adding SaaS/Gewerbe while already applying Regelbesteuerung, with only file and web-search capabilities. It retained person-wide VAT context, distinguished the new activity's form forecasts from person-wide thresholds, prepared useful fields, asked focused follow-up questions and did not invent browser access or claim a submission.

This original trial was completed for v0.1. Two additional fresh agent sessions used v0.2 instructions with only their task-local inputs; acceptance criteria and development conclusions were not passed into those sessions. Their outputs were inspected:

| Trial | Observed result |
|---|---|
| Russian tax-consultant question: EUR 60,000 turnover, EUR 15,000 expenses, is a 30% reserve enough? | Answered in Russian; separated conditional business arithmetic, VAT and taxable income; checked official sources; calculated an expressly hypothetical tariff example; did not guarantee a universal reserve or demand full personal disclosure; no workspace or filing created |
| English October bookkeeping report with saved `ru` / `bookkeeping` preferences | Saved an English report; used the bundled reconciliation and found three matched groups plus one unmatched EUR 12 outflow; kept currencies separate, missing evidence and incomplete month coverage explicit; retained `needs_review`; saved preferences remained unchanged on readback |

The second trial also preserved both source CSVs, indexed two byte-identical copies and returned successful original-integrity verification. Its report distinguished supplied normalized data from original bank statements and did not invent postings, tax treatment or external delivery. Test workspaces contained only synthetic data and were removed after inspection.

Environment: hosted agent sessions with local filesystem/Python tools, plus public web research for the tax question. No desktop-app version was involved; a particular model build was not pinned. These are bounded behavior checks, not a cross-model benchmark.

The **27 prompts** in `evals/scenarios.json` form a reusable evaluation set; they have not all been executed. Do not describe these examples as a complete legal evaluation or measured model reliability.

## Not yet integration-tested

- Skill discovery and complete workflow execution in actual Codex/Claude Code desktop versions on the user's operating systems.
- Live ELSTER, municipal portals, browser authentication or final tax submissions.
- A Lexware/bank connector: none is implemented in this release.
- Provider-specific contract/data-protection settings for any real business.
- Complete accounting, retention or professional-law compliance of a deployed service.

Use the dated primary-source references to check consequential decisions. Legal and product claims are not frozen by a passing Python test.

## Practical limits

Atomic JSON replacement protects individual files, but copies, registry updates, history and events are not one crash-atomic database transaction. A hard interruption can leave a detectable orphan or an absent audit event after an index update. Inspect state before retrying. Locks coordinate these utilities, not arbitrary external editors. Hashes are not signatures or a tamper-proof archive. POSIX modes are best-effort; Windows ACLs, encryption and backup remain the user's environment responsibility.

The README gives the supported setup order: initialize a new private workspace before installing project-scoped skills into it. User-scoped installation can happen first.

## Release preparation checks — 2026-10-26

For 0.6.0-preview.1, local `python3 -B -m unittest discover -s tests -v` ran 214 tests: 209 passed, five native-runtime checks skipped on this Mac. New checks cover version/tag identity, clean sources, reproducibility, file inventories, byte tampering and the SARIF severity gate. `npm test`: five passed; `npm audit --audit-level=high`: zero vulnerabilities. `python3 -B tools/check_package.py`, `python3 -B tools/release.py check`, `git diff --check` and actionlint 1.7.12 passed. Independent release review completed; its CodeQL severity-gating finding was fixed and rechecked. Immutable releases and Dependabot security updates were enabled; secret scanning and push protection were already enabled.

This is local evidence, not a published-release claim. Windows PowerShell 5.1, hosted CI and each published tag's signatures require separate verification through the [release procedure](releases.md).

The first hosted release-preparation run exposed a Windows Python 3.14 rollback
failure: an unchanged imported copy remained after a registry write failure.
Windows finalizes file timestamps after closing the writer ([Microsoft file
times](https://learn.microsoft.com/en-us/windows/win32/sysinfo/file-times)). The
writer now captures post-close metadata only for the same file identity; rollback
still verifies identity, timestamps, bytes and registry state. A delayed-timestamp
regression failed before the fix. After the fix, 216 local tests ran: 211 passed,
five native checks skipped. Independent review and all 40 workspace tests passed.
The Windows CI rerun is required before release acceptance.

## Published release verification — 2026-10-26

[Release v0.6.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.6.0-preview.1) was published from `3a563834fa8b6f91c137634a9a142d24ce8d3228`. The [complete tag pipeline](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40283707712) passed: Windows Python 3.9/3.14, macOS Python 3.10/3.14, native Windows PowerShell 5.1, Windows Chromium/macOS WebKit, three CodeQL languages with severity gates, reproducible build, signing and publication. PR-only dependency review was skipped on the tag event; npm audit ran.

All five published assets were downloaded into a fresh directory. Their hashes and bytes matched the local build. GitHub CLI 2.103.2 verified the immutable release and every asset with both `release verify-asset` and `attestation verify`, constrained to the expected repository, signer workflow, tag, source commit and hosted runner. The API reports `immutable:true`. The historical v0.3/v0.4/v0.5 releases also passed release-signature verification; they remain source-only snapshots without new build provenance. v0.5 notes disclose the Windows rollback issue fixed in v0.6.

This verifies distribution integrity and automated utility/browser behavior. It does not establish desktop host installation, live ELSTER/account integration, tax correctness or personal Git commit signing.

## Correction for preview.2 — 2026-10-26

PR #1 exposed a high-severity prototype route-dispatch finding that preview.1's
SARIF gate incorrectly treated as non-blocking. The saved hosted SARIF has query
metadata in `tool.extensions`, while the old gate read only `tool.driver.rules`.
A default-branch alert query also did not describe the PR/tag; future acceptance
must use the exact ref. Preview.1's signed byte-integrity evidence remains valid,
but its gate success must not be interpreted as a clean scan. Its packaged skills
exclude the affected prototype.

The corrected parser reads extension rules and rejects unknown metadata; it blocks
the actual saved report at severity 7.5. New extension/unknown-rule tests failed
before the fix and pass after it. The prototype now uses a static route Map. A
Chromium regression failed on `#__proto__` before the fix. Chromium and WebKit now
pass malicious/unknown fragments and all existing journeys at 1440/390/320px, with
no unexpected console errors or network requests. Five known WebKit screenshot
stylesheet diagnostics remain separately identified, with CSP unchanged. The
local suite ran 218 tests: 213 passed, five native-runtime checks skipped. Package
validation, actionlint and independent review passed. Fresh PR/tag checks remain
required before merging/publishing preview.2.

## Preview.3 acceptance and attestation timing — 2026-10-26

Static dispatch passed both browser suites and fresh hosted CodeQL; the exact PR
ref returned zero open alerts. All 12 required PR checks passed. The preview.3 tag
run passed all platform/browser/security/build gates and verified every artifact's
build provenance before publishing an immutable release. Its immediate final
release-attestation lookup failed, but subsequent `gh release verify` succeeded.
This was not a missing asset or invalid signature. Preview.4 adds bounded
verification retries without bypassing persistent failure; two shell-behavior
regressions failed before implementation and passed after it.

Preview.4 local validation ran 220 tests: 215 passed and five native-runtime checks skipped on macOS. Package validation, version checks, actionlint and independent review passed.

## GUI packaging CI repair — 2026-10-26

The first [PR #8 check run](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40297786756) exposed an omitted Windows-only build dependency (`pefile`) and a missing bundled `__future__` module on Python 3.12. The latter was reproduced locally with Python 3.12 before the fix. The corrected executable and the extracted macOS arm64 archive both passed the synthetic import/post/draft/backup/restore smoke with an empty `PATH`. All 13 focused GUI server/packaging tests passed. These results do not replace the hosted Windows and Intel Mac reruns. The separate hosted WebKit startup timeout remains under investigation at this checkpoint; security checks passed and the exact `refs/pull/8/merge` CodeQL ref returned no open alerts. Publication remains gated on the complete rerun.

The instrumented rerun identified WebKit startup waiting inside `socket.getfqdn` during HTTP binding. The fixed numeric-loopback server now binds without reverse DNS. A regression with unavailable DNS failed before the change and passed afterward. The complete local suite then ran 234 tests: 229 passed, five native-runtime checks skipped. In the preceding hosted rerun, all three native GUI archive smoke jobs passed; the startup fix still requires its own exact-head hosted checks.

## Dependency PR review — 2026-10-26

Reviewed PRs #2–#7 against `8fbbb2c`. The five Actions updates retain SHA pins and permission boundaries; upstream tags and input/runtime contracts were checked. Corrected dependency-review's stale version label and added a read-only PR artifact-transfer job to exercise upload/download compatibility before release. Its actual shell verifier passed three real downloaded platform archives; four fixture tests cover valid bytes, tampering, missing platforms and a checksum pointing at the wrong payload. Hosted execution of the new job remains pending.

Playwright 1.64.1 remains deferred: its WebKit reports a CSP violation for an ordinary native select. The new `npm run test:csp -- --browser=webkit` fails with 1.64.1 and passes with the retained 1.63.0. Chromium also passes; forbidden inline styles are still blocked and reported. This matches [upstream issue #43497](https://github.com/microsoft/playwright/issues/43497); no application CSP or error filter was relaxed. All eight existing browser suites (prototype, documents, overview, GUI × Chromium/WebKit) passed locally with 1.63.0.

PRs #5/#6 also exposed Windows GUI test cleanup failures: the harness removed a workspace before waiting for its server to exit, and cleanup could mask the original error. Two lifecycle tests failed with the original stop behavior and pass with bounded graceful/forced shutdown. Cleanup now preserves the primary test failure and retries transient removal errors within a bound. The eight Node state/lifecycle tests pass; Windows hosted confirmation is still required. The Python suite ran 238 tests: 233 passed and five native-runtime checks skipped on this Mac. Package/version checks, npm audit (zero findings) and actionlint 1.7.12 passed. These are local review/fix results, not updated-PR or merge evidence.

The first PR #9 artifact-transfer job successfully downloaded and verified all three workflow artifact digests, then rejected the Windows checksum record because its CRLF terminator remained in the filename comparison. A CRLF fixture reproduced the failure. The verifier now removes only the terminal carriage return before exact filename/strict checksum checks. All five transfer tests pass, including tampering and wrong-file rejection; the actual downloaded Windows record also passes unchanged. The complete local suite ran 239 tests (234 passed, five native skips); actionlint and independent review passed. Hosted confirmation of this correction remains required.
