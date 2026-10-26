# Your first start, step by step

**English** · [Русский](install.ru.md)

This guide takes you from choosing an AI app to getting your first useful answer. You can start without programming, terminal commands, Python or accounting software. You need a Windows PC or Mac, internet access and an account with access to one of the apps below. Use fictional details for your first try.

![An entrepreneur turning an idea into documents and next steps](images/entrepreneur-journey.png)

*Illustration, not an application screenshot.*

## 1. Choose one app

**Codex** and **Claude Code** are AI assistants that can work with files on your computer and use specialist instructions. A **skill** is a set of instructions and supporting materials for the assistant. **German Business Kit** supplies seven connected skills for starting and running a business in Germany.

You need **one** supported app. Choose the one you already have access to; if you have neither, check account access before subscribing.

| Choose | Where to begin | What to open after sign-in |
| --- | --- | --- |
| OpenAI / Codex | [Official desktop download and setup](https://learn.chatgpt.com/docs/app) | The **Codex** experience in the desktop app. Current documentation calls the app **ChatGPT desktop**; some releases/download pages still say **Codex**. |
| Anthropic / Claude Code | [Official Claude desktop download and setup](https://code.claude.com/docs/en/desktop-quickstart) | **Code** in the Claude desktop sidebar, then the **Local** environment. |

Codex access and limits depend on your account and workspace policy. Claude Code desktop currently requires Pro, Max, Team or Enterprise. Ordinary chat access alone does not establish Code access. The skills do not include an AI subscription or service accounts. Provider instructions were checked on **2026-10-26**; follow the official download page for current compatibility and access requirements.

**Done when:** you have chosen one app and confirmed that your account can use its local Codex/Code experience.

## 2. Install and sign in

1. Open the official setup link for your chosen app from the table above.
2. Select the download for **Windows** or **macOS** on that page. If asked which Mac you have, use Apple menu → **About This Mac** to check Apple Silicon or Intel.
3. Open the downloaded installer and follow the provider's instructions. On macOS, move the app to **Applications** if the installer asks; on Windows, complete its installation prompts.
4. Launch the app from **Applications** on Mac or **Start** on Windows.
5. Sign in through the app's official account screen. Complete browser sign-in if it opens, then return to the app.
6. Open **Codex**, or **Code → Local** in Claude. You do not need a terminal version of the app for this route.

If your computer or organization blocks installation, use its approved installation process. Do not disable security settings. Enter passwords and verification codes in the sign-in screens, never in a chat.

**Done when:** you can start a local Codex/Code conversation. If you only see ordinary Chat or Cowork, check the app/account requirements before continuing.

## 3. Create and open an assistant project

1. In **File Explorer** (Windows) or **Finder** (Mac), create a folder called **Business Assistant** in a private location on your computer. For this trial it contains only the skill installation, not real invoices or personal records.
2. In Codex, open/select that local folder as your project and start **New chat**. The folder control's label varies by app version; confirm the selected project is **Business Assistant**.
3. In Claude **Code → Local**, use the project folder control → **Open folder…**, then select **Business Assistant**.
4. If asked to trust/access the folder, confirm only the folder you just created.

**Done when:** the conversation is attached to **Business Assistant**, on this computer. Typing a folder name in ordinary chat does not by itself give the assistant access to it.

![Three steps: open an assistant project, add all seven skills, ask one question](images/setup-map.en.svg)

*Diagram of the process; button positions and app screens are not depicted.*

## 4. Download German Business Kit

1. Open the project's [0.8.0-preview.1 release](https://github.com/ilyafedotov-ops/german-business-skills/releases/tag/v0.8.0-preview.1).
2. Expand **Assets** if the files are hidden. Choose exactly one skill archive:
   - Codex: **`de-business-kit-0.8.0-preview.1-codex.zip`**.
   - Claude Code: **`de-business-kit-0.8.0-preview.1-claude.zip`**.
3. Download **`SHA256SUMS`** from that same release into the same download folder. This file lists checksums used to detect a damaged or changed download.
4. Keep both files together. The `-gui-` archives are a separate optional records application; **Source code** archives are for another installation route.

The next step asks the assistant to verify the selected archive before using its contents. A matching checksum checks file integrity; release/provenance verification checks origin. They are different checks. The [full verification procedure](https://github.com/ilyafedotov-ops/german-business-skills/blob/main/docs/releases.md#download-and-verify) is available for the assistant or a technical helper.

**Done when:** you have the correct ZIP and `SHA256SUMS` from the named release. This newer guide may describe source documentation that is not yet included in that immutable release; the seven-skill directory layout is the same.

## 5. Ask the assistant to install the seven skills

In your **Business Assistant** conversation, provide access to just the downloaded ZIP and `SHA256SUMS`: use the app's file-access control or give their full local paths and approve the specific access request. A chat attachment alone may not grant local file access. On Windows, right-click a file → **Copy as path**; on Mac, select it in Finder, hold **Option**, then use **Copy … as Pathname** from the Edit menu.

Copy this message, adding the two paths and your chosen app:

> I am setting up German Business Kit in this local Business Assistant project, using [Codex / Claude Code]. My downloaded ZIP is at [full ZIP path] and SHA256SUMS is at [full checksum-file path]. Check the ZIP against the matching checksum before using its contents. Verify release provenance for repository ilyafedotov-ops/german-business-skills and tag v0.8.0-preview.1 using https://github.com/ilyafedotov-ops/german-business-skills/blob/main/docs/releases.md#download-and-verify if the required verification tools are already available; state exactly what was and was not verified. Stop if a check fails. Extract into a new folder. Inspect the package, then install all seven complete skill folders into this project's .agents/skills for Codex, or .claude/skills for Claude Code. Use the existing supported installer where available, or copy complete folders with native file tools. Preserve existing files; stop if a destination already exists. Do not install runtimes, alter security settings, or change global app configuration. Tell me the seven installed names, the destination and how to start a fresh session.

The app may ask to read these files or write the skill directories. Review that the requested paths match your download and **Business Assistant** project. If it cannot access files, use the [manual fallback](#manual-fallback). If provenance tools are unavailable, checksum success must not be described as signature verification; use the linked verification procedure with a helper if you need that assurance before proceeding.

**Done when:** the assistant reports all seven installed names and the correct project-local destination. Extracting the ZIP, registering a marketplace or getting a friendly “ready” response alone does not prove installation.

## 6. Start a fresh conversation and check discovery

1. Start a **new conversation in the same Business Assistant project**. If the new skills are absent, fully close and reopen the app, then reopen that project.
2. In Codex, open **Skills** in the sidebar if available, or use the skill selector provided by your version. You can explicitly ask it to use **`de-business-kit`**. In the Codex CLI/IDE, `/skills` or `$` opens skill selection; desktop controls may differ.
3. In Claude Code, type **`/`** (or **+ → Slash commands**) and look for **`de-business-kit`**. Select **`/de-business-kit`** for this standalone installation. Plugin installations use a different, namespaced command.
4. Ask: **“Check which German Business Kit skills are actually available in this project. List their names and flag anything missing.”**

You should find:

| Skill name | Helps with |
| --- | --- |
| `de-business-kit` | Starting, continuing, choosing the next task |
| `de-business-start` | Preparing and opening an activity |
| `de-business-operations` | Proposals, invoices and everyday correspondence |
| `de-business-accounting` | Documents and accounting records |
| `de-business-tax` | Tax questions, reports and Finanzamt letters |
| `de-business-services` | Banking, insurance, software and service access |
| `de-business-changes` | Changes, hiring, pausing and closing |

If the host cannot confirm discovery, ask it to inspect the installation paths and report that limitation. Reading names from a folder is useful diagnosis, but not proof that the host has enabled them. Avoid enabling the same bundle as both a standalone skill and a plugin.

**Done when:** the host exposes the installed skills and can load `de-business-kit` in this new session. Seven skills share one business context; you do not need seven chats or seven setups.

## 7. Try one small task

Send this fictional example:

> Use de-business-kit. I am just trying the assistant with a fictional example: I want to start working as a translator in Germany. I do not know where to begin. Help me choose one small first step.

A useful result is one understandable action, with questions only where facts are needed. You should not have to pick accounting software, create a full business workspace or upload private documents to ask this question. The first answer is not proof of a completed registration or tax check.

You can continue in English or Russian. To try your own task, describe what you want: understand a letter, prepare a form, organize documents, compare services, or plan a change. The assistant should check current official sources for legal/tax conclusions and say what remains unknown.

**Done when:** you understand the result and know the next action. If the answer is too technical, say: **“Explain this in plain language and give me only the next step.”**

## 8. Save work when you need it

For an ongoing task, ask:

> Help me choose a separate private business folder and save a readable result and next action there. If I already have a workspace, continue it. Explain what content will be sent to the AI service before using real personal documents.

**Business Assistant** holds skills; a separate folder such as **My business** holds your records. Do not put business records inside a skill folder or source repository. Initialize a new business workspace only when needed and in a new empty destination; do not reinitialize existing records. A cloud-synced Documents/Desktop folder may not be the private local location you intended.

At your next visit, open the same assistant project and say: **“Continue from my saved result in [business folder]. Show the next action.”** Grant access to that separate folder when needed. Existing accounting software remains authoritative if you choose it; a question does not force that decision.

**Next:** [first working task](start.en.md), [task menu](tasks.en.md), [everyday user guide](user-guide.en.md).

## Manual fallback

Use this after verifying the archive as described above, if the assistant cannot copy files. No terminal commands are needed for copying; a file manager copy does not validate the package or provide the installer's conflict checks.

1. Extract the ZIP into a new folder: Windows → right-click → **Extract All…**; Mac → double-click the ZIP.
2. Open `codex/plugins/de-business-kit/skills` or `claude/plugins/de-business-kit/skills` inside the extracted contents. A file manager may add an outer folder with the ZIP's name.
3. In **Business Assistant**, create **`.agents/skills`** for Codex or **`.claude/skills`** for Claude Code. These are two nested folders. On Windows, enable **View → Show → Hidden items** if needed. On Mac, press **Command+Shift+.** to show hidden items; if Finder refuses to create a dot-prefixed folder, ask the assistant or a helper to create this exact destination. Do not substitute a folder without its leading dot.
4. Copy **all seven `de-business-*` folders together** into that destination, including their contents. If any target folder already exists, stop; do not merge or overwrite it. Use the update instructions linked below.
5. Confirm the structure below, then return to step 6. Do not copy just `SKILL.md`, only `de-business-kit`, or an extra enclosing `skills` folder.

```text
Business Assistant/
└── .agents/                  ← Codex; use .claude for Claude Code
    └── skills/
        ├── de-business-kit/
        │   ├── SKILL.md
        │   ├── assets/
        │   ├── guides/
        │   ├── references/
        │   └── scripts/
        ├── de-business-start/SKILL.md
        ├── de-business-operations/SKILL.md
        ├── de-business-accounting/SKILL.md
        ├── de-business-tax/SKILL.md
        ├── de-business-services/SKILL.md
        └── de-business-changes/SKILL.md
```

## If you get stuck

| What you see | Next action |
| --- | --- |
| No Codex/Code area | Check the official app, supported computer, account access and organization policy. Ordinary chat is a different surface. |
| Downloaded files cannot be read | Provide exact paths and grant only the required local access. Do not paste passwords or security tokens. |
| No skills after installation | Check the selected local project, leading-dot destination, all seven folders and fresh session. Avoid nested `skills/skills`. |
| The app wants to install Python or change security policy | Stop that setup step and use native file copying or an approved helper; basic skill installation needs neither. |
| Destination already exists | Preserve it. Follow [update instructions](https://github.com/ilyafedotov-ops/german-business-skills/blob/main/docs/distribution.md), keeping any customizations and business records. |
| No access to bank, email or Lexware | Installing skills does not connect services. Continue with a fictional example or selected local export; establish each connection separately. |
| A command fails | Keep the message, app version, operating system and step number. Ask for help with that specific step; remove personal details before sharing publicly. |

## Evidence and further help

This desktop route follows [OpenAI app instructions](https://learn.chatgpt.com/docs/app), [OpenAI local skills](https://learn.chatgpt.com/docs/build-skills), [Claude desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart) and [Claude skill locations](https://code.claude.com/docs/en/skills#choose-where-skills-load), checked **2026-10-26**. Installation instructions are not a claim that every app version or nontechnical-user journey has passed. See the [actual validation record](https://github.com/ilyafedotov-ops/german-business-skills/blob/main/docs/validation.md).

For optional terminal/plugin routes, see [advanced installation](https://github.com/ilyafedotov-ops/german-business-skills/blob/main/docs/distribution.md). The [local records application](https://github.com/ilyafedotov-ops/german-business-skills/blob/main/gui/README.md) is an additional tool; it is not required to use the skills or ask a question.
