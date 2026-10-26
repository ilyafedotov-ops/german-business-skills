> Dated review, not current implementation status. See [current status](../project-status.md) for delivery and acceptance.

# Architecture review: findings and gaps

Review date: **2026-10-26**. Baseline inspected: **`14a3360`** (`0.9.0-preview.1` plus merged service work). This is a maintainer review of architecture, features and gaps, performed inline in one Claude Code session without an independent reviewer. It is not a security audit, a usability test or a legal assessment. Legal timelines below come from the repository's own dated source map and need a current primary-source check before they drive implementation.

## Verdict

The engineering foundation is strong: careful filesystem and HTTP safety, honest capability boundaries and a mature release pipeline. The main risks are product gaps, not code quality. Two are time-sensitive or structural (e-invoice issuance; VAT in the local journal), and one blocks the roadmap's own non-technical acceptance (unsigned desktop applications).

Baseline health at review time: `python3 -B -m unittest discover -s tests` ran 277 tests, all passed with 5 environment skips; `python3 -B tools/check_package.py` passed.

## Architecture summary

| Layer | Implementation | Assessment |
| --- | --- | --- |
| Skills | Router plus six domain skills; compact `SKILL.md` files (~2.5–3 KB) with 49 progressively loaded references | Well factored; clear task ownership and handoffs |
| Engine | Standard-library Python: `workspace.py` core (74 KB) plus `casefiles/*`, exposed through `desk.py` | Careful I/O primitives; tightly coupled private helpers (finding 8) |
| Persistence | JSON registers, history snapshots, audit log, one workspace lock, expected-hash concurrency | Appropriate for sole-trader volume; atomic per file, not across files (documented) |
| Delivery | Assistant/CLI, session-protected loopback GUI with bundled runtime, native PowerShell subset | Three routes with documented, different capability sets |

Documentation outweighs production code roughly 2.5:1 (about 1.37 MB of Markdown, 597 KB of it in the skill bundle, against 542 KB of production code). Progressive disclosure keeps a typical route's loaded context small.

## Verified strengths

- **Filesystem safety** ([workspace.py](../../skills/de-business-kit/scripts/workspace.py) lines 73–313): `O_NOFOLLOW`/`O_EXCL`, symlink-chain refusal, `fsync`, Git/skill-directory boundary checks.
- **GUI HTTP boundary** ([server.py](../../gui/server.py) lines 296–337): exact `Host` pinning against DNS rebinding, bearer token delivered in the URL fragment and kept in `sessionStorage`, `Origin`/`Sec-Fetch-Site` checks, strict CSP, idempotent request IDs.
- **GUI escaping**: `esc()` covers every interpolated value through `field`, `option`, `label`, `textarea` and `summary`; CSP `script-src 'self'` is a second layer. No XSS finding.
- **Release supply chain**: OS × Python matrix, Windows PowerShell 5.1 job without Python, SHA-pinned Actions, CodeQL, build-provenance attestation.

## Findings

Severity reflects user impact at review time. Status is as of the end of the review session; fixes are on the named branch until merged.

| # | Severity | Finding | Status |
| --- | --- | --- | --- |
| 1 | High | No structured e-invoice issuance | Open |
| 2 | High | VAT lost between reviewed proposal and cash journal | Addressed on branch `claude/vat-journal-lock-recovery` |
| 3 | High | Desktop applications not code-signed | Open |
| 4 | Medium | Stale workspace lock has no recovery path | Addressed on branch `claude/vat-journal-lock-recovery` |
| 5 | Medium | Read operations take the exclusive write lock | Mitigated on branch `claude/vat-journal-lock-recovery`: writers wait briefly |
| 6 | Medium | Behavioral scenarios are not run automatically | Open |
| 7 | Medium | Workspaces under any symlinked path are refused | Message addressed on branch `claude/vat-journal-lock-recovery`; refusal kept |
| 8 | Low | Cross-module use of private helpers | Open |
| 9 | Low | Audit log rewritten whole on each write | Open |
| 10 | Low | Inconsistent CLI language defaults | Open |
| 11 | Low | Parent directory not synced after atomic replace | Addressed on branch `claude/vat-journal-lock-recovery` (POSIX) |
| 12 | Low | Prototype duplicates the real GUI | Open |

### 1. No structured e-invoice issuance (High)

The repository's sourced rule ([german-rules.md](../../skills/de-business-kit/references/german-rules.md) line 53, from the BMF E-Rechnung FAQ dated 23 March 2026, checked 2026-10-25) ends the general issuance transition after 2026, extended through 2027 where prior-year turnover does not exceed €800,000. For most target users that points to **1 January 2028**. The same reference says remaining exceptions, such as small businesses, need checking. The code only inspects standalone UBL/CII XML ([invoice_xml.py](../../skills/de-business-kit/scripts/casefiles/invoice_xml.py)); it cannot generate XRechnung/ZUGFeRD, extract XML embedded in a PDF, or validate structure and business rules. Operations-skill invoice drafts would therefore not meet the domestic B2B obligation.

Recommendation: decide explicitly whether issuance is in scope, or route issuance to the user's chosen software and keep the kit's role to preparation and inspection.

### 2. VAT lost between proposal and journal (High) — addressed on branch

At baseline, proposals recorded net, VAT, gross and rate with arithmetic checks ([reviews.py](../../skills/de-business-kit/scripts/casefiles/reviews.py) lines 12–15, 89–133), but a cash line held only `kind`, `amount`, `category` and `activity_id`, and an entry had no link to the proposal it settled. The documented evidence chain broke between review and accounting entry, the local route produced no VAT inputs, and free-text categories prevented stable aggregation.

Addressed on branch `claude/vat-journal-lock-recovery`: cash entries `schema_version` 2 record per-line VAT as stated (`stated`, `none_stated` or `unresolved`) and can link the current approved proposal they settle. Links are fingerprinted; reports and filing preflight stop when a linked proposal changes. Period reports group stated VAT by currency, kind and rate and flag `vat_unresolved`/`vat_not_recorded`. The register stays version 1, so existing entries and the native overview keep working. See the [accounting workflow](../../skills/de-business-kit/references/accounting-workflow.md) and the validation row for this checkpoint in [validation](../validation.md).

Remaining from this finding: categories are still free text, and nothing checks that payments linked to one proposal sum to its gross amount.

### 3. Desktop applications not code-signed (High)

Authenticode and Apple Developer ID signing/notarization are not configured ([gui.md](../gui.md) line 54). Gatekeeper and SmartScreen block or warn on first launch, and the documentation correctly tells users not to bypass OS policy. P7's nontechnical first-launch acceptance therefore cannot pass until signing exists. Set up signing before running those user trials.

### 4. Stale lock has no recovery path (Medium)

The lock records `pid` and `created_at` (workspace.py lines 272–292), but no code reads them. With a stale lock, `doctor` reports `workspace_locked` (line 1161) without saying whether the owning process is alive. A GUI user without an assistant is stuck. Recommendation: have `doctor` report owner liveness and age on the same host, and add an unlock command that requires the expected PID and refuses while that process runs.

Addressed on branch `claude/vat-journal-lock-recovery`: locks record process, computer and time (Python and `windows.ps1`). `doctor` reports `lock.assessment` as `active`, `stale` or `unverifiable`. `workspace.py unlock --expected-sha256` and a GUI lock check remove a stale lock, or an unverifiable one only after explicit confirmation, preserving it in history and the audit log; an active lock is never removed. The Windows liveness probe uses `OpenProcess` because `os.kill` would terminate a Windows process. Remaining: standalone PowerShell has no unlock action, and `recovery.ps1` locks hold only a token, so they assess as unverifiable.

### 5. Reads take the exclusive write lock (Medium)

The GUI `status` snapshot holds the workspace lock for its whole read ([server.py](../../gui/server.py) line 229), and `_locked` fails immediately when the lock exists. While the GUI refreshes, a concurrent assistant write fails with "Workspace is locked". A short bounded wait in `_locked` would remove most collisions.

Mitigated on branch `claude/vat-journal-lock-recovery`: writers wait up to five seconds (`LOCK_WAIT_SECONDS`) before refusing. Reads still take the exclusive lock, so an operation longer than the wait, such as a large backup, still blocks others; native PowerShell writers do not wait.

### 6. Behavioral scenarios are not run automatically (Medium)

[scenarios.json](../../evals/scenarios.json) held 73 cases at review time, now 74. `check_package.py` validates only their structure. 17 of 73 scenario IDs appear in the English validation records; `invoice-injection` is not among them. Because skill Markdown is the program for the assistant route, wording changes can regress routing unnoticed. Recommendation: a headless runner with a rubric judge, starting with about ten safety-critical scenarios.

### 7. Symlinked paths refused (Medium)

Confirmed: `workspace.py init --root /tmp/...` fails on macOS because `/tmp` and `/var` are symlinks. Users with symlinked Documents or cloud-sync folders get "Symlinked paths are not allowed" without the offending component. The threat is symlinks inside the workspace. Recommendation: resolve ancestors once at creation, or at least name the component in the error.

Addressed on branch `claude/vat-journal-lock-recovery` for the message only: Python and native PowerShell now name the linked component (and, in Python, its real location), for example "/tmp links to /private/tmp. Use the real location instead." The refusal itself is unchanged; resolving ancestors would change a trust boundary and needs a separate decision.

### 8–12. Lower-severity findings

- **Private-helper coupling.** About 300 calls to underscore-prefixed `workspace.py` helpers across 14 modules (`_inside` 65, `_workspace` 35, `_load` 26). Extracting path and I/O primitives into a public module would stabilize the contract the architecture document already acknowledges.
- **Audit log growth.** `_audit` reloads and rewrites one JSON array per event (workspace.py lines 648–655). At a measured ~314 bytes per event, the 50 MiB read limit is reached after about 167,000 events, which is decades for a sole trader. Append-only JSONL would also allow a hash chain for tamper evidence; the documentation currently claims none.
- **Language defaults.** `init` defaults to Russian (line 1278) and creates Cyrillic folders; `start` (line 1260) and the GUI default to English.
- **Durability.** `_atomic_json` synced the temporary file but not the parent directory after `os.replace`; a POSIX power loss could lose the rename. Addressed on branch `claude/vat-journal-lock-recovery`: atomic and exclusive writes sync their folder on POSIX (measured cost negligible); Windows has no directory sync, and this is not crash-tested.
- **Two frontends.** `prototype/` duplicates much of `gui/`; consider retiring it now that `demo` workspaces exist.

## Missing features

Beyond items the project already declares out of scope:

- VAT return preparation (Voranmeldung, Zusammenfassende Meldung). Finding 2 supplies stated inputs; calculation and form mapping remain with the chosen tool.
- Deadline reminders without a scheduler: export dated tasks as an `.ics` file so the user's calendar handles delivery.
- An update notification for the GUI application.
- Optional DATEV export for users who share with an adviser, and a documented encryption route for backups (for example FileVault or BitLocker).

## Recommended order

1. Start code signing now (finding 3); nothing else in P7 passes without it.
2. Make the e-invoice scope decision (finding 1).
3. Review and merge the journal VAT and lock changes (findings 2, 4, 5, 7 and 11).
4. Add the automated scenario runner (finding 6).

## Method and limits

Evidence came from reading source and documentation, running the unit suite and package check, and targeted probes in scratch workspaces outside the repository: workspace creation under a symlinked path, a simulated stale lock with `doctor`/`status`, audit-event sizing from a `demo` workspace, and escaping in the GUI renderers. One intermediate count was corrected during the review: the scenario-ID count is 17 of 73, not zero (a shell word-splitting error). The review was inline; the repository's independent-review gate for cross-cutting changes was not met by it.
