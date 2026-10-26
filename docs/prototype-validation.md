# Guided workspace prototype: verification

[English](prototype-validation.md) | [Русский](prototype-validation.ru.md)

Current capabilities are summarized in [project status](project-status.md). Dated entries below retain their original scope and results; they are not cumulative proof for later code.

Checked on **2026-10-25**, on macOS ARM64, Node 22.23.2 and Playwright 1.63.0. Scope: the static fictional prototype in `prototype/`, not the installed skill, a production desktop application or live accounting services.

## Functional browser evidence

- Commands: `npm run test:browser` and `npm run test:browser -- --browser=webkit`.
- Chromium and WebKit open the real `prototype/index.html` through `file://`, with no development server and no application network requests.
- All four journeys pass: selected sample-folder intake; correction of the invoice total with unresolved category; investigation/defer/link of a payment; close/reopen/resume of saved work.
- Additional states: empty catalog, empty search, no selected files, invalid review fields and source-focused error links, contextual help, explicit reset/cancel, failed storage writes and conflicting edits in two tabs. Onboarding preview position and selected subset survive reload.
- Screens checked: Home, Documents, invoice review, This month, payment investigation, Taxes and letters, Accounts and services, Settings and onboarding. Viewports: 1440×1000, 390×844 and 320×844; all narrow screens checked for page overflow.
- Keyboard checks: skip-to-content retains the current screen and focuses main; error links focus fields; modal Escape closes help and restores the trigger focus.
- No unexpected application console errors or failed requests. WebKit emits five exact CSP refusals while Playwright injects its screenshot stylesheet. A separate load-and-capture probe reproduced this tool-only behavior. The test identifies that diagnostic only during screenshot capture; application CSP is unchanged. It does not suppress other console errors.

Developer-only dependencies are locked in `package-lock.json`. Browser CI is configured for Chromium on Windows and WebKit on macOS; a local macOS run is not proof that those hosted jobs passed.

## Visual evidence and Impeccable

Reference: the user's written five-screen brief and [saved recommendation](research/gui-ux-recommendation.md). No approved pixel screenshot or Figma baseline was supplied. Comparison is against written layout and interaction criteria, not a claim of pixel parity.

The Impeccable refinement used its Operate/polish guidance: preserve task behavior, give the next action priority, use consistent controls, visible contextual instructions, readable supporting text and structural responsive layouts. Removed decorative heading labels and illustration; navigation uses authored SVG icons and wraps on narrow screens. No remote fonts or images are needed.

Captured desktop Home/review and mobile review images live in ignored `output/prototype/` as `chromium-home-desktop.png`, `chromium-review-desktop.png`, `chromium-review-390.png`, `chromium-review-320.png` and corresponding WebKit captures. Storage-error screenshots are retained there too. Screenshots are synthetic. There is no pixel diff artifact because the reference is written, not visual.

Design-hook triage: supporting text below the readable size was enlarged; muted text was darkened; the destructive button's hover foreground/background contrast was corrected. The manual Impeccable detector also flagged the unused Inter preference, which was removed in favor of the native system stack. No detector suppression was added. These checks do not certify WCAG conformance.

## Automated state and repository checks

`npm test` passes five state tests: exact amount parsing, retained draft/resume, storage failure, conflicting writes and malformed saved data. The initial test run failed because the state module did not exist; it passed after implementation. Browser regressions reproduced lost onboarding state and incorrect keyboard navigation before the fixes. WebKit identified focus restoration needing an explicit handler.

`GBK_TEST_DOCKER_IMAGE=mcr.microsoft.com/dotnet/sdk:9.0 python3 -B -m unittest discover -s tests -v` passed **173 tests**. This includes the new package-check scope regression and PowerShell interoperability using the developer container; it is not native Windows PowerShell 5.1 evidence.

## Remaining acceptance work

No moderated usability study, screen-reader study, native Windows desktop session, real folder import, PDF rendering, OCR, live connector, accounting posting, tax calculation or submission was tested by this prototype. The English interface still needs localization before a bilingual product release. Test with nontechnical Windows/macOS participants before selecting a production desktop shell and connecting the interface to validated commands.
