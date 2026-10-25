# Validation status — v0.1.0 preview

Checked **2026-10-25**. Tests use synthetic temporary data, never live business records or accounts.

## Automated local checks

The Python test suite contains **39 passing tests**: **10 installer tests** and **29 workspace tests**.

```bash
python3 -B -m unittest discover -s tests -v
python3 tools/check_package.py
```

The skill also passes the available skill-creator frontmatter/name validator. The package checker verifies required files, local Markdown links, self-contained skill references and JSON syntax. It does not check every remote source or establish legal accuracy.

A synthetic end-to-end local run initialized the workspace, recorded a fact, imported original CSV bytes, reconciled the supplied examples, verified integrity and installed the skill into both project directories. It correctly produced **3 matched groups and 1 unmatched bank operation**, with status `needs_review`. This exercised local files and installer behavior, not either desktop UI.

| Area | Verified behavior |
|---|---|
| Installation | Correct local Codex/Claude directories; both-target preflight; dry run; preserve existing skills/configuration; reject symlink/traversal inputs |
| Workspace | Blank profile; all twelve months; no overwrite; actual Git/worktree/bare-repo and skill boundaries, including a later Git initialization |
| Updates | Provenance requirements; before/after profile history; active lock protection; corrupt audit preflight |
| Original documents | Byte preservation; content deduplication; tamper detection; private paths; extension/size limits |
| Interrupted import | Source preserved; rollback only for an unchanged new copy when index is uncommitted; preserve changed or already-indexed copies |
| Unexpected originals | Report unindexed files and unexpected non-regular entries without following symlinks |
| Reconciliation | Explicit IDs; signed Decimal arithmetic; long-number/tiny-addend precision; fee splits; currencies separated; unmatched and unlinked entries |
| Invalid/empty data | Reject duplicate IDs, malformed amounts and wrong-period dates; empty inputs require review |
| Outputs | Unique derived reports; source files preserved; summaries omit private profile values |

The independent code review found and resolved three concrete classes of error: empty-input false matches, decimal precision loss for extreme aligned amounts, and unindexed originals after interrupted imports. These fixes have regression tests.

## Behavioral trial

One fresh agent session used the skill for a synthetic user adding SaaS/Gewerbe while already applying Regelbesteuerung, with only file and web-search capabilities. It retained person-wide VAT context, distinguished the new activity's form forecasts from person-wide thresholds, prepared useful fields, asked focused follow-up questions and did not invent browser access or claim a submission.

This was one behavioral trial. The **12 prompts** in `evals/scenarios.json` form a reusable evaluation set; the remaining prompts have not all been executed. Do not describe this as a complete legal evaluation or measured model reliability.

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
