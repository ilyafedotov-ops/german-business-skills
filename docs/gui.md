# Real workspace interface — 0.7.0-preview.1

[English](gui.md) | [Русский](gui.ru.md) | [User instructions](../gui/README.md)

The `gui/` application connects a browser interface to the real workspace writers.
The separate `prototype/` remains a fictional demonstration. Version
[0.7.0-preview.1](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.7.0-preview.1)
adds standalone Windows x64, macOS Apple Silicon and macOS Intel packages. Use a
matching archive only after publication and verification; a local build or
passing test is not a published platform release. [Download verification](releases.md)
and [application instructions](../gui/README.md) explain how to start without
installing Python.

## Supported work

- Open/create a private workspace and use English, Russian or German navigation.
- Import selected PDFs, XML, images and CSVs; see per-file results and review
  catalog details alongside a safe text/image preview or original download.
- Choose local or external authoritative accounting explicitly. Post reviewed
  cash entries with split lines and evidence; reverse/correct without rewriting history.
- Create frozen filing versions, inspect preflight blockers, review/authorize,
  record a manual attempt, record an observed receipt, and retain authority responses.
  Cancel/replace only when the existing state machine permits it.
- Save incomplete forms as separate workspace drafts and resume them after restart.
- Produce period reports/overview and create/verify/restore full backups.

The interface does not add a tax engine, OCR engine, live bank/software connector,
ELSTER transport or background reminder service. Existing accounting programs
remain authoritative when chosen. Document catalog review is not invoice-field
extraction or accounting posting. Source metadata and technical validation errors
can remain in their original language; report templates remain English/Russian.

## Delivery and security

The application opens the user's browser and runs an authenticated service bound
only to `127.0.0.1` on a random port. Requests require a fresh session credential,
exact host checks and same-origin checks. No cross-origin access is enabled.
Workspace identities reject stale tabs after a workspace switch. Native dialogs
use fixed platform commands, never interpolated user input. There are no remote
assets, telemetry or automatic AI calls.

The API delegates mutations to existing validated writers and preserves original
bytes, record hashes, locks and history. Saved forms are nonauthoritative drafts
with version checks and completed history checkpoints. Original files are served
only through the authenticated document API, not a public directory server.
HTML files are downloads, not application content. The browser stores no business
forms; save them explicitly in the workspace before closing.

[PyInstaller](https://pyinstaller.org/en/stable/) is a **build-only dependency**:
platform builds bundle the interpreter with the existing engine. Windows users
do not install Python. Build tools are pinned with wheel hashes. Windows x64,
macOS Apple Silicon and macOS Intel have separate CI build/smoke jobs; the
workflow requires each packaged executable to pass a smoke test with an empty `PATH`.
This does not claim native PowerShell parity for advanced accounting operations.

Portable skill ZIPs remain reproducible. Native GUI archives include a file/link
manifest and archive checksum; byte reproducibility is not claimed for compiled
native bundles. The release workflow adds their archives to the same provenance
verification and immutable release process. Authenticode and Apple Developer ID
signing/notarization are not configured. An OS policy block is not permission to
disable protection. First-run acceptance with nontechnical users is still required.

## Developer operation

With an existing supported Python runtime, run `python3 -B gui/server.py`; the
browser opens automatically. End users of a packaged release do not run this
command. `--root /absolute/private/workspace` opens an existing workspace.
`--no-browser` is for test automation and prints an ephemeral session credential;
do not paste that output into public reports.

```sh
python3 -B -m unittest discover -s tests -p test_gui_server.py -v
npm run test:gui -- --browser=chromium
npm run test:gui -- --browser=webkit
```

In a separate build environment, install `tools/gui-build-requirements.txt` using
`pip install --require-hashes -r tools/gui-build-requirements.txt`. Then:

```sh
python3 -B tools/build_gui.py --output /absolute/new/gui-app
python3 -B tests/gui-packaged-smoke.py --executable /absolute/new/gui-app/GermanBusinessKit
python3 -B tools/package_gui.py --bundle /absolute/new/gui-app --output /absolute/new/gui-archives
```

Use `GermanBusinessKit.exe` on Windows. Build on each target OS; PyInstaller is
not a cross-compiler. Source: [official packaging documentation](https://pyinstaller.org/en/stable/usage.html),
checked 2026-10-26. [GitHub runner architectures](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
establish the CI labels, not desktop acceptance. Record actual results separately
in [validation](validation.md).
