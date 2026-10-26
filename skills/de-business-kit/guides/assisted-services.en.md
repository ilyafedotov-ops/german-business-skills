# Help inside ELSTER and your accounting software

**English** · [Русский](assisted-services.ru.md)

You can ask the assistant to help operate a service, not just explain it. For
example: **“Help me fill this draft; I will check and submit it myself.”** With
suitable permitted browser or computer tools, it can enter supported fields,
inspect the result and guide you through the remaining steps. Availability is
checked for your actual app, account and requested operation.

Start with the [skill invocation instructions](user-guide.en.md#call-a-skill). For a service-access task select `de-business-services`; for the business task below name `de-business-operations`.

## When to enable browser or computer tools

German Business Kit supplies business instructions. Your assistant supplies the
actual tools, helper skills and permissions. Enabling a skill alone does not
connect a bank, open your browser session or authorize changes.

| Your task | Useful capability |
| --- | --- |
| Research current rules or read public help pages | Web search/page reading; interactive browser or desktop access is usually unnecessary. |
| Read or update records through an existing supported connection | The suitable connector and its scoped permissions; no extra browser setup for operations it already supports. |
| Navigate a supported site, inspect a draft, enter agreed fields or obtain a selected export | Interactive browser tools; verify support for the actual site, account, save/download/upload operation and data. |
| Work in an installed application with no suitable connector/browser route | Native computer use, only when the host supports that app, OS, operation and data. |
| Explain a question or work with an already supplied file | Chat and file/document tools; browser/computer access is optional. |

**Check suitability before sensitive accounts.** Anthropic currently strongly
advises against using its built-in browser or Chrome integration for financial
accounts, medical information or other people's personal data, and advises against
granting native control to banking, healthcare or government apps. Some sites are
blocked. Do not use desktop control to bypass a browser restriction. For real
ELSTER, bank or client-record work, check the chosen host's current restrictions
and processing terms first; use a suitable supported connection, appropriately
minimized file or guided manual route when UI control is unsuitable. You can still
prepare values and review evidence without giving the assistant control of a portal.
[Data-processing guidance](user-guide.en.md#ai-limits-and-your-data).

### Enable the capability in your app

These provider-documented routes were checked **26 October 2026**. Names,
availability and organizational policies can differ; the assistant should inspect
what is actually available rather than claim that a switch exists for every user.

| App/route | Setup when offered |
| --- | --- |
| Codex / ChatGPT desktop, built-in browser | Ask to use **@Browser**. It uses a separate browser profile; manage access in **Settings → Browser → Agent permissions**. It currently cannot automate file uploads; handle those manually or use another supported route. [Browser guide](https://learn.chatgpt.com/docs/browser). |
| Codex with your existing browser session | **Settings → Computer Use → select browser → Install** the official extension; return to confirm **Manage**, then select **@Chrome**, **@Edge** or the supported browser in the conversation. [Extension guide](https://learn.chatgpt.com/docs/chrome-extension). |
| Codex with native applications | **Plugins → Computer Use → Install plugin/Enable**, enable its server and skill controls, then **Try now**. Review app permissions under **Settings → Computer use** and the prompted OS permissions. [Computer Use guide](https://learn.chatgpt.com/docs/computer-use). |
| Claude Cowork, browser | Where available, its built-in browser needs no extension. Choose under **Settings → Cowork → Preferred browser**. For existing Chrome tabs, use **Customize → Connectors → Claude in Chrome → Configure**, then enable it for the conversation. [Built-in browser](https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork), [Chrome setup](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome). |
| Claude with native applications | Current beta: Pro/Max on supported macOS/Windows desktop. Use **Settings → Capabilities**, or **System → This computer → Enable computer use**, when shown; review app access. Current documentation excludes Team/Enterprise from this native feature. [Computer-use setup and limits](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork). |

Start with the smallest access needed. Keep login, MFA and certificates in the
official user-controlled flow; never share secrets in chat. Browser content,
screenshots and tool results may reach the AI provider. Review requested scope
and hide unrelated sensitive content before screen access. Enabling control does
not authorize sending, purchasing, paying or submitting; your task's scope and
any final action you reserve for yourself still apply. You can disable access
again in the host. Do not disable security controls or install arbitrary tools.

Try a public or fictional task first:

> Use de-business-services. Check whether you can open and read this public help page with the available browser tools. Do not log in, fill forms or change anything. Tell me what you actually observed and whether this tool supports the interaction I will need later.

The assistant should read the relevant installed helper skill's instructions, if
present, and verify a small permitted operation after setup. **Configured** is
not the same as **tested for this operation**. If the tool is absent or you prefer
not to enable it, continue with a field worksheet, selected export or manual steps.
The kit does not require Python, Playwright or a developer environment for this.

## 1. Say what you want to finish

Give the service name and result, such as preparing a registration form, editing
an invoice draft or downloading October's documents. If a draft already exists,
point to it. You do not need to know about APIs, connectors or file schemas.

> Use de-business-operations. I use Lexware Office in my browser. Help me correct an existing invoice draft.
> Fill the confirmed information and show me the preview. I will finalize and
> send it myself. Tell me what you can access before making changes.

The assistant checks the available tools and current product instructions. An
existing suitable connection may be used for supported actions; a browser can
cover parts that the connector cannot. Missing API access does not automatically
mean buying a higher plan or changing accounting software.

## 2. Open the right account

The assistant explains the route and any access that is actually missing. If login
is required, sign in yourself on the official page, including MFA, certificates
or CAPTCHA. Then say you are ready. Do not paste passwords, TANs, API keys or
ELSTER certificate files into the conversation.

Before real personal documents or screenshots, establish what content the AI
service may receive. A local browser does not mean local AI processing. The
assistant should confirm the intended account/company and draft after you return.
If a new browser integration is needed, it should explain the supported setup and
permissions before asking you to enable it; it must not silently install one.

## 3. Prepare and fill the draft

The assistant gathers only the facts needed for this task and prepares proposed
values with their sources. Unknown details stay open. It can fill authorized
fields using the actual visible labels, check the entered values and save a draft
where supported. Entry may autosave to the service; the agreed scope includes
that effect before typing begins. You need not approve every field again when
you have already authorized this work.

For missing information, the assistant should continue independent fields and
ask one clear question. It must not invent a tax ID, turnover estimate, tax
choice or formula to get past a required field. Calculations use checked sources
and an appropriate official or selected-software tool; unavailable calculations
remain identified gaps.

**ELSTER example:**

> Help me prepare the tax-registration questionnaire for my activity in Germany.
> Check the correct form and my existing account. Fill the facts we know into a
> draft where your tools allow it; ask about missing choices. I will sign in and
> submit after reviewing it. Also explain whether my activity needs a separate
> Gewerbeanmeldung and whether my municipality offers a combined route.

The ELSTER tax-registration questionnaire and municipal Gewerbeanmeldung are
distinct procedures. The route depends on the actual activity and location;
a filled tax questionnaire alone does not prove a trade registration.

## 4. Review together, then confirm yourself

The assistant shows what was entered, the form/document/year and recipient,
remaining warnings, proposed tax choices and attachments. It distinguishes
**save draft**, **preview**, **finalize**, **send** and **submit**.

If you said you would finish manually, the assistant leaves that action to you.
It should tell you where the saved draft is and which observed control to use
when ready. If a required value or warning is unresolved, it explains what is
missing before you submit. A different account or material edit needs a fresh
check of the affected information.

After your action, return to the conversation. The assistant can inspect the
status or a non-secret receipt where available. Your “done” message is recorded
as your report until confirmed by evidence. If the result is uncertain, it checks
history before proposing another attempt.

## Exporting or importing data

> Download the selected October documents from my accounting software. Check the
> date filter and original formats. Do not lock postings, finalize drafts or
> transfer anything to an adviser. If the export cannot avoid those effects,
> explain the alternative before continuing.

Some exports change records or send data elsewhere. The assistant checks the
chosen route, confirms selection/side effects, then inspects the actual downloaded
files and reports partial coverage. A PDF preview is not necessarily the original
invoice XML. An import is a separate write: review the target, mapping and duplicate
handling before it runs. Export/import does not silently change your main books.

For **Lexware Office**, an existing invoice draft may require browser editing;
the currently documented API does not provide an invoice-update operation or a
downloadable invoice file for a draft. The assistant must not finalize the invoice
just to obtain a PDF. These provider details must be rechecked when used; see the
[dated official-source record](../references/assisted-services-sources.md).

## If the assistant cannot operate the page

It should say which capability is missing and complete the available preparation.
For example: “I can prepare these values but cannot upload the attachment in this
browser. Please use the upload control shown on your screen, select this file,
then return so I can check the result.” It can provide a short field-by-field
worksheet or inspect a selected local export. You do not need to install Python
or disable security protections for this fallback.

Keep the saved draft/reference and next action so the next session can resume.
This kit supplies workflows, not a built-in ELSTER/Lexware connector or a guarantee
that every screen is supported. Only local Lexware examples have been tested; live acceptance remains
unperformed. [Choose a task](user-guide.en.md#first-task) · [Everyday help](user-guide.en.md).
