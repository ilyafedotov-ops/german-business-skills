# Validation summary

[English](validation.md) · [Русский](validation.ru.md) · [Technical documentation](index.md)

Evidence index updated **2026-10-27**. Automated tests and public examples use synthetic data; authorized live checks keep account evidence private. [Current status](project-status.md) owns the capability matrix and remaining P1–P7 work; this page records what was checked. Old results do not validate newer source automatically.

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

## Evidence by scope

| Scope | Observed result | Limits and detailed record |
| --- | --- | --- |
| Receipt-to-period and filing continuation — local 2026-10-27 | 15 runtime regressions passed; full Python 362 passed / 11 skipped. PDF trial preserved 3 originals and 2 unapproved proposals; fresh legacy-filing continuation preserved 5 immutable files and created a blocked linked draft with 10 sources | [Acceptance and limits](#receipt-to-period-and-filing-continuation--2026-10-27); unsupported-text trials retained separately; no provider/official-form acceptance |
| Saved prepayment workflow and source recovery — local 2026-10-27, changed product skills after `085489d` | Ordinary request saved German/English files; fresh-session corrected forecast saved German/Russian v02; 13/13 initial files preserved. Official full-act fallback observed. Independent content/instruction review clear; full Python 347 passed / 11 skipped | [Acceptance and limits](#saved-prepayment-workflow--2026-10-27); standalone private folder, synthetic facts, no authenticated ELSTER operation |
| FAQ batch 6 — local 2026-10-27, unchanged skills `085489d` | Three cases plus one correction: 4/4 sessions and 27/27 criteria passed; no retests or rubric changes. Runner 18/18; full Python 347 passed / 11 skipped | No-sales VAT, annual loss/return request and prepayment adjustment; actual arithmetic and separate notice/request states checked. Whole 38-session selection tested with fake host |
| FAQ batch 5 — local 2026-10-27, unchanged skills `085489d` | Four cases plus one follow-up: original 3 passed / 1 failed / 1 uncertain; 32 criteria passed / 1 failed / 1 uncertain. Clarified consumer retest: 2 sessions and 13 criteria passed. Runner 18/18; full Python 347 passed / 11 skipped | Original omission and Washington-source uncertainty preserved; all seven sessions mechanically passed. Whole 34-session selection tested with fake host; details below |
| FAQ batch 4 — local 2026-10-27, unchanged skills `085489d` | Five cases plus two follow-ups: original 6 passed sessions / 1 uncertain; 45 criteria passed / 2 uncertain. One unchanged vehicle retest failed session integrity. Runner 18/18; full Python suite 347 passed / 11 skipped | Assets, mixed costs and ordinary EU consultancy; source-access uncertainty and unexpected retest `.DS_Store` preserved below. Whole 29-session selection tested with fake host |
| FAQ batch 3 — local 2026-10-27, unchanged skills `085489d` | Four new cases plus two follow-ups: 6/6 sessions and 40/40 criteria passed independent review; no rubric changes or retests. Runner 18/18; full Python suite 347 passed / 11 skipped | Bounded invoice/expense/deadline cases; partial web payload retention and official-source fallback limits recorded below. Whole 22-session selection tested with fake host |
| FAQ batch 2 — local 2026-10-27, unchanged skills `085489d` | Six new cases plus one follow-up; original strict review 5 pass / 2 fail. Three fresh retest sessions with explicit comparison requests passed, 20/20 criteria. Runner 17/17; full Python suite 346 passed / 11 skipped | Original missing-content failures retained; prompts clarified, no skill repair. All ten sessions captured successfully; only bounded synthetic/public-source acceptance, details below |
| Research evaluation runner — local 2026-10-27, unchanged skills `085489d` | Three fresh targeted sessions passed independent review, 20/20 criteria; actual Decimal commands and outputs captured. New runner tests 16/16; full-suite recheck 355 run, 344 passed, 11 skipped | Historical pilot remains 7 pass / 2 uncertain. Earlier full suite had one PowerShell timeout; isolated 9/9 passed. New full nine-session selection tested with fake host, not rerun live; details below |
| FAQ public-source pilot — local 2026-10-27, skill source `085489d` | All 60 question numbers mapped; 7 new cases plus 2 context-replay follow-ups. Nine fresh Codex CLI 0.164.0 sessions completed with public web search, requested GPT-6 Astra/high and read-only shell sandbox; unchanged skill copies and no unexpected session files | Criterion review and limits below; no all-pass certificate, product repair or provider/desktop acceptance |
| Published `0.10.0-preview.1`, source `9a4f33dc2dc5c02fdf26edd9daaf2d97e1f7ba56` — 2026-10-26 | [PR #16](https://github.com/ilyafedotov-ops/german-business-skills/pull/16): all 17 checks passed. [Exact-tag run 40412289498](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40412289498): 16 jobs passed, PR-only dependency review skipped; all three CodeQL analyses registered with zero findings/errors and zero open alerts. All eight downloaded assets passed checksums, immutable-release attestation and repository/workflow/tag/commit provenance using GitHub CLI 2.103.2. Both skill ZIPs, metadata and notes matched the exact-tag local rehearsal byte for byte | Automated Windows/macOS, PowerShell 5.1, browser and package evidence; no ordinary-user desktop, live-service or complete-tax acceptance. Local full suite: 340 run, 329 passed, 11 platform skips; npm 8/8. Marketplace advanced only after asset verification; earlier tags/assets unchanged |
| Optional browser/computer guidance — local 2026-10-26 | Official setup/limits checked; EN/RU and shared instructions aligned; independent review clear; three fresh read-only trials confirmed conditional activation, no research screen gate and no native bypass; package/link/diff passed | No live activation, account access or desktop acceptance. |
| Folder coverage and readable destinations — local 2026-10-26 | Actual EN/RU/DE workspace creation/resume; baseline hidden report → visible revised output; old case preserved with versioned result. Localized 5/5, workspace 41/41, packaging 16/16; independent review clear | Instruction-level routing; no schema/path migration, new organizer or native Windows acceptance. |
| AI notice and provider processing — local 2026-10-26 | EN/RU notices and dated primary-source policy distinctions; independent review clear; three fresh read-only dialogs evidenced the main boundaries; package/link/diff checks passed | Sensitive-data trial did not explicitly distinguish GDPR Articles 6/9; no all-criteria pass, account audit or legal sign-off. |
| Model recommendations — local 2026-10-26 | Primary sources checked; EN/RU guides and shared instructions recommend Opus 5.5 / High or GPT-6 Astra / High where available. Three fresh read-only guidance trials passed; package/link/diff checks passed | Not a benchmark or model-picker acceptance. |
| Visual onboarding guides — local 2026-10-26 | Three EN/RU diagram pairs and a real Claude repository-entry screenshot; packaging 16/16, release tests 7/7; Chromium/WebKit previews at 390/1280 px: 24 page cases and 12 SVG bounds checks passed | Local Markdown previews, not GitHub rendering or completed installation. |
| Assistant-led installation and 24 lifecycle examples — local 2026-10-26 | EN/RU README/install parity; fresh usage-help and no-controls installation-guidance trials; independent review clear. Full suite **340: 329 passed, 11 skipped**, package/diff checks and **941 local links/anchors** passed | Read-only synthetic CLI trials, not actual installation, desktop discovery or live integrations. |
| Assistant-first guides, shared prerequisites and sourced bounded calculations — local 2026-10-26 | Before/after ordinary-request trial changed calculator-only refusal to executed result with honest unverified-check status; ambiguity, saved-fact persistence and fresh-session reuse observed; historical arithmetic and discrepancy checks observed. Independent instruction review resolved contradictions. Package/diff checks passed; 935 local Markdown links/anchors in 135 files passed | Full suite 340: 328 passed, 11 skipped, 1 native PowerShell timeout; isolated module 9/9 passed. Separate calculation reviewer unavailable and current BMF rounding-source access incomplete; no desktop usability or complete-tax acceptance. |
| Claude GitHub marketplace and Cowork-first README/install guides, working tree after `869395b` | Claude Code 2.1.310 `plugin validate .` passed (warnings only: no icon, root `CLAUDE.md` not loaded, untracked ignored `.DS_Store`). With an isolated `CLAUDE_CONFIG_DIR`, `marketplace add` of the local checkout and `plugin install de-business-kit@german-business-kit` fetched `b7f85c0` from GitHub; `plugin details` listed 7 skills and the installed `skills/` tree was byte-identical to that commit; the user's own Claude configuration was unchanged. 2 new marketplace tests pass and fail on a wrong commit pin; packaging 16/16; package, release and `git diff --check` passed; 197 local links/anchors in 17 changed Markdown files resolved; EN/RU guide structure matches. Full suite rerun: 340 run, 329 passed, 11 platform skips (135 s). An earlier full run had 5 errors, all 40 s `pwsh` timeouts in `test_native_task_overview`; that module passed 9/9 alone and the timeouts did not recur | The `owner/repo` address works only after merge to the default branch. No install in the Cowork, claude.ai or desktop UI, no ordinary-user trial and no Codex re-trial. PowerShell timeouts under full-suite load remain unexplained, as before |
| Published `0.9.0-preview.1`, source `b7f85c0422429f94159a6cc6352f8b83ab4b5d63` | Exact-tag run: 16 jobs passed, PR-only dependency-review skipped; all eight downloaded assets verified against immutable release proof and exact source provenance | [Acceptance record](#090-preview1-acceptance--2026-10-26); automated platform evidence, not ordinary-user or live-service acceptance |
| Published `0.8.0-preview.1`, source `04bcd80a008d48fcd4cdc635988440e17291c5a1` | Tag run [40342363902](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40342363902): 16 jobs passed, PR-only dependency-review skipped; all eight downloaded assets verified against checksums, exact repository/workflow/tag/commit provenance and immutable release proof | Automated Windows/macOS, PowerShell 5.1, browser and package evidence; not tax certification, ordinary-user desktop acceptance or live service operations. |
| Lock wait and stale-lock recovery, linked-path messages and folder sync, branch `claude/vat-journal-lock-recovery` from `14a3360` | Local Python 3.14 (macOS): 298 tests, 293 passed/5 environment skips, including 7 lock, 1 linked-path and 1 GUI-adapter test; package and release checks passed. GUI journey removing a left-over lock and settings at 320/390/1440 px passed in Chromium and WebKit; overview passed in Chromium. A real PowerShell-written lock was assessed stale and removed by Python. `windows-smoke`, `overview-smoke` and `recovery-smoke` passed under PowerShell 7.5.4 with a non-linked temporary folder | Not Windows PowerShell 5.1 acceptance; the Windows process probe (`OpenProcess`) runs only in Windows CI, which was not run. Folder sync is not crash-tested; standalone PowerShell has no unlock action |
| Cash-entry line VAT and proposal links, branch `claude/vat-journal-lock-recovery` from `14a3360` | Local Python 3.14 (macOS): 289 tests, 284 passed/5 environment skips, including 12 new cash-VAT/GUI-adapter tests; package and release checks passed. GUI journeys with stated VAT at 390/1440 px and real overview passed in Chromium and WebKit. A mixed v2/linked/legacy register was read by the Python overview and native `windows.ps1` overview under PowerShell 7.5.4 | Not Windows PowerShell 5.1 acceptance; packaged GUI smoke and hosted CI not run; no fresh-session trial of the new `cash-line-stated-vat` scenario. Stated-VAT sums are not checked against any tax calculation |
| Beginner onboarding at `325a04e824600b428f4f544881ecd1808b4f3daf` | Local Python: 277 tests, 272 passed/5 native skips; detached packaging: 14 passed. Codex CLI 0.164.0 EN/RU and constrained Claude Code 2.1.310 discovery/first-answer trials on macOS; initial Claude scope regression fixed and retested | Conversations are not desktop download/sign-in/install acceptance. |
| Assisted-service source through `9f37d8106b64e961aadf181158b79704e1e2dea7` | Local Python: 277 tests, 272 passed/5 native skips; package checks/builds and synthetic browser-fixture smoke passed. Russian draft trial saved/reviewed known fields, final-send count 0. Fresh export retest generated once, lock count 0 | Agent-tool download retrieval remains unverified after timeout/policy block; fixture CSV success does not repair that gap. Claude unknown-field/formula regression fixed and retested; manual “done” without a receipt remained unconfirmed. |


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
- Broader service-specific access, exports/submissions and readback beyond the bounded Lexware browser run above. Live API adapter acceptance remains open. No real ELSTER authentication or transmission was tested by the synthetic portal.
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

This section preserves the preparation-stage evidence and then-pending gates. The later acceptance record below supersedes those pending states, without changing the earlier observations.

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

Follow-up on `700b254`: all three CodeQL analyses registered successfully for PR merge commit `16441d7dfe0ba369c3e9a3813b176d610b6dbcaa`, each with zero findings. The Windows diagnostic run then exposed a different failure: the task assertion's 3 s window expired while the `status` request was still pending (3,007 ms), with loaded scripts and no browser errors. A controlled 4 s response delay reproduced that failure locally. The test now waits for refresh completion before the unchanged 3 s render assertion. The same delayed Chromium journey passed after the fix, as did the full WebKit GUI journey. Independent review confirmed the synchronization. Logs: `/private/tmp/gbk-090-windows-browser-diagnostic.log`, `/private/tmp/gbk-090-slow-refresh-{red,green}.log`, `/private/tmp/gbk-090-gui-webkit-sync.log`. This resolves the demonstrated test timing assumption; it does not determine the original reload failure's cause. Exact-head Windows acceptance is still required.

## 0.9.0-preview.1 acceptance — 2026-10-26

[PR #15](https://github.com/ilyafedotov-ops/german-business-skills/pull/15) head `023c5df972264f7ea203aaf51b35904955d8a67f` passed all **17 checks**: [platform/browser run](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40370070393) and [security run](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40370070529). All three CodeQL analyses registered for its merge ref at `e9f51592818ce59c5789833b7250c3fe6c7a2bc6` with zero findings and zero open alerts. Windows Chromium passed the original reload journey with diagnostics enabled; the Windows Python 3.14 suite ran 277 tests with 9 skips. Successful reruns do not establish the original bootstrap failure's cause. The PR merged as `b7f85c0422429f94159a6cc6352f8b83ab4b5d63` with an identical file tree to the checked head.

The immutable [release](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.9.0-preview.1) was published on **2026-10-26 at 18:00:50 UTC**, from that exact merge commit. [Tag run 40372386103](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40372386103) passed **16 jobs**; only PR-specific dependency review was skipped. It covered Windows/macOS, native PowerShell 5.1 without Python setup, Chromium/WebKit, all three native GUI archives, reproducible skill-package builds and publication. The exact tag has three registered CodeQL analyses with zero findings, no analysis errors and zero open alerts.

All **eight downloaded assets** passed release-attestation and build-provenance verification using GitHub CLI 2.103.2, restricted to this repository, `.github/workflows/release.yml`, `refs/tags/v0.9.0-preview.1`, source commit `b7f85c0422429f94159a6cc6352f8b83ab4b5d63` and GitHub-hosted runners. All seven listed file checksums matched. The Codex/Claude ZIPs, `release.json` and `release-notes.md` also matched the exact-tag local rehearsal byte for byte; native archive reproducibility is not claimed. Local proof: `/private/tmp/gbk-090-published-verification-20261026/summary.json` and adjacent per-asset verification outputs.

The Git tag is annotated, not cryptographically signed; the release and build provenance are signed. Earlier immutable assets were not replaced. No hosted production application was deployed. Ordinary-user desktop acceptance, real service operations, complete assisted export retrieval and the other open gaps above remain unchanged.

## PR #13 integration and bounded refresh wait — 2026-10-26

After publication, [PR #13 run40373286210](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40373286210) at `7df1eee` failed a different Windows Chromium assertion on the same application tree. The saved-notice deadline covered filing creation (2,792 ms), draft persistence (344 ms) and a status request still pending after 26,879 ms. The application intentionally shows the notice only after the snapshot completes; scripts were loaded and no browser/server error was recorded. This does not show a failed filing write or explain the underlying Windows filesystem cost.

The test now registers the snapshot-request waiter before confirming the replacement filing, then waits for busy state to clear. Both waits retain the existing 30-second default; saved-notice and three-record assertions are unchanged. No runtime code or protected validation changed. A controlled 4-second creation plus 28-second refresh reproduced the old failure and passed the corrected full Chromium journey. A separate 31-second refresh probe still failed at the 30-second busy wait, proving the bound remains enforced. The full WebKit journey passed; independent review found no issues. Logs: `/private/tmp/gbk-090-pr13-windows.log`, `/private/tmp/gbk-090-filing-refresh-{red,green-final,bound}.log`, `/private/tmp/gbk-090-pr13-webkit-final.log`.

Package checks, **885 local links/anchors across 132 Markdown files**, release-version check and `git diff --check` passed. Application/runtime evidence above is reused only for unchanged code; the exact PR-head Windows and security results are tracked in [PR #13](https://github.com/ilyafedotov-ops/german-business-skills/pull/13). The published tag and assets remain unchanged.

## Review follow-up implementation — 2026-10-26

Local changes from `0450c97` add cross-period invoice payment allocation, readable discrepancies, source-report freshness checks, native lock diagnosis/recovery with exact evidence, consistent English creation defaults and an opt-in POSIX evaluation runner. The GUI reuses filing checks within one locked snapshot.

- Full suite: **337 run, 326 passed, 11 platform-specific skips** in 128.032 s; subsequent final evaluator refinement: **15/15 focused tests passed**. Independent review findings were fixed and rechecked.
- Chromium/WebKit GUI and EN/RU overview passed, including the settlement journey and EN/RU/DE mobile/desktop captures. WebKit had 24 existing screenshot-only CSP diagnostics, with no unexpected console/network failures. The macOS bundled executable passed the empty-PATH smoke; both skill bundles and 14 detached-package tests passed.
- Native lock suite: **6/6 on local PowerShell 7.5.4**; native lock/recovery/windows smoke passed locally. This is not Windows PowerShell 5.1 acceptance; current-head hosted CI and ordinary-user desktop trials remain open.
- Ten fresh Codex CLI 0.164.0 scenarios ran. Eight initially passed deterministic checks; two failed because of added bytecode caches and passed on later-source repeats with bytecode disabled. Separate observer review evidenced 33/35 original criteria; retention inventory and actual official submission status remained uncertain. This is not an all-ten final-source pass or a legal certificate.
- A separate available-host Chrome trial saved/reviewed a synthetic draft and verified the actual September payment-date CSV after a download-event timeout, without regenerating it. Server state: one export, zero locks, zero sends. Live provider acceptance remains open.
- Package/version/link/diff checks passed. Signing preparation is documented in [release guidance](releases.md#desktop-signing-prepared-next-step); no signing credentials, notarization upload, publication, commit or push was performed.

## FAQ pilot — 2026-10-27

Source `085489d3773c1ac04d877951b6e06d21cedb5fb3`; unchanged skill-tree SHA256
`b685dc0b903c2d3bd5951e1def90f981d40d6fc72ed4cbeb35c4c455f9a27c11`.
The [60-question map](../evals/faq-coverage.json) and
[evaluation protocol](../evals/README.md#faq-coverage-and-public-source-pilot) separate
secondary question discovery from dated primary-source expectations. There are
93 catalogue cases; the existing opt-in runner still selects its original ten.

Nine ephemeral Codex CLI 0.164.0 sessions on macOS used existing host-managed
authentication, ignored user configuration, native public web search and a
read-only shell sandbox. GPT-6 Astra/high was requested; the event stream does not
independently attest effective model identity. All nine completed within the
240-second per-session bound (38–134 seconds, rounded), retained unchanged skill
copies and created no unexpected files in their session directories. Observed
commands read copied skills; no out-of-session read, account operation or rubric
access was observed. This is not OS access isolation or a complete network audit.

Independent criterion review found two rubric/fixture mismatches: the founding
case already supplied qualifying turnover, and the GKV user requested a factual
clarification draft rather than a separate checklist. Original strict assessments
and exact criteria were retained; two criteria were calibrated to those requests
and the same answers reassessed. This is **not a skill fix or a fresh retest**. Original strict grading was 6 pass,
2 fail, 1 uncertain; calibrated grading is **7 pass, 0 fail, 2 uncertain**.

| Trial | Reviewed result after calibration | Evidence and limitation |
| --- | --- | --- |
| Founding-year VAT | Uncertain overall; legal/task criteria passed | Correct threshold/crossing/earlier-transaction explanation; claimed executed/reverse-checked arithmetic is not established by aggregate CLI tool events |
| Advised 2025 deadline | Pass | Correct deadline, applicable year and useful preparation step |
| Incoming foreign SaaS | Uncertain overall; legal/task criteria passed | Correct bounded recipient-liability route; calculation-execution claim has the same evidence gap |
| Classification | Pass | Actual work/qualification evidence, honest description and unresolved classification retained |
| Voluntary GKV income | Pass | Rental income, provisional/final distinction and factual German clarification draft; no invented premium |
| One-client pension/status | Pass | Separate assessments and useful fact checklist; direct DRV interpretation-page failure and indexed-fragment reliance explicitly disclosed |
| KSK and trade registration | Pass | No automatic exclusion; mixed-activity evidence and individual assessment retained |
| Two changed-fact follow-ups | Both pass | Corrected business history and tax year change the answer; explicit context replay, not host resume or workspace persistence |

The calculation events do not establish execution or fabrication. These two
cases remain uncertain rather than passed; a follow-up evaluation needs an
observable calculation tool/expression/output trail and separately evidenced
checking. No product instructions were changed to fit the answers. Broader
coverage priorities remain in [project status](project-status.md).

Local evidence is outside Git at `/private/tmp/gbk-faq-pilot-20261027`: raw JSONL,
requests, frozen skills, source/request hashes, host invocations and durations,
observed checks, original criteria, calibration record and independent review.
Timestamps in the additional observation record come from filesystem metadata,
not host events. The temporary evidence may not survive host cleanup; it is not a
published or portable certification. No real accounts, applications, submissions,
ordinary-user desktop trials or cross-host comparison were performed.

Checks: `python3 -B -m unittest discover -s tests -p test_eval_runner.py -v`
**15/15 passed**; package/JSON/local-link check and `git diff --check` passed.
Mapping checks cover 60 unique numbers, resolvable owners/scenario/source IDs,
93 unique scenario IDs and two follow-ups. EN/RU additions and changed Markdown
links/anchors were inspected. Full runtime/native/browser suites were not rerun:
only evaluation data/documentation changed, with no skill, application or runner
implementation change. No commit, push or publication was performed.

## Repeatable research evaluation and calculation evidence — 2026-10-27

The new opt-in [research runner](../tools/run_research_evals.py) preserves frozen
inputs, raw host events, command/output observations, review sheets and a validated
assessment. The existing `tools/run_evals.py` and product skills are unchanged.
This adds evaluation infrastructure, not business functionality.

Three fresh Codex CLI 0.164.0 sessions on macOS, requesting GPT-6 Astra/high,
covered founding-year VAT, its corrected-history follow-up and incoming foreign
SaaS. They completed in 109, 64 and 110 seconds respectively (rounded), with
unchanged session inputs. The new wrapper requests observable exact/decimal
execution: both calculation cases captured Python 3.14.6 Decimal expressions,
inputs, outputs and reverse checks. Answers honestly identified independent
checking as unavailable at answer time. A separate reviewer derived expectations
from official sources using rational arithmetic and integer cents before seeing
the transcripts, then assessed all three cases: **20/20 criteria passed**.
`--summarize` validated evidence/review bindings and produced **3/3 passed**.
This later observer review is separate from the tested assistant's own work.

The skill source/hash is the same as the pilot above. The new capture protocol
closes the observability gap for these fresh runs; it does not establish whether
the original hidden calculations ran. The original **7 pass / 2 uncertain**
assessment remains unchanged. All seven bases plus two follow-ups are selectable;
that nine-session route has fake-host integration coverage, not a new full live run.

Validation: **16/16** new runner tests passed, including incomplete/duplicate
streams, empty answers, timeout, mutation, unsafe paths, replay isolation, frozen
criteria, review-byte binding and preservation of unrelated files. Independent
read-only review found no remaining blocker. Full-suite recheck: **355 tests,
344 passed, 11 skipped** in 147.163 s. The earlier full run had 343 passes,
11 skips and one unchanged PowerShell overview timeout; the isolated module then
passed **9/9**. Its intermittent cause remains unresolved. The final summary-only
path guard was added after the full-suite recheck and passed the 16-test focused
suite and independent review; unchanged live capture evidence was reused.
Package, changed Markdown links/anchors and diff checks passed; EN/RU additions
were inspected. No fresh native Windows, browser, desktop or hosted CI acceptance
is claimed.

Evidence is retained outside Git under
`/Users/ilya/Developer/evaluation-evidence/german-business-kit/`:
`research-20261027-acceptance/` contains the sealed run and attributed reviews;
`research-independent-check-20261027.{json,md}` contains the blinded derivation;
`research-runner-checks-20261027/` holds validation logs. The original temporary
pilot was copied to `faq-pilot-20261027-original/`: **1,459 files verified with
matching tree hashes**, with a separate preservation receipt. Original files were
retained. Hashes establish consistency, not authenticity or reviewer identity;
requested model identity, read-only shell sandbox and observed tool metadata do
not establish OS read isolation or a complete network audit. No commit, push,
publication or real-account operation was performed.

## FAQ batch 2 — 2026-10-27

Added six synthetic cases for FAQ 40, 44–46, 56 and 58: pension contribution
options, family health cover, parental/child benefits, work permission and startup
support. A changed-fact permission follow-up brings this batch to seven sessions.
The catalogue contains **99 base cases**; the research runner selects **13 bases
and 3 follow-ups**. Dated primary-source expectations are in the existing
[coverage map](../evals/faq-coverage.json); historical baseline labels are unchanged.
Source `085489d` and the skill-tree hash above remain unchanged.

Ten fresh Codex CLI 0.164.0 sessions on macOS requested GPT-6 Astra/high: the
original seven plus a child-benefit retest and a new permission base/replay pair.
All completed within the 240-second bound, with unchanged session inputs and
valid mechanical capture. The independent source expectations preceded the trial
outputs. Captured income arithmetic, year/date checks and threshold comparisons
were separately checked; the tested assistant's own reverse-checks were not
relabelled independent verification.

The original strict assessment is **5 cases passed, 2 failed; 46 criteria passed,
2 failed**. The child-benefit answer omitted the rubric's Elterngeld comparison;
the permission follow-up omitted explicit professional-authorisation discussion.
Review found missing required content, not a materially wrong legal conclusion.
The broad original prompts did not explicitly request those named comparisons.
Both prompts were clarified and fresh trials run with **unchanged criteria and
product skills**. Original failures and exact old/new prompts are retained; these
retests do not establish a repair of the original broad-prompt behavior.

All three retest sessions passed independent review: **20/20 criteria**. Across
all ten observed sessions the retained record is **8 pass, 2 fail; 66 criteria
passed, 2 failed**. All three `--summarize` operations validated their sealed
evidence and review bindings: original assessment `failed`, both retest assessments
`passed`. One retest cited archived 2021 employment guidance; its material claims
were corroborated against the current BMAS brochure and that source limit was
recorded. No criterion was waived or silently regraded.

Checks: runner **17/17 passed**, including the new permission replay and the full
16-session fake-host selection; independent runner review passed. Full Python
suite: **357 run, 346 passed, 11 skipped**, 153.443 s, with no PowerShell timeout
in this run; prior intermittent timeouts remain unexplained. Package, map/ID,
Markdown links/anchors and diff checks passed; EN/RU changes were inspected.
Prompt-only clarifications after that full run reused unchanged runtime checks
and were exercised by fresh host sessions. No new whole-catalogue, desktop,
native Windows, hosted CI, account or submission acceptance is claimed.

Evidence under `/Users/ilya/Developer/evaluation-evidence/german-business-kit/`:
`research-20261027-batch2/`, `research-20261027-batch2-child-explicit/` and
`research-20261027-batch2-permission-explicit/` retain snapshots, raw events and
attributed reviews; `research-batch2-checks-20261027/` retains test logs and the
pre-trial source note. Separate source, arithmetic and fixture-refinement records
retain access limits and exact prompt changes. Some source reads used targeted
indexed official text after direct-page failures; this is not a complete archived
page corpus or network audit. The full sixteen-session selection was not rerun
live. No commit, push or publication was performed.

## FAQ batch 3 — 2026-10-27

Four new cases cover small-invoice particulars, the 2026 e-invoice transition,
home-working expenses and Q3 VAT deadlines. Two follow-ups change the invoice
gross total and the existing-extension fact. The catalogue now has **103 base
cases**; the opt-in research runner selects **17 bases plus 5 follow-ups**.
Expectations in [the source map](../evals/faq-coverage.json) were independently
checked before launch, including prompt/rubric alignment and numeric/date results.

**Six fresh sessions passed all 40 criteria**, without post-trial rubric changes
or retests. The invoice answer changes at EUR 250.01; PDF transition and structured
receipt duties stay separate; homeworking arithmetic yields EUR 1080 with no tax
saving claim; the deadline changes from 12 October to 10 November and overdue
status is retracted. Raw command/output evidence supports the calculations.
Codex CLI 0.164.0 on macOS requested GPT-6 Astra/high; sessions took 70–187 seconds
(rounded), all within 240 seconds, with unchanged session inputs. Skills remain
at source `085489d` and the previously recorded tree hash. The independent review
is subsequent observer work, not a claim that each tested assistant had a reviewer.
`--summarize` verified the manifest/review bindings and produced `passed` for all six.

Runner tests **18/18 passed**, including selection deduplication and case-specific
replay isolation; independent code review also checked different prior answers.
Full Python suite: **358 run, 347 passed, 11 skipped**, 181.435 s. Package, source-map
references, local Markdown links/anchors and diff checks passed; EN/RU additions
were inspected. Final pretrial wording clarifications were exercised live while
unchanged runtime checks were reused. The full 22-session selection passed with
a fake host, not a new whole-selection live run. Product skills and the original
ten-case runner are unchanged; no native desktop, account or filing acceptance.

Evidence remains outside Git in
`/Users/ilya/Developer/evaluation-evidence/german-business-kit/research-20261027-batch3/`;
`research-batch3-checks-20261027/` retains test logs and frozen pretrial source
expectations. Web metadata is not a complete page archive. Some trial page reads
failed and used alternative official sources or official indexed excerpts;
independent review verified decisive text, and homeworking disclosed those limits.
Earlier results are preserved. No commit, push or publication was performed.

## FAQ batch 4 — 2026-10-27

Five new cases cover GWG and computer depreciation, mixed phone and vehicle costs,
and ordinary consultancy to an EU business. Two follow-ups change the asset price
and customer status. The catalogue has **108 base cases**; the research runner
selects **22 bases plus 7 follow-ups**. Primary-source expectations and numeric
results were independently checked before launch; frozen criteria were not revised
after seeing answers. Product skills remain at `085489d` with the previously
recorded tree hash.

Codex CLI 0.164.0 on macOS requested GPT-6 Astra/high. All seven original sessions
completed mechanically in 115–234 seconds (rounded), within the unchanged
240-second bound. The computer case came close to that bound. Raw commands and
outputs retain the calculations; observer review is separate from any verification
claimed by the tested assistant.

**Original independent review: 6 passed sessions and 1 uncertain; 45 criteria
passed and 2 uncertain, none failed.** Asset-price and customer-status corrections
revise the answers appropriately. Phone shares reconcile to the supplied gross
total, with paid input VAT kept separate; the car arithmetic is EUR 6000 private
and EUR 4000 business. The original car answer explicitly left 2026 applicability
unconfirmed after current-source retrieval failures, so its two source criteria
remain uncertain. Later observer access cannot upgrade the tested host's evidence.
`--summarize` verified original manifest/review bindings and returned `uncertain`.

One unchanged-prompt vehicle retest completed in 142 seconds, but **failed the
mechanical integrity gate**: `skills/.DS_Store` appeared in its session copy. All
original skill-file bytes remained unchanged; the file's creator is unestablished.
The file and failed run are preserved, with no bypass or further retry. This is
not an accepted retest. Content-only review passed all seven criteria: current §6
and an applicable BFH judgment were successfully retrieved, and Decimal execution
was captured. `--summarize` still returned `failed`; improved source access does
not repair session integrity or change the original uncertainty.

Runner tests **18/18 passed** after a red/green selection-count check. Independent
code review confirmed the five-case extension and exercised all 29 sessions with
a fake host, including isolated context replay; the whole selection was not rerun
live. Full Python suite: **358 run, 347 passed, 11 skipped**, 149.567 s. Package,
source-map references, local Markdown links/anchors and diff checks passed; EN/RU
additions were inspected. No product skills, original ten-case runner, accounting
writers or platform contracts changed. No native desktop, account or submission
acceptance is claimed.

Evidence remains outside Git under
`/Users/ilya/Developer/evaluation-evidence/german-business-kit/`: original
`research-20261027-batch4/`, separate `research-20261027-batch4-vehicle-retest/`
and `research-batch4-checks-20261027/`. Frozen manifests preserve the exact trial
inputs; subsequent source-registry spacing cleanup changes no expectations.
Official-source access failures and indexed-text fallbacks remain visible; web
metadata is not a full page archive. No commit, push or publication was performed.

## FAQ batch 5 — 2026-10-27

Four cases cover US business/consumer technical advice, specific-site French
architectural plans and automated software crossing the EU place-of-supply
threshold. One follow-up moves the consumer to metropolitan France. The catalogue
now has **112 base cases**; the research runner selects **26 bases and 8 follow-ups**.
The previous 108 cases are unchanged. Independent primary-source and Decimal
expectations preceded launch; criteria were frozen and withheld from tested hosts.

**Original review: 3 passed sessions, 1 failed and 1 uncertain; 32 criteria passed,
1 failed and 1 uncertain.** All five sessions completed mechanically, with
unchanged session files, in 71–223 seconds (rounded) within the 240-second bound.
Codex CLI 0.164.0 on macOS requested GPT-6 Astra/high; model identity is not
independently attested. Skills remain at `085489d` with the previously recorded
tree hash. `--summarize` verified the sealed manifest and review bindings and
returned `failed`; the original outcomes are preserved.

- US business: core German VAT/ZM conclusions and boundaries passed. The extra
  Washington IT-tax/nexus example remains uncertain: official search metadata
  lacks a supporting extract or successful page open, and reviewer access failed.
- US consumer: correct tax treatment, sources and captured arithmetic; failed
  only the criterion requesting evidence-retention guidance, which the original
  prompt did not explicitly ask for. This is a prompt/rubric alignment issue,
  not an established tax-rule defect.
- France correction, property and digital cases: all criteria passed. Captured
  Decimal results include EUR 190/1190 for the correction and EUR 10300 aggregate
  turnover, EUR 100 VAT and EUR 600 gross for the entire crossing sale. French
  liability branches remain conditional on the missing customer status.

The consumer prompt now explicitly asks what service-description and residence
evidence to retain. Facts, criteria, follow-up, skill instructions and runner
controls are unchanged. The original failed answer is not relabelled.

**Two fresh clarified-request sessions passed all 13 criteria**, including useful
evidence-retention guidance and the unchanged France correction. They completed
mechanically in 189 and 95 seconds (rounded), with unchanged session files;
`--summarize` verified their separate manifest/review bindings and returned
`passed`. This demonstrates the clarified request, not a retroactive pass or
proof of a deterministic cause for model variability. The original business
source uncertainty remains unresolved.

Runner tests **18/18 passed** after the expected 22-versus-26 red check; independent
code review found no issues and verified distinct-answer replay isolation with a
fake host. Full Python suite: **358 run, 347 passed, 11 skipped**, 137.067 s.
Package, 150 local Markdown links/anchors, source-map references and diff checks
passed; EN/RU additions were inspected. Full-suite evidence precedes the final
prompt-only clarification; unchanged runtime checks are reused. The whole
34-session selection used a fake host, not a new whole-selection live run.

Evidence outside Git under `/Users/ilya/Developer/evaluation-evidence/german-business-kit/`:
`.research-20261027-batch5/`, `.research-20261027-batch5-consumer-explicit/` and
`research-batch5-checks-20261027/`. New hidden run directories reduce incidental
desktop interaction without weakening integrity checks; no general fix for the
previous unexplained metadata-file creation is claimed. Full BMF PDF and official
statutory/ELSTER/Commission fallbacks supported research where direct pages failed;
web event metadata remains a partial capture, not a full page archive. Product
skills are unchanged. No native desktop, account, complete foreign compliance or
submission acceptance is claimed. No commit, push or publication was performed.

## FAQ batch 6 — 2026-10-27

Three new cases cover a no-sales VAT period with input tax, a requested annual
return showing a business loss, and an income-tax prepayment adjustment. One
follow-up changes the VAT invoice to wholly private use. The catalogue has
**115 base cases**; the opt-in research selection has **29 bases and 9 follow-ups**.
The previous 112 cases are unchanged. Exact prompt/rubric alignment, primary
sources and independent Decimal expectations were checked before launch.

**Four sessions passed all 27 criteria**, without retests or post-launch rubric
changes. The VAT excess changes from EUR 19 to zero while the filing duty remains;
EUR -1200 business loss does not establish zero personal tax; the draft requests
EUR 200 while preserving EUR 600 due under the unchanged prepayment notice.
All claimed calculations, including additional checks and comparisons, appear
in executed Decimal output. No record, account, payment or submission action
was performed. Observer review remains separate from the tested hosts' own checks.

Codex CLI 0.164.0 on macOS requested GPT-6 Astra/high. Sessions completed in
100–129 seconds (rounded), within 240 seconds, with unchanged session files.
Skills remain at `085489d` and the previously recorded tree hash. `--summarize`
verified the sealed manifest/review bindings and returned `passed`. Official
complete-act/ELSTER/DRV fallbacks recovered individual-page failures; material
extra source claims were independently corroborated. Web metadata remains a
partial capture, not a complete page archive or proof of every host read.

Runner tests **18/18 passed** after the expected 26-versus-29 red check; independent
code review verified actual-answer replay isolation and unchanged integrity checks.
Full Python suite: **358 run, 347 passed, 11 skipped**, 149.587 s. Package,
150 local Markdown links/anchors, source-map references and diff checks passed;
EN/RU additions were inspected. The whole 38-session selection used a fake host,
not a new whole-selection live run. No product skill or original-runner change.

Evidence outside Git under `/Users/ilya/Developer/evaluation-evidence/german-business-kit/`:
`.research-20261027-batch6/` and `research-batch6-checks-20261027/`. Earlier failures
and uncertainties remain unchanged. This does not establish complete tax-period,
native desktop, account or filing acceptance. No commit, push or publication.
