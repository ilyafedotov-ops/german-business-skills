# Validation status — v0.2.0 preview

[English](validation.md) | [Русский](validation.ru.md)

Checked **2026-10-25**. Tests use synthetic temporary data, never live business records or accounts.

## Automated local checks

The Python test suite contains **47 passing tests**: **10 installer tests** and **37 workspace tests**. Eight new tests cover language/mode persistence, compatibility, history, invalid requests and preservation of tax facts.

```bash
python3 -B -m unittest discover -s tests -v
python3 tools/check_package.py
```

The skill also passes the available skill-creator frontmatter/name validator. The package checker verifies required files, local Markdown links, self-contained skill references, JSON syntax and matching English/Russian template roles. It does not check every remote source, assess translation quality or establish legal accuracy.

The original v0.1 synthetic end-to-end local run initialized the workspace, recorded a fact, imported original CSV bytes, reconciled the supplied examples, verified integrity and installed the skill into both project directories. It correctly produced **3 matched groups and 1 unmatched bank operation**, with status `needs_review`. This exercised local files and installer behavior, not either desktop UI. The full local suite above was rerun against v0.2.

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

## Behavioral trials

One fresh agent session used the skill for a synthetic user adding SaaS/Gewerbe while already applying Regelbesteuerung, with only file and web-search capabilities. It retained person-wide VAT context, distinguished the new activity's form forecasts from person-wide thresholds, prepared useful fields, asked focused follow-up questions and did not invent browser access or claim a submission.

This original trial was completed for v0.1. Two additional fresh agent sessions used v0.2 instructions with only their task-local inputs; acceptance criteria and development conclusions were not passed into those sessions. Their outputs were inspected:

| Trial | Observed result |
|---|---|
| Russian tax-consultant question: EUR 60,000 turnover, EUR 15,000 expenses, is a 30% reserve enough? | Answered in Russian; separated conditional business arithmetic, VAT and taxable income; checked official sources; calculated an expressly hypothetical tariff example; did not guarantee a universal reserve or demand full personal disclosure; no workspace or filing created |
| English October bookkeeping report with saved `ru` / `bookkeeping` preferences | Saved an English report; used the bundled reconciliation and found three matched groups plus one unmatched EUR 12 outflow; kept currencies separate, missing evidence and incomplete month coverage explicit; retained `needs_review`; saved preferences remained unchanged on readback |

The second trial also preserved both source CSVs, indexed two byte-identical copies and returned successful original-integrity verification. Its report distinguished supplied normalized data from original bank statements and did not invent postings, tax treatment or external delivery. Test workspaces contained only synthetic data and were removed after inspection.

Environment: hosted agent sessions with local filesystem/Python tools, plus public web research for the tax question. No desktop-app version was involved; a particular model build was not pinned. These are bounded behavior checks, not a cross-model benchmark.

The **18 prompts** in `evals/scenarios.json` form a reusable evaluation set; they have not all been executed. Do not describe these examples as a complete legal evaluation or measured model reliability.

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
