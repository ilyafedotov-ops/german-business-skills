# Opt-in fresh-session skill trials

[English](README.md) · [Русский](README.ru.md)

`scenarios.json` owns the behavioral prompts and review criteria. The standard-library runner executes ten bounded critical cases using an explicitly installed **Codex CLI**. Other hosts and the browser-based practice portal need separate trials. It is a development tool, not part of the installed skill or a nondeterministic CI gate. Running a host may use billable model inference; listing cases and the unit tests make no model calls.

```sh
python3 -B tools/run_evals.py --list
python3 -B tools/run_evals.py --case archive-integrity --output /absolute/new/eval-evidence
python3 -B tools/run_evals.py --all --output /absolute/new/ten-case-evidence --timeout 150
```

Use `--codex /absolute/path/to/codex` for a selected executable and `--model HOST_MODEL` when choosing a supported model. The runner pins no model. With `--model` omitted the clean host default applies, which can differ from the user's configured model. The adapter targets the flags checked in Codex CLI 0.164.0; unsupported versions fail rather than use a privilege bypass. It uses existing Codex authentication with `--ignore-user-config` so normal account connectors, profiles and configured hooks are not requested. It does not copy credentials, load real business records, enable web search, install a plugin, change provider configuration or add external service adapters. Use it only with the intended Codex/OpenAI authentication route; custom-provider configurations need a separately reviewed adapter rather than silently copying host settings.

Each case starts a new ephemeral CLI session with its own working directory, copied complete skill set, synthetic facts and canonical workspace writers. A source snapshot is frozen once for the run; it includes only `skills/`, not the checkout, tests, scenarios or criteria. Output must be a new absolute directory outside the checkout; existing output and symlink ancestry are refused. Sessions have a wall-clock timeout (300 seconds by default, at most 3600). A timed-out session preserves its partial transcript and failed result. The host runner currently supports POSIX only and stops its process group after success, failure or timeout before inspecting evidence. File readers and tree hashes traverse pinned directory descriptors and refuse symlinks/special files; incidental Python bytecode writes are disabled in the child environment. Windows execution is explicitly refused until process-tree cleanup has separate implementation and acceptance; product native Windows support is unchanged.

The ten cases cover setup-free entry, external accounting authority, invoice prompt injection, original preservation, retention hold, temporary versus persistent language/mode changes, missing submission proof, uncertain submission and XML review boundaries. The fixtures deliberately have no live connection or filing receipt. Their external accounting choice and profile facts are created through canonical writers; fixture PDF/XML bytes are synthetic placeholders, not technical invoice-validation fixtures. For these cases, all original inputs, existing profile facts and accounting configuration/register must stay unchanged; the persistent preference case must also produce the requested marker values and actual configuration history. A legitimate action outside this narrow fixture can require another evaluation rather than weakening the existing validator.

The result separates two kinds of evidence:

- **Deterministic checks** inspect actual workspace hashes, preferences, canonical register, history, source snapshot, completed host event stream and observed command text. The tests prove these checks detect original corruption, omitted preference changes, observed network commands and timeouts even when the agent claims success. The command-text detector is bounded; it is not a complete network/tool monitor.
- **Transcript rubric** lives outside the session copy under `rubric/`. Every criterion starts as `pending_review`. A reviewer must inspect the transcript, actual deliverables and state evidence, then record pass/fail/uncertain with references. Host self-reports and passing state checks do not pass the rubric. The runner does not turn manually edited rubric files into an aggregate certification.

Exit `0` means the selected deterministic checks passed, with overall status **pending_review**. Exit `1` means at least one completed/attempted case failed those checks. Exit `2` means configuration, setup or host-launch failure; retain the output and any `incomplete` report instead of treating missing cases as passes.

The evidence directory records package/runner/host/Python/platform versions, source/scenario/runner hashes, requested model, exact invocation, timestamps, per-case duration, transcripts, stderr, before/after state hashes, copied skills, deliverables and separate rubric sheets. `requested_model: null` does not identify the effective model. No claim about model identity should exceed the host evidence. Keep real user data out of these files and do not commit local host transcripts by default.

Separate directories and a `workspace-write` sandbox are **not a confidentiality boundary for reads**. Criteria are omitted from the tested prompt and skill copy, and the prompt restricts the task to that session, but an unrestricted host can potentially read sibling evidence or the source checkout. Host/global instructions and model-provider retention can also affect a trial; ephemeral CLI sessions do not establish zero provider retention. For adversarial hidden-criteria evaluations use a separately configured OS/container environment with only the skill snapshot and fixture mounted, and keep criteria/evidence under the observer's control. This runner does not certify that stronger isolation, legal/tax correctness, live integration, browser behavior or native Windows compatibility.

Runner regression checks:

```sh
python3 -B -m unittest discover -s tests -p test_eval_runner.py -v
python3 -B tools/check_package.py
git diff --check
```

## Prerequisites and calculation trials

`scenarios.json` also contains `tax-bounded-local-calculation`,
`general-prerequisites-ambiguous-tax`, `general-prerequisites-resume-invoice`,
`calculation-historical-period-and-rounding` and
`calculation-discrepancy-and-no-source`. These are fresh-session manual host trials,
not selections in the ten-case runner above. Public-source cases need actual web
access; the no-source case deliberately withholds it. Give the tested agent the
prompt and synthetic inputs, never its criteria or expected numerical answers.
Inspect actual retrieved sources, executed arithmetic and saved records before
rating a result. A reported independent-check failure tests truthful fallback,
not successful independent verification. See [validation](../docs/validation.md)
for recorded host versions, outcomes and limitations.

`usage-guidance-after-install` and `assistant-install-guidance-no-controls` also
use manual fresh sessions: check a short relevant introduction and a truthful
user-held installation step when plugin controls are unavailable. These read-only
trials do not install a plugin or prove discovery in a desktop app.

## FAQ coverage and public-source pilot

[FAQ coverage](faq-coverage.json) indexes all 60 numbered questions in the
[Finber FAQ](https://finber.de/faq_freiberufler_germany/), reviewed on
**2026-10-27**, against baseline source `085489d`. It stores short topic labels,
skill owners and scenario IDs, not a copy of the article or an endorsed answer key.
The baseline has 2 questions with central-concern coverage, 29 partial, 24 without
a dedicated case and 5 whose complete specialized outcome is outside current
scope. Coverage is not a passing trial or a promise to answer every subquestion.
Outside-scope cases still need useful factual preparation and appropriate routing.

Seven independent synthetic `faq-*` prompts in `scenarios.json` form the first
pilot: founding-year VAT, advised filing deadlines, incoming foreign SaaS,
classification evidence, voluntary GKV income, one-client pension/status questions
and KSK. Two `follow_up` objects change material facts after the initial answer.
The second batch adds six cases: family health cover, pension contribution options,
Elterngeld, Kindergeld, work permission and startup support. A third follow-up
corrects the residence document wording. The third batch adds small-invoice
requirements, the 2026 e-invoice transition, home-working expenses and quarterly
VAT deadlines, with invoice-total and deadline-extension follow-ups. The catalogue
now includes a fourth batch for GWG/computer assets, mixed phone/car costs and
ordinary EU consultancy, with asset-price and customer-status corrections. A fifth batch covers US business/consumer advice, French property services and
automated digital sales crossing the EU threshold, with a consumer-location
correction. The sixth batch covers no-sales VAT returns, annual loss/return duties
and income-tax prepayment adjustment, with a private-expense correction. There
are 115 base cases; the research runner selects 29 of them and nine follow-ups
(38 sessions).
The coverage file holds dated primary-source expectations for these bounded cases;
remaining questions need their own source checks before an answer rubric is used.
The secondary site's answer must not override a contrary applicable official source.

The separate standard-library [research runner](../tools/run_research_evals.py)
executes these cases on supported POSIX developer hosts. It leaves the original
ten-case runner unchanged and does not add product connectors or permissions.
The first manual pilot remains historical evidence in [validation](../docs/validation.md).

```sh
python3 -B tools/run_research_evals.py --list
python3 -B tools/run_research_evals.py --all --model HOST_MODEL --output /absolute/new/persistent-evidence
python3 -B tools/run_research_evals.py --case faq-founding-year-2026 --case faq-foreign-saas-2026 --model HOST_MODEL --output /absolute/new/calculation-evidence
python3 -B tools/run_research_evals.py --summarize /absolute/existing/persistent-evidence
```

`--all` explicitly opts into twenty-nine base sessions and nine follow-ups, potentially
billable. A selected case includes its follow-up when defined. `--model` is
required; `--effort` defaults to `high`, `--timeout` to 240 seconds per session
(maximum 3600), and `--codex` can select an installed executable. No installation
or provider reconfiguration occurs. Codex CLI 0.164.0 is the locally checked host.
Use the intended existing Codex/OpenAI authentication route, not a custom-provider
configuration silently replaced by ignored user settings. Model identity is
recorded as requested, not independently attested. Case dates remain the dates
in their prompts; a new run date does not update historical legal assumptions.

Use a **new absolute persistent directory outside the checkout**, not a temporary
folder. Existing output, symlink ancestry and unsafe skill inputs are refused.
The observer freezes skills, scenarios, coverage, runner/helper bytes, version,
full review criteria and hashes. Each session gets only its skill copy and request;
expected answers and rubrics stay outside it. The host uses existing authentication,
`--ignore-user-config`, ephemeral sessions, a read-only shell sandbox and native
public web search. No account connectors or external submissions are requested.
Timeouts/failures retain partial evidence. Cleanup stops the host process group;
it does not prove containment of deliberately detached processes or OS read isolation.

The wrapper asks for exact/decimal local execution when arithmetic is performed,
with inputs, expressions and outputs printed. This is a changed capture protocol,
not proof that earlier hidden calculations ran or a repair of skill instructions.
Raw JSONL and `observations/` retain completed command text/output/exit status,
source-action/result metadata, final answer and line references. Web metadata is
not a full page/calculator payload. No command-pattern heuristic or model claim
certifies execution, numerical correctness or independent checking. Incomplete
items, invalid/duplicate events, empty final answers or session changes fail
mechanical capture. Follow-ups require a valid unchanged base and replay its
recorded user request and final answer: **context replay, not persistent resume**.

Run exit `0` means mechanical capture passed and quality is `pending_review`;
`1` means capture/host failure; `2` means setup, launch or interruption error.
Inspect `report.json`, including `incomplete` and blocked/not-run cases. A failed
or incomplete run cannot become a passing assessment through reviewer edits.

An independent reviewer fills each observer-only `reviews/<case>.json`: reviewer
identity, `assessment` (`pass`, `fail`, `uncertain`, or `pending_review`), a concrete
`note` and `evidence` such as `[ {"line": 12} ]` referring to that case's raw
transcript. Inspect actual sources, applicable period, useful outcome and every
execution/action claim. A self-report alone is insufficient. Preserve criterion
text, bindings and original evidence. Checks that the tested host could not perform
must be labelled honestly; an observer's later calculation is a separate check.

`--summarize` makes no model calls. It verifies the captured manifest and exact
review bindings/criteria, validates evidence references, and writes `assessment.json`
with `passed`, `failed`, `uncertain`, `pending_review` or `incomplete`. Exit `0`
means the summary is valid, **not that its status is passed**. Invalid/tampered
input returns `2` and removes the stale generated assessment in a recognized run;
an unrelated directory's files are preserved. It hashes the same
review bytes it assessed; later edits require summarization again. Hashes detect
changes relative to the manifest, not authenticity or a verified reviewer identity.
The summary aggregates attributed judgments; it is not an automated tax certificate.

Preserve raw runs and reviews in persistent storage before cleanup. Keep synthetic
transcripts outside Git by default. Review errors separately from product failures;
record rubric calibrations without silently relabelling old runs. Change skills
only for demonstrated causes and rerun affected cases against a new snapshot.
See [validation](../docs/validation.md) and [project status](../docs/project-status.md)
for current outcomes and gaps. No desktop, provider, filing or cross-host acceptance
follows from this bounded developer pilot.

```sh
python3 -B -m unittest discover -s tests -p test_research_eval_runner.py -v
```
