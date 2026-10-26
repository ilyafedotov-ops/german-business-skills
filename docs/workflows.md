# International business, payments and forms

[English](workflows.md) | [Русский](workflows.ru.md)

Start with a plain-language request in Codex or Claude Code. The assistant uses the existing private workspace and handles the local commands. You do not need to edit JSON, choose a tax answer just to complete setup, or know whether the computer runs Windows or macOS. It checks the available tools and Python launcher first. See [first-time setup](quickstart.md).

| Your task | Example prompt | Result |
|---|---|---|
| Foreign purchase / reverse charge | “I am a Kleinunternehmer and bought foreign SaaS. Prepare the facts and check which VAT questions remain.” | Transaction worksheet, applicable source checks and missing evidence |
| International sales | “Prepare my EU business and non-EU customer invoices for review; distinguish services, goods and consumer digital sales.” | Separate review routes for each transaction; conditional OSS/ZM/customs questions |
| Payments and payouts | “Reconcile this synthetic payment export, fees, partial refund and payout against the bank.” | Per-currency balances, explicit payout links and open items |
| Gewerbe / Freiberufler | “I teach and also sell materials. Help clarify the activities and prepare questions for Finanzamt or my adviser.” | Activity/qualification worksheet; mixed-activity and person-wide VAT checks |
| ELSTER preparation | “Prepare a UStVA worksheet for this period. Keep unknown fields open and show the exact current German labels.” | Evidence-linked fields, calculation notes and a reviewable draft |

The assistant asks only for facts that affect the next step. Keep source invoices/contracts, statement exports and authority letters in the private workspace. Use synthetic or minimized examples until the actual AI data-processing setup has been assessed. Never provide passwords, TANs or ELSTER certificates in chat or worksheets.

For a payment report, confirm the account, period, timezone, type of balance (for example available vs total), opening/closing balances and completeness of the exports. Preserve provider originals. A normalized derivative can represent different providers; the shipped provider-specific reader supports a strict subset of **Stripe itemized activity CSV**, including explicit managed-payment/withheld-tax columns. Stripe payouts are a separate export and need a reviewed normalization. Other providers have no automatic reader or live connection in this release.

Every preparation creates a new English/Russian Markdown report and adjacent JSON under the mapped logical path `07_exports/<period>/`. Resolve its actual folder through the workspace tools; see [folder mapping](folder-structure.md). Reports show facts or balance calculations, sources and remaining checks. `needs_review` means open information/checks remain. `ready_for_review` means the supplied worksheet passed structural checks. `arithmetic_matched` means the supplied statement arithmetic and linked payouts agree; it does not mean tax treatment is correct or the whole bank statement has been reconciled. Existing originals and business profile are preserved.

The form catalogue includes registration, UStVA, annual VAT, EÜR, business inputs for Anlage S/G, conditional Gewerbesteuer and ZM, Dauerfristverlängerung, advance-payment adjustments, supplementary evidence and messages. Which forms are needed depends on your facts and period. A filled worksheet stays **not submitted**. The assistant prepares a concrete draft before any separately authorized official action; receipt and authority response remain separate evidence.

These offline preparation tools are available through the assistant/CLI route. The optional [local GUI](gui.md) covers its documented record operations; it does not provide screens for every preparation worksheet, a complete tax engine or a filing connector. The [technical preparation contract](../skills/de-business-kit/references/preparation.md), [payment format](../skills/de-business-kit/references/payments.md) and [validation record](validation.md) explain the supported scope and evidence.
