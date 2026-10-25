# Data boundary and privacy

This is a practical workflow, not a compliance certificate. Use synthetic/redacted samples until the user has established an appropriate processing setup for real client data. Do useful non-personal preparation meanwhile.

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

## Scope of the free project

Distributing static skills does not automatically give the author access to user documents. v0.1 scripts make no network calls and include no telemetry. Any later hosted service, support upload, analytics or error collector changes the data flow and must be assessed separately. Model providers, bookkeeping software and account providers still have their own terms and fees.

## Official starting sources

Checked 2026-10-25; verify terms for the actual account before using real third-party data.

- GDPR, especially Articles 5, 6, 13/14, 28, 32, 35 and Chapter V: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- DSK guidance, selection and use of AI: https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf
- DSK technical/organizational measures: https://www.datenschutz-berlin.de/fileadmin/user_upload/pdf/publikationen/DSK/2025/20250617-DSK-OH_KI-Systeme.pdf
- OpenAI API data controls (API scope): https://developers.openai.com/api/docs/guides/your-data
- Claude Code data usage and local logs: https://code.claude.com/docs/en/data-usage
- Anthropic commercial DPA: https://privacy.claude.com/en/articles/7996862-how-do-i-view-and-sign-your-data-processing-addendum-dpa

Use privacy/source questions as targeted preparation, not a blanket refusal to help the user organize their own business.
