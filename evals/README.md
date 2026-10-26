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
