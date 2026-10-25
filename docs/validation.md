# Validation status — v0.4.0 preview

[English](validation.md) | [Русский](validation.ru.md)

Checked **2026-10-25**. Tests use synthetic temporary data, never live business records or accounts.

## Automated local checks

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
| Workspace | Blank profile; all twelve months; no overwrite; actual Git/worktree/bare-repo and skill boundaries, including a later Git initialization |
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
