# Primary-source UX research for an owner-operated accounting desk

Historical research: the proposals and source-check dates below describe that investigation. For subsequent implementation and remaining gaps, see [current project status](../project-status.md), [prototype](../prototype.md) and [validation](../validation.md). This note does not renew the external-source checks.

Maintainer research note. Sources checked online on **2026-10-25**. This records design evidence and hypotheses; it does not implement or validate a GUI, certify accessibility, or establish German tax obligations.

## Audience and scope

The intended user is a nontechnical business owner using Windows or macOS, with Codex or Claude Code available, who wants to do their own accounting and tax work. A friendly graphical or web interface should expose meaningful tasks and evidence without requiring Python installation, command knowledge, or an accountant handoff. Those are project constraints, not conclusions from the external sources. Choosing packaging, runtime, storage and host integration needs separate technical evidence.

The research question is how to make a recurring, document-heavy financial workflow understandable, recoverable and controllable. These sources support candidate patterns; they do not prove that this project's users will find a particular interface intuitive.

## Evidence classification

- **Normative standard:** WCAG success criteria define conformance requirements at stated levels. This note proposes WCAG 2.2 AA as an engineering target, without asserting which accessibility laws apply to this project. A selected-criteria checklist cannot establish full conformance.
- **Source advice:** GOV.UK patterns describe that service ecosystem's practice. Microsoft HAX supplies AI interaction design guidance. The W3C COGA document is a Working Group Note with supplemental guidance, not additional requirements for WCAG conformance. Their recommendations are not German accounting rules.
- **Project inference:** The proposed flows, labels, safeguards and evaluation targets below adapt the advice to this audience. They remain hypotheses until evaluated with users and the actual product.

## Source register

All ten entries are first-party sources and were checked on **2026-10-25**. GOV.UK and HAX pages are living guidance; the date is a retrieval date, not an effective tax period.

| ID | Exact source URL | Status and directly supported finding | Affected workflow |
| --- | --- | --- | --- |
| S1 | [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | W3C Recommendation, published version dated 12 December 2024. Covered financial/legal/data submissions need at least one of reversibility, error checking with correction, or review/confirmation/correction under 3.3.4 AA. Other relevant criteria cover keyboard access, reflow, focus, labels, errors and status messages. | All interactions, review and consequential actions |
| S2 | [W3C COGA: Making Content Usable](https://www.w3.org/TR/coga-usable/) | Working Group Note dated 29 April 2021; non-normative supplemental guidance. Sections 4.4.8, 4.5.6–7 and 4.8.2–5 advise short summaries, visible labels, nearby instructions, examples, explanations of consequences and findable help. | Help, complex financial information and onboarding |
| S3 | [GOV.UK: Question pages](https://design-system.service.gov.uk/patterns/question-pages/) | Ask only necessary questions and explain their purpose. Start with one question per page; allow valid uncertainty answers. Short hints serve common needs; longer explanations belong in structured content. Preserve previous answers and working Back navigation. | First use, profile and unfamiliar tax questions |
| S4 | [GOV.UK: Complete multiple tasks](https://design-system.service.gov.uk/patterns/complete-multiple-tasks/) | Use for longer transactions spanning multiple sessions, after simplifying the transaction. Group related actions into tasks, show their statuses and return users to the task overview when they resume. | Monthly work and period close |
| S5 | [GOV.UK: Check answers](https://design-system.service.gov.uk/patterns/check-answers/) | Provide a review stage; larger transactions can have section reviews, subject to user testing. Specific Change links and prepopulated answers enable correction. | Document review and final preparation |
| S6 | [GOV.UK: Error summary](https://design-system.service.gov.uk/components/error-summary/) | Validation errors need a summary and corresponding field messages; move focus to the summary, link to affected answers and use matching messages. This is GOV.UK component guidance, not a universal requirement to copy its exact wording. | Invalid input and recovery |
| S7 | [Microsoft HAX G1: Make clear what the system can do](https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-what-the-system-can-do/) | Set realistic task/domain expectations. Suggested patterns include an introductory explanation, visible controls and examples of inputs and outputs. | First use, empty states and capability disclosure |
| S8 | [Microsoft HAX G9: Support efficient correction](https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-correction/) | AI may be partly correct. Enable output edits and recovery; patterns include changing classifications, detailed edits, undo and batch editing. | Extracted fields, categories and AI proposals |
| S9 | [Microsoft HAX G11: Make clear why the system did what it did](https://www.microsoft.com/en-us/haxtoolkit/guideline/make-clear-why-the-system-did-what-it-did/) | Offer suitable explanations, including local explanations. The page explicitly warns that explanations can increase trust and overreliance; explanation design needs judgment. | Proposal rationale, evidence and uncertainty |
| S10 | [GOV.UK: Using moderated usability testing](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing) | Observe likely users completing relevant, believable tasks with neutral instructions. Think-aloud can reveal understanding. Include accessible arrangements and assistive-technology research; the participant is not being tested. | Evaluation of the proposed experience |

## Candidate interaction patterns

The following are **project inferences**, with their motivating sources identified. Example labels are illustrative English maintainer copy. Production user-facing copy needs the repository's English/Russian parity and must preserve official German form labels where relevant.

### Start with one useful result

First use should explain the supported outcome, data location and any external processing, then offer a synthetic example or a first task such as “Organize this month's documents.” Ask for necessary profile decisions when they affect that task; provide an editable profile summary. Let users pause a question with “I'm not sure” where the workflow can safely retain it as unresolved. A long mandatory setup tour is an untested burden, not a prerequisite for understanding the product. [S3, S7]

An empty Documents view could show one example invoice, the fields the desk can propose and a “Try with sample documents” action. Any installation prerequisite should be handled by the delivery design; user instructions should describe actions they can actually perform on their operating system. [S7; packaging remains out of scope]

### Organize the desk around recurring work

Use a stable overview with tasks such as “Add documents,” “Review 3 documents,” “Match payments,” and “Prepare this period.” Show the selected business and period, the next useful action and reasons for blocked work. Keep completed tasks available for inspection. Do not force a task list onto a short, single-step action. [S4]

Use distinct textual states for document processing and period progress. A proposed document vocabulary is “Added,” “Reading,” “Needs your review,” “Reviewed,” and “Could not read.” “Reviewed” must have an explicit definition; it cannot imply that a return has been filed. Show saved progress when returning to an interrupted period. [S4; exact state model is project-specific]

### Put help where the decision happens

Pair each unfamiliar field with a short hint or example. Put longer “Why is this needed?” material behind an accessible, explicitly labelled disclosure beside the task. Keep consequences needed for the immediate decision visible. A tooltip may supplement help, but required understanding must not depend on hovering or remembering an earlier tour. Use ordinary controls and offer a normal file-picker alternative to drag and drop. [S2, S3]

For a private/business split, show a synthetic worked example of how the entered percentage affects the proposed amount. Keep the original amount and the applied assumption visible. This illustrates the calculation; it does not establish a legally correct deduction. [S2; financial treatment requires separate authority]

### Make document review an evidence task

Present the source document with editable extracted fields. At narrow widths, offer a predictable stacked layout or labelled document/fields switch. Link a disputed value to its page or evidence location when available. Keep original, proposed and accepted values distinguishable. Offer “Accept,” “Edit” and “Leave unresolved,” with an explicit result for each. [S5, S8, S9]

For a synthetic invoice where extraction proposes EUR 119.00 but the source shows EUR 119.80, the user should be able to inspect the source, correct only that value and recheck the totals. An explanation should identify evidence and missing information; it should not convert fluent rationale into proof. Avoid uncalibrated numerical confidence scores and let the user reject a suggestion without composing a prompt. [S8, S9; score policy is project inference]

### Separate proposals, accepted work and external outcomes

Preparing a draft, accepting a proposed change, exporting a file and submitting externally need distinct labels and receipts. Show the destination, period, included items and unresolved issues before a consequential action. Keep a review path back to the specific items. An export result should identify the saved artifact; a submission claim requires evidence of the receiving system's outcome. [S5; outcome evidence is project-specific]

Do not show a generic “all done” state when only local preparation is complete. Offer optional professional help for questions the owner chooses to escalate; do not make an accountant handoff the default completion condition. [Project constraints; S5 motivates explicit completion boundaries]

### Recover without losing the user's work

For invalid values, show a linked summary and a precise field-level correction. For an unreadable document or service failure, explain what was preserved and offer a specific next step such as another file or manual entry. Distinguish invalid input from processing failure. Keep a failed item visible instead of silently dropping it. [S6; processing recovery is project inference]

Allow undo for reversible proposals. If an external operation has an unknown outcome, show “Outcome not confirmed” and a status-check route; a retry must not invite an accidental duplicate. This requires backend duplicate prevention and read-back design, not just friendly error text. [S8; external-operation semantics require separate technical validation]

## Accessibility acceptance candidates

These are a **subset** of S1, not a conformance audit:

- Operate every action by keyboard without traps; keep focus visible and unobscured (2.1.1, 2.1.2, 2.4.7, 2.4.11).
- Provide labels, identifiable errors and usable suggestions (3.3.1–3.3.3); announce asynchronous status messages appropriately (4.1.3).
- Support reflow at 320 CSS pixels, with the criterion's exceptions for content that needs two dimensions (1.4.10).
- Meet target-size or spacing alternatives and stated exceptions (2.5.8).
- For covered consequential changes, satisfy at least one 3.3.4 safeguard. A confirmation dialog on every action is not required by that criterion.

Keep colour supplementary to state text and test hover/focus help if used (1.4.1, 1.4.13). Source: [WCAG 2.2](https://www.w3.org/TR/WCAG22/). Detailed implementation must check the full criteria and exceptions.

## Small evaluation protocol

Following S10, observe likely nontechnical users across Windows and macOS with synthetic records, accessible arrangements and neutral task instructions. Proposed tasks: start a month, correct an extracted amount, leave an ambiguous category unresolved, recover from an unreadable file, resume and export. Ask what is saved and whether anything was submitted. Record completion, assistance, missed errors and understanding of AI suggestions. Include keyboard and relevant screen-reader checks.

Proposed blockers: lost work, unnoticed acceptance of the planted amount error, confusion between export and filing, or recovery requiring technical help. Fix problems and repeat affected tasks with fresh participants. This proposed round can expose problems; it is neither completed research nor general effectiveness proof. [S10; task selection and blockers are project choices]

## Limits and maintenance

No real accounts, customer documents or personal financial data were accessed. No provider UI was evaluated, no competitor effectiveness claims are made, and no tax workflow or integration was certified. The sources do not establish packaging compatibility with Codex or Claude Code, offline behaviour, privacy properties, or production readiness. Recheck living guidance when turning these hypotheses into an implementation specification; verify legal and provider claims in their own authoritative research.
