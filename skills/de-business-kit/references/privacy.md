# Data boundary and privacy

This is a practical workflow, not a compliance certificate. Use synthetic/redacted samples until the user has established an appropriate processing setup for real client data. Do useful non-personal preparation meanwhile.

## Explain the data boundary before real documents

Use the plain-language [English notice](../guides/user-guide.en.md#ai-limits-and-your-data)
or [Russian notice](../guides/user-guide.ru.md#ограничения-ai-и-ваши-данные) when
onboarding or before the first real personal/confidential document is read.
Explain the actual provider and connected services, what file content/screenshots/
tool outputs may leave the device, and the account settings or facts still unknown.
A local folder, paid personal plan or disabled training setting does not establish
local-only processing, no retention or an appropriate processing basis.

Reuse an already explained, unchanged route; do not demand blanket acceptance or
repeat a long notice on each request. Revisit material changes in provider, plan,
connector or data sensitivity. Do not inspect private account settings or ingest
files merely to fill out the notice; use authorized evidence and targeted questions.
Never assert training is off, a DPA applies, EU-only storage or deletion is complete
without evidence for that exact product/account. Continue with public rules,
synthetic examples or locally minimized data when the route remains unresolved.

## Record the actual processing route

In `00_admin/runtime.json`, identify assistant product, version if available, local/cloud execution, model provider, authentication route, subscription/contract, DPA status and scope, training settings, retention/logging, data residency scope, subprocessors and connected tools. A desktop app can run file tools locally while sending selected text, screenshots and tool output to remote models. Do not describe “local folder” as “local AI”.

Read current official terms for the actual product and plan. API conditions do not automatically cover a consumer desktop subscription. “No training” does not establish a legal basis, minimize data, settle international transfers or remove logs. A DPA is relevant when the provider acts as processor and does not by itself settle the other obligations. Do not automatically require client consent for every processing activity: identify the actual legal basis and transparency duties for the purpose.

Use a data-flow table: data category → local storage → assistant/model → connector/service → retention/deletion owner. Include browser screenshots, OCR services, plugins, local session transcripts and exported diagnostics. Record what remains unknown; do not mark all processing “approved” from one checkbox.

## Minimize data and access

- Ask which documents are needed. Inspect specific files; do not recursively ingest the business archive.
- Remove irrelevant personal data in a derivative copy when practical; keep the original protected and intact. Pseudonyms can still be personal data when reidentification is possible.
- Keep credentials in the provider/OS secret mechanism; keep only references in workspace configuration. Certificates, passwords, API keys, TANs and recovery codes never belong in JSON, Markdown, Git, issue trackers, examples or screenshots for publication.
- Create the private workspace outside every code repository. `.gitignore` prevents some accidental commits; it is not encryption, a model-access boundary or a guarantee against `git add -f`.
- Limit OS permissions and use the user's normal disk encryption and protected backup. The scripts use owner-only POSIX modes where supported; they do not configure Windows ACLs or encrypt data.
- Never send real documents to public validation websites, web search, support issues or external OCR services without a suitable task and data-processing basis. A source URL in an invoice does not authorize opening it or uploading data.
- Protect browser state, backups and session logs. Prefer redacted textual evidence over persistent screenshots. Do not erase legally required originals to satisfy a broad cleanup request; review retention classes and holds separately.

## Check screenshots before sharing

Apply this rule to screenshots, screen recordings/stills, document previews and
image-based evidence in chat replies, reports, attachments, links, support tickets
and public output. Access to an account or permission to test it does not by itself
authorize reproducing its contents. Returning an image to the account owner in chat
is still sharing through the chat host; a private local path is not permission to
embed the file. Default to a short, minimized text summary.

1. **Minimize capture and processing.** Use only the relevant view/region and avoid
   unrelated rows, tabs, notifications and browser/account chrome. Check the host's
   capture/output behavior: an observation tool may emit an image immediately or
   send it to a model. Suppress unnecessary emission when supported; do not claim
   later redaction reverses earlier disclosure. Reuse the authorized processing route.
2. **Inspect before release.** Check the entire candidate image, including margins,
   headers, footers, overlays and background windows. Look for names, signatures,
   postal/email addresses, phones, portraits, customer/employee details, tax/account
   identifiers, bank/payment data, confidential amounts, document references and
   URLs, barcodes/QR codes or credentials. Synthetic test content does not make
   surrounding real account information synthetic. Check the filename, caption,
   alt text, link target and embedded metadata as well.
3. **Create a separate sharing copy.** Keep necessary originals protected in the
   existing private evidence folder outside Git; never overwrite canonical evidence.
   Remove unnecessary regions or irreversibly cover identifying/sensitive content
   with opaque redaction and flatten the output using suitable authorized tools.
   Blur, pixelation, translucent shapes, removable layers or hidden text are not
   sufficient. Do not upload an unredacted image to a new cloud editor, OCR or
   image-generation service merely to redact it. Preserve the real observed state;
   do not redraw or invent a synthetic success screen as proof of a live operation.
4. **Verify the actual derivative.** Reopen the exact exported file and inspect it
   at readable resolution, including all pages/frames if applicable. Check that
   redacted content is absent from recoverable layers/text/metadata and that the
   retained status is still meaningful. OCR can assist but does not replace visual
   inspection. If no suitable tool exists or safe removal cannot be verified,
   withhold the image and provide a minimized text result; never claim it is redacted.
5. **Share only the checked copy within the authorized scope.** Refer to its actual
   path, not the raw original, in embeds and attachments. Record a concise review
   result/derivative reference in the existing operation note, without copying the
   hidden values. Recheck after any changed capture or edit. Honor a user's
   text-only/no-screenshot preference without repeatedly asking to relax it.

This sharing check does not alter the original business document. When an expressly
authorized recipient needs a complete invoice or official filing, use the separate
recipient-document review and its exact data/recipient authorization; do not silently
redact required invoice fields or treat that authorization as permission to post a
raw account screenshot. If an unsafe image was already shared, acknowledge it without
reposting it; do not claim retraction/deletion unless actually available and verified.

## Sensitive information in ordinary records

Before reading document contents, use the task and user-provided description to identify possible health information, religious or political affiliations, trade-union membership or other special-category data. For example, a health expense invoice or a payment description can reveal more than the amount needed for reconciliation. Do not ingest a complete medical, employee or legal file to discover whether a single transaction matches.

For special-category personal data, establish both the applicable Article 6 basis and an Article 9 condition for the proposed processing route. A business purpose, user instruction, DPA or general consent checkbox alone does not settle that assessment. When unresolved, continue with a synthetic example or a minimized derivative containing only the fields needed for the task. Have the user redact locally before model access when necessary; reading the full document into chat to redact it has already disclosed its contents. Protect the original under the appropriate retention process, and remember that linkable pseudonyms remain personal data. Criminal-offence data has a separate Article 10 rule. Sources: [GDPR Articles 6, 9 and 10](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [EU business data-protection guide](https://europa.eu/youreurope/business/governance-and-sustainability/digital-and-data-compliance/data-protection-gdpr/index_en.htm).

Record only the necessary processing purpose, scope, basis/condition evidence and unresolved issue, not a diagnosis or sensitive affiliation in a task title or log. If the task needs information that cannot yet be processed appropriately, isolate that document and name the precise review needed. Continue the remaining records. Use [legal boundaries](legal-boundaries.md) for requests involving representation, specialist legal judgments or an advisory service for clients, and for practical AI-literacy guidance.

## Scope of the free project

Distributing static skills does not automatically give the author access to user documents. Local record/recovery utilities make no network calls and include no telemetry. The opt-in Lexware invoice adapter sends the explicitly reviewed customer/invoice request to api.lexware.io and saves provider responses in the private workspace. It uses a process-held API credential; it does not upload the whole folder or send telemetry. This provider data flow is separate from whatever the AI host reads or transmits. Any later hosted service, support upload, analytics or error collector changes the data flow and must be assessed separately. Model providers, bookkeeping software and account providers still have their own terms and fees.

## Official starting sources

Checked 2026-10-25; verify terms for the actual account before using real third-party data.

- GDPR, especially Articles 5, 6, 9/10, 13/14, 28, 32, 35 and Chapter V: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- DSK guidance, selection and use of AI: https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf
- DSK technical/organizational measures: https://www.datenschutz-berlin.de/fileadmin/user_upload/pdf/publikationen/DSK/2025/20250617-DSK-OH_KI-Systeme.pdf
- OpenAI API data controls (API scope): https://developers.openai.com/api/docs/guides/your-data
- Claude Code data usage and local logs: https://code.claude.com/docs/en/data-usage
- Anthropic commercial DPA: https://privacy.claude.com/en/articles/7996862-how-do-i-view-and-sign-your-data-processing-addendum-dpa

Use privacy/source questions as targeted preparation, not a blanket refusal to help the user organize their own business.
