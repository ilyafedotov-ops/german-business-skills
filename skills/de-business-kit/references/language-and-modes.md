# English, Russian and working modes

Use a single skill, profile and evidence history for both supported languages. Agent instructions and machine identifiers are kept in English; user conversations, explanations, questions, summaries and generated Markdown reports must use the selected language. Do not make the user understand internal English instructions to complete a workflow.

## Resolve the language

1. Follow an explicit language request for the current task, including a requested translation of a particular deliverable.
2. Otherwise read the saved `language` in `00_admin/workspace.json`.
3. If no saved preference exists, use the dominant language of the user's task: Russian or English. Use English for an unclear/mixed request unless the session already establishes the preference.
4. Persist a preference when the user asks to change the default, or when initializing with the language they chose. A request such as “write this report in English” changes that report only.

New workspace folders and start guides support `en`, `ru` and `de`; folder language is chosen once and remains fixed when conversation preferences change. German has no complete localized template set in v0.4; do not silently claim that it does or migrate its saved setting. If the user needs German output, adapt the English template while retaining its evidence fields and state the supported document languages when relevant.

Keep official German labels such as **Kleinunternehmerregelung**, **Regelbesteuerung**, **Einnahmenüberschussrechnung (EÜR)** and **Fragebogen zur steuerlichen Erfassung**. Explain them in the user's language on first use. Quote actual form field labels exactly. Translate explanatory text, not legal quotations, authority names, document numbers or evidence.

Keep JSON keys, enum values, logical path references, document IDs and ISO dates stable. Resolve physical paths with `workspace.py folders` or native `-Action folders` before using ordinary file tools. Do not rename existing folders when switching language. Record monetary values as decimal strings with a currency. In user tables, use readable local formatting without changing the underlying amount; explain net/gross and the tax period. Do not turn a German decimal comma into a thousands separator or infer an ambiguous date.

## Resolve the mode

| Identifier | English label | Russian label | Load |
|---|---|---|---|
| `general` | Startup and organization | Открытие и организация бизнеса | The relevant intake/formation/provider module |
| `bookkeeping` | Bookkeeping | Ведение бухгалтерии | [Bookkeeping](bookkeeping.md) |
| `tax-consultant` | Tax questions and preparation | Налоговые вопросы и подготовка | [Tax preparation](tax-consultant.md) and relevant [German rules](german-rules.md) |

Treat the user's current task as the priority. Reuse the saved mode for an open-ended request such as “continue.” If a bookkeeping task raises a tax issue, use the tax module for that issue and continue evidence work; do not abandon the whole month or rewrite the default. If the user explicitly says “switch to tax-consultant mode,” save that choice for an existing private workspace. If they only request a single tax explanation, answer it without changing the default.

Modes organize work; they do not change VAT treatment, bookkeeping method, source evidence, external permissions or professional qualifications. Both modes use the same provenance and review rules. The tax mode supplies useful analysis for the user's own decisions; it must not describe the agent as a licensed Steuerberater.

## Persist a requested setting

```bash
python3 <skill-directory>/scripts/workspace.py configure --root /absolute/private-workspace --language ru --mode bookkeeping
python3 <skill-directory>/scripts/workspace.py configure --root /absolute/private-workspace --language en --mode tax-consultant
python3 <skill-directory>/scripts/workspace.py status --root /absolute/private-workspace
```

Use either setting on its own when only that preference changes. Do not request another confirmation for the same explicit local setting change. If no private workspace exists, apply the preference in the current session; do not create a folder in the public checkout or require setup before a general answer. Record durable preferences once a suitable private workspace is initialized.

## Localized templates

Read [the locale manifest](../assets/locales.json) and copy the selected Markdown template to its private destination. Replace placeholders with the user's evidence or an explicit unknown. The package checker verifies that both languages include the same template roles.

| Deliverable | English | Russian | Private destination |
|---|---|---|---|
| Working agreement | [Template](../assets/en/bookkeeping-workflow.md) | [Шаблон](../assets/ru/bookkeeping-workflow.md) | `04_accounting/workflow.md` |
| Monthly preparation | [Template](../assets/en/month-close.md) | [Шаблон](../assets/ru/month-close.md) | `06_bookkeeping/YYYY/MM/close.md` |
| Form worksheet | [Template](../assets/en/form-worksheet.md) | [Шаблон](../assets/ru/form-worksheet.md) | `02_registration/` or `05_tax/YYYY/` |
| Tax consultation | [Template](../assets/en/tax-consultation.md) | [Шаблон](../assets/ru/tax-consultation.md) | `05_tax/YYYY/consultations/` |

Preserve an existing report/decision and link its revision. A requested language change does not authorize rewriting original evidence or historical reports. Produce a translation as a linked derivative when needed; preserve its source, effective date and review status. A translation is not new verification.

Machine templates remain shared: [proposal](../assets/proposal.json), [operation](../assets/operation.json), [source check](../assets/source-check.json). Put human-readable explanations in the selected language, while keeping enum values and keys unchanged. CLI JSON and error codes are technical English interfaces; explain their meaning to the user in the selected language.

## State vocabulary

| Machine state | English explanation | Russian explanation |
|---|---|---|
| `unknown` | Unknown; evidence is missing | Неизвестно; нет данных |
| `declared` | Stated by the user/source, not independently checked | Указано пользователем/источником; отдельно не проверено |
| `proposed` | Suggested treatment, awaiting a decision | Предложение, ожидающее решения |
| `verified` | Supported by inspected evidence for the stated fact | Подтверждено проверенным источником для данного факта |
| `needs_review` | A specific issue remains to be reviewed | Требуется проверка конкретного вопроса |
| `not_posted` | No accounting-system posting has been established | Проводка в бухгалтерской системе не подтверждена |
| `submission_unconfirmed` | Transmission result has not been confirmed | Результат отправки не подтверждён |

Translate these for readability without changing their meaning. Never turn “prepared,” “matched” or “submitted” into “legally correct,” “closed” or “accepted.”
