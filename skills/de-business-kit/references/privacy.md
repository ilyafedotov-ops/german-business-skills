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

## Sensitive information in ordinary records

Before reading document contents, use the task and user-provided description to identify possible health information, religious or political affiliations, trade-union membership or other special-category data. For example, a health expense invoice or a payment description can reveal more than the amount needed for reconciliation. Do not ingest a complete medical, employee or legal file to discover whether a single transaction matches.

For special-category personal data, establish both the applicable Article 6 basis and an Article 9 condition for the proposed processing route. A business purpose, user instruction, DPA or general consent checkbox alone does not settle that assessment. When unresolved, continue with a synthetic example or a minimized derivative containing only the fields needed for the task. Have the user redact locally before model access when necessary; reading the full document into chat to redact it has already disclosed its contents. Protect the original under the appropriate retention process, and remember that linkable pseudonyms remain personal data. Criminal-offence data has a separate Article 10 rule. Sources: [GDPR Articles 6, 9 and 10](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [EU business data-protection guide](https://europa.eu/youreurope/business/governance-and-sustainability/digital-and-data-compliance/data-protection-gdpr/index_en.htm).

Record only the necessary processing purpose, scope, basis/condition evidence and unresolved issue, not a diagnosis or sensitive affiliation in a task title or log. If the task needs information that cannot yet be processed appropriately, isolate that document and name the precise review needed. Continue the remaining records. Use [legal boundaries](legal-boundaries.md) for requests involving representation, specialist legal judgments or an advisory service for clients, and for practical AI-literacy guidance.

## Scope of the free project

Distributing static skills does not automatically give the author access to user documents. v0.4 scripts make no network calls and include no telemetry. Any later hosted service, support upload, analytics or error collector changes the data flow and must be assessed separately. Model providers, bookkeeping software and account providers still have their own terms and fees.

## Official starting sources

Checked 2026-10-25; verify terms for the actual account before using real third-party data.

- GDPR, especially Articles 5, 6, 9/10, 13/14, 28, 32, 35 and Chapter V: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- DSK guidance, selection and use of AI: https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf
- DSK technical/organizational measures: https://www.datenschutz-berlin.de/fileadmin/user_upload/pdf/publikationen/DSK/2025/20250617-DSK-OH_KI-Systeme.pdf
- OpenAI API data controls (API scope): https://developers.openai.com/api/docs/guides/your-data
- Claude Code data usage and local logs: https://code.claude.com/docs/en/data-usage
- Anthropic commercial DPA: https://privacy.claude.com/en/articles/7996862-how-do-i-view-and-sign-your-data-processing-addendum-dpa

Use privacy/source questions as targeted preparation, not a blanket refusal to help the user organize their own business.
