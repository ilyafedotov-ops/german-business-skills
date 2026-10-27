# Versions, releases and verification

[English](releases.md) | [Русский](releases.ru.md)

`VERSION` is the canonical package version. Both plugin manifests must match it;
both root changelogs must describe it. Use SemVer (`major.minor.patch`) with
`-preview.N` while capabilities and compatibility are still being developed.
Increment minor for new capabilities, patch for compatible fixes, and major for
breaking contracts once stable. Before 1.0, document breaking changes explicitly.
Package version and workspace `schema_version` are different: a package update
must never imply automatic migration of private records.

## What is signed

- `SHA256SUMS` detects changed release bytes. Every host ZIP also contains
  `FILE-MANIFEST.json` with the version and SHA-256 of each packaged plugin file.
- The release workflow signs build provenance for all uploaded assets using
  GitHub Actions OIDC and Sigstore; no stored personal signing key is needed.
- GitHub immutable releases protect published assets and their tags and add a
  separate signed release attestation. A repository administrator must enable
  immutability before publishing. The workflow checks the published release's
  immutable status and signature before reporting success. The settings endpoint
  requires admin access, which is deliberately not granted to the workflow.
- This does **not** sign every Git commit, add Windows Authenticode signatures,
  notarize an application, or prove tax correctness or absence of vulnerabilities.
  Commit signing requires a maintainer's separately managed trusted key. Never
  manufacture a key on someone else's behalf or rewrite published history.

Historical `0.3.0-preview`, `0.4.0-preview`, and `0.5.0-preview` releases preserve
the commits in [the changelog](../CHANGELOG.md). They are source-only milestones,
first published now rather than backdated. They have no new build attestations;
GitHub-generated source ZIPs are not individually verified release assets. Use
the current preview's named packages for the attested distribution.

## Download and verify

On the repository's [Releases page](https://github.com/ilyafedotov-ops/german-business-skills/releases),
choose [version 0.11.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.11.0-preview.1) and confirm the **Immutable** marker. Availability requires completed
publication and verification; an absent platform archive is not ready for use.
Download the matching GUI archive or optional Codex/Claude ZIP, plus `SHA256SUMS`,
into a new folder. Application archives are named:

- `de-business-kit-0.11.0-preview.1-gui-windows-x64.zip`
- `de-business-kit-0.11.0-preview.1-gui-macos-arm64.tar.gz` (Apple Silicon)
- `de-business-kit-0.11.0-preview.1-gui-macos-x86_64.tar.gz` (Intel)

The examples below verify the optional Codex ZIP; substitute the exact downloaded
GUI filename to verify an application archive. On Windows, native
PowerShell can compute the hash without Python:

```powershell
Get-FileHash .\de-business-kit-0.11.0-preview.1-codex.zip -Algorithm SHA256
```

On macOS use `shasum -a 256 de-business-kit-0.11.0-preview.1-codex.zip`. Compare with
the matching line of `SHA256SUMS`. A checksum from the same untrusted source is
not authentication. With a current optional GitHub CLI, verify the downloaded archive
(historical validation used 2.103.2; 2.80 could not read those attestation bundles):

```sh
gh release verify v0.11.0-preview.1 -R ilyafedotov-ops/german-business-skills
gh release verify-asset v0.11.0-preview.1 de-business-kit-0.11.0-preview.1-codex.zip -R ilyafedotov-ops/german-business-skills
gh attestation verify de-business-kit-0.11.0-preview.1-codex.zip --repo ilyafedotov-ops/german-business-skills --signer-workflow ilyafedotov-ops/german-business-skills/.github/workflows/release.yml --source-ref refs/tags/v0.11.0-preview.1 --deny-self-hosted-runners
```

For stricter pinning add `--source-digest` with the expected full Git commit from
the release tag. Do not execute downloaded scripts before verification. Extract
into a new folder and follow [application instructions](../gui/README.md) for a GUI
archive or [skill installation guidance](distribution.md) for a Codex/Claude ZIP; preserve
the previous package and back up the private workspace before upgrading. No
Python installation or automatic update is required for Windows users.

## Maintainer publication

1. Change `VERSION`, both manifests, current-version docs and both changelogs.
   Keep historical evidence dates. Run `python3 -B tools/release.py check`,
   package tests and the repository's required checks. Review the release diff.
2. Commit and push the reviewed branch. With publication authorization, create an
   annotated `v<VERSION>` tag at the exact clean commit and push that tag. If a
   trusted signing key is already configured, prefer `git tag -s`; otherwise
   annotated tags plus the verified GitHub release attestations are the supplied
   route. Do not describe unsigned annotated tags as cryptographic signatures.
3. `release.yml` reruns Windows/macOS, native PowerShell 5.1, browser and security
   jobs. An unprivileged job builds twice, compares bytes and uploads immutable
   workflow artifacts. A separate job checks bytes, attests, verifies identity,
   creates a draft with every asset, then publishes it. No project code runs in
   that job with repository write permissions.
4. Inspect the run and use `gh release verify` and `gh attestation verify` on
   downloaded assets. A pushed tag, local build or successful upload alone is not
   a successful release. If a draft remains after failure, inspect it explicitly;
   the workflow never overwrites existing releases. A published mistake needs a
   new version, not a moved tag or replaced asset.
5. Only after step 4 succeeds, set `ref` in the root `.claude-plugin/marketplace.json`
   to the new tag and `sha` to its commit, run `python3 -B -m unittest tests.test_packaging -v`
   and merge that change to the default branch. Until then the
   [GitHub marketplace](distribution.md#github-marketplace-for-claude) keeps
   installing the previous verified release; it never installs unreleased source.

Local rehearsal after creating the exact tag:

```sh
python3 -B tools/release.py prepare --tag v0.11.0-preview.1 --output /absolute/new/release-assets
python3 -B tools/release.py verify --directory /absolute/new/release-assets
```

CI uses pinned action commits, read-only default permissions, no persisted Git
credentials, time limits and separate publication permissions. Dependabot proposes
action/npm updates; npm audit and dependency review reject high-severity dependency
issues. CodeQL analyzes Python, JavaScript and Actions. Fresh SARIF results block release
for security severity >= 7 (high/critical) or error-level findings. Rule metadata
is resolved from driver and extension components; missing analysis or unknown
rule metadata fails. Inspect alerts for the exact PR/tag ref. Lower-severity findings still require review. CODEOWNERS
records ownership; it does not by itself enforce branch review rules. Scheduled
scans and Dependabot configuration become active from the default branch after
the changes are merged there.

Primary sources checked 2026-10-26: [GitHub attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations),
[release integrity](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/verify-release-integrity),
and [secure Actions use](https://docs.github.com/en/actions/reference/security/secure-use).

## CI coverage and duplicate-run prevention

`Checks` always starts and ends with a stable **Checks gate**; it does not use
workflow-level path skips. Every selected mode validates packages, release metadata,
the fetched marketplace tag/commit, local documentation links and the selector's
regressions on Ubuntu. Security analysis and PR dependency review run independently
with their existing triggers and policies.

- **Full:** runtime, skill instructions, tests, tooling, workflows, dependencies,
  version/build changes and unknown paths retain Windows/macOS Python, browsers,
  native PowerShell, GUI builds and artifact-transfer checks. Tags and reusable
  release calls always select this mode and produce fresh release artifacts.
- **Documentation:** only regular root Markdown, Markdown below `docs/` or
  `packaging/`, and the root marketplace manifest may take the short path. Changes
  to portable skill guides/templates still require full checks. Renames are checked
  as deletion plus addition; unreadable diffs or special file modes select full.
- **Reuse after merge:** a `main` push may reuse a completed successful Checks run
  from the same repository and associated merged PR. Its latest attempt must record
  that PR number, **full** coverage and the exact whole Git tree in the successful
  gate step. Matching the PR head SHA alone is insufficient. Missing, stale,
  ambiguous or inaccessible evidence falls back to full checks; fork PRs do not reuse.

Production branch protection requires **Checks gate** from GitHub Actions,
plus the existing app-bound CodeQL language checks, dependency review and CodeQL
result. Strict up-to-date enforcement and the other branch protections remain in
place. Replace individual runtime check names only after the reviewed gate has
passed and its workflow is merged; preserve security check identities and retain
a rollback copy of the prior settings. Outdated PRs must update from `main` to
emit the new gate.

The final gate rejects failed planners/quick checks, missing matrix results and
unexpected skips before recording evidence. Reuse skips only duplicate runtime
matrices; quick checks and current security scans still run. A CI-only deployment
activates these workflows on `main`; it does not replace immutable product assets
or advance the marketplace version. [Validation](validation.md) distinguishes
local regression checks from actual hosted full/reuse/documentation runs.

GitHub behavior checked **2026-10-27**: [PR merge checkout semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request)
and [required/skipped status checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

## Native GUI archives in 0.7.0-preview.1

Version 0.7.0-preview.1 adds separate Windows x64, macOS arm64 and macOS x86_64 applications.
The `gui-package` CI matrix builds them with hash-locked build tools and exercises
the extracted archive with no external Python on `PATH`. Each bundle includes
`GUI-MANIFEST.json` covering regular files and native library links. The archive
builder rejects special files and checks actual archived bytes against the manifest.
Only then is its outer checksum produced. Portable plugin ZIPs stay independent.

Publication waits for every platform build and smoke check. The privileged job
checks the three downloaded native archives, adds them to `SHA256SUMS`, then signs
and verifies all assets through the existing release workflow. It executes no
project code or native binary. Native bundles are not claimed byte-reproducible;
the existing build-twice check applies to the portable skill packages. GitHub
provenance does not provide Windows Authenticode or Apple notarization.

Actual results and remaining gates are in [GUI guidance](gui.md) and
[validation](validation.md). Confirm publication and verification on the exact
version’s release page; source documentation alone does not establish either.

## Desktop signing: prepared next step

**Preparation checked 2026-10-26; signing is not implemented or validated.**
Signing identities belong to the release maintainer. Business users receiving
assistance through MCP, a browser or installed skills do not need a certificate,
a developer account or a desktop signing setup. The following work concerns the
optional desktop distribution.

The current [builder](../tools/build_gui.py) invokes pinned PyInstaller 6.22.3
with `--onedir`, without a signing identity or `--windowed`, adds the licence and
readmes, then captures file hashes and library links in `GUI-MANIFEST.json`.
It produces a `GermanBusinessKit` directory, not a macOS `.app` bundle.
The [packager](../tools/package_gui.py) checks that manifest, creates Windows ZIP
or macOS `.tar.gz`, verifies the actual archive contents, then writes its checksum.
Consequently, signing after `build_gui.py` returns currently changes already
hashed files and must fail packaging; adding a signing command after packaging
would also invalidate release checksums. A reviewed implementation must separate
assembly, signing and final manifest capture.

1. **macOS identity and format.** Use the maintainer's authorized Developer ID
   Application identity. PyInstaller's `--codesign-identity` signs the collected
   binaries and enables hardened runtime; default ad-hoc signatures do not provide
   that identity. Review only the entitlements the application needs and verify
   the resulting signatures and secure timestamps. See [PyInstaller signing](https://pyinstaller.org/en/stable/feature-notes.html#macos-binary-code-signing)
   and [Apple notarization requirements](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution).
   Select a real `.app` in a suitable distribution container, or a supported
   installer/disk-image route for the existing directory. Apple accepts ZIP,
   UDIF disk images and signed flat installer packages for submission; neither
   the current `.tar.gz` nor a standalone executable can be assumed to support
   stapling. ZIP tickets attach to supported contained items, followed by
   repackaging. This is a packaging decision still to implement, not a rename
   of the current archive. See [Apple's custom workflow](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow).
2. **Windows identity and verification.** Select an authorized maintainer signing
   identity and its key custody mechanism. Define the owned executable signing
   inventory and check bundled third-party signatures separately. The planned
   SignTool step uses SHA-256 file digests and RFC 3161 timestamping
   (`/fd SHA256`, `/tr` with the selected service, `/td SHA256`); validate results
   with `signtool verify /pa /all /v /tw` and reject failures or timestamp warnings.
   Certificate/provider selection and timestamp service remain maintainer decisions.
   See [Microsoft SignTool](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool).
3. **Final bytes and CI custody.** Finish signing before manifest capture. For
   macOS, submit the chosen supported payload with `notarytool`, inspect its
   acceptance and log, staple where supported, then capture the final distributable
   inventory and package it. Keep the manifest outside any sealed `.app` resources
   so writing it does not invalidate the signature. Adapt archive verification to
   the selected format and prove that signatures and tickets survive extraction.
   Only then calculate outer checksums and attest the final assets. This sequence
   is the proposed integration design; today's scripts do not perform it.
   Keep ordinary PR build/test jobs without signing credentials. A protected signing stage
   should consume the reviewed exact-ref artifacts, use tightly scoped credentials
   and publish no private key, credential or secret-bearing log. The existing
   privileged publication job must continue to execute no project code or product
   binary. Certificate provisioning, CI secret changes, signing-service requests,
   notarization uploads and publication require their applicable explicit
   authorization; this document performs none of them.
4. **Acceptance evidence.** Require the expected publisher/Team ID, platform
   signature verification, macOS accepted notarization and ticket validation,
   unchanged post-signing manifest verification, and fresh downloaded-artifact
   launch trials on Windows, Apple Silicon and Intel macOS. Include a fresh Mac
   and offline launch where the chosen container supports stapling; retain actual
   OS dialogs and outcomes without promising that signing removes every warning.
   Apple recommends testing the distributed package on a separate Mac, including
   the ticket's availability offline: [distribution testing](https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution).
   Record only observed results in [validation](validation.md); the desktop
   acceptance gaps in [GUI guidance](gui.md) remain open until those trials pass.
