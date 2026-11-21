# Interface development

[English](gui.md) | [Русский](gui.ru.md) | [User instructions](../gui/README.md)

The `gui/` application connects a browser interface to the real workspace writers. The separate `prototype/` is a fictional demonstration. Windows x64, macOS Apple Silicon and macOS Intel builds bundle the runtime. [Current status](project-status.md) identifies the published release and newer source changes; follow [download verification](releases.md) and the [application instructions](../gui/README.md).

## Supported work

- See active business tasks across months, including tasks without dates, dependencies and evidence status. Continue through the existing assistant-request dialog; this does not call an AI service or update tasks. Empty workspaces start with the intended business task.
- Open/create a private workspace and use English, Russian or German navigation.
- Import selected PDFs, XML, images and CSVs; see per-file results and review
  catalog details alongside a safe text/image preview or original download.
- Choose local or external authoritative accounting explicitly. Post reviewed
  cash entries with split lines, line VAT as stated, optional links to approved proposals and
  evidence; reverse/correct without rewriting history.
- Create frozen filing versions, inspect preflight blockers, review/authorize,
  record a manual attempt, record an observed receipt, and retain authority responses.
  Cancel/replace only when the existing state machine permits it.
- Save incomplete forms as separate workspace drafts and resume them after restart.
- Produce period reports/overview and create/verify/restore full backups.
- Check a workspace lock after a program closed unexpectedly. A lock whose process
  has ended on this computer can be removed and recorded in history; a running
  owner's lock is kept, and an unverifiable one needs explicit confirmation.

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

## Snapshot profiling

Run `python3 -B tools/profile_gui.py --filings 12 --samples 3` for a disposable synthetic snapshot profile. Use `--filings 60` for a larger fixture. It reports timings and evidence-check call counts without loading a real workspace. Snapshot construction now loads accounting state once and reuses filing preflight results within that same workspace lock. No cache survives the snapshot, and writes still run the canonical preflight.

The month page expands each invoice's recorded allocations, outstanding amount and currency/correction warnings. It uses the existing disclosure and summary controls in EN/RU/DE. “Amounts match” is a local arithmetic result, not an external paid status.

## Fictional prototype

Open [prototype/index.html](../prototype/index.html) in a desktop browser, keeping its sibling CSS/JS files together. This separate English demo uses fictional records only; no installation, login or runtime is needed. Do not enter business data. Its screens are Home, Documents, This month, Taxes and letters, and Accounts and services.

Try sample intake; review the invoice total from `119.00` to `119.80`; investigate the €12 example payment; then close/reopen the same file and continue. “Help me with this” prepares text to copy to an assistant, without sending. No demo operation opens real folders, connects services, posts entries or submits returns.

State lives only in the current browser's local storage. A failed save or conflicting tab leaves edits visible but unsaved; copy them before leaving. Clearing data, private browsing, another browser or moving the file can prevent recovery. Reset affects only fictional data. This is not synchronization, encryption or backup.

Developer checks use the existing Node/Playwright dependencies:

```sh
npm ci --ignore-scripts
npx playwright install chromium webkit
npm test
npm run test:browser
npm run test:browser -- --browser=webkit
```

Tests open the HTML file directly; synthetic screenshots go to ignored `output/prototype/`. No production dependency or network request is added. See the [validation summary](validation.md) for evidence limits and the dated [design research](research/gui-ux-recommendation.md). The real GUI above is implemented separately; ordinary-user usability acceptance remains open.

## Guided setup page

[installer/index.html](../installer/index.html) is a static English/Russian/German setup wizard for people who have never used Claude or ChatGPT/Codex. Keep the `installer` folder together and open the HTML file in a desktop browser; the page itself needs no installation, runtime or account. Its steps are: what to prepare; assistant choice with plan requirements; account creation on the provider's official page; app download for Windows or Mac, including the provider's model-training setting; data and AI notes; German Business Kit installation; and a finish page with one fictional first task, with four demos and copyable requests behind "More examples". Each step shows a few short instructions; the detailed steps, account-safety notes and provider links open from a "More…" section. There is nothing to tick: a step counts as done when the user moves on. The language can be changed on every step. The step list shows a done count and bar (one compact numbered row on phones), and the Claude marketplace screenshot opens enlarged in a dialog. On a phone the first page says that setup runs on a computer.

Its kit-installation step starts with the one-sentence request that the README and the [installation guide](../skills/de-business-kit/guides/install.en.md) recommend: the user copies it into a Claude Cowork task or a Codex project and confirms the plugin installation or file access that the assistant asks for. The guide's click-by-click routes stay available in a collapsed "install manually" section: the Claude plugin marketplace address, and the Codex project-skill copy from the published release ZIP with `SHA256SUMS`. The page never downloads or runs installers, changes host settings, reads files, or collects passwords, payment details, codes or keys. It has no text inputs. Its CSP forbids network connections; official sites open in a new tab only when the user selects a link. Language, assistant, computer type, finished steps and the answer on the data step stay in that browser's local storage. If storage is refused, the page keeps working and says that progress is not saved.

Wording lives in `installer/text.js` (one strict-JSON object per language); official destinations and their check date live in `installer/links.js`. On **2026-11-20** the sign-up, plan, download and skill-location facts were checked against [Claude download](https://claude.com/download), [Claude plans](https://claude.com/pricing), [Claude plugins](https://claude.com/docs/plugins/overview), [Claude login](https://support.claude.com/en/articles/13189465), [Claude phone verification](https://support.claude.com/en/articles/8287232), [ChatGPT desktop app](https://learn.chatgpt.com/docs/app), [ChatGPT for Windows](https://learn.chatgpt.com/docs/windows/windows-app), [Codex with a ChatGPT plan](https://help.openai.com/en/articles/11369540), [ChatGPT plans](https://chatgpt.com/pricing) and [Codex skill locations](https://learn.chatgpt.com/docs/build-skills). Practical consequence on that date: Cowork and plugins need Claude **Pro or higher**, while Codex is included in every ChatGPT plan, **Free and Go included**, with plan-dependent limits. The page nevertheless recommends only paid plans, **Claude Pro or higher** or **ChatGPT Plus or higher**, because free limits run out quickly in regular business work; it does not suggest starting on a free plan. Recheck these pages and record a new date when links or plan rules change. `tests/test_installer.py` checks EN/RU/DE structure, skill names, official HTTPS hosts, documentation anchors and that release links match the tag pinned in `.claude-plugin/marketplace.json`.

The **Data & risks** step comes after the app install, so the account exists, and before the kit, demos and real documents. It reads like a licence agreement: three short warnings (AI mistakes in amounts and deadlines, file content going to Anthropic or OpenAI, not a tax adviser), the full notes in a scrolling box, and the options “I have read and understand” and “I do not accept”. “I do not accept” is selected by default; Next, the kit step and the finish page stay unavailable until the user chooses “I have read and understand”. In plain language the box explains typical AI mistakes and the user's responsibility; that file content read by the assistant can go to Anthropic or OpenAI and stay in the account; GDPR basics for other people's data, health data and redaction in a local copy; that a personal plan is not a business data processing agreement; the AI-literacy duty when staff use AI; and the kit's MIT licence without warranty. An optional six-card "would you share this?" self-test and the [user guide's](../skills/de-business-kit/guides/user-guide.en.md#ai-limits-and-your-data) request for a data-route explanation open on demand. The provider's own training setting is shown on the app step. The answer and the practice answers stay in local storage with the other progress; nothing is sent. Choosing “I have read and understand” only records, in that browser, that the user read the notes; it is not legal advice, a compliance certificate or a waiver, and the page cannot see or change account settings.

On **2026-11-20** that step's claims were checked against [Anthropic model-improvement settings](https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings), Anthropic [consumer](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training) and [commercial](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training) training pages, the [Anthropic DPA](https://support.claude.com/en/articles/7996862-how-do-i-view-and-sign-your-data-processing-addendum-dpa), [OpenAI data controls](https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt), [OpenAI business data](https://openai.com/business-data/) and the [European Commission's AI-literacy Q&A](https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers). Practical consequence on that date: personal Claude use follows **Settings → Privacy → Help improve our AI models**, and thumbs up/down feedback stores the whole conversation for up to five years; personal ChatGPT Free/Plus/Pro has **Improve the model for everyone** on by default, it also covers Codex, and switching it off does not delete saved chats; Claude for Work, ChatGPT Business/Enterprise and the APIs do not train on content by default; Anthropic's DPA is part of its Commercial Terms and OpenAI supports a DPA for business customers; after the Digital Omnibus amendment, AI Act Article 4 still requires providers and deployers to support their staff's AI literacy, without a mandated level. Menu labels are shown in English because localized labels were not verified.

The page is not yet published at a web address or as a release asset; users reach it from a downloaded copy of the repository. It cannot detect whether an app is installed or verify a plugin installation, and it does not replace observing a real first run.

```sh
python3 -B -m unittest discover -s tests -p test_installer.py -v
npm run test:installer -- --browser=chromium
npm run test:installer -- --browser=webkit
```

The browser test opens the file directly in EN/RU/DE for both assistants with Windows and Mac user agents, at 1280, 390 and 320 px. It also checks that no step needs ticking, that Next and the later steps wait for “I have read and understand” (also after a reload), answers the optional self-test (a keyboard answer and a corrected wrong answer), opens the "More…" and "install manually" sections and the screenshot dialog, and checks the progress count and bar. Synthetic screenshots go to ignored `output/installer/`.
