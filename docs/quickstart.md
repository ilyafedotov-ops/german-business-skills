# Start with German Business Kit

[English](quickstart.md) | [Русский](quickstart.ru.md)

Already have records in Gmail, Lexware, sevdesk, WISO or a folder? [Start with those records](existing-data.md).

Version 0.5.0 preview supports managing your own German sole-trader bookkeeping/accounting and tax reporting. You can prepare registration documents, organize your records, reconcile payments and research tax questions. Complete ledger functionality and ELSTER submission integration are core capabilities still to be completed: the current utilities prepare evidence, proposals and form worksheets. Optional accountant consultation or export addresses a specific need; it is not a required stage.

## Choose the app you already use

Use a local Codex or Claude Code session on Windows or macOS. The app must be able to access your selected folder. On Windows, use the [native path](windows.md): Windows PowerShell 5.1 handles setup and document intake without Python. Advanced Python utilities are optional and have a separate capability boundary. A plugin does not provide those capabilities itself. Claude Cowork and cloud sessions need separate testing; this preview does not promise the same local-file workflow there.

Install the reviewed skill using the [installation guide](../README.md#install), or have a technical helper prepare the [local plugin package](distribution.md). Plugin bundles are available as locally built preview artifacts, not an already-published one-click marketplace listing. A ZIP must be extracted before its marketplace folder is registered. Installing the open-source kit does not include an AI subscription.

After installation, choose **German Business Kit** from the available skill picker. In a local standalone Codex setup you can mention `$de-business-kit`; in Claude Code use `/de-business-kit` for a standalone installation or `/de-business-kit:de-business-kit` for the plugin.

## Send this first message

> Help me start German Business Kit in English. I am using it for my own business. Check the tools available here, guide me to a private folder, and show me the synthetic demonstration before using real documents. Ask only for what is needed for the next step.

You do not need to edit JSON or choose accounting categories to begin. The assistant should guide the setup and explain anything that it cannot check. For tax questions, tell it the relevant year and whether you already have another business activity.

Choose a private folder outside the downloaded source code and outside Git repositories. If the app offers to create a Git repository for that folder, use a local folder session instead. The assistant must explain where selected document contents may be sent: a local folder does not mean the AI model runs locally.

The demonstration uses invented data. The native Windows example shows folder preview, preserved originals, integrity checks and resumption. With the optional Python engine, the reconciliation example finds three matching payment groups and one unmatched EUR 12 outflow. You can inspect this result before choosing to use real records. Keep the demo folder separate from your business folder.

## Everyday requests

- **Set up my business:** “Help me prepare the next registration step. I already have these activities: …”
- **Manage this month:** “Help me manage October myself. Organize receipts, reconcile payments, prepare records for my review and show missing evidence and remaining posting or filing steps.”
- **Tax questions and preparation:** “Explain this tax question using the relevant year's official sources. Show assumptions and anything needing review.”
- **Continue:** “Continue work in my existing private folder. Show what is done, what needs attention, and the next action.”

The tax-workflow ID remains `tax-consultant` for compatibility. The visible label describes preparation and research, not professional status.

## Understand the status

| What the assistant reports | Meaning |
|---|---|
| Setup incomplete | The workspace exists; some processing settings or assessment evidence are still missing. Synthetic/public-data preparation can continue. |
| Needs attention | A listed file, record, evidence item or lock requires inspection. Do not recreate the workspace. |
| Configuration recorded | An assessment was saved. It is limited to its stated scope; it is not legal certification or permission for every action. |
| Needs review on a reconciliation | Some supplied records do not match or coverage needs attention. A successful command does not mean bookkeeping is complete. |

Preparation, your approval, evidence of actual posting/submission and the Finanzamt response are separate stages. A records archive marked `prepared_with_open_items` or `prepared_for_self_review` describes local preparation; neither status means monthly closing or filing completion. Before anything is sent or changed in an external account, review the concrete destination and action. Authentication, certificates and TANs remain in the official login flow. A draft is not a submission, and a submission receipt is not acceptance of its tax treatment.

## When something goes wrong

Ask: “Run the local diagnosis for this workspace and explain the next safe step.” The assistant uses native `verify`, or `doctor` and `verify` with the optional Python engine; neither establishes desktop or legal compliance. Keep error details private and use synthetic/redacted examples for support.

Do not delete an existing folder, originals or a lock just because setup stopped. Keep protected backups, and verify a restoration into a separate folder. Skill updates should preserve the business workspace. See [workspace recovery](../skills/de-business-kit/references/onboarding.md#recovery).

Native Windows/macOS utility CI has passed; desktop-app acceptance remains pending in [validation](validation.md). This guide describes the intended supported workflow, not evidence that every app version has passed it.

Next: [document workflow](document-workflow.md), [international transactions, payment systems and ELSTER preparation](workflows.md), and the [documentation index](index.md).
