# Validation summary

[English](validation.md) · [Русский](validation.ru.md) · [Technical documentation](index.md)

Evidence index updated **2026-11-25**. Automated tests and public examples use synthetic data; authorized live checks keep account evidence private. [Current status](project-status.md) owns the capability matrix and remaining P1–P7 work; this page records what was checked. It keeps evidence for current behaviour only; superseded runs and per-case details are in this page's Git history. Old results do not validate newer source automatically.

## Run the relevant checks

From the checkout, using an existing development runtime:

```sh
python3 -B tools/check_package.py
python3 -B -m unittest discover -s tests -v
git diff --check
```

Choose additional checks by the changed area in [AGENTS.md](../AGENTS.md#validation-and-delivery): native Windows contracts, overview, recovery, guided setup page, printable documents, skill trials or packaging. The former GUI and browser prototype were removed in 0.14; entries below that mention them are historical evidence. Documentation-only work needs package/link/anchor/parity checks; resource moves also need detached-package verification. Build into a new absolute directory outside the checkout. Node/Playwright and Python development tools are not user prerequisites.

Native Windows acceptance requires Windows PowerShell 5.1 on Windows; a macOS/Linux PowerShell run is not equivalent. A fresh-session skill trial must record host/version, actual tools and observable outcomes without exposing evaluation criteria. A successful test, CI upload, health endpoint or polished file is not evidence of an external action.

## Open validation gaps

- Ordinary-user desktop install, sign-in, first launch, continuation and recovery on supported Windows/macOS hosts; other discovery routes and real installation screenshots/video.
- Broader service-specific access, exports/submissions and readback beyond the bounded Lexware browser run above. Live API adapter acceptance remains open. No real ELSTER authentication or transmission was tested by the synthetic portal.
- Complete browser artifact retrieval in the assisted export journey; generation confirmation alone is insufficient.
- Representative complete accounting/reporting periods and actual selected calculation/form-tool results, beyond local cash arithmetic.
- The welcome wizard with Claude Code's interactive multiple-choice questions, in the Claude app and in the Codex app, and with a model on the native Windows route.
- Fresh-session trials of the German guides and report templates; the German text has had no independent native-speaker or tax-professional review.
- Intermittent local PowerShell timeouts remain unexplained in historical runs. Later successful checks do not establish their cause or universal host reliability.

GitHub provenance does not supply Windows Authenticode or Apple notarization. No hosted production service was deployed. New source/package checks do not alter published archives.

## Published releases

Each pin of the Claude marketplace moved only after these checks on freshly downloaded assets: checksums, immutable-release attestation and build provenance pinned to this repository, `.github/workflows/release.yml`, the exact tag and its commit, and GitHub-hosted runners. Native application archives are not claimed reproducible.

| Release | Tag commit | Published (UTC) | Release run and verification |
| --- | --- | --- | --- |
| [0.14.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.14.0-preview.1) | `ba4f974` | 2026-11-25 15:09 | Run 45639015635; all 5 assets passed with GitHub CLI 2.105.0; both skill ZIPs matched a local rebuild byte for byte |
| [0.13.0-preview.2](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.13.0-preview.2) | `656715e` | 2026-11-21 12:59 | Run 44906156351; all 8 assets passed with GitHub CLI 2.105.0; both skill ZIPs matched a local rebuild byte for byte |
| [0.13.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.13.0-preview.1) | `01eb044` | 2026-11-21 11:08 | Run 44897078006; all 8 assets passed with GitHub CLI 2.105.0; both skill ZIPs matched a local rebuild byte for byte |
| [0.12.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.12.0-preview.1) | `e6c78c0` | 2026-11-21 10:39 | Run 44894885649; all 8 assets passed with GitHub CLI 2.105.0; both skill ZIPs matched a local rebuild |
| [0.11.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.11.0-preview.1) | `9e2bc4c` | 2026-10-27 16:32 | Run 40538907997, 16 jobs; all 8 assets passed with GitHub CLI 2.103.2; skill ZIPs, metadata and notes matched the exact-tag rehearsal |
| [0.10.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.10.0-preview.1) | `9a4f33d` | 2026-10-26 22:36 | Run 40412289498, 16 jobs; all 8 assets passed with GitHub CLI 2.103.2; skill ZIPs matched the rehearsal |
| [0.9.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.9.0-preview.1) | `b7f85c0` | 2026-10-26 18:00 | Exact-tag run, 16 jobs; all 8 assets passed |
| [0.8.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.8.0-preview.1) | `04bcd80` | 2026-10-26 14:54 | Run 40342363902, 16 jobs; all 8 assets passed |

These are automated platform checks, not ordinary-user desktop acceptance, tax certification or live service operations. GitHub provenance is not Windows Authenticode or Apple notarization.

## German and Russian launch videos and 0.14.0-preview.2 preparation — 2026-11-25

Branch `claude/de-ru-videos-0.14.0-preview.2` adds German and Russian versions of both launch videos,
a Russian carousel and three real questions asked in Russian with the released 0.14.0-preview.1 kit,
makes the video renderer language-aware, and sets `VERSION` to 0.14.0-preview.2. Skills, helper
programs and record formats are unchanged.

- `tools/release.py check` accepted 0.14.0-preview.2; `git diff --check` was clean.
- The full unit suite passed (500 tests; 12 skipped because they need Windows).
- `tools/check_package.py` passed on a clean copy of the tracked and new files (the main checkout
  also scans a local, Git-excluded worktree). `tools/check_doc_links.py` checked 449 links and
  anchors with no errors.
- Renderer: before the caption-break fix, the English timelines and captions matched the published
  English SRT files line for line; the fix changes six English caption groups for future renders only.
  A browser measurement of every receipt row found two German rows overflowing; both were shortened
  and re-measured. All 46 narration clips end in silence (no truncation); the four rendered videos
  measured −15.6 to −15.9 LUFS integrated loudness.
- Published: the German (https://youtu.be/rY_VdGS7mPs) and Russian (https://youtu.be/sVlPgHtQ6zg)
  walkthroughs, each uploaded after a SHA-256 match with the local render, with its own captions;
  both answered through YouTube's public oEmbed endpoint. This is not a check of viewing on every device.

## GUI removal, German parity and 0.14.0-preview.1 preparation — 2026-11-25

Branch `claude/decommission-gui-german-parity` removes the local GUI application, the fictional
browser prototype, their tests and their CI/release jobs; adds German guides, illustrations,
message catalogs, report templates and German output in the Python renderers and the native
overview; adds the launch materials in `presentation/`; and sets `VERSION` to 0.14.0-preview.1.

- `tools/release.py check` accepted 0.14.0-preview.1; `git diff --check` was clean.
- The full unit suite passed (500 tests; 12 skipped because they need Windows). Report, overview,
  journey and packaging tests now also run in German.
- `tools/check_package.py` passed apart from a local, Git-excluded worktree; it now rejects a missing
  language for template roles, catalog keys, guides or guide illustrations.
  `tools/check_doc_links.py` checked 447 links and anchors with no errors.
- `test:csp`, `test:documents`, `test:overview` (including German pages) and `test:installer` passed
  in Chromium and WebKit on macOS.
- The native German overview was generated with PowerShell 7 on macOS; this is not the required
  Windows PowerShell 5.1 acceptance, which runs in hosted CI.
- All twelve EN/RU/DE guide illustrations were measured in Chromium with no text overflow.

## Documentation cleanup and 0.13.0-preview.2 preparation — 2026-11-21

Branch `claude/docs-cleanup` (merged as `0c1f572`) removed four superseded research notes, kept these
pages to current evidence, rewrote the project status and shortened the release page. Branch
`claude/release-0.13.0-preview.2` sets `VERSION` to 0.13.0-preview.2. Since the 0.13.0-preview.1
tag, packaged files changed only in the install guides' release links and one contradictory sentence
of the native Windows reference; no helper program, schema or test changed.

- `tools/release.py check` accepted 0.13.0-preview.2 in `VERSION`, both manifests, `assets/version.json`
  and both changelogs; `git diff --check` was clean.
- The full unit suite passed (523 tests; 12 skipped because they need Windows).
- `tools/check_package.py` passed on a clean export of the branch.

Not run locally: the native PowerShell checks, which the release workflow runs on Windows, and live
skill trials, since skill behaviour did not change.

## Welcome wizard and setup check — 2026-11-21

Branch `claude/welcome-wizard` adds the welcome wizard (`references/welcome.md`), `setup-check` in
`workspace.py` and `windows.ps1`, `assets/version.json`, and sets `VERSION` to 0.13.0-preview.1.

- Red/green regressions: the setup check reports a complete kit and an empty folder as ready and
  writes nothing; a missing skill and a second installed copy; existing, earlier-preview, filled,
  Git-contained and synced folders; the command under `python3 -I`; and `release.py check`
  refusing a kit version file that differs from `VERSION`. A cross-runtime test compares the
  Python and native reports for missing, empty, workspace and filled folders; the native smoke
  script runs the check under PowerShell 7 and, in CI, Windows PowerShell 5.1.
- The full unit suite passed (523 tests; 12 skipped because they need Windows); the
  PowerShell-gated tests and four native smoke scripts passed under PowerShell 7 on macOS.
- Live trials in fresh Claude Code 2.1.329 sessions (Claude Opus 5.5, High) with the built plugin:
  an English five-turn welcome ran the check, asked one question per step, created the workspace
  with `start` only after the folder choice, offered made-up data first and, when the user stopped,
  showed a summary, saved an unfinished-setup task through `entry` and removed its temporary input;
  `verify` reported `ok`. Russian first turns then skipped the welcome text: the model had written
  it before the tool call, where it stayed in hidden reasoning. With the welcome moved into the
  visible reply after the check, both English and Russian first turns showed the welcome, the AI
  notice, the approval line and a plain command description.

Not run: Claude Code's interactive multiple-choice questions (print mode has none), the Claude app,
the Codex app, a native Windows welcome with a model and a German live trial.

## Ask-to-install quick start — 2026-11-21

Branch `claude/ask-to-install-first` after `06f1cec` makes one request to the assistant the first
install route in both READMEs, both install guides, the German start guide and the guided setup
page. The Claude app, Claude Code and Codex steps follow as manual routes; the Claude Code commands
have their own section. The request now asks for the published release, checks all seven skills
and ends with a fresh session.

- `tests/test_installer.py` (8 tests, including the identical README and setup-page request),
  `tests/test_packaging.py`, `tests/test_doc_links.py`, `tools/check_package.py` on a clean copy,
  `tools/check_doc_links.py` (520 links), `tools/release.py check` and `git diff --check` passed.
- `npm run test:installer` passed in **Chromium** and **WebKit**; the German Claude kit-step
  screenshot shows the longer request without overflow.

Not run: the request itself in Claude Code, the Claude app or Codex. In Claude Code it would change
the tester's own plugin settings.

Hosted Windows CI (Python 3.14, tests 2/2) then hit an intermittent `PermissionError` in
`test_writer_waits_for_a_lock_that_another_writer_releases`: on Windows, creating the lock fails
while the previous holder is still deleting it. The bounded wait now treats that like a held lock
and re-raises a lasting refusal; two red/green regressions cover both cases, and the full unit
suite passed again locally.

## Onboarding live trials and fixes — 2026-11-21

Live trials used `main` at `fa7f785`, built with `tools/build_package.py` and loaded through
`claude -p --plugin-dir` (Claude Code 2.1.329, Claude Opus 5.5, High effort) in fresh sessions
without user settings, user instructions or MCP servers. Prompts were copied from the guides;
all data was fictional. Six sessions cost about USD 2.84 in total.

- The English and Russian first-task requests and "show me how to use this" gave one small step
  or three copyable requests without setup. The English first answer omitted the first-use AI
  notice that the Russian one included.
- Private-folder setup created the documented layout and saved facts, questions and tasks
  through the validated writers; `verify` reported `ok`.
- The start guide's inbox request imported both files without waiting for a choice, and its first
  `desk.py scan-folder` under `python3 -I` failed with `ModuleNotFoundError` before the model
  retried. Resuming read internal JSON and could not finish a manual hash check. The records app
  did not show files waiting in the inbox.
- The checkout installer's copy matched the packaged Codex skills byte for byte and refused a
  second install; the records app created the documented layout on first run.

Branch `claude/onboarding-fixes` addresses these, checked on macOS arm64:

- Red/green regressions: the helper programs start under `python3 -I` from another folder; the
  records app lists waiting inbox files read-only with the preview's skip rules and imports only
  names from that listing, which then move to Imported; the demo also runs in German and keeps
  its inputs in storage-year folders.
- 515 unit tests passed (11 skipped; those 11 and 8 related tests passed under PowerShell 7
  through the local stand-in), and the four native smoke scripts passed under PowerShell 7.
  `npm run test:gui` passed in **Chromium** and **WebKit**, including the inbox journey and the
  narrow-screen checks in EN/RU/DE; the 320 px Documents page first overflowed on a long result
  path, now wrapped. `tools/check_package.py` (clean copy), `tools/check_doc_links.py` (518 links),
  `tools/release.py check` and `git diff --check` passed.
- Retrials with the rebuilt bundle: the new inbox request previewed both files under `python3 -I`,
  mentioned the approval prompt, imported nothing and asked for the files and storage month.
  Resuming used `start` and `verify`, finished the integrity check and saved a new note version
  instead of editing the outdated one. In both, the very first shell command (before reading the
  references) was still a compound one; `SKILL.md` now states the plain-command rule too, not yet
  retested.

Not run: Cowork or Codex desktop apps, the native Windows route with a model, and Russian or
German folder setup by a model. Hosted CI for this branch is pending.

## Current record formats only — 2026-11-21

Local branch `claude/workspace-layout-phase0` after `ee283ff` removes read compatibility for record
formats from earlier previews. Checks ran on macOS arm64:

- New red/green regressions: a marker without saved language or mode is refused by `status` and
  `configure` without changes; a cash entry without `schema_version` 2 stops period reports and
  reversal; an install source without its skill catalog is refused. The installer fixtures now use
  a catalogued bundle, and the catalog-symlink test runs again after that change first made it skip.
  Integrity checks for malformed facts, untyped register entries, unfingerprinted verified facts and
  token-only locks are unchanged and lost their "legacy" names.
- The full unit suite passed (499 tests; 11 skipped because they require Windows or a configured
  PowerShell container image). `tools/check_package.py` passed on a clean copy;
  `tools/check_doc_links.py` (512 links/anchors), `git diff --check` and `tools/release.py check`
  passed.
- `npm run test:gui` and `npm run test:overview` passed in **Chromium** and **WebKit**.
- Under PowerShell 7 on macOS, the four native smoke scripts and the Windows-gated interop tests
  (through the local `pwsh` stand-in described in the folder-structure entry below) passed.

Not run: hosted Windows CI and Windows PowerShell 5.1, the packaged GUI smoke and fresh-session
evaluations; nothing is pushed, tagged or published.

## Single workspace folder structure and 0.12.0-preview.1 preparation — 2026-11-21

Local branch `claude/workspace-layout-phase0` after `fdcdd90` replaces the earlier layouts with one
folder structure (see the [folder-structure review](research/workspace-layout-review-2026-11-21.md)),
removes the layout options and hash-named originals, adds a procedure documentation draft at
setup, and sets `VERSION` to 0.12.0-preview.1. Checks ran on macOS arm64:

- The full unit suite passed (500 tests; 11 skipped because they require Windows or a configured
  PowerShell container image). The new `tests/test_workspace_layout.py` covers the EN/RU/DE tree,
  start guides and procedure draft, a one-to-one reversible mapping, refusal of earlier-preview
  folders (numbered folders, a version-1 or newer descriptor) without changes, numbered originals,
  inbox filing, the root overview, the internal register and bank year folders. The former
  layout test modules were folded into it; tests now resolve paths through the mapping and put
  assistant inputs in the work folder, and the case-insensitive evidence-alias test runs again.
- `tools/check_package.py` passed on a clean copy; `tools/check_doc_links.py` (512
  links/anchors, 33 files), `git diff --check` and `tools/release.py check` (0.12.0-preview.1)
  passed, as did the release, packaging and installer tests.
- `npm run test:gui` and `npm run test:overview` passed in **Chromium** and **WebKit**; the
  overview fixture builder was ported after its first run failed on a legacy path. `npm test`
  and `npm run test:documents` passed.
- Under PowerShell 7 on macOS (`TMPDIR` on a non-symlinked path), `windows-smoke.ps1` (single
  layout, procedure draft, numbering, inbox filing, refusal of earlier-preview folders),
  `overview-smoke.ps1`, `recovery-smoke.ps1` and `lock-smoke.ps1` passed. The Windows-gated
  interop tests (native lock recovery, native task overview, native/Python workspace and recovery
  interop) also passed through local PowerShell 7 with a scratch `docker` stand-in that runs
  `pwsh` on the same paths.
- A CLI run of a new English workspace showed the documented tree, filed the inbox source under
  `01 Inbox/Imported/2026-10/`, stored `2026-00001_Supplier invoice 42.pdf` and wrote
  `OVERVIEW.html`; a folder with an earlier-preview marker was refused with "nothing was changed".

Not run: hosted Windows CI and Windows PowerShell 5.1, the packaged GUI smoke, fresh-session
`evals/scenarios.json` trials and any release publication; 0.12.0-preview.1 is not tagged or
published, and the marketplace still pins 0.11.0-preview.1.

## Guided setup data and AI-risk step — 2026-11-20

Local branch work based on `4407107` adds a **Data & risks** step and usability
changes to the [guided setup page](setup-page.md), after a review of every
screen at 1280 and 390 px found the risk notice reduced to one welcome card, no
prompt to check the provider's training setting, no overall progress count, a phone
layout that pushed each heading about 410 px down and an unreadable marketplace
screenshot. Provider privacy and AI Act claims were checked on official pages the
same day; sources and consequences are in the [GUI scope](setup-page.md).
Checks ran on macOS arm64 with Playwright 1.63.0 and Python 3.15.2:

- `tests/test_installer.py` (6 tests) passed, including identical EN/RU/DE structure
  for the new step, the six practice-check cards matching the answer table in
  `installer/app.js`, the data request calling `de-business-kit` and the added
  official hosts.
- `npm run test:installer` passed in **Chromium** and **WebKit**. In each of the six
  journeys it ticks the provider's data settings, answers the practice check by
  keyboard (focus stays on the answer), corrects a wrong answer, keeps answers after
  a reload, copies the data request, opens, zooms and closes the screenshot dialog
  with Escape (focus returns), and checks the 7-of-7 count and bar. Without a chosen
  assistant the step shows both providers' settings. At 390 px the app-step heading
  starts within the top 300 px. No form or text inputs, console errors or non-file requests
  were found. WebKit reported 42 screenshot-injection CSP diagnostics;
  the page CSP was not relaxed.
- The first WebKit run failed "answering keeps focus": WebKit, like Safari, does not
  focus a button on a mouse click. The test now answers with the keyboard, which is
  the case where losing focus would matter.
- The full unit suite passed (495 tests; 11 skipped because they require Windows
  PowerShell). `tools/check_package.py`, `tools/check_doc_links.py` (499 links/anchors)
  and `git diff --check` passed.

Limits: the page cannot see or verify account settings; menu labels are shown in
English because localized labels were not checked. The GDPR and AI Act text is general
information, not a legal review, and the six practice cards simplify (health data is
covered in the text, not as a card). No screen-reader check, nontechnical-user trial or
hosted CI run exists for this change yet.

## Windows Checks wall time — 2026-11-20

[PR #30](https://github.com/ilyafedotov-ops/german-business-skills/pull/30) shortens
the Windows jobs that set `Checks` wall time. Nothing waited or timed out. The cause
was `workspace._read_regular()` requesting `limit + 1` (50 MiB + 1) bytes per read:
on hosted Windows runners that buffer cost **7.5–7.7 ms (Python 3.9) and
13.6–13.9 ms (3.14)** for a small file, versus 25–34 µs for a size-bounded read.
Path handling multiplied it: each evidence check reread the layout record and
shipped folder catalog about 24 times. The earlier suspect tests came from
misreading log timestamps, which mark when a `unittest -v` line finishes.
Defender real-time protection was already off on the runners; no OS setting changed.

Changes: evidence checks read the layout once and `stat` each protected record
once; the shipped catalog bytes are read once per process; reads are sized from
`fstat` and still refuse growth past the limit. Each Windows Python version runs
two `unittest -k` shards of the unchanged discover command, and a selector test
proves every discovered test runs exactly once. Symlink chain checks, the
workspace layout record, locks, `Checks gate` and Windows Python 3.9 coverage are
unchanged.

Temporary same-VM diagnostics ([44812573163](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/44812573163),
[44815333060](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/44815333060);
changed code first, so warm caches favoured the baseline) ran four heavy modules
(41 tests): Windows 3.9 **305 s → 49.5 s**, 3.14 **434 s → 29.8 s**.

| Hosted `Checks` run | Commit | Selector start → gate end | Windows 3.9 jobs | Windows 3.14 jobs | Prototype Windows |
| --- | --- | --- | --- | --- | --- |
| [44799353738](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/44799353738) (PR #28, attempt 1) | `9c3e5e9` | 15 min 26 s, failed gate | 881 s | 911 s | 383 s |
| [44806269174](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/44806269174) (PR #29) | `89e67c5` | 21 min 43 s | 799 s | 1,287 s | 658 s |
| [44815442989](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/44815442989) (PR #30) | `bb82e2c` | **5 min 30 s** | 272 s + 229 s | 134 s + 146 s | 135 s |

In that PR #30 run the unit-test steps took 210 s + 164 s (Python 3.9) and
122 s + 133 s (3.14), and Prototype `test:gui` took 31 s (294 s in the PR #29 run).
Shard weights were then updated from those logs (predicted Python 3.9 split
190 s/189 s). The next PR #30 run, [44818005665](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/44818005665)
at `a2678c5`, passed from selector start to gate end in **4 min 14 s**, with
unit-test steps of 127 s + 120 s (Python 3.9) and 121 s + 153 s (3.14) on faster
runners. Locally on macOS arm64, Python 3.15.2 ran
**494 tests with 11 Windows-only skips** in 72.9 s, and Python 3.9.6 ran the two
shards as 255 + 239 tests with the same skips. Package, release-version, Markdown
link and diff checks passed.

Limits: one hosted run per configuration, and runner allocation varies (the PR #29
Prototype job included a 205 s checkout stall). Remaining Windows-specific costs:
`fsync` on the runners' C: drive (where `%TEMP%` is) takes 4–13.5 ms per call
versus about 0.4 ms on D:. One `test_native_lock_recovery` PowerShell call exceeded
its 45 s timeout in PR #28 attempt 1; that is unrelated to this change and unresolved.

## Guided setup page — 2026-11-20

Local branch work based on `d89f796` adds the static [guided setup page](setup-page.md).
Checks ran on macOS arm64 with the existing Playwright 1.63.0 development dependency:

- `tests/test_installer.py` (5 tests) passed: identical EN/RU/DE structure with no
  untranslated sentences, unchanged skill names, official HTTPS hosts, release links
  matching the marketplace pin, and existing documentation anchors.
- `npm run test:installer` passed in **Chromium** and **WebKit**. Each run covers six
  journeys (EN/RU/DE × Claude/ChatGPT with alternating Windows/Mac user agents),
  official link targets, ticking and reload, a language switch that keeps the step
  and choices, refused storage, a phone user agent, unknown and inherited-property
  routes, and 1280/390/320 px without horizontal overflow. It found no form or text
  input fields, no console errors and no non-file network requests. Chromium checked
  copied clipboard text; WebKit automation cannot grant clipboard access, so only the
  displayed copy outcome was checked there. WebKit reported 24 CSP diagnostics, one
  per screenshot, from Playwright's injected screenshot stylesheet (as in the
  prototype tests); the page CSP was not relaxed.
- The full unit suite passed (486 tests; 11 skipped because they require Windows
  PowerShell). `tools/check_package.py`, `tools/check_doc_links.py` (489 links/anchors)
  and `git diff --check` passed.
- Hosted CI: [Checks run 44806269174](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/44806269174) at PR head `89e67c5`
  (after merging `main`) passed all 20 checks. `npm run test:installer` passed in headless
  Chromium on `windows-latest` and WebKit on `macos-latest`; the Windows Python 3.9 job
  ran 486 tests, including the five installer content tests (43 POSIX-only tests skipped).
- Official links on 2026-11-20: OpenAI, Microsoft Store and GitHub release URLs
  answered a one-byte range request with disk-image, installer or ZIP content.
  `claude.ai` refuses command-line requests (403), so the Claude sign-up page and its
  three download endpoints were checked in a desktop browser session: all three
  returned redirects. Nothing was downloaded or installed.

Limits: no account was created, no plan bought, no provider installer run and no
plugin or skill installed through the page. There is no nontechnical-user trial,
screen-reader check or interactive Windows/macOS desktop check; the hosted runs are
headless automation. The page is not published at a web address. Provider pages, labels and plans can
change after the check date.

User acceptance recorded **2026-10-27**: the user confirmed that the Lexware
browser integration works E2E. The accepted Office L zero-value invoice and manual
correction scope is stated in [current status](project-status.md); this adds user
acceptance of the observed runs, not a new provider/API test.

## Filed-return correction threshold — 2026-11-05

The shared tax reference now distinguishes missing evidence, uncertain treatment
and a subsequently recognized incorrect/incomplete return with possible tax
shortfall. It checks filing state/deadlines and separates prompt notification from
necessary later quantification. Three new catalogue cases provide four sessions:
anonymous USDT income, its 2025/2026 continuation, unresolved VAT treatment and a
recognized omitted taxable sale. No runtime, calculator or filing transport changed.

Independent read-only review found no blocking issues in the rule, routing,
EN/RU guides or scenarios. AO §153 and AEAO nos. 2.4/5.1 were checked against
actual official 2025 and 2026 text; the BMF crypto guidance was also inspected.
This observer verification does not retroactively establish tested-host access.

Eight fresh Codex CLI **0.166.0** sessions on macOS requested **gpt-6-astra/high**:
two baseline, four updated and two calibrated repeats. All completed within the
360-second limit with unchanged session files and valid mechanical capture.
The existing research runner's `run()` function was invoked by a private explicit
case adapter; neither predefined CLI selection nor runner implementation changed.
Follow-ups replayed the actual preceding answer, not a persistent host session.

- Baseline: **12 criteria pass, 2 fail, 2 uncertain**. One failure was an overly
  strict requirement to ask every intake question immediately; the other omitted
  individual authority-deadline facts. Notification-threshold clarity and source
  completeness remained uncertain. The earlier conversational concern was not
  reproduced as an unambiguous premature statutory-duty assertion.
- Updated: **23 pass, 1 fail, 4 uncertain**. The sole failure preserves the old
  question rubric. The continuation and both §153 branches passed their behavior
  criteria, including deadline qualifications and no delay for full calculation.
  All four source checks remain uncertain: full current BMF/AEAO access was
  incomplete; one session used official 2023 AEAO with an explicit currency limit.
- The intake rubric now permits one next question while requiring identification
  of missing material facts. Two fresh repeats yield **14 pass, 0 fail, 2 uncertain**:
  all non-source behavior criteria pass. The follow-up recovered the full BMF
  crypto PDF, but full AEAO access remained unresolved. Earlier frozen criteria,
  answers and assessments are preserved.

Baseline and updated `--summarize` returned valid **failed** assessments; the
calibrated pair returned **uncertain**, not all-green certification. This is
bounded instruction hardening with observed model
variability, not proof of deterministic causation or universal tax correctness.

`python3 -B -m unittest discover -s tests -v`: **481 run, 470 passed, 11 skipped**,
135.565 s; skips require native Windows/PowerShell acceptance. Package/JSON,
167 local Markdown file/anchor targets and diff checks passed. Runtime tests preceded the question-rubric-only
calibration and final evidence notes; unchanged runtime evidence is reused.
EN/RU additions were inspected. No desktop, provider or submission acceptance.

Private evidence: `<private-evidence>/german-business-kit/tax-correction-20261105/`
(`baseline`, `updated`, `calibrated`, adapter and unit log). Source base `d89f796`;
updated portable-skill SHA-256:
`830210863b053385f6d79bff8fb30e235f31045f93642e692e34fcd2f6098bdd`.
Raw transcripts stay outside Git. No notification, return, release or installation
was sent or performed by these trials.

## Test-data privacy audit — 2026-10-27

At source `87859b7`, all **294 tracked files**, including **75 test/evaluation
files**, were checked for known private account identifiers and live-test markers.
The only matches were **12 local home-directory references** in these EN/RU
validation notes; they now use `<private-evidence>` as a location placeholder.
No private account identifiers were found in the inspected tests or fixtures.

All five artifacts from full CI run **40550000915** were downloaded and inspected:
**1,247 file/archive entries**, **118 screenshots** using local OCR, and **three
PDFs** using text extraction. The two tracked guide images and fixture PDF were
also checked. No known private account identifiers were found. Browser fixtures
use fresh temporary workspaces and synthetic records; independent review confirmed
reserved example/test/invalid domains in test/evaluation email examples.

The scan of **1,661 reachable historical blobs** found the earlier home-directory
references only in these two validation pages. History was not rewritten. This is
a bounded identifier/OCR/source audit, not a guarantee about uninspected historical
artifacts or arbitrary future data. Local agent evaluations are not an OS-level
read-confidentiality boundary; their raw transcripts remain private and require
review/redaction before sharing. Public repository attribution is retained.

## Selective CI deployed: full and reuse paths — 2026-10-27

[PR #20](https://github.com/ilyafedotov-ops/german-business-skills/pull/20) passed all
**20 checks** at `6ef40cb` and merged under the previous branch requirements as
`175ab0936b64a1751ed085d43af37b0e269e789f`.
[Full Checks run 40550000915](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40550000915)
selected `full`, passed every platform matrix and the final gate in **18 min 58 s**.
The gate recorded PR **20**, full coverage and tree
`c3c5e96e361f3f69a8df9e9b3f164aae97e6dff8`.

[Main Checks run 40553134356](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40553134356)
selected `reuse` of that same PR run and tree and succeeded in **45 s**: selector,
quick checks and final gate passed; five duplicate runtime job groups were
intentionally skipped without scheduling their matrices. These are observed run
wall times, not a general performance guarantee. Independent main security scans
passed; all three analyses at the merge commit had zero results/errors and zero
open alerts. PR security scans were also clear on the exact tested merge ref.

After merging under the old requirements, the seven individual runtime check names
were replaced by app-bound `Checks gate`. All five security requirements, their
App IDs, strict up-to-date enforcement and every other branch-protection field
were verified unchanged. Exact before/after and rollback settings remain outside
Git. No published product asset or marketplace version changed; the verified
immutable release remains `v0.11.0-preview.1`. Tag/reusable calls are configured to
force full validation; no new release-tag run is claimed by this CI-only deployment.

[PR #21](https://github.com/ilyafedotov-ops/german-business-skills/pull/21) at `4bb511d`
then exercised the documentation-only path. [Checks run 40553701420](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40553701420)
selected `docs` and passed in **39 s**, with three successful jobs and five
intentionally skipped runtime groups. Independent security checks passed with
three zero-result/error analyses and zero open alerts on that exact PR merge ref.
This is hosted lightweight-path evidence, separate from the full runtime run above.

## Customer payment follow-up drafts — 2026-10-27

Implementation after `aff8e4a` adds protected `payment-followup-template`,
`payment-followup-prepare` and `payment-followup-check` commands. The writer uses
the current payment-comparison fingerprint under the same workspace lock and saves
DE/EN/RU customer text, a separate EN/RU private review and frozen input/review
snapshots with an audit-bound manifest. Positive, current and unblocked comparisons
support a factual difference query; clarification omits amounts. Nothing sends,
changes provider/payment state, claims overdue debt or adds fees/deadlines.

TDD first failed for the missing module. The final focused follow-up suite passed
**9 tests**, and the existing payment-comparison suite passed **12 tests**. Coverage
includes recipient/private separation, zero/negative/unresolved amounts, stale
comparison/hash, changed sources/corrections, artifact/manifest/frozen-review
corruption, preserved versions, invalid destination fields, date checks and CLI
execution in all three recipient languages. Independent read-only code and docs
review found no material issue; its additional probes confirmed stale bank/review
sources and changed manifest recipients fail appropriately.

Two fresh ephemeral **Codex CLI 0.164.0** sessions used copied skills and synthetic
workspaces without criteria. Both executed the protected writer/check and inspected
actual recipient and private files: a German EUR 29.00 difference query and a
Russian amount-free clarification for unconfirmed coverage. **8/8 criteria passed**.
Parent checks confirmed unchanged invoice hashes, current artifacts and no private
marker, bank identifier, internal path or hash in the recipient text. No network or
send command was observed. Evidence remains outside Git.

`python3 -B -m unittest discover -s tests -v`: **448 run, 437 passed, 11 skipped**
in 166.478 s. Package, changed-file Markdown links/anchors and `git diff --check`
passed. This validates local preparation, not external delivery, legal reminders,
mailbox state, native Windows or live provider settlement. `not_sent` describes
this preparation-only writer; later delivery needs separately observed evidence.

## Issued-invoice payment comparison — 2026-10-27

Implementation after `c15d344` adds `invoice-payment-template`,
`invoice-payment-prepare` and `invoice-payment-check`. It saves private, immutable
JSON/EN-RU Markdown comparisons from reviewed invoice-stated due and explicit
normalized bank references. Evidence snapshots, current invoice hash, correction
family fingerprint and audit checkpoints protect preparation and reuse. It makes
no bank/provider/ledger mutation, payment demand or paid-status claim.

TDD first failed for the missing module; later targeted regressions failed for
malformed treatment, overwritten repeated-source fingerprints and an as-of date
before issue. Independent review identified the latter two; fixes preserve the
first capture, verify the exact parsed bytes and leave pre-issue dates unresolved.
Initial fixture inheritance also re-ran unrelated invoice tests against an already
issued fixture; fixture reuse was corrected without changing production behavior.
Final independent review found no remaining material issue in the reviewed scope.

`python3 -B -m unittest discover -s tests -p test_invoice_payments.py -v` passed
**12 tests**, including CLI execution, prepayment exclusion, cross-period partial
receipts/refunds, wrong signs/unknown/duplicate IDs, bounded partial amounts,
currency/coverage/date/correction blockers, stale context, corruption and EN/RU
reports. Full `python3 -B -m unittest discover -s tests -v` passed: **439 run,
428 passed, 11 skipped**, in 178.140 s. Package validation, changed-file Markdown
links/anchors and `git diff --check` passed. No native Windows acceptance added.

A fresh ephemeral **Codex CLI 0.164.0** session used copied skills, a synthetic
workspace and the scenario prompt without criteria. It executed preparation and
freshness checking, inspected the actual Russian report, and independently checked
**89 - 60 - 29 + 10 = EUR 10.00**, excluding the already-included EUR 30 prepaid
receipt. All four criteria passed; parent inspection confirmed the saved remainder,
current evidence and unchanged invoice hash. Evidence remains outside Git. This
is local workflow execution with supplied reviewed inclusion/coverage facts, not
live bank/provider settlement or tax acceptance. The host invoked Python without
`-B` inside its disposable copy; no source checkout mutation was observed.

## Manual correction on the current plan — 2026-10-27

Working source after `475d418` adds the observed manual correction route and
same-object persistence/PDF checks to the portable Lexware reference, with EN/RU
guidance. In the authorized existing Office L company, one synthetic zero-value
manual correction was saved, independently reopened, edited, previewed and
exported as a draft PDF. A footer edit initially did not survive reload; a separate
edit/save/completion/readback succeeded. The timing cause remains unknown. The
original reference is textual; local `corrects` does not prove provider linkage.

After the user's explicit finalization approval, the same correction was finalized
once and left unsent. A readback timeout was resolved by inspecting the existing
object without repeating the write. Independent reload showed **offen**, not
**Entwurf**, with no sent history. The downloaded final PDF passed header,
one-page, number/original-reference, zero-amount and approved-footer checks.
Layout-preserving extraction plus whitespace normalization recovered a wrapped
reference that default extraction missed. A minimal corner render distinguished
the draft's graphical **Entwurf** band from the final PDF; this is not a complete
layout or statutory review. Initial failed checks remain in the private evidence.

The protected writer recorded `confirm-issued` as `issued` / `not_prepared`, with
no reported issues; EN/RU status reports were exported. The original stayed sent,
not cancelled, and its local record hash was unchanged. No refund, payment
reallocation, correction delivery, tariff change, paid setup or API call occurred.
Account readbacks/PDFs remain private outside Git; no personal screenshots are
included here. Zero-value issue does not validate nonzero credits, provider-native
linkage, cancellation, refund settlement, correction delivery or API acceptance.

Two synthetic fresh-session cases used read-only, ephemeral **Codex CLI 0.164.0**,
copied skills and prompts without criteria. The readback-disagreement case passed
all four criteria. The first manual-route response passed three of four, but omitted
the full pending verification sequence. An explicit preparation/simulation instruction
was added; a fresh same-prompt retest passed all four. The retest recovered from an
initial relative-path miss and read the copied reference. These are response checks,
not live-provider proof. Independent read-only review found no material issues in
the route, finalization boundaries or EN/RU scope; it did not inspect private evidence.

`python3 -B -m unittest discover -s tests -p test_eval_runner.py -v` passed **15 tests**.
Package, changed-file Markdown links/anchors and `git diff --check` passed.
Runtime code is unchanged; the prior full-suite result, including its PowerShell
timeout/rerun limits below, is reused rather than claimed as a new clean run.

## Screenshot privacy and draft PDF export — 2026-10-27

Working source after `da50004` adds a sharing check to the contract used by all
seven skills, with EN/RU guidance and operation-note fields. The observed regression
was an account screenshot embedded in owner chat with personal data. The new rule
covers capture/output minimization, separate irreversible redaction, inspection of
the actual exported file and metadata, and withholding unsafe images in favor of
text. It does not implement an automatic redactor or alter authorized complete
recipient invoices.

Four fresh read-only, ephemeral **Codex CLI 0.164.0** sessions passed manual review:
raw test-account screenshot in chat, reversible SVG redaction with hidden data,
separate invoice-recipient authorization, and draft-only PDF export. Sessions read
copied skills without evaluation criteria and used synthetic observations. These
checks establish the observed instruction-following responses, not effectiveness
of image-redaction software. Independent read-only review found no material issues
in the privacy boundaries or the added draft-only print route.

Live continuation on the existing Office L account inspected the draft's **Drucken**
dialog: its default **Fertigstellen + drucken** would finalize. Selecting **Als
Entwurf drucken** changed the action button to that label before execution. The
browser opened the draft PDF; download completed through Chrome/native Save into
the private evidence folder. Local `pdfinfo`/`pdftotext` checks confirmed one page,
PDF bytes, the draft marker, corrected test reference/text, VAT label and zero total.
An independent provider reload showed the same object remained **Entwurf**, with
no sent history. The protected local draft record/hash remained unchanged.

No tariff change, paid setup, API access, new invoice, finalization or send occurred.
Only a cropped PDF toolbar containing UI icons was displayed for tool navigation;
account/invoice screenshots and the original PDF were not embedded in the report.
Private PDF/readback evidence stays outside Git. No redacted image was produced or
claimed. PDF checks establish header/text content and provider state, not a complete
visual-layout review, statutory correctness or live API acceptance.

`python3 -B -m unittest discover -s tests -p test_eval_runner.py -v` passed
**15 tests**. Package/EN-RU/local-file checks, **168 changed-file Markdown
links/anchors**, and `git diff --check` passed. Runtime code is unchanged; the
preceding full-suite result and its two PowerShell timeout/rerun limits below
are reused, not reported as a new clean run. No native Windows or release
acceptance was added.

## Cost check and current-plan draft correction — 2026-10-27

Working source after `ee26590` adds a shared cost check before paid setup, with
EN/RU guidance and operation-note fields. The observed defect was upgrade-flow
navigation before a cost warning; no purchase occurred. All seven direct skill
entries now require the shared check. Three fresh-session cases in
`evals/scenarios.json` passed manual review on **Codex CLI 0.164.0**: paid trial and
incremental cost, declined upgrade with draft continuation, and unknown usage
charges despite bounded spending approval. Each used a separate read-only,
ephemeral session and a copied skill bundle without criteria; prices/account
observations were supplied synthetic facts. They prove instruction-following in
these scenarios, not enforcement by tools or actual billing behavior.

In the same authorized existing-company browser test environment described below,
a separate zero-value draft was saved, reopened from the list, corrected only in
its introduction, saved and independently reloaded. The provider UUID/number,
quantity, VAT setting and zero total matched; the rendered preview showed the
correction. **Entwurf speichern** left it visibly **Entwurf**, unissued and unsent.
The earlier issued invoice was not edited or resent. Private before/after evidence,
a protected local `draft` / `not_prepared` record and EN/RU reports remain outside
Git. This proves draft-text correction on the current plan, not correction or
cancellation of an issued invoice, nonzero tax correctness or API acceptance.

The account's API settings had disabled key creation and stated XL was required
on the tested L plan. The user's no-upgrade decision was retained; no plan change,
trial, new key or API request was made. Independent read-only review found no
blockers in the portable cost workflow and scenario coverage; it did not inspect
private account evidence. Runtime code is unchanged.

Validation commands: `python3 -B tools/check_package.py`, a changed-file check of
**174 local Markdown links/anchors**, and `git diff --check` passed. The full
`python3 -B -m unittest discover -s tests -v` run completed **427 tests: 414 passed,
11 skipped, 2 errors**. Both errors were 40-second PowerShell subprocess timeouts
in `test_native_task_overview` (accounting corruption and cyclic/unsafe evidence).
Both cases passed a focused rerun without code changes (**2 tests, 11.460 s**).
A standalone PowerShell startup probe also exceeded 8 seconds; the underlying
host timing cause remains unresolved. The initial full run is not reported as
clean, and macOS PowerShell does not establish native Windows acceptance.

## Lexware live browser acceptance — 2026-10-27

Against source `7a3ad48`, the connected Chrome browser on macOS completed one
owner-authorized **zero-value test invoice in an existing business company**.
This was not a provider sandbox. The user explicitly selected the company and
own recipient address after the accounting-record effect was explained. Private
account identity, original PDFs, screenshots and protected evidence stay outside
Git under `lexware-live-20261027`; no API credential or adapter request was used.
Host: macOS **27.0.1**, installed Chrome **156.0.8078.48**.

Observed journey: save one draft, independently select it from the document list
and reopen it, preview, finalize that same UUID with **Abschließen + speichern**,
inspect/download the one-page final PDF, review the exact email/sole recipient,
disable the default extra copy, send once and reopen the provider's **versendet
am** history. The sent recipient, subject, message and single PDF matched review.
The actual sent-history attachment was downloaded and was **byte-identical** to
the final reviewed PDF. The user explicitly acknowledged receiving the email and
PDF; this is recipient acknowledgement, not an independently inspected mailbox receipt.
Protected local issue/delivery attempts finished as `issued` / `delivered` with
EN/RU reports and preserved evidence.

Live findings: the browser rejected a title longer than 25 characters; saving the
draft already assigned a number; the zero-value finalized invoice automatically
showed **bezahlt**, without a payment action. The email iframe failed to render;
its exact observed same-origin UI URL worked in a separate tab. Browser extension
popups interrupted work and required user dismissal; native macOS Save dialogs
required completion. A finalization readback timed out, so the result was checked
without repeating the write. These observations refine the portable route;
this assisted run does not establish unattended reliability.

Package/local-link checks, **116** changed-file Markdown links/anchors and
`git diff --check` passed. Canonical invoice preflight reported no issues; preserved
evidence hashes and final/sent PDF equality were verified. Independent read-only
review found no blockers; it relied on the reported live observations, without
accessing private account artifacts. Runtime code is unchanged.

Still open: live API adapter/TLS acceptance, ordinary nonzero invoice tax/payment
correctness, required structured e-invoices, provider corrections and error/retry
journeys, native Windows and release acceptance. Earlier synthetic results below
retain their original scope; this live run does not convert them into provider tests.

## Lexware provider draft and sending route — 2026-10-27

Local implementation after `2a26dfe` adds an opt-in, fixed-origin Lexware Office
draft/readback adapter and a same-object browser finalization/sending handoff.
**24 provider regressions** and **23 existing invoicing tests** passed independent
review. Coverage includes durable intent before POST, exact authorized bytes,
account/object mismatch, one-attempt creation, GET-only recovery, malformed JSON,
preserved responses, redirects/credential echoes, download version drift and stale
browser authorization. A temporary mutation restoring the unsafe post-lock request
reread failed the race regression as expected; repository source was unchanged.

Full `python3 -B -m unittest discover -s tests -v`: **427 run, 416 passed, 11
platform skips** on macOS/Python 3.14.6. Package, local Markdown links/anchors and
`git diff --check` passed. Loopback HTTP tests exercised actual request paths and
headers; TLS configuration was inspected through a test socket replacement, not
a real provider handshake. Independent final code/contract review found no blockers.

Fresh Codex CLI **0.164.0** trials used copied skills and an explicitly synthetic
HTTP fixture. The initial session could not reach the fixture from its child
sandbox: the account check failed before POST, and it saved an honest blocked
report/task with zero creations. A fresh continuation with test-session network
access enabled reused the unchanged authorization, created exactly one draft and
independently GET-read the same UUID. It preserved the blocked report, left the
invoice unissued/unsent and distinguished stipulated amounts from missing computed
totals in that fixture response. The blocked run is not relabelled successful.

A third fresh session resumed supplied evidence of the owner's manual finalization
and send of that same object. It GET-read version 2, downloaded the PDF between
matching readbacks, inspected its text/render and recorded only historical issue
and dispatch. The fixture's total remained **one POST**; this session used six
GETs and no writes. Recipient receipt stayed unconfirmed, with an open task and a
new Russian report. **31** prior non-mutable files survived the first continuation,
then **52** survived the second; audit prefixes and evidence hashes were preserved.
**35** readable-report links resolved. Raw Markdown evidence copies retain their
original bytes/source-relative links, not links rebased to the snapshot directory.

All **144** baseline skill files per session stayed unchanged, with no cache extras.
Only provider/privacy documentation and the CLI help description differed between
copies; the final copy matches current portable source. Independent artifact and
provenance review found no blockers. Requested model/effort were GPT-6 Astra/high;
this records the request, not independently attested serving identity. The custom
writable harness is not sealed-runner or isolation acceptance.

Sources and supported-operation limits are in the [portable provider record](../skills/de-business-kit/references/assisted-services-sources.md#lexware-api-and-browser-route--2026-10-27).
Evidence stays outside Git under `.lexware-route-20261027`. The wrapper replaces
the fixed provider TLS socket with local HTTP and uses a synthetic credential;
these are synthetic API/CLI trials, not live Lexware, production TLS, actual browser
finalization/send, recipient receipt, legal/tax/format, native Windows, hosted CI
or published-package acceptance. API draft creation consumes a provider number;
the browser handoff itself performs no external action.

## Invoice correction and delivery workflow — 2026-10-27

Local implementation after `45337e6` adds protected invoice/correction records,
issue attempts, delivery packages and receipt evidence. **23 focused regressions**
pass, including stale authorization after a sibling correction, corrupt related
evidence, corrected unissued customer/currency facts, historical manual dispatch
and outcome chronology. Independent code and EN/RU contract review found no blockers.

`python3 -B -m unittest discover -s tests -v`: **403 run, 392 passed, 11 platform
skips**. The earlier 400-test run had one 40-second PowerShell timeout in an existing
overview test; the isolated native task-overview module then passed **10/10**, and
the final full run passed without changing timeouts. Its initial timeout cause
remains unconfirmed. `npm run test:overview -- --browser=chromium` and its WebKit
variant passed EN/RU empty, blocked, corrupt and lifecycle cases at 390/1280 px,
with keyboard/escaping checks and no console/network errors. Package, local
Markdown links/anchors and `git diff --check` passed.

`tests/native/overview-smoke.ps1` and `tests/native/windows-smoke.ps1` passed under
local PowerShell **7.5.4** with `TMPDIR=/private/tmp`. The first overview invocation
correctly refused macOS's linked `/var` temporary path; no guard was weakened.
These checks and the cross-runtime unit tests are not Windows PowerShell 5.1
acceptance. Windows CI wiring was inspected; this local source was not run there.

Two fresh Codex CLI **0.164.0** sessions requested `gpt-6-astra` / high and exited
zero. The initial session recorded an already issued original and description
amendment, adopted the owner's historical send without fabricated authorization,
left it dispatched without a receipt and saved an English result/open task. The
fresh continuation inspected the supplied customer acknowledgement, recorded
delivery against the same observed send and saved Russian v02/completed receipt
task. Original-invoice delivery, agreement and payment remained unknown. Independent
artifact/provenance review found no blockers: the original record and **41** prior
non-mutable files were unchanged, audit history remained a prefix, frozen evidence
hashes/checkpoints matched and **19** report links resolved.

Both sessions preserved all **143** baseline skill files, but each added **14**
bytecode-cache files; these writable trials are not sealed-runner acceptance.
Between copies only the invoicing chronology guards and EN/RU guides changed;
the second baseline matches the final portable source. Prompts and continuation
criteria are retained in `evals/scenarios.json`; actual supplied fixtures, runs,
hashes and reports stay outside Git under `.invoicing-workflow-20261027`.
Requested models are recorded, not independently attested; evidence authenticity
was stipulated for the synthetic case.

Legal/provider checks are dated in the [portable source map](../skills/de-business-kit/references/assisted-services-sources.md#invoice-correction-and-delivery-check--2026-10-27).
No live provider, external issue/cancellation/send, tax/format certification,
native Windows desktop, GUI invoicing controls, hosted CI or published-package
acceptance is claimed. The runtime records evidence; actual provider operations
still use the chosen authorized host/manual route.

## EU goods VAT warnings — 2026-10-27

Local changes after `3066d5a` add shared pre-order and received-invoice checks,
including Kleinunternehmer and German destination-VAT/OSS branches. The earlier
manual live trial on `e7544e3` found no explicit warning. Three new catalogue
cases plus two changed-fact follow-ups now exercise these instructions.

Five fresh Codex CLI **0.164.0** sessions completed with unchanged session files
on snapshot `bc5feaf1fbe7` (skill-tree SHA-256 prefix). Independent review found
**4 cases passed / 1 failed; 35/36 criteria passed**: the general answer omitted
the Kleinunternehmer acquisition-tax-without-deduction consequence despite reading
it. A narrow instruction refinement requires that consequence even in a short
warning. The same question and unchanged criteria then passed **7/7** in a fresh
session on final snapshot `cbf168bc8087`, which matches the final skill tree.
The original failed assessment remains failed; no rubric was weakened.

The other four outcomes retain their original evidence: ordinary pre-order
advice, corrected Kleinunternehmer advice, paid Austrian-VAT invoice with German
supplier draft, and replacement German-VAT/OSS facts. Later changes were the short
warning requirement and EN/RU usage-help paragraphs. Two threshold comparisons
were executed visibly and independently checked. Six new sessions captured
**42 passed / 1 failed** criteria including the preserved failure; follow-ups
replay conversation context rather than resume a saved business workspace.

Full Python: **379 run, 368 passed, 11 platform skips**. Research-runner tests:
**18/18**, including fake-host execution of the expanded 43-session selection.
Package/local Markdown links and anchors, EN/RU parity and `git diff --check`
passed. Independent source/diff review found no blockers. Sealed manifests and
review bindings passed aggregation. Evidence remains outside Git under
`.gbk-eu-goods-20261027-245bd9c1` and its `-warning-retest` sibling; requested model
and effort are recorded there, not independently attested. No live purchase,
supplier contact, posting, refund, filing, installed-bundle update, native desktop
or hosted CI acceptance is claimed. Source applicability is in the
[portable reference](../skills/de-business-kit/references/international.md#eu-goods-sources-and-applicability).

## Customer payment continuation — 2026-10-27

Local implementation after `e7544e3` adds invoice-stated prepaid/rounding fields
and a saved customer-reply workflow. Six new regressions were observed failing
before their fixes; the final XML/proposal module passed **17 tests**. Full
`python3 -B -m unittest discover -s tests -v`: **379 run, 368 passed, 11 platform
skips**. Package, local links and `git diff --check` passed. `npm run test:gui` and
its `-- --browser=webkit` variant passed; WebKit retained 24 known screenshot-only
CSP diagnostics. Independent code review and malformed-input/approval probes found
no blockers. The journal settlement projection remains gross minus explicitly
allocated journal payments; the new fields do not change that projection.

Two fresh Codex CLI **0.164.0** sessions requested `gpt-6-astra` / high and exited
zero. The first saved German reply + English review at **EUR 68.99**, retaining
an already included EUR 50 advance once. A new session read the saved case,
added the explicitly allocated EUR 20 receipt and saved German/Russian v02 at
**EUR 48.99**. The unissued EUR 23.80 correction stayed separate; EUR 25.19 was
conditional only. All **10** initial immutable evidence/result files remained
byte-identical, 32 local Markdown links resolved, the same task stayed open with
new evidence, external accounting configuration stayed unchanged, and no paid
dates, journal entries or filings were inferred. Independent saved-content and
provenance reviews of both versions found no blockers.

Each session preserved authored skill files but generated 13 bytecode-cache extras;
these writable trials are not sealed-runner integrity acceptance. Skill copies,
prompts, events, file hashes and checks are outside Git under the synthetic
`.customer-payment-20261027` evidence directory. Runtime and operations instructions
were unchanged between trials; guides and the documented journal boundary were
finished between copies. Parent Chromium render checks covered four saved HTML
files at 390/1100 px: eight renders without document overflow or page errors;
representative German/Russian screenshots were inspected separately from the
host's text-only checks. No PDF/print, live provider, issue/send, technical
XML-profile validation, statutory correctness, hosted CI or new native Windows
acceptance is claimed. Primary format sources are dated in
[the portable source map](../skills/de-business-kit/references/correction-xml-sources.md#invoice-stated-prepayments-and-rounding).

## Receipt-to-period and filing continuation — 2026-10-27

Changed product routing, bookkeeping/monthly/filing references and EN/RU guides;
`workflows.py` validates preparation evidence and `casefiles/accounting.py` freezes
recognized report dependencies and checks them before advancement. No schema,
new ledger or transport was added. Four public-API regressions failed against the
frozen prior engine: stale receipt accepted, missing frozen dependencies, unresolved
preparation accepted and preparation used as payload. Independent review found a
capture race; a fifth red test reproduced it before the capture-once fix. All
**15 focused tests** now pass, including each preflight gate, nested preparation/
cash reports, other supported kinds, malformed evidence, depth limits and recording
an uncertain attempt's outcome after working originals disappear. Frozen-copy
damage still blocks historical actions. Independent final code review found no blocker.

Five writable Codex CLI **0.164.0** sessions on macOS requested GPT-6 Astra/high.
Evidence is outside Git in `.receipt-period-20261027`, with prompts, source hashes,
event logs, seeded old-filing evidence and `final-verification.json`. The synthetic
business cutoff was 10 November; actual retrieval/execution was 27 October.

- Original text-fixture baseline saved a useful worksheet after unsupported `.txt`
  intake. The first changed-skill run instead ingested labelled CSV transcripts;
  originals were preserved, but this was **partial**, not original-intake acceptance.
  Independent review identified the unmonitored original-to-derivative link. The
  portable fallback was tightened; a fresh bounded document-preparation retest saved
  the worksheet and next step with unchanged originals and no manufactured catalog
  records/proposals. Its prompt omitted tax research; it was not a full period retest.
- The supported-PDF trial preserved **3/3 incoming originals byte for byte**, saved
  **2 draft proposals** and a sourced review separating the ordinary service's
  October input VAT from November payment/EÜR timing. Laptop mixed-use/asset
  treatment and period coverage remained unresolved. No local entries or filings;
  the external accounting choice remained authoritative. A fixture reference to
  `payments.txt` was explicitly distinguished from the supplied `payments.pdf`.
- A fresh session resumed a **seeded legacy draft**, with the invoice-possession
  date corrected to November. It cancelled only the unsubmitted old version and
  created linked `october-v2` as draft, with **10 frozen sources**, no review/
  authorization/attempt events and **5 blockers**. Only the €19 service component
  moved to November; it was not treated as a zero October return. All **5 seeded
  immutable files** and the old frozen metadata were preserved; the continuation
  note and actual writer state were inspected independently.

`python3 -B -m unittest discover -s tests -v`: **373 run, 362 passed, 11 native
platform skips**, 147.517 s. Package, changed-Markdown file/anchor and diff checks
passed. `npm run test:gui` and `npm run test:gui -- --browser=webkit` passed their
existing lifecycle/security/stale-tab journeys, each with 54 localized route-width
and 6 task-home checks. WebKit recorded 24 known screenshot-only CSP diagnostics.
Authored trial bundle files stayed unchanged; each writable trial generated 13
bytecode cache files, retained as evidence. This is not strict sealed-runner integrity.

Limits: synthetic local preparation and state transitions; no real provider export,
official field mapping, complete period/return calculation, transmission, authority
decision, native Windows or Cowork acceptance. Unknown report kinds and authored
Markdown remain opaque evidence and require explicit underlying sources. Capture
can preserve partial files on failure; no multi-file transaction is claimed.

## Saved prepayment workflow — 2026-10-27

Product changes are in `de-business-tax/SKILL.md`, shared tax/source references
and EN/RU guides. Three completed Codex CLI **0.164.0** sessions on macOS requested
GPT-6 Astra/high: baseline, changed-skill ordinary request and fresh continuation
without the earlier transcript. Each used a copied complete bundle and a private
synthetic folder; final product bytes match the continuation bundle. Evidence is
outside Git in `.implementation-prepayment-20261027` under the evaluation-evidence
directory, with prompts, events, frozen bundle hashes and `final-verification.json`.

The baseline already saved useful files, but recorded an unresolved full-text
applicability check. The changed run recorded a failed individual provision fetch
and successful official full-act recovery, including applicability sections.
Root web metadata records URLs/opens, not complete returned text or every child
tool call; independent source review supplies corroboration, not a retrieval audit.

The first package proposed €200 from the €2,000 forecast and €1,800 credits. A
fresh Russian request with a corrected €2,300 forecast produced a linked €500
proposal while retaining the €600 current-notice obligation. German recipient
drafts, separate EN/RU reviews, input snapshots, executed arithmetic and continuation
were inspected. Both calculations reproduced saved output; all **13 initial files**
remained byte-identical and **21 local artifact links** resolved. No new task registry
or external action was created. Independent instruction and artifact reviews found
no blocking issue; the suggested ELSTER help link was added before continuation.

`python3 -B -m unittest discover -s tests -v`: **358 run, 347 passed, 11 native
platform skips**, 141.707 s. Package and changed-Markdown file/anchor checks and
`git diff --check` passed. The trial's direct Chrome preview failed (exit -6);
separate repository Playwright Chromium checks rendered both versions' recipient
and private HTML at 390/1100 px: **8 cases**, no horizontal overflow or page errors;
screenshots inspected. A trial text-check assertion was corrected for inline-link
whitespace; the saved document content was intact.

Limits: instruction-level host execution, one bounded standalone-folder journey;
no managed-register continuation trial, Windows/Cowork acceptance, PDF/print
acceptance, authenticated form fields, transmission or authority decision. The
supplied annual-tax forecast was not independently derived. Historical FAQ results
remain unchanged; this evidence does not establish general tax correctness.

## FAQ public-source trials — 2026-10-27

Skill source `085489d`, unchanged for every batch. The [60-question map](../evals/faq-coverage.json) links an external FAQ to task owners and cases; the opt-in [research runner](../tools/run_research_evals.py) keeps frozen inputs, host events, executed arithmetic and independent reviews bound to exact artifacts. Fresh Codex CLI 0.164.0 sessions on macOS used public web search and requested GPT-6 Astra/high; the event stream does not attest the effective model.

| Batch | Topics | Reviewed result |
| --- | --- | --- |
| Pilot | Nine questions, including founding-year VAT, an advised filing deadline and foreign SaaS | Strict review 6 pass / 2 fail / 1 uncertain; after calibrating two criteria to what the users asked, 7 pass / 2 uncertain (a reassessment, not a retest) |
| Research runner | Founding-year VAT with a corrected history, foreign SaaS | 3 sessions, 20/20 criteria; Decimal commands and reverse checks captured |
| 2 | Family cover, pension options, parental and child benefits, work permission, startup support | Strict review 5 pass / 2 fail; three retests with explicit comparison requests passed 20/20 |
| 3 | Small invoices, invoice fields, the 2026 e-invoice transition, home-office costs, quarterly VAT | 6/6 sessions, 40/40 criteria |
| 4 | Low-value assets and computers, mixed phone and car costs, EU consultancy | 6 pass / 1 uncertain; 45 criteria passed / 2 uncertain; one vehicle retest failed session integrity |
| 5 | US advice, French property services, EU digital sales threshold | 3 pass / 1 fail / 1 uncertain; the clarified consumer retest passed 13/13 |
| 6 | No-sales VAT returns, losses and return duties, prepayment adjustment | 4/4 sessions, 27/27 criteria |

These are bounded behaviour trials, not tax certification. The product skills and the ten-case runner were unchanged; per-case transcripts and criteria are in this page's Git history.
