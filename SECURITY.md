# Security and data handling

[English](SECURITY.md) | [Русский](SECURITY.ru.md)

This preview contains offline scripts and agent instructions. It is not an isolation boundary against the AI host, a local administrator or other software. Prompt instructions cannot grant or enforce tool permissions; the runtime must enforce its own access controls.

Do not file a public issue with live invoices, bank statements, tax identifiers, credentials, ELSTER certificates, private filesystem contents or exploitable secrets. Use a synthetic reproducer and redact paths. If a private vulnerability-reporting channel is enabled on the published GitHub repository, use it for sensitive findings. Otherwise contact the maintainer through a channel actually published there; this document does not invent a private contact address.

Never create a client workspace inside the code repository. Keep API tokens and certificates in appropriate secret storage, not profile fields. Protect backups and AI session logs as well as original files. Hash verification detects some changes; it does not prove regulatory compliance or protect against someone changing both files and their index.

Before adding an adapter, assess untrusted-document prompt injection, credential handling, target-domain control, overbroad scopes, duplicate retries, destructive updates and state verification. Do not enable arbitrary commands or URL destinations supplied by document content.

The supplied tests use synthetic temporary data. Live host integration, professional-law review and complete accounting/retention-process assurance are separate activities; do not advertise them as completed.

Language and mode settings are workflow preferences, not new permissions. Translation must preserve evidence, numbers and review status. A tax-consultant mode does not authorize external submissions or establish a licensed professional relationship.
