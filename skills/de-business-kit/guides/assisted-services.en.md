# Help inside ELSTER and your accounting software

**English** · [Русский](assisted-services.ru.md)

You can ask the assistant to help operate a service, not just explain it. For
example: **“Help me fill this draft; I will check and submit it myself.”** With
suitable permitted browser or computer tools, it can enter supported fields,
inspect the result and guide you through the remaining steps. Availability is
checked for your actual app, account and requested operation.

## 1. Say what you want to finish

Give the service name and result, such as preparing a registration form, editing
an invoice draft or downloading October's documents. If a draft already exists,
point to it. You do not need to know about APIs, connectors or file schemas.

> I use Lexware Office in my browser. Help me correct an existing invoice draft.
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
unperformed. [Choose a task](tasks.en.md) · [Everyday help](user-guide.en.md).
