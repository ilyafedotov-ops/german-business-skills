# GUI/UX research recommendation

Research date: **2026-10-25**. Baseline inspected: **`c4c00ab`**. This is a maintainer design brief, not an implemented interface, a usability-test result or a change to the accounting contract. Concurrent uncommitted accounting work is outside this assessment. See the [primary UX sources](gui-ux-primary-sources.md) for source findings and their authority.

Implementation follow-up: the [synthetic clickable prototype](../prototype.md) now exercises the four proposed journeys. Its [verification record](../prototype-validation.md) is separate from this research baseline; production integration and participant testing remain open.

## Recommendation

Build a **guided business workspace with contextual assistant help**. The user should choose a task, inspect the relevant evidence, resolve a small number of questions and continue later. Make ordinary work understandable through the interface; do not make remembering prompts, reading a manual, learning accounting jargon or installing Python part of the normal journey.

Use a reusable web interface with a narrow adapter to the existing canonical records and validated operations. First validate the interaction design with synthetic data. Then prove a deployment route in the actual Windows/host combination before committing to a framework. A local desktop shell is the leading independent delivery candidate; an embedded host interface could reduce app-switching where actual client capabilities are verified. No new SaaS, cloud account or model subscription is assumed.

## Existing interface: useful foundation and specific gaps

The committed [overview generator](../../skills/de-business-kit/scripts/casefiles/overview.py) produces a local HTML/Markdown snapshot. It has semantic headings/tables, visible keyboard focus, responsive CSS, expandable evidence/technical detail, explicit capability gaps and a next-action explanation. These are useful foundations.

The five navigation links are anchors into one page. The next action is text; document rows and open issues do not open review flows. There is no file picker, source connection flow, search/filter, editable field review, per-item action, live refresh or saved UI position. The page deliberately runs no application JavaScript. Adding buttons would require a real command/data boundary, not just styling this report.

The [native Windows path](../windows.md) removes Python from basic setup/intake, but does not provide a GUI or full parity with the advanced engine. The [core capability plan](../core-capabilities.md) still describes the committed ledger/submission gaps. A GUI must expose actual available actions and keep useful preparation available. An archive or approved proposal must never appear as completed accounting or a submitted return.

This is a source-based interface audit. No new screenshot evaluation, screen-reader test or participant session was performed in this research.

## Screen structure

Start with five destinations, then test whether the labels make sense to users:

| Destination | Main user question | First useful action |
| --- | --- | --- |
| Home | What should I do next? | Continue the highest-priority relevant task |
| Documents | What have I received, and what needs checking? | Add files or open the next review item |
| This month | Which records and payments remain unresolved? | Review an unmatched item or missing evidence |
| Taxes and letters | What needs preparation, submission or a response? | Open a form worksheet or authority letter |
| Accounts and services | Where are my records, and are my current services suitable? | Inspect a source connection or compare services |

Keep preferences, data-processing details and technical diagnostics in Settings/help. Preserve context when switching pages: business/activity, period, selected item and filter. Show ordinary labels; keep JSON keys, hashes and command names behind technical details.

Home should show one primary next action, a short attention list and a factual progress summary. For example: “3 documents need your review” or “1 payment has no linked receipt.” Treat these as sample copy, not current workspace figures. Use “No documents added yet” for an empty workspace and “We could not check these records” for a read error; neither is a healthy zero.

Use concrete progress such as reviewed items out of received items. Keep source coverage separately visible: receiving 10 files does not establish that the month contains only 10 documents. Do not show a single “tax readiness” percentage without a meaningful denominator and rules.

## Guided onboarding and useful hints

Start with **Organize existing records**, **Start a business**, and **Continue my work**. Let users ask a tax question or try a synthetic example without completing setup. Reuse existing profile facts rather than repeating a registration interview.

For existing records, use a short, resumable sequence: choose period/source → preview selected records and omissions → review the proposed destination/import → inspect the result. Group closely related questions; do not turn every small preference into a separate page. Ask for more detail only when it changes the next action.

Show sources as capabilities, not decorative provider logos. Gmail, Lexware, sevdesk and WISO cards should distinguish access not checked, a verified bounded read, partial retrieval and unavailable access. Explain the next supported action and retain file/export fallback. Do not make a browser login, listed plugin or brand choice look like completed synchronization. Existing systems remain authoritative unless a reviewed migration is chosen.

Use three levels of help:

1. **Visible one-line hint:** what to provide and a concrete example.
2. **Expandable “Why is this needed?” / “Where do I find it?”:** explanation beside the relevant field.
3. **Contextual assistant help:** the current question, item and relevant period, using only the actual host's permitted capabilities and data scope.

Essential help must not require hovering. Tooltips can clarify an unfamiliar icon; they should not contain the only explanation of a tax choice. Avoid compulsory product tours, repeated permission dialogs for harmless navigation, and long legal text before any useful action. Explain data destinations at the point of selecting a source, without a blanket “I certify compliance” checkbox.

## Interactions that matter most

**Document review:** source preview on one side and proposed fields on the other; stack these on narrow screens. Selecting a field should expose its original wording/location where available. Distinguish missing evidence, a conflicting value and a proposed accounting treatment. Let users correct a field, save a draft, defer a specific question or continue to the next item. Use “Save reviewed details” instead of an ambiguous “Approve everything.”

**Bank import:** show a sample column mapping and resulting dates, signs, decimal separators and currencies before approval. Keep raw exports unchanged. Drag-and-drop is a convenience alongside an accessible file-picker button, never the only route. Explain unsupported files and skipped items individually.

**Errors/recovery:** keep entered values, give a specific inline error plus a focusable summary where appropriate, and offer a recoverable next action. Distinguish cancellation from failure. On interrupted imports, show per-file outcomes and inspect prior results before retrying. Show “Saved” only after the validated operation succeeds; show a conflict when records changed elsewhere.

**Decisions and submissions:** keep preparation, review, actual posting, transmission receipt and authority response as separate states. Before a consequential external action, show the recipient, period, payload summary and unresolved blockers. Apply confirmation where the action needs it, not to every click. Undo can reverse a local draft edit; posted entries and transmitted returns need their actual correction procedures.

**Service comparison:** start with current services and must-haves. Compare normal costs, promotional costs, exclusions and unknowns; show why a recommendation fits. Retaining current cover/account or buying nothing must remain valid outcomes. A comparison is not a purchase flow.

**Visual language:** calm hierarchy, readable text, consistent button placement, explicit labels and generous hit areas. Use color plus text/icons for statuses. Avoid celebratory “all done” screens when accounting or filing remains open. Support keyboard use, zoom/reflow, screen-reader labels, visible focus and announced save/error states. Maintain EN/RU parity while retaining official German form labels with optional explanations.

These patterns are project recommendations, informed by the cited UX guidance. They are not claims that a particular design has already succeeded with this audience.

## GUI versus web: delivery decision

| Option | Advantage | Material limitation | Recommendation |
| --- | --- | --- | --- |
| Existing generated HTML | Simple local status report with no running application | Snapshot; no validated interactive actions | Retain as printable/shareable fallback |
| Browser-only application | Easy demonstration; shared interface | Persistent local-folder access is not equally available across browsers; permission/hosting/storage model needs proof | Good prototype route; do not promise universal workspace editing |
| Interactive UI inside an AI host | Keeps assistant context and may reuse connected tools | Host/edition support varies; an installed skill does not supply an app server or UI bridge | Test exact intended Codex/Claude surfaces before adopting |
| Packaged local app with a shared web UI and native bridge | Native file dialogs and controlled local operations with a common Windows/macOS interface | Requires packaging, signing, updates, permission and OS-specific acceptance work | Leading independent delivery candidate |
| Windows-only native UI | Fits Windows platform controls closely | Separate macOS implementation and maintenance | Consider if product scope becomes Windows-only |

MDN documents limited browser availability, secure-context and user-activation constraints for [`showDirectoryPicker`](https://developer.mozilla.org/en-US/docs/Web/API/Window/showDirectoryPicker). That limits a promise that one ordinary web page can manage arbitrary private folders consistently everywhere; it does not prevent file-upload/download workflows.

[MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview) supports interactive HTML through an explicit host protocol and states that client support varies. Its documentation is not acceptance evidence for the user's exact Codex or Claude Code surface, plan or version. A separate GUI also must not assume that it can reuse an existing chat subscription as a model API or silently send context into a chat.

[Tauri's process model](https://v2.tauri.app/concept/process-model/) uses OS webviews: WebView2 on Windows and WKWebView on macOS. Its [capability system](https://v2.tauri.app/security/capabilities/) can constrain frontend access. It is a plausible spike candidate, not a selected dependency. Keep sensitive operations behind a narrow validated command boundary; do not expose arbitrary shell execution or whole-home filesystem access to the UI.

Microsoft requires [WebView2 runtime detection/distribution](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution), including handling machines where it is absent. “No Python installation” does not mean “every runtime is already present.” The installer must handle necessary runtime delivery through a reviewed route, with an offline/managed-device story. Developer Rust/Node/.NET toolchains must never become end-user setup steps. Microsoft also describes [self-contained Windows App SDK deployment](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/self-contained-deploy/deploy-self-contained-apps), with larger packages as a tradeoff.

A local GUI must keep the existing source-of-truth records, locking, expected-version checks and evidence links. Do not recreate accounting rules in JavaScript or maintain a second UI-only task list. Before adding action buttons, resolve the no-Python execution route for each operation. A graphical wrapper does not solve missing validation or posting capabilities.

## First prototype and acceptance evidence

Prototype four connected journeys with synthetic data: existing-folder onboarding; reviewing one ambiguous invoice; resolving one unmatched payment; closing and resuming the same task. Include empty, loading, unavailable connection, missing capability, changed record, cancelled operation and partial failure states. Show actual uncertainty and allow leaving a task unfinished.

Suggested formative study: 6–8 participants across two small rounds, primarily nontechnical Windows users, with macOS representation, EN/RU coverage and accessibility needs. This is a practical starting sample, not a statistically representative benchmark. Use their own words and observe unassisted behavior; do not teach the UI before the task.

Measure task completion, requests for help, wrong actions, time to first useful result, recovery after interruption and understanding of what has or has not been posted/submitted. Proposed design gates: ordinary journeys need no terminal/JSON editing; participants can identify the next action and resume position; each participant distinguishes a saved draft from an actual submission; any mistaken external-submission belief blocks release until corrected. Set timing targets after observing a baseline, not from invented industry averages.

Separately test keyboard/focus, screen reader, zoom/reflow, error identification and status announcements against applicable WCAG 2.2 criteria. Human research, accessibility checks, utility tests and native Windows/host acceptance are different evidence categories. Passing one does not substitute for the others.

Next deliverable: an interactive prototype and observed usability findings, followed by a small deployment/command-bridge spike. No production UI, new framework dependency, installation or service integration was introduced by this research.
