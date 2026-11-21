/* Installer wording. Translate values only: keys, skill names, app menu labels in bold and URLs stay shared. */
window.INSTALLER_TEXT = {
  "en": {
    "meta": {"language": "English", "title": "German Business Kit setup", "locale": "en-GB"},
    "ui": {
      "skip": "Skip to content",
      "brand": "German Business Kit",
      "brandSub": "Guided setup",
      "languageLabel": "Language",
      "progressLabel": "Setup steps",
      "stepOf": "Step {current} of {total}",
      "back": "Back",
      "next": "Next",
      "more": "More…",
      "preview": "What it looks like…",
      "ok": "OK",
      "toContinue": "To continue, click Next.",
      "whenDone": "When you have finished, click Next.",
      "start": "Start setup",
      "copy": "Copy",
      "copied": "Copied. Paste it with Ctrl+V (Windows) or Cmd+V (Mac).",
      "copyFailed": "Could not copy automatically. Select the text and press Ctrl+C (Windows) or Cmd+C (Mac).",
      "newTab": "opens in a new tab",
      "done": "done",
      "saved": "Your progress is saved in this browser on this computer only.",
      "notSaved": "This browser does not allow saving progress. Keep this page open until you finish.",
      "checked": "Provider details checked on {date}. Plans, prices and menus can change; the provider's own page is authoritative.",
      "safety": "This guide never asks for passwords, payment details, verification codes or keys. Enter them only on the provider's own website or in its app.",
      "illustration": "Illustration. Real screens may look different.",
      "chooseFirst": "Choose your assistant first.",
      "acceptFirst": "First read the text and choose “I have read and understand”.",
      "mobile": "Setup runs on a computer. Open this page on Windows or a Mac.",
      "progressSummary": "{done} of {total} steps done",
      "enlarge": "Enlarge screenshot",
      "zoom": "Zoom in",
      "close": "Close",
      "footer": "German Business Kit is AI-assisted self-help software, not tax or legal advice. This page sends nothing; links open official websites only when you select them."
    },
    "steps": {"welcome": "Welcome", "assistant": "Assistant", "account": "Account", "app": "App", "safety": "Data & risks", "skills": "Skills", "demos": "First tasks"},
    "welcome": {
      "eyebrow": "Guided setup · about 30 minutes",
      "title": "Welcome to the German Business Kit Setup Wizard",
      "lead": "This wizard helps you set up an AI assistant for your business: an account, the app and German Business Kit. No programming skills are needed.",
      "needTitle": "What you need",
      "need": [
        "A Windows PC or a Mac with internet access",
        "An email address you can open now",
        "A mobile phone that receives SMS",
        "A bank card for a paid plan: Claude Pro or ChatGPT Plus"
      ],
      "aiTitle": "Good to know before you start",
      "aiShort": "German Business Kit is not a tax adviser, and AI can make mistakes.",
      "ai": "German Business Kit is AI-assisted self-help software, not a tax adviser (Steuerberater). AI can make mistakes, including in amounts and deadlines. Files the assistant reads are processed by Anthropic or OpenAI. Use made-up examples until you have read the data guidance.",
      "aiLink": "Read about AI limits and your data"
    },
    "assistant": {
      "title": "Choose your assistant",
      "business": "Will you work with customers' or employees' data? Personal plans, such as Claude Pro or ChatGPT Plus, do not include a business data processing agreement (DPA); business plans such as Claude Team or ChatGPT Business offer one. The “{name}” step explains this.",
      "lead": "Choose the app German Business Kit will work in. You can set up the other one later.",
      "choose": "Choose {name}",
      "chosen": "Selected",
      "unsure": "Not sure? Choose **Claude**: it has the fewest setup steps.",
      "work": "Using an account from your employer or school? Its administrator may block apps, plugins or skills. Ask them first.",
      "claude": {
        "name": "Claude",
        "maker": "by Anthropic",
        "app": "Claude desktop app with Cowork",
        "summary": "Fewest setup steps. Needs **Pro** or higher.",
        "pricing": "Claude plans and prices",
        "points": [
          "Easiest setup: you add the kit inside the app with a few clicks.",
          "Needs a paid plan: **Pro** or higher (Pro, Max, Ultra, Team or Enterprise). The free plan does not include Cowork.",
          "Works with the files in a folder you choose."
        ]
      },
      "openai": {
        "name": "ChatGPT with Codex",
        "maker": "by OpenAI",
        "app": "ChatGPT desktop app with Codex",
        "summary": "A few more setup steps. We recommend **Plus** or higher.",
        "pricing": "ChatGPT plans and prices",
        "points": [
          "We recommend a paid plan: **Plus** or higher (Plus, Pro, Business or Enterprise). Free and Go have low limits.",
          "More setup steps: you download a file and Codex copies the kit into a project folder.",
          "Works with the files in a project folder on your computer."
        ]
      }
    },
    "account": {
      "lead": "You sign up on the provider's own website. This guide only opens the official page in a new tab.",
      "labelsNote": "Button names can differ by language or app version.",
      "already": "Already have an account? Just click Next.",
      "safetyTitle": "Keep your account safe",
      "safety": [
        "Type passwords, codes and card details only on the provider's own page or in its app.",
        "Nobody from this project will ask you for codes or passwords.",
        "Check the address bar: **claude.ai** or **claude.com** for Claude, **chatgpt.com** or **openai.com** for ChatGPT."
      ],
      "claude": {
        "title": "Create your Claude account",
        "open": "Open the official Claude sign-up page",
        "short": [
          "Sign up with Google or with your email address.",
          "Confirm your mobile number with the code from the SMS.",
          "Choose **Pro** or higher and pay on the Claude website."
        ],
        "steps": [
          "On the official page, choose **Continue with Google**, or enter your email address and choose **Continue with email**.",
          "If you used email, open the message from Claude and select its sign-in link. Claude does not use a password.",
          "Enter a mobile number that can receive text messages and type the 6-digit code you receive. Internet-based and landline numbers do not work.",
          "Choose a plan. German Business Kit needs **Pro** or higher. Pay only on Claude's own website."
        ],
        "diagram": ["Open page", "Confirm email", "Verify phone", "Choose plan"]
      },
      "openai": {
        "title": "Create your ChatGPT account",
        "open": "Open the official ChatGPT sign-up page",
        "short": [
          "Choose **Sign up** and use your email address or another offered option.",
          "Confirm your email address.",
          "Choose **Plus** or higher and pay on the OpenAI website."
        ],
        "steps": [
          "On the official page, choose **Sign up**. Use your email address or one of the account options the page offers.",
          "Follow the page's steps to confirm your email address.",
          "When you first use Codex, the app may ask you to add or verify a phone number. Do this only in the ChatGPT app or on chatgpt.com.",
          "Choose a plan: **Plus** or higher. Pay only on OpenAI's own website."
        ],
        "diagram": ["Open page", "Confirm email", "Verify phone", "Choose plan"]
      }
    },
    "app": {
      "osTitle": "Your computer",
      "detected": "This looks like a {os} computer.",
      "unknown": "We could not detect your computer. Choose it below.",
      "windows": "Windows",
      "mac": "Mac",
      "other": "Linux or another system? Use the official download page; this guide covers Windows and Mac.",
      "official": "Open the official download page instead",
      "blocked": "Does a work computer block the installation? Ask your IT department. Never turn off security settings to install an app.",
      "stepsTitle": "Install and sign in",
      "claude": {
        "title": "Install the Claude app",
        "download": {
          "mac": "Download Claude for Mac",
          "windows": "Download Claude for Windows",
          "windowsArm": "Windows on ARM, for example a Snapdragon laptop? Download this version instead."
        },
        "short": [
          "Download and install the app with the button above.",
          "Open Claude and sign in.",
          "In **Settings → Privacy**, turn off **Help improve our AI models** if you do not want your chats used to train AI models."
        ],
        "mac": [
          "Download the file with the button above. It is saved in your **Downloads** folder.",
          "Open the downloaded file. In the window that appears, drag the Claude icon onto the **Applications** folder.",
          "Open Claude from **Applications**. If your Mac asks whether to open an app downloaded from the internet, confirm only if it is Claude from the official link above.",
          "Sign in with the account from the previous step."
        ],
        "windows": [
          "Download the file with the button above. It is saved in your **Downloads** folder.",
          "Open the downloaded file. If Windows asks for permission, check that the publisher is Anthropic, then allow it.",
          "Wait until the installation finishes. Claude opens by itself; otherwise find **Claude** in the Start menu.",
          "Sign in with the account from the previous step."
        ],
        "doneWhen": "**Done when:** the Claude app is open and you are signed in.",
        "diagram": ["Download", "Install", "Sign in"]
      },
      "openai": {
        "title": "Install the ChatGPT app",
        "download": {
          "macArm": "Download ChatGPT for Mac with Apple chip (M1 or newer)",
          "macIntel": "Download ChatGPT for Mac with Intel processor",
          "windows": "Get ChatGPT for Windows from the Microsoft Store"
        },
        "short": [
          "Download and install the app with the button above.",
          "Open ChatGPT, sign in and choose **Codex**.",
          "In **Settings → Data controls**, turn off **Improve the model for everyone** if you do not want your chats used to train AI models."
        ],
        "macWhich": "Which Mac do I have? Open the Apple menu and choose **About This Mac**. **Chip: Apple M…** means Apple chip; **Processor: Intel** means Intel.",
        "mac": [
          "Download the file for your Mac with a button above. It is saved in your **Downloads** folder.",
          "Open the downloaded file. In the window that appears, drag the app icon (ChatGPT or Codex) onto the **Applications** folder.",
          "Open the app from **Applications**. If your Mac asks whether to open an app downloaded from the internet, confirm only if it is ChatGPT from the official link above.",
          "Sign in with the account from the previous step and choose **Codex**."
        ],
        "windows": [
          "Select the button above and open the downloaded installer.",
          "Follow the steps in the Microsoft Store window and wait until the installation finishes.",
          "Open **ChatGPT** from the Start menu.",
          "Sign in with the account from the previous step and choose **Codex**."
        ],
        "doneWhen": "**Done when:** the ChatGPT app is open, you are signed in and you can choose **Codex**.",
        "diagram": ["Download", "Install", "Sign in"]
      }
    },
    "safety": {
      "title": "Read before you start",
      "lead": "Read this once before the assistant sees real documents. It takes about five minutes. It is general information, not legal advice.",
      "warnings": [
        "AI can make mistakes, including in amounts and deadlines. Check everything before you send, sign or pay.",
        "Files the assistant reads are sent to {provider} for processing.",
        "German Business Kit is not a tax adviser or a lawyer."
      ],
      "boxNote": "Please read the following text. Scroll down to see all of it.",
      "license": "German Business Kit is free software under the MIT License. It is provided “as is”, without warranty of any kind.",
      "question": "Do you understand these points? To continue, choose “I have read and understand”.",
      "understand": "I have read and understand",
      "decline": "I do not accept",
      "selfTest": "Test yourself…",
      "risksTitle": "What AI can get wrong",
      "risks": [
        {"title": "Confident mistakes", "text": "It can misread a document, use the wrong year's rules or cite a source that does not exist, and still sound sure."},
        {"title": "Numbers and deadlines", "text": "Amounts, VAT and deadlines can be wrong. Compare them with the original document and an official source."},
        {"title": "Not a tax adviser", "text": "German Business Kit is self-help software, not a Steuerberater or lawyer. Using it creates no adviser–client relationship."},
        {"title": "You decide", "text": "The assistant prepares drafts. Check them before you send, sign, pay or file anything. A neat draft is not proof that anything was submitted."}
      ],
      "flowTitle": "Where your data goes",
      "flow": ["Your files", "AI app", "Provider's servers", "Saved in your account"],
      "flowText": [
        "When the assistant reads a file, its content can be sent to {provider} to be processed. A folder on your computer does not mean the AI works only on your computer.",
        "Tasks, chats and their content can stay saved in your account. Deleting a file on your computer does not delete them.",
        "Connected services, such as cloud storage or email, process data under their own terms."
      ],
      "either": "Anthropic or OpenAI",
      "gdprTitle": "Data protection (GDPR) in plain words",
      "gdpr": [
        "**Your own papers**, such as your receipts or tax letters, are mostly about you. Still check the data settings below before the assistant reads them.",
        "**Other people's data**, for example customers, contact persons or employees, is personal data under the GDPR. Use it only for a clear business purpose and share only what the task needs.",
        "**Personal plans are not business contracts.** Plans such as Claude Pro or ChatGPT Plus do not include a data processing agreement (DPA, Article 28 GDPR). Business plans such as Claude Team or Enterprise and ChatGPT Business or Enterprise offer one. Check this before the assistant processes customers' or employees' data.",
        "**Health information**, such as a sick note, is a special category of data (Article 9 GDPR). Use a made-up example or only the few details the task needs.",
        "**Remove details first.** Black out names, addresses and ID numbers in a copy on your computer before the assistant reads it. Asking the AI to do this is too late: it has already read them.",
        "**If others work for you**, explain these rules to them. The EU AI Act asks businesses that use AI to support their staff's AI literacy (Article 4)."
      ],
      "gdprNote": "This page is not legal advice and not a GDPR compliance certificate.",
      "aiActLink": "European Commission: AI literacy questions and answers",
      "fullLink": "Read the full guidance: AI limits and your data",
      "settingsTitle": "Check your data settings",
      "settingsLead": "Do this once in the app or on the website. Menu names are shown in English and can differ in another app language. This guide cannot see or change your settings.",
      "claude": {
        "name": "Claude",
        "steps": [
          "Open **Settings → Privacy** in the Claude app or on claude.ai.",
          "Find **Help improve our AI models**. While it is on, Anthropic may use your chats and coding sessions to train its models. Decide whether to switch it off.",
          "Do not use the thumbs up/down buttons in chats with real data: feedback sends the whole conversation to Anthropic, where it can be kept for up to five years."
        ],
        "link": "Anthropic: change the model-improvement setting",
        "business": "Using Claude Team or Enterprise? Your organization's commercial terms apply, and by default that content is not used for training."
      },
      "openai": {
        "name": "ChatGPT",
        "steps": [
          "Open **Settings → Data controls** in the ChatGPT app or on chatgpt.com.",
          "Find **Improve the model for everyone**. On Free, Plus and Pro it is on by default, and it also covers your Codex tasks. Decide whether to switch it off.",
          "Switching it off does not delete saved chats. Delete chats with real data that you no longer need."
        ],
        "link": "OpenAI: data controls in ChatGPT",
        "business": "Using ChatGPT Business or Enterprise? Your workspace settings apply, and by default OpenAI does not train on that content."
      },
      "quizTitle": "Quick check: would you share this?",
      "quizLead": "Choose an answer for each card. Nothing is sent anywhere; this is only practice.",
      "quizChoices": {"ok": "Fine to try", "check": "Check first", "never": "Never"},
      "quizRight": "Right.",
      "quizWrong": "Not quite. Better: {answer}.",
      "quizScore": "{answered} of {total} answered, {right} right",
      "quiz": {
        "demo": {"item": "The made-up receipts from this guide's demos", "why": "Fictional data is the safest way to learn how the assistant works."},
        "question": {"item": "A general question: “What is the Kleinunternehmer rule?”", "why": "General questions without personal details are fine. Still check the answer against an official source."},
        "customer": {"item": "An invoice with your customer's name and address", "why": "That is another person's data under the GDPR. Check your plan and settings, and share only what the task needs."},
        "letter": {"item": "A letter from the tax office (Finanzamt) about you", "why": "It contains your tax number and personal details. Check your data settings first and black out what the task does not need."},
        "elster": {"item": "Your ELSTER certificate file and its password", "why": "Logins, certificates, TANs and recovery codes never belong in a chat. Sign in on the official website yourself."},
        "banking": {"item": "Your online-banking login, so the AI can check payments itself", "why": "Never hand over banking access. Download a statement yourself and share only the lines the task needs."}
      },
      "askTitle": "Before your first real document",
      "askLead": "Ask the assistant to explain the data route for your setup:",
      "askLabel": "Question about your data",
      "ask": "Use de-business-kit. Before reading my real documents, explain which data would go to which provider or connected service, what account settings matter, and what I can remove locally. If you cannot verify a setting, say so. Start with a fictional example."
    },
    "skills": {
      "listTitle": "The seven skills you get",
      "list": {
        "de-business-kit": "Starting, continuing, choosing the next task",
        "de-business-start": "Preparing and opening an activity",
        "de-business-operations": "Proposals, invoices and everyday correspondence",
        "de-business-accounting": "Documents and accounting records",
        "de-business-tax": "Tax questions, reports and Finanzamt letters",
        "de-business-services": "Banking, insurance, software and service access",
        "de-business-changes": "Changes, hiring, pausing and closing"
      },
      "once": "Install the kit only once per app. Two copies of the same skills cause duplicates.",
      "stuck": "Something looks different?",
      "stuckLink": "See “If you get stuck” in the installation guide",
      "claude": {
        "title": "Add German Business Kit to Claude",
        "lead": "Ask Claude to install the kit for you. It takes one request.",
        "short": [
          "Open Claude, switch to **Cowork** and start a new task.",
          "Copy this request, paste it into the task and send it:",
          "Follow Claude's answer. When it asks, select **Install** or confirm the action yourself."
        ],
        "steps": [
          "Open the Claude app, switch to **Cowork** and start a new task.",
          "Copy the request below, paste it into the task and send it.",
          "Follow Claude's answer. When it asks you to select **Install** in **Plugins** or to confirm an action, do it yourself: Claude tells you where, but cannot click for you.",
          "Start a **new task** and check that the seven skills below are available: open German Business Kit and its **Skills** tab, or ask Claude which German Business Kit skills it can use."
        ],
        "promptLabel": "Request for Claude",
        "prompt": "Install German Business Kit from https://github.com/ilyafedotov-ops/german-business-skills and show me how to use it. Follow the repository's installation instructions for my app, check that the complete kit is available, and help me try one small example.",
        "manualTitle": "Install manually…",
        "result": {
          "alt": "German Business Kit page in the Claude app after Add: status Added and the kit's skills",
          "caption": "The real Claude app on 21 November 2026. Your version may look different."
        },
        "manualSteps": [
          "In the Claude app, open **Customize** in the sidebar, then **Plugins**. If your version shows a separate **Cowork** selector, switch to Cowork first.",
          "Select **Add**, then **Add marketplace**. If offered, choose **Add from a repository**. Paste the address below and select **Sync**.",
          "Find **German Business Kit** in the list (look under **Discover** if needed) and select **Install**. Some versions say **Add**.",
          "Open German Business Kit and its **Skills** tab. Check that the seven skills below are listed."
        ],
        "addressLabel": "Marketplace address",
        "github": "This is the project's public page on GitHub. You do not need a GitHub account.",
        "review": "Anthropic reviews plugins in its own directory, not plugins added by address. This address installs the project's verified release.",
        "shotAlt": "Claude desktop dialog for adding a marketplace, with the project address entered and the Sync button",
        "shotCaption": "Actual Claude desktop app 3.6556.2 on macOS, captured on 26 October 2026 before selecting Sync. Labels may differ in your version.",
        "diagram": ["Cowork", "Paste request", "Install", "New task"]
      },
      "openai": {
        "title": "Add German Business Kit to Codex",
        "lead": "Ask Codex to install the kit for you. It takes one request.",
        "short": [
          "Create an empty folder called **Business Assistant**, for example in Documents.",
          "In ChatGPT, choose **Codex**, open this folder as a project and start a **New chat**.",
          "Copy this request, paste it into Codex and send it:",
          "Follow Codex's answer. Allow internet access or file changes for this project only."
        ],
        "steps": [
          "Create a new folder called **Business Assistant** in a private place, for example in Documents. It holds only the kit, not your business records.",
          "In the ChatGPT app, choose **Codex**, open the **Business Assistant** folder as your project and start a **New chat**. If asked to trust a folder, confirm only this one.",
          "Copy the request below, paste it into Codex and send it. If Codex asks for internet access or permission to change files, allow it for this project only.",
          "Start a **new chat in the same project**. Open **Skills** in the sidebar and check that the seven skills below are listed. If they are missing, close and reopen the app."
        ],
        "promptLabel": "Request for Codex",
        "prompt": "Install German Business Kit from https://github.com/ilyafedotov-ops/german-business-skills and show me how to use it. Follow the repository's installation instructions for my app, check that the complete kit is available, and help me try one small example.",
        "manualTitle": "Install manually…",
        "result": {
          "alt": "Codex lists the seven German Business Kit skills in a table",
          "caption": "The real ChatGPT app with Codex on 21 November 2026. Your answer will look different."
        },
        "manualSteps": [
          "Download these two files into the same folder, for example Downloads.",
          "Copy the full path of each file. Windows: right-click the file and choose **Copy as path**. Mac: select the file in Finder, hold **Option** and choose **Edit → Copy … as Pathname**.",
          "Copy the request below, paste it into Codex, replace the two parts in square brackets with your paths and send it.",
          "Start a new chat in the same project. Open **Skills** in the sidebar and check that the seven skills below are listed."
        ],
        "zip": "Download {file}",
        "checksums": "Download {file} (checksum list)",
        "releasePage": "Open the release page",
        "manualPromptLabel": "Request with file paths",
        "manualPrompt": "I am setting up German Business Kit in this local Business Assistant project in Codex. My ZIP is at [full ZIP path] and SHA256SUMS is at [full checksum-file path]. Check the ZIP against its checksum and stop if it does not match. Extract it into a new folder, then copy all seven complete skill folders into this project's .agents/skills. Use native file tools, preserve existing files and stop if a destination already exists. Do not install runtimes, change security settings or change global app configuration. Tell me the seven installed names and how to start a fresh session.",
        "checksumNote": "The checksum list lets Codex check that the download is complete and unchanged. It does not prove who published the file.",
        "manual": "Codex could not copy the files? Follow the manual steps in the installation guide.",
        "diagram": ["Project folder", "Paste request", "Allow access", "New chat"]
      }
    },
    "demos": {
      "title": "Try your first tasks with made-up examples",
      "doneTitle": "Setup is complete",
      "doneLead": "German Business Kit is ready. Try a first task with made-up data: pick the example closest to you and paste it into a new task in Claude or a new chat in Codex.",
      "more": "More examples…",
      "result": {
        "claudeAlt": "Claude answers the content-creator example with one small first step",
        "openaiAlt": "Codex answers the programmer example with one small first step",
        "caption": "Real answers on 21 November 2026 to the fictional examples. Your answer will look different."
      },
      "lead": "Each demo uses fictional details only. Copy a request, paste it into a **new task** in Claude or a **new chat in your Business Assistant project** in Codex, then compare the answer with the checklist.",
      "callTitle": "How to call the kit",
      "call": {
        "claude": "In Claude, type **/** or open **+** and select **de-business-kit**, or start your message with **Use de-business-kit**.",
        "openai": "In Codex, start your message with **Use de-business-kit** or **$de-business-kit**."
      },
      "privacy": "Start with made-up data. Before using real documents, read which content is sent to the AI service.",
      "open": "Open demo",
      "tried": "Tried",
      "back": "All demos",
      "markTried": "I tried this demo",
      "prepareTitle": "Before you start",
      "promptTitle": "Paste this request",
      "answersTitle": "If the assistant asks",
      "checkTitle": "Check the answer",
      "checkNote": "A useful answer can look different. These points help you judge it.",
      "nextTitle": "Try a follow-up",
      "promptLabel": "Request to paste",
      "answersLabel": "Fictional answers",
      "nextLabel": "Follow-up request",
      "prototype": "Want to see an example workspace first?",
      "prototypeLink": "Open the interactive demo with fictional data (English only)",
      "finishTitle": "You are ready",
      "finish": "Next time, describe the result you want in normal words: understand a letter, prepare a form, organize documents or plan a change. Keep using made-up data until you are comfortable.",
      "guideLink": "Open the user guide",
      "items": {
        "first": {
          "title": "First step: freelance programmer",
          "summary": "Ask for one small next step for a fictional freelance programmer.",
          "time": "About 5 minutes",
          "prepare": ["Start a **new task** in Claude or a **new chat** in your Business Assistant project in Codex. No folder is needed."],
          "prompt": "Use de-business-kit. I am trying the assistant with a fictional example: I am a programmer and want to start freelancing in Germany, building websites and apps for small companies. I do not know where to begin. Help me choose one small first step. Ask only what you need for that step.",
          "answers": "This is a fictional example. I live in Berlin, I have not registered anything yet and I expect my first client next month.",
          "check": [
            "One understandable next step, not a long lecture.",
            "Questions only where a fact is really needed.",
            "No request to upload private documents or choose accounting software yet.",
            "No claim that anything was registered or filed."
          ],
          "next": "Explain this in plain language and give me only the next step."
        },
        "creator": {
          "title": "First step: content creator",
          "summary": "Ask for one small next step for a fictional Instagram and YouTube creator.",
          "time": "About 5 minutes",
          "prepare": ["Start a **new task** in Claude or a **new chat** in your Business Assistant project in Codex. No folder is needed."],
          "prompt": "Use de-business-kit. I am trying the assistant with a fictional example: I make videos for Instagram and YouTube, and the first brands want to pay me for posts. I live in Germany and have not registered anything yet. Help me choose one small first step. Ask only what you need for that step.",
          "answers": "This is a fictional example. I live in Munich, I am a student, and a brand has offered me EUR 300 and a free product for one video next month.",
          "check": [
            "One understandable next step, not a long lecture.",
            "Questions only where a fact is really needed.",
            "The brand's free product is treated as something to clarify, not ignored.",
            "No claim that anything was registered or filed."
          ],
          "next": "Explain this in plain language and give me only the next step."
        },
        "records": {
          "title": "First month's records",
          "summary": "Organize three fictional receipts in a separate practice folder.",
          "time": "About 10 minutes",
          "prepare": [
            "Create a new, empty folder called **Practice business**. Keep it outside the Business Assistant folder.",
            "Claude: start a new task in Cowork and select this folder. Codex: keep your Business Assistant project open and allow access to the practice folder when asked."
          ],
          "prompt": "Use de-business-accounting. This is a fictional practice exercise. Use only my selected folder Practice business. Create three made-up receipts from November 2026 for a freelance programmer: a USB-C cable EUR 19.90, a train ticket to a client EUR 49.00 and a cloud hosting subscription EUR 11.90. Organize them for my first month, show what is still unclear and save a short readable summary with the next step. Do not use real data or connect any service.",
          "answers": "This is practice. In this example I am a Kleinunternehmer and have not chosen accounting software. Keep anything uncertain as an open question.",
          "check": [
            "New files and a summary appear only in the practice folder.",
            "Amounts and dates match the example.",
            "Unclear points, such as private use or VAT, stay open questions instead of guesses.",
            "Nothing is sent, connected or submitted."
          ],
          "next": "Use de-business-kit. Read the saved summary in my practice folder and show me the next action."
        },
        "invoice": {
          "title": "Prepare an invoice",
          "summary": "Draft an invoice for a fictional customer without sending it.",
          "time": "About 10 minutes",
          "prepare": ["Use the same **Practice business** folder, or start without a folder."],
          "prompt": "Use de-business-operations. Fictional example: prepare a draft invoice for programming work I delivered. Customer: Beispiel Shop GmbH (fictional). Service: building a contact form for the customer's website, 8 hours at EUR 50, delivered on 3 November 2026. Agreed price: EUR 400. In this example I am a Kleinunternehmer. Use clearly marked placeholders for my address, tax number and bank details. Do not send anything.",
          "answers": "This is practice. Keep clearly marked placeholders instead of real personal details.",
          "check": [
            "A readable draft with customer, service, delivery date and amount.",
            "If VAT is mentioned, it explains why none is charged in this Kleinunternehmer example.",
            "Placeholders instead of real addresses, tax or bank numbers.",
            "It says the draft is neither issued nor sent."
          ],
          "next": "Show me what is still missing before an invoice like this could go to a real customer."
        },
        "continue": {
          "title": "Continue next time",
          "summary": "Come back later and pick up where you stopped.",
          "time": "About 5 minutes",
          "prepare": [
            "Try **First month's records** first.",
            "Start a new task in Claude or a new chat in the same Codex project, with the same practice folder."
          ],
          "prompt": "Use de-business-kit. Read the saved facts and progress in my Practice business folder, then show what is done, what is still open and the next action.",
          "answers": "Use the folder Practice business. Everything in it is made up.",
          "check": [
            "It reads the saved summary instead of asking everything again.",
            "Done and open items are listed separately.",
            "It suggests one next action."
          ],
          "next": "Save a short continuation note with the next step and link the file."
        }
      }
    }
  },
  "ru": {
    "meta": {"language": "Русский", "title": "Установка German Business Kit", "locale": "ru-RU"},
    "ui": {
      "skip": "Перейти к содержимому",
      "brand": "German Business Kit",
      "brandSub": "Пошаговая установка",
      "languageLabel": "Язык",
      "progressLabel": "Шаги установки",
      "stepOf": "Шаг {current} из {total}",
      "back": "Назад",
      "next": "Далее",
      "more": "Подробнее…",
      "preview": "Как это выглядит…",
      "ok": "OK",
      "toContinue": "Чтобы продолжить, нажмите «Далее».",
      "whenDone": "Когда закончите, нажмите «Далее».",
      "start": "Начать установку",
      "copy": "Копировать",
      "copied": "Скопировано. Вставьте с помощью Ctrl+V (Windows) или Cmd+V (Mac).",
      "copyFailed": "Не удалось скопировать автоматически. Выделите текст и нажмите Ctrl+C (Windows) или Cmd+C (Mac).",
      "newTab": "откроется в новой вкладке",
      "done": "выполнено",
      "saved": "Ваш прогресс сохраняется только в этом браузере на этом компьютере.",
      "notSaved": "Этот браузер не разрешает сохранять прогресс. Не закрывайте страницу до конца установки.",
      "checked": "Сведения о сервисах проверены {date}; тарифы, цены и меню могут меняться, решающей остаётся страница самого сервиса.",
      "safety": "Эта инструкция никогда не спрашивает пароли, платёжные данные, коды подтверждения или ключи. Вводите их только на сайте или в приложении самого сервиса.",
      "illustration": "Схема. Настоящие экраны могут выглядеть иначе.",
      "chooseFirst": "Сначала выберите ассистента.",
      "acceptFirst": "Сначала прочтите текст и выберите «Я прочитал(а) и понимаю».",
      "mobile": "Установка выполняется на компьютере. Откройте эту страницу на Windows или Mac.",
      "progressSummary": "Выполнено шагов: {done} из {total}",
      "enlarge": "Увеличить снимок экрана",
      "zoom": "Приблизить",
      "close": "Закрыть",
      "footer": "German Business Kit — программа для самостоятельной работы с помощью AI, а не налоговая или юридическая консультация. Эта страница ничего не отправляет; ссылки открывают официальные сайты, только когда вы их выбираете."
    },
    "steps": {"welcome": "Начало", "assistant": "Ассистент", "account": "Аккаунт", "app": "Приложение", "safety": "Данные и риски", "skills": "Скиллы", "demos": "Первые задачи"},
    "welcome": {
      "eyebrow": "Пошаговая установка · около 30 минут",
      "title": "Вас приветствует мастер установки German Business Kit",
      "lead": "Мастер поможет подготовить AI-ассистента для бизнеса: аккаунт, приложение и German Business Kit. Навыки программирования не нужны.",
      "needTitle": "Что понадобится",
      "need": [
        "Компьютер с Windows или Mac и доступом в интернет",
        "Адрес почты, который можно открыть сейчас",
        "Мобильный телефон, принимающий SMS",
        "Банковская карта для платного тарифа: Claude Pro или ChatGPT Plus"
      ],
      "aiTitle": "Важно знать до начала",
      "aiShort": "German Business Kit — не налоговый консультант, а AI может ошибаться.",
      "ai": "German Business Kit — программа для самостоятельной работы с помощью AI, а не налоговый консультант (Steuerberater). AI может ошибаться, в том числе в суммах и сроках. Файлы, которые читает ассистент, обрабатываются Anthropic или OpenAI. Используйте вымышленные примеры, пока не прочитаете рекомендации о данных.",
      "aiLink": "Ограничения AI и ваши данные"
    },
    "assistant": {
      "title": "Выберите ассистента",
      "business": "Будете работать с данными клиентов или сотрудников? Личные тарифы, например Claude Pro или ChatGPT Plus, не включают договор об обработке данных для бизнеса (DPA); его предлагают бизнес-тарифы, например Claude Team или ChatGPT Business. Подробнее — на шаге «{name}».",
      "lead": "Выберите приложение, в котором будет работать German Business Kit. Второе можно настроить позже.",
      "choose": "Выбрать {name}",
      "chosen": "Выбрано",
      "unsure": "Сомневаетесь? Выберите **Claude**: у него меньше всего шагов установки.",
      "work": "Аккаунт от работодателя или учебного заведения? Администратор может запретить приложения, плагины или скиллы. Сначала спросите у него.",
      "claude": {
        "name": "Claude",
        "maker": "от Anthropic",
        "app": "Приложение Claude для компьютера с Cowork",
        "summary": "Меньше всего шагов установки. Нужен тариф **Pro** или выше.",
        "pricing": "Тарифы и цены Claude",
        "points": [
          "Самая простая установка: набор добавляется в приложении в несколько кликов.",
          "Нужен платный тариф: **Pro** или выше (Pro, Max, Ultra, Team или Enterprise). Бесплатный тариф не включает Cowork.",
          "Работает с файлами в папке, которую вы выберете."
        ]
      },
      "openai": {
        "name": "ChatGPT с Codex",
        "maker": "от OpenAI",
        "app": "Приложение ChatGPT для компьютера с Codex",
        "summary": "Чуть больше шагов установки. Рекомендуем тариф **Plus** или выше.",
        "pricing": "Тарифы и цены ChatGPT",
        "points": [
          "Рекомендуем платный тариф: **Plus** или выше (Plus, Pro, Business или Enterprise). У Free и Go низкие лимиты.",
          "Больше шагов при установке: вы скачиваете файл, а Codex копирует набор в папку проекта.",
          "Работает с файлами в папке проекта на вашем компьютере."
        ]
      }
    },
    "account": {
      "lead": "Регистрация проходит на сайте самого сервиса. Эта инструкция только открывает официальную страницу в новой вкладке.",
      "labelsNote": "Названия кнопок могут отличаться в зависимости от языка или версии приложения.",
      "already": "Аккаунт уже есть? Просто нажмите «Далее».",
      "safetyTitle": "Безопасность аккаунта",
      "safety": [
        "Вводите пароли, коды и данные карты только на странице самого сервиса или в его приложении.",
        "Никто из этого проекта не будет спрашивать ваши коды или пароли.",
        "Проверяйте адресную строку: **claude.ai** или **claude.com** для Claude, **chatgpt.com** или **openai.com** для ChatGPT."
      ],
      "claude": {
        "title": "Создайте аккаунт Claude",
        "open": "Открыть официальную страницу регистрации Claude",
        "short": [
          "Зарегистрируйтесь через Google или по адресу почты.",
          "Подтвердите номер мобильного телефона кодом из SMS.",
          "Выберите тариф **Pro** или выше и оплатите его на сайте Claude."
        ],
        "steps": [
          "На официальной странице выберите **Continue with Google** или введите адрес почты и выберите **Continue with email**.",
          "Если вы выбрали почту, откройте письмо от Claude и нажмите ссылку для входа. Claude не использует пароль.",
          "Введите номер мобильного телефона, который принимает SMS, и наберите 6-значный код из сообщения. Интернет-номера и стационарные номера не подходят.",
          "Выберите тариф. Для German Business Kit нужен **Pro** или выше. Оплачивайте только на сайте Claude."
        ],
        "diagram": ["Открыть страницу", "Подтвердить почту", "Проверить телефон", "Выбрать тариф"]
      },
      "openai": {
        "title": "Создайте аккаунт ChatGPT",
        "open": "Открыть официальную страницу регистрации ChatGPT",
        "short": [
          "Выберите **Sign up** и зарегистрируйтесь по почте или другим предложенным способом.",
          "Подтвердите адрес почты.",
          "Выберите тариф **Plus** или выше и оплатите его на сайте OpenAI."
        ],
        "steps": [
          "На официальной странице выберите **Sign up** (**Зарегистрироваться**). Используйте адрес почты или один из вариантов входа, которые предлагает страница.",
          "Следуйте шагам на странице, чтобы подтвердить адрес почты.",
          "При первом запуске Codex приложение может попросить добавить или подтвердить номер телефона. Делайте это только в приложении ChatGPT или на chatgpt.com.",
          "Выберите тариф: **Plus** или выше. Оплачивайте только на сайте OpenAI."
        ],
        "diagram": ["Открыть страницу", "Подтвердить почту", "Проверить телефон", "Выбрать тариф"]
      }
    },
    "app": {
      "osTitle": "Ваш компьютер",
      "detected": "Похоже, это компьютер с {os}.",
      "unknown": "Не удалось определить ваш компьютер. Выберите его ниже.",
      "windows": "Windows",
      "mac": "Mac",
      "other": "Linux или другая система? Используйте официальную страницу загрузки; эта инструкция описывает Windows и Mac.",
      "official": "Открыть официальную страницу загрузки",
      "blocked": "Рабочий компьютер не даёт установить приложение? Обратитесь в IT-отдел. Никогда не отключайте защиту ради установки приложения.",
      "stepsTitle": "Установите и войдите",
      "claude": {
        "title": "Установите приложение Claude",
        "download": {
          "mac": "Скачать Claude для Mac",
          "windows": "Скачать Claude для Windows",
          "windowsArm": "Windows на ARM, например ноутбук со Snapdragon? Скачайте эту версию."
        },
        "short": [
          "Скачайте и установите приложение кнопкой выше.",
          "Откройте Claude и войдите в аккаунт.",
          "В **Settings → Privacy** выключите **Help improve our AI models**, если не хотите, чтобы ваши разговоры использовались для обучения AI."
        ],
        "mac": [
          "Скачайте файл кнопкой выше. Он сохранится в папке **Загрузки** (Downloads).",
          "Откройте скачанный файл. В появившемся окне перетащите значок Claude в папку **Программы** (Applications).",
          "Откройте Claude из папки **Программы**. Если Mac спросит, открыть ли приложение из интернета, подтверждайте, только если это Claude, скачанный по официальной ссылке выше.",
          "Войдите с аккаунтом из предыдущего шага."
        ],
        "windows": [
          "Скачайте файл кнопкой выше. Он сохранится в папке **Загрузки**.",
          "Откройте скачанный файл. Если Windows запросит разрешение, проверьте, что издатель — Anthropic, и разрешите.",
          "Дождитесь окончания установки. Claude откроется сам; иначе найдите **Claude** в меню «Пуск».",
          "Войдите с аккаунтом из предыдущего шага."
        ],
        "doneWhen": "**Готово, когда:** приложение Claude открыто и вы вошли в аккаунт.",
        "diagram": ["Скачать", "Установить", "Войти"]
      },
      "openai": {
        "title": "Установите приложение ChatGPT",
        "download": {
          "macArm": "Скачать ChatGPT для Mac с чипом Apple (M1 или новее)",
          "macIntel": "Скачать ChatGPT для Mac с процессором Intel",
          "windows": "Установить ChatGPT для Windows из Microsoft Store"
        },
        "short": [
          "Скачайте и установите приложение кнопкой выше.",
          "Откройте ChatGPT, войдите в аккаунт и выберите **Codex**.",
          "В **Settings → Data controls** выключите **Improve the model for everyone**, если не хотите, чтобы ваши разговоры использовались для обучения AI."
        ],
        "macWhich": "Какой у меня Mac? Откройте меню Apple и выберите **Об этом Mac**. **Чип: Apple M…** означает чип Apple; **Процессор: Intel** означает Intel.",
        "mac": [
          "Скачайте файл для вашего Mac одной из кнопок выше. Он сохранится в папке **Загрузки**.",
          "Откройте скачанный файл. В появившемся окне перетащите значок приложения (ChatGPT или Codex) в папку **Программы**.",
          "Откройте приложение из папки **Программы**. Если Mac спросит, открыть ли приложение из интернета, подтверждайте, только если это ChatGPT, скачанный по официальной ссылке выше.",
          "Войдите с аккаунтом из предыдущего шага и выберите **Codex**."
        ],
        "windows": [
          "Нажмите кнопку выше и откройте скачанный установщик.",
          "Следуйте шагам в окне Microsoft Store и дождитесь окончания установки.",
          "Откройте **ChatGPT** из меню «Пуск».",
          "Войдите с аккаунтом из предыдущего шага и выберите **Codex**."
        ],
        "doneWhen": "**Готово, когда:** приложение ChatGPT открыто, вы вошли в аккаунт и можете выбрать **Codex**.",
        "diagram": ["Скачать", "Установить", "Войти"]
      }
    },
    "safety": {
      "title": "Прочтите перед началом работы",
      "lead": "Прочитайте это один раз, прежде чем ассистент увидит настоящие документы. Это займёт около пяти минут. Здесь общая информация, а не юридическая консультация.",
      "warnings": [
        "AI может ошибаться, в том числе в суммах и сроках. Проверяйте всё, прежде чем отправить, подписать или оплатить.",
        "Файлы, которые читает ассистент, отправляются для обработки в {provider}.",
        "German Business Kit — не налоговый консультант и не юрист."
      ],
      "boxNote": "Прочтите текст ниже. Прокрутите его, чтобы увидеть полностью.",
      "license": "German Business Kit — свободная программа по лицензии MIT. Она предоставляется «как есть», без каких-либо гарантий.",
      "question": "Вам понятны эти пункты? Чтобы продолжить, выберите «Я прочитал(а) и понимаю».",
      "understand": "Я прочитал(а) и понимаю",
      "decline": "Не принимаю",
      "selfTest": "Проверить себя…",
      "risksTitle": "В чём AI может ошибиться",
      "risks": [
        {"title": "Уверенные ошибки", "text": "AI может неверно прочитать документ, применить правила не того года или сослаться на несуществующий источник — и при этом звучать уверенно."},
        {"title": "Суммы и сроки", "text": "Суммы, НДС и сроки могут быть неверными. Сверяйте их с оригиналом документа и официальным источником."},
        {"title": "Не налоговый консультант", "text": "German Business Kit — программа для самостоятельной работы, а не Steuerberater или юрист. Её использование не создаёт отношений консультанта и клиента."},
        {"title": "Решаете вы", "text": "Ассистент готовит черновики. Проверяйте их, прежде чем что-либо отправить, подписать, оплатить или подать. Аккуратный черновик не доказывает, что что-то подано."}
      ],
      "flowTitle": "Куда попадают ваши данные",
      "flow": ["Ваши файлы", "AI-приложение", "Серверы сервиса", "Сохранено в аккаунте"],
      "flowText": [
        "Когда ассистент читает файл, его содержимое может отправляться в {provider} для обработки. Папка на вашем компьютере не означает, что AI работает только на вашем компьютере.",
        "Задачи, разговоры и их содержимое могут оставаться сохранёнными в вашем аккаунте. Удаление файла на компьютере их не удаляет.",
        "Подключённые сервисы, например облачное хранилище или почта, обрабатывают данные по своим условиям."
      ],
      "either": "Anthropic или OpenAI",
      "gdprTitle": "Защита данных (GDPR) простыми словами",
      "gdpr": [
        "**Ваши собственные бумаги**, например ваши чеки или налоговые письма, касаются в основном вас. Всё равно проверьте настройки данных ниже, прежде чем ассистент их прочитает.",
        "**Данные других людей**, например клиентов, контактных лиц или сотрудников, — это персональные данные по GDPR. Используйте их только для понятной деловой цели и передавайте только то, что нужно для задачи.",
        "**Личный тариф — не договор для бизнеса.** Тарифы вроде Claude Pro или ChatGPT Plus не включают договор об обработке данных (DPA, статья 28 GDPR). Бизнес-тарифы, например Claude Team или Enterprise и ChatGPT Business или Enterprise, его предлагают. Проверьте это, прежде чем ассистент будет обрабатывать данные клиентов или сотрудников.",
        "**Сведения о здоровье**, например больничный лист, — особая категория данных (статья 9 GDPR). Используйте вымышленный пример или только те немногие сведения, которые нужны для задачи.",
        "**Сначала уберите лишнее.** Закройте имена, адреса и идентификационные номера в копии на своём компьютере, прежде чем ассистент её прочитает. Просить об этом AI уже поздно: он их уже прочитал.",
        "**Если на вас работают другие люди**, объясните им эти правила. Закон ЕС об AI (AI Act) требует от компаний, использующих AI, поддерживать грамотность сотрудников в области AI (статья 4)."
      ],
      "gdprNote": "Эта страница — не юридическая консультация и не сертификат соответствия GDPR.",
      "aiActLink": "Европейская комиссия: вопросы и ответы о грамотности в области AI (на английском)",
      "fullLink": "Полные рекомендации: ограничения AI и ваши данные",
      "settingsTitle": "Проверьте настройки данных",
      "settingsLead": "Сделайте это один раз в приложении или на сайте. Названия меню даны на английском; на другом языке приложения они могут отличаться. Эта инструкция не видит и не меняет ваши настройки.",
      "claude": {
        "name": "Claude",
        "steps": [
          "Откройте **Settings → Privacy** в приложении Claude или на claude.ai.",
          "Найдите **Help improve our AI models**. Пока переключатель включён, Anthropic может использовать ваши разговоры и сессии программирования для обучения моделей. Решите, выключить ли его.",
          "Не нажимайте «палец вверх/вниз» в разговорах с настоящими данными: отзыв отправляет в Anthropic весь разговор, и там он может храниться до пяти лет."
        ],
        "link": "Anthropic: как изменить настройку улучшения моделей (на английском)",
        "business": "Используете Claude Team или Enterprise? Действуют коммерческие условия вашей организации, и по умолчанию это содержимое не используется для обучения."
      },
      "openai": {
        "name": "ChatGPT",
        "steps": [
          "Откройте **Settings → Data controls** в приложении ChatGPT или на chatgpt.com.",
          "Найдите **Improve the model for everyone**. На тарифах Free, Plus и Pro он включён по умолчанию и распространяется на ваши задачи в Codex. Решите, выключить ли его.",
          "Выключение не удаляет сохранённые разговоры. Удалите разговоры с настоящими данными, которые вам больше не нужны."
        ],
        "link": "OpenAI: управление данными в ChatGPT (на английском)",
        "business": "Используете ChatGPT Business или Enterprise? Действуют настройки вашего рабочего пространства, и по умолчанию OpenAI не обучает модели на этом содержимом."
      },
      "quizTitle": "Быстрая проверка: вы бы этим поделились?",
      "quizLead": "Выберите ответ для каждой карточки. Ничего никуда не отправляется — это только тренировка.",
      "quizChoices": {"ok": "Можно пробовать", "check": "Сначала проверить", "never": "Никогда"},
      "quizRight": "Верно.",
      "quizWrong": "Не совсем. Лучше: {answer}.",
      "quizScore": "Отвечено: {answered} из {total}, верно: {right}",
      "quiz": {
        "demo": {"item": "Вымышленные чеки из примеров этой инструкции", "why": "Вымышленные данные — самый безопасный способ понять, как работает ассистент."},
        "question": {"item": "Общий вопрос: «Что такое правило Kleinunternehmer?»", "why": "Общие вопросы без личных данных — это нормально. Всё равно сверяйте ответ с официальным источником."},
        "customer": {"item": "Счёт с именем и адресом вашего клиента", "why": "Это данные другого человека по GDPR. Проверьте тариф и настройки и передавайте только то, что нужно для задачи."},
        "letter": {"item": "Письмо из налоговой (Finanzamt) о вас", "why": "В нём ваш налоговый номер и личные сведения. Сначала проверьте настройки данных и закройте то, что не нужно для задачи."},
        "elster": {"item": "Файл сертификата ELSTER и его пароль", "why": "Логины, сертификаты, TAN и коды восстановления никогда не должны попадать в разговор. Входите на официальный сайт сами."},
        "banking": {"item": "Логин от онлайн-банка, чтобы AI сам проверил платежи", "why": "Никогда не передавайте доступ к банку. Скачайте выписку сами и передайте только нужные для задачи строки."}
      },
      "askTitle": "Перед первым настоящим документом",
      "askLead": "Попросите ассистента объяснить путь данных для вашей настройки:",
      "askLabel": "Вопрос о ваших данных",
      "ask": "Используй de-business-kit. Перед чтением настоящих документов объясни, какие данные получит какой провайдер или подключённый сервис, какие настройки аккаунта важны и что можно удалить локально. Если настройку нельзя проверить, скажи об этом. Начни с вымышленного примера."
    },
    "skills": {
      "listTitle": "Семь скиллов, которые вы получите",
      "list": {
        "de-business-kit": "Начать, продолжить, выбрать следующую задачу",
        "de-business-start": "Подготовить и открыть деятельность",
        "de-business-operations": "Предложения, счета и текущая переписка",
        "de-business-accounting": "Документы и учётные записи",
        "de-business-tax": "Налоговые вопросы, отчётность и письма Finanzamt",
        "de-business-services": "Банки, страхование, программы и доступ к сервисам",
        "de-business-changes": "Изменения, найм, приостановка и закрытие"
      },
      "once": "Устанавливайте набор только один раз в каждом приложении. Две копии одних и тех же скиллов приводят к дублям.",
      "stuck": "Что-то выглядит иначе?",
      "stuckLink": "Раздел «Если что-то не получается» в инструкции по установке",
      "claude": {
        "title": "Добавьте German Business Kit в Claude",
        "lead": "Попросите Claude установить набор за вас. Для этого нужен один запрос.",
        "short": [
          "Откройте Claude, перейдите в **Cowork** и начните новую задачу.",
          "Скопируйте этот запрос, вставьте его в задачу и отправьте:",
          "Следуйте ответу Claude. Когда он попросит, нажмите **Install** или подтвердите действие сами."
        ],
        "steps": [
          "Откройте приложение Claude, перейдите в **Cowork** и начните новую задачу.",
          "Скопируйте запрос ниже, вставьте его в задачу и отправьте.",
          "Следуйте ответу Claude. Когда он попросит выбрать **Install** в разделе **Plugins** или подтвердить действие, сделайте это сами: Claude подскажет, где это, но нажать за вас не может.",
          "Начните **новую задачу** и проверьте, что доступны семь скиллов из списка ниже: откройте German Business Kit и вкладку **Skills** или спросите Claude, какие скиллы German Business Kit ему доступны."
        ],
        "promptLabel": "Запрос для Claude",
        "prompt": "Установи German Business Kit из https://github.com/ilyafedotov-ops/german-business-skills и покажи, как им пользоваться. Следуй инструкции репозитория для моего приложения, проверь доступность полного набора и помоги попробовать один небольшой пример.",
        "manualTitle": "Установить вручную…",
        "result": {
          "alt": "Страница German Business Kit в приложении Claude после нажатия Add: статус Added и скиллы набора",
          "caption": "Настоящее приложение Claude, 21 ноября 2026 года. В вашей версии всё может выглядеть иначе."
        },
        "manualSteps": [
          "В приложении Claude откройте **Customize** на боковой панели, затем **Plugins**. Если в вашей версии есть отдельный переключатель **Cowork**, сначала перейдите в Cowork.",
          "Выберите **Add**, затем **Add marketplace**. Если предложено, выберите **Add from a repository**. Вставьте адрес ниже и выберите **Sync**.",
          "Найдите **German Business Kit** в списке (при необходимости в разделе **Discover**) и выберите **Install**. В некоторых версиях кнопка называется **Add**.",
          "Откройте German Business Kit и вкладку **Skills**. Проверьте, что там семь скиллов из списка ниже."
        ],
        "addressLabel": "Адрес маркетплейса",
        "github": "Это публичная страница проекта на GitHub. Аккаунт GitHub не нужен.",
        "review": "Anthropic проверяет плагины из своего каталога, но не плагины, добавленные по адресу. Этот адрес устанавливает проверенный выпуск проекта.",
        "shotAlt": "Окно Claude для добавления маркетплейса с введённым адресом проекта и кнопкой Sync",
        "shotCaption": "Настоящее приложение Claude 3.6556.2 на macOS, снимок от 26 октября 2026 года до нажатия Sync. В вашей версии названия могут отличаться.",
        "diagram": ["Cowork", "Вставить запрос", "Install", "Новая задача"]
      },
      "openai": {
        "title": "Добавьте German Business Kit в Codex",
        "lead": "Попросите Codex установить набор за вас. Для этого нужен один запрос.",
        "short": [
          "Создайте пустую папку **Business Assistant**, например в «Документах».",
          "В ChatGPT выберите **Codex**, откройте эту папку как проект и начните **New chat**.",
          "Скопируйте этот запрос, вставьте его в Codex и отправьте:",
          "Следуйте ответу Codex. Разрешайте доступ в интернет и изменение файлов только для этого проекта."
        ],
        "steps": [
          "Создайте новую папку **Business Assistant** в приватном месте, например в «Документах». В ней будет только набор, а не ваши деловые записи.",
          "В приложении ChatGPT выберите **Codex**, откройте папку **Business Assistant** как проект и начните **New chat** (новый разговор). Если приложение спросит, доверять ли папке, подтвердите только эту.",
          "Скопируйте запрос ниже, вставьте его в Codex и отправьте. Если Codex попросит доступ в интернет или разрешение изменить файлы, разрешите это только для этого проекта.",
          "Начните **новый разговор в том же проекте**. Откройте **Skills** на боковой панели и проверьте, что там семь скиллов из списка ниже. Если их нет, закройте и снова откройте приложение."
        ],
        "promptLabel": "Запрос для Codex",
        "prompt": "Установи German Business Kit из https://github.com/ilyafedotov-ops/german-business-skills и покажи, как им пользоваться. Следуй инструкции репозитория для моего приложения, проверь доступность полного набора и помоги попробовать один небольшой пример.",
        "manualTitle": "Установить вручную…",
        "result": {
          "alt": "Codex показывает семь скиллов German Business Kit в таблице",
          "caption": "Настоящее приложение ChatGPT с Codex, 21 ноября 2026 года. Ваш ответ будет выглядеть иначе."
        },
        "manualSteps": [
          "Скачайте эти два файла в одну папку, например в «Загрузки».",
          "Скопируйте полный путь к каждому файлу. Windows: щёлкните файл правой кнопкой и выберите **Копировать как путь**. Mac: выберите файл в Finder, удерживайте **Option** и выберите **Правка → Скопировать … как путь**.",
          "Скопируйте запрос ниже, вставьте его в Codex, замените две части в квадратных скобках своими путями и отправьте.",
          "Начните новый разговор в том же проекте. Откройте **Skills** на боковой панели и проверьте, что там семь скиллов из списка ниже."
        ],
        "zip": "Скачать {file}",
        "checksums": "Скачать {file} (контрольные суммы)",
        "releasePage": "Открыть страницу выпуска",
        "manualPromptLabel": "Запрос с путями к файлам",
        "manualPrompt": "Я устанавливаю German Business Kit в этот локальный проект Business Assistant в Codex. ZIP находится по пути [полный путь к ZIP], а SHA256SUMS — по пути [полный путь к файлу контрольных сумм]. Проверь ZIP по контрольной сумме и остановись, если она не совпадает. Распакуй архив в новую папку, затем скопируй все семь полных папок скиллов в .agents/skills этого проекта. Используй обычные файловые инструменты, сохраняй существующие файлы и остановись, если папка назначения уже существует. Не устанавливай среды выполнения, не меняй настройки безопасности и глобальную конфигурацию приложения. Назови семь установленных скиллов и объясни, как начать новый разговор.",
        "checksumNote": "Файл контрольных сумм позволяет Codex проверить, что загрузка полная и не изменена. Он не доказывает, кто опубликовал файл.",
        "manual": "Codex не смог скопировать файлы? Выполните ручные шаги из инструкции по установке.",
        "diagram": ["Папка проекта", "Вставить запрос", "Разрешить доступ", "Новый разговор"]
      }
    },
    "demos": {
      "title": "Попробуйте первые задачи на вымышленных примерах",
      "doneTitle": "Установка завершена",
      "doneLead": "German Business Kit готов к работе. Попробуйте первую задачу на вымышленных данных: выберите пример, который ближе вам, и вставьте его в новую задачу Claude или в новый разговор Codex.",
      "more": "Ещё примеры…",
      "result": {
        "claudeAlt": "Claude отвечает на пример контент-креатора одним небольшим первым шагом",
        "openaiAlt": "Codex отвечает на пример программиста одним небольшим первым шагом",
        "caption": "Настоящие ответы от 21 ноября 2026 года на вымышленные примеры. Ваш ответ будет выглядеть иначе."
      },
      "lead": "В каждом примере только вымышленные данные. Скопируйте запрос, вставьте его в **новую задачу** в Claude или в **новый разговор в проекте Business Assistant** в Codex и сравните ответ со списком проверки.",
      "callTitle": "Как вызвать набор",
      "call": {
        "claude": "В Claude введите **/** или откройте **+** и выберите **de-business-kit**, либо начните сообщение со слов **Используй de-business-kit**.",
        "openai": "В Codex начните сообщение со слов **Используй de-business-kit** или **$de-business-kit**."
      },
      "privacy": "Начните с вымышленных данных. Прежде чем использовать настоящие документы, прочитайте, какое содержимое отправляется в AI-сервис.",
      "open": "Открыть пример",
      "tried": "Опробовано",
      "back": "Все примеры",
      "markTried": "Я попробовал(а) этот пример",
      "prepareTitle": "Перед началом",
      "promptTitle": "Вставьте этот запрос",
      "answersTitle": "Если ассистент спросит",
      "checkTitle": "Проверьте ответ",
      "checkNote": "Полезный ответ может выглядеть иначе. Эти пункты помогают его оценить.",
      "nextTitle": "Попробуйте продолжение",
      "promptLabel": "Запрос для вставки",
      "answersLabel": "Вымышленные ответы",
      "nextLabel": "Следующий запрос",
      "prototype": "Хотите сначала посмотреть пример рабочей папки?",
      "prototypeLink": "Открыть интерактивную демонстрацию с вымышленными данными (только на английском)",
      "finishTitle": "Всё готово",
      "finish": "В следующий раз опишите нужный результат обычными словами: понять письмо, подготовить форму, разобрать документы или спланировать изменение. Пока не освоитесь, используйте вымышленные данные.",
      "guideLink": "Открыть руководство пользователя",
      "items": {
        "first": {
          "title": "Первый шаг: программист-фрилансер",
          "summary": "Попросите один небольшой следующий шаг для вымышленного программиста-фрилансера.",
          "time": "Около 5 минут",
          "prepare": ["Начните **новую задачу** в Claude или **новый разговор** в проекте Business Assistant в Codex. Папка не нужна."],
          "prompt": "Используй de-business-kit. Я пробую ассистента на вымышленном примере: я программист и хочу начать работать фрилансером в Германии — делать сайты и приложения для небольших компаний. Не знаю, с чего начать. Помоги выбрать один небольшой первый шаг. Спрашивай только то, что нужно для этого шага.",
          "answers": "Это вымышленный пример. Я живу в Берлине, ещё ничего не регистрировал(а) и жду первого клиента в следующем месяце.",
          "check": [
            "Один понятный следующий шаг, а не длинная лекция.",
            "Вопросы только там, где действительно нужен факт.",
            "Пока нет просьбы загрузить личные документы или выбрать бухгалтерскую программу.",
            "Нет утверждений, что что-то уже зарегистрировано или подано."
          ],
          "next": "Объясни это простыми словами и назови только следующий шаг."
        },
        "creator": {
          "title": "Первый шаг: контент-креатор",
          "summary": "Попросите один небольшой следующий шаг для вымышленного автора в Instagram и YouTube.",
          "time": "Около 5 минут",
          "prepare": ["Начните **новую задачу** в Claude или **новый разговор** в проекте Business Assistant в Codex. Папка не нужна."],
          "prompt": "Используй de-business-kit. Я пробую ассистента на вымышленном примере: я снимаю видео для Instagram и YouTube, и первые бренды хотят платить мне за публикации. Я живу в Германии и ещё ничего не регистрировал(а). Помоги выбрать один небольшой первый шаг. Спрашивай только то, что нужно для этого шага.",
          "answers": "Это вымышленный пример. Я живу в Мюнхене, я студент(ка), и бренд предложил мне 300 EUR и бесплатный товар за одно видео в следующем месяце.",
          "check": [
            "Один понятный следующий шаг, а не длинная лекция.",
            "Вопросы только там, где действительно нужен факт.",
            "Бесплатный товар от бренда упомянут как то, что нужно прояснить, а не пропущен.",
            "Нет утверждений, что что-то уже зарегистрировано или подано."
          ],
          "next": "Объясни это простыми словами и назови только следующий шаг."
        },
        "records": {
          "title": "Записи первого месяца",
          "summary": "Разберите три вымышленных чека в отдельной учебной папке.",
          "time": "Около 10 минут",
          "prepare": [
            "Создайте новую пустую папку **Учебный бизнес**. Держите её отдельно от папки Business Assistant.",
            "Claude: начните новую задачу в Cowork и выберите эту папку. Codex: оставьте открытым проект Business Assistant и разрешите доступ к учебной папке, когда приложение спросит."
          ],
          "prompt": "Используй de-business-accounting. Это вымышленное учебное упражнение. Используй только выбранную папку Учебный бизнес. Создай три вымышленных чека за ноябрь 2026 года для программиста-фрилансера: кабель USB-C 19,90 EUR, билет на поезд к клиенту 49,00 EUR и подписка на облачный хостинг 11,90 EUR. Разбери их для моего первого месяца, покажи, что ещё неясно, и сохрани короткую понятную сводку со следующим шагом. Не используй настоящие данные и не подключай никакие сервисы.",
          "answers": "Это упражнение. В этом примере я Kleinunternehmer и ещё не выбрал(а) бухгалтерскую программу. Всё неясное оставь открытым вопросом.",
          "check": [
            "Новые файлы и сводка появляются только в учебной папке.",
            "Суммы и даты совпадают с примером.",
            "Неясные моменты, например личное использование или НДС, остаются открытыми вопросами, а не догадками.",
            "Ничего не отправлено, не подключено и не подано."
          ],
          "next": "Используй de-business-kit. Прочитай сохранённую сводку в моей учебной папке и покажи следующий шаг."
        },
        "invoice": {
          "title": "Подготовить счёт",
          "summary": "Черновик счёта для вымышленного клиента без отправки.",
          "time": "Около 10 минут",
          "prepare": ["Используйте ту же папку **Учебный бизнес** или начните без папки."],
          "prompt": "Используй de-business-operations. Вымышленный пример: подготовь черновик счёта за выполненную работу по программированию. Клиент: Beispiel Shop GmbH (вымышленный). Услуга: разработка контактной формы для сайта клиента, 8 часов по 50 EUR, выполнено 3 ноября 2026 года. Согласованная цена: 400 EUR. В этом примере я Kleinunternehmer. Для моего адреса, налогового номера и банковских данных используй явно помеченные заполнители. Ничего не отправляй.",
          "answers": "Это упражнение. Оставь явно помеченные заполнители вместо настоящих личных данных.",
          "check": [
            "Понятный черновик с клиентом, услугой, датой выполнения и суммой.",
            "Если упоминается НДС, объяснено, почему в этом примере с Kleinunternehmer он не начисляется.",
            "Заполнители вместо настоящих адресов, налоговых и банковских номеров.",
            "Сказано, что черновик не выставлен и не отправлен."
          ],
          "next": "Покажи, чего ещё не хватает, чтобы такой счёт можно было отправить настоящему клиенту."
        },
        "continue": {
          "title": "Продолжить в следующий раз",
          "summary": "Вернитесь позже и продолжите с того места, где остановились.",
          "time": "Около 5 минут",
          "prepare": [
            "Сначала попробуйте пример **Записи первого месяца**.",
            "Начните новую задачу в Claude или новый разговор в том же проекте Codex с той же учебной папкой."
          ],
          "prompt": "Используй de-business-kit. Прочитай сохранённые сведения и прогресс в моей папке Учебный бизнес, затем покажи, что сделано, что ещё открыто и какой следующий шаг.",
          "answers": "Используй папку Учебный бизнес. Всё в ней вымышлено.",
          "check": [
            "Ассистент читает сохранённую сводку, а не спрашивает всё заново.",
            "Сделанное и открытое перечислены отдельно.",
            "Предложен один следующий шаг."
          ],
          "next": "Сохрани короткую заметку для продолжения со следующим шагом и дай ссылку на файл."
        }
      }
    }
  },
  "de": {
    "meta": {"language": "Deutsch", "title": "German Business Kit einrichten", "locale": "de-DE"},
    "ui": {
      "skip": "Zum Inhalt springen",
      "brand": "German Business Kit",
      "brandSub": "Geführte Einrichtung",
      "languageLabel": "Sprache",
      "progressLabel": "Einrichtungsschritte",
      "stepOf": "Schritt {current} von {total}",
      "back": "Zurück",
      "next": "Weiter",
      "more": "Mehr…",
      "preview": "So sieht es aus…",
      "ok": "OK",
      "toContinue": "Klicken Sie auf „Weiter“, um fortzufahren.",
      "whenDone": "Wenn Sie fertig sind, klicken Sie auf „Weiter“.",
      "start": "Einrichtung starten",
      "copy": "Kopieren",
      "copied": "Kopiert. Fügen Sie es mit Strg+V (Windows) oder Cmd+V (Mac) ein.",
      "copyFailed": "Automatisches Kopieren war nicht möglich. Markieren Sie den Text und drücken Sie Strg+C (Windows) oder Cmd+C (Mac).",
      "newTab": "öffnet in einem neuen Tab",
      "done": "erledigt",
      "saved": "Ihr Fortschritt wird nur in diesem Browser auf diesem Computer gespeichert.",
      "notSaved": "Dieser Browser erlaubt kein Speichern des Fortschritts. Lassen Sie diese Seite bis zum Ende geöffnet.",
      "checked": "Anbieterangaben geprüft am {date}. Tarife, Preise und Menüs können sich ändern; maßgeblich ist die Seite des Anbieters.",
      "safety": "Diese Anleitung fragt nie nach Passwörtern, Zahlungsdaten, Bestätigungscodes oder Schlüsseln. Geben Sie diese nur auf der Website oder in der App des Anbieters ein.",
      "illustration": "Schema. Echte Bildschirme können anders aussehen.",
      "chooseFirst": "Wählen Sie zuerst Ihren Assistenten.",
      "acceptFirst": "Lesen Sie zuerst den Text und wählen Sie „Ich habe gelesen und verstanden“.",
      "mobile": "Die Einrichtung erfolgt am Computer. Öffnen Sie diese Seite unter Windows oder auf einem Mac.",
      "progressSummary": "{done} von {total} Schritten erledigt",
      "enlarge": "Screenshot vergrößern",
      "zoom": "Hineinzoomen",
      "close": "Schließen",
      "footer": "German Business Kit ist KI-gestützte Selbsthilfe-Software und keine Steuer- oder Rechtsberatung. Diese Seite sendet nichts; Links öffnen offizielle Websites nur, wenn Sie sie auswählen."
    },
    "steps": {"welcome": "Start", "assistant": "Assistent", "account": "Konto", "app": "App", "safety": "Daten & Risiken", "skills": "Skills", "demos": "Erste Aufgaben"},
    "welcome": {
      "eyebrow": "Geführte Einrichtung · etwa 30 Minuten",
      "title": "Willkommen beim Setup-Assistenten für German Business Kit",
      "lead": "Der Assistent hilft Ihnen, einen KI-Assistenten für Ihr Unternehmen einzurichten: Konto, App und German Business Kit. Programmierkenntnisse sind nicht nötig.",
      "needTitle": "Das brauchen Sie",
      "need": [
        "Ein Windows-PC oder Mac mit Internetzugang",
        "Eine E-Mail-Adresse, die Sie jetzt öffnen können",
        "Ein Mobiltelefon, das SMS empfängt",
        "Eine Bankkarte für einen kostenpflichtigen Tarif: Claude Pro oder ChatGPT Plus"
      ],
      "aiTitle": "Gut zu wissen vor dem Start",
      "aiShort": "German Business Kit ist keine Steuerberatung, und KI kann Fehler machen.",
      "ai": "German Business Kit ist KI-gestützte Selbsthilfe-Software und kein Steuerberater. KI kann sich irren, auch bei Beträgen und Fristen. Dateien, die der Assistent liest, werden von Anthropic oder OpenAI verarbeitet. Verwenden Sie erfundene Beispiele, bis Sie die Hinweise zu Ihren Daten gelesen haben.",
      "aiLink": "KI-Grenzen und Ihre Daten (auf Englisch)"
    },
    "assistant": {
      "title": "Wählen Sie Ihren Assistenten",
      "business": "Arbeiten Sie mit Daten von Kundinnen, Kunden oder Beschäftigten? Private Tarife wie Claude Pro oder ChatGPT Plus enthalten keinen Auftragsverarbeitungsvertrag (AVV) für Unternehmen; Business-Tarife wie Claude Team oder ChatGPT Business bieten einen an. Mehr dazu im Schritt „{name}“.",
      "lead": "Wählen Sie die App, in der German Business Kit arbeiten soll. Die andere können Sie später einrichten.",
      "choose": "{name} wählen",
      "chosen": "Ausgewählt",
      "unsure": "Unsicher? Wählen Sie **Claude**: Dort sind es die wenigsten Einrichtungsschritte.",
      "work": "Nutzen Sie ein Konto Ihres Arbeitgebers oder Ihrer Hochschule? Die Verwaltung kann Apps, Plugins oder Skills sperren. Fragen Sie zuerst dort nach.",
      "claude": {
        "name": "Claude",
        "maker": "von Anthropic",
        "app": "Claude-Desktop-App mit Cowork",
        "summary": "Die wenigsten Einrichtungsschritte. Benötigt **Pro** oder höher.",
        "pricing": "Claude: Tarife und Preise",
        "points": [
          "Einfachste Einrichtung: Sie fügen das Kit in der App mit wenigen Klicks hinzu.",
          "Erfordert einen kostenpflichtigen Tarif: **Pro** oder höher (Pro, Max, Ultra, Team oder Enterprise). Der kostenlose Tarif enthält kein Cowork.",
          "Arbeitet mit den Dateien in einem Ordner Ihrer Wahl."
        ]
      },
      "openai": {
        "name": "ChatGPT mit Codex",
        "maker": "von OpenAI",
        "app": "ChatGPT-Desktop-App mit Codex",
        "summary": "Ein paar Einrichtungsschritte mehr. Empfohlen: **Plus** oder höher.",
        "pricing": "ChatGPT: Tarife und Preise",
        "points": [
          "Wir empfehlen einen kostenpflichtigen Tarif: **Plus** oder höher (Plus, Pro, Business oder Enterprise). Free und Go haben niedrige Limits.",
          "Mehr Einrichtungsschritte: Sie laden eine Datei herunter, und Codex kopiert das Kit in einen Projektordner.",
          "Arbeitet mit den Dateien in einem Projektordner auf Ihrem Computer."
        ]
      }
    },
    "account": {
      "lead": "Die Registrierung erfolgt auf der Website des Anbieters. Diese Anleitung öffnet nur die offizielle Seite in einem neuen Tab.",
      "labelsNote": "Schaltflächen können je nach Sprache oder App-Version anders heißen.",
      "already": "Sie haben schon ein Konto? Klicken Sie einfach auf „Weiter“.",
      "safetyTitle": "So bleibt Ihr Konto sicher",
      "safety": [
        "Geben Sie Passwörter, Codes und Kartendaten nur auf der Seite oder in der App des Anbieters ein.",
        "Niemand aus diesem Projekt fragt Sie nach Codes oder Passwörtern.",
        "Prüfen Sie die Adresszeile: **claude.ai** oder **claude.com** für Claude, **chatgpt.com** oder **openai.com** für ChatGPT."
      ],
      "claude": {
        "title": "Legen Sie Ihr Claude-Konto an",
        "open": "Offizielle Claude-Registrierung öffnen",
        "short": [
          "Registrieren Sie sich mit Google oder Ihrer E-Mail-Adresse.",
          "Bestätigen Sie Ihre Mobilnummer mit dem Code aus der SMS.",
          "Wählen Sie **Pro** oder höher und bezahlen Sie auf der Claude-Website."
        ],
        "steps": [
          "Wählen Sie auf der offiziellen Seite **Continue with Google** oder geben Sie Ihre E-Mail-Adresse ein und wählen Sie **Continue with email**.",
          "Wenn Sie E-Mail gewählt haben, öffnen Sie die Nachricht von Claude und wählen Sie den Anmeldelink. Claude verwendet kein Passwort.",
          "Geben Sie eine Mobilnummer ein, die SMS empfangen kann, und tippen Sie den 6-stelligen Code aus der Nachricht ein. Internet- und Festnetznummern funktionieren nicht.",
          "Wählen Sie einen Tarif. German Business Kit braucht **Pro** oder höher. Bezahlen Sie nur auf der Website von Claude."
        ],
        "diagram": ["Seite öffnen", "E-Mail bestätigen", "Telefon prüfen", "Tarif wählen"]
      },
      "openai": {
        "title": "Legen Sie Ihr ChatGPT-Konto an",
        "open": "Offizielle ChatGPT-Registrierung öffnen",
        "short": [
          "Wählen Sie **Sign up** und nutzen Sie Ihre E-Mail-Adresse oder eine andere angebotene Option.",
          "Bestätigen Sie Ihre E-Mail-Adresse.",
          "Wählen Sie **Plus** oder höher und bezahlen Sie auf der OpenAI-Website."
        ],
        "steps": [
          "Wählen Sie auf der offiziellen Seite **Sign up** (**Registrieren**). Verwenden Sie Ihre E-Mail-Adresse oder eine der Anmeldeoptionen auf der Seite.",
          "Folgen Sie den Schritten auf der Seite, um Ihre E-Mail-Adresse zu bestätigen.",
          "Beim ersten Start von Codex kann die App Sie bitten, eine Telefonnummer hinzuzufügen oder zu bestätigen. Tun Sie das nur in der ChatGPT-App oder auf chatgpt.com.",
          "Wählen Sie einen Tarif: **Plus** oder höher. Bezahlen Sie nur auf der Website von OpenAI."
        ],
        "diagram": ["Seite öffnen", "E-Mail bestätigen", "Telefon prüfen", "Tarif wählen"]
      }
    },
    "app": {
      "osTitle": "Ihr Computer",
      "detected": "Das sieht nach einem {os}-Computer aus.",
      "unknown": "Wir konnten Ihren Computer nicht erkennen. Wählen Sie ihn unten aus.",
      "windows": "Windows",
      "mac": "Mac",
      "other": "Linux oder ein anderes System? Nutzen Sie die offizielle Download-Seite; diese Anleitung behandelt Windows und Mac.",
      "official": "Stattdessen die offizielle Download-Seite öffnen",
      "blocked": "Blockiert ein Arbeitscomputer die Installation? Fragen Sie Ihre IT-Abteilung. Schalten Sie niemals Sicherheitseinstellungen ab, um eine App zu installieren.",
      "stepsTitle": "Installieren und anmelden",
      "claude": {
        "title": "Installieren Sie die Claude-App",
        "download": {
          "mac": "Claude für Mac herunterladen",
          "windows": "Claude für Windows herunterladen",
          "windowsArm": "Windows auf ARM, zum Beispiel ein Snapdragon-Laptop? Laden Sie stattdessen diese Version."
        },
        "short": [
          "Laden Sie die App mit der Schaltfläche oben herunter und installieren Sie sie.",
          "Öffnen Sie Claude und melden Sie sich an.",
          "Schalten Sie unter **Settings → Privacy** **Help improve our AI models** aus, wenn Ihre Chats nicht zum Training von KI-Modellen genutzt werden sollen."
        ],
        "mac": [
          "Laden Sie die Datei über die Schaltfläche oben herunter. Sie landet im Ordner **Downloads**.",
          "Öffnen Sie die heruntergeladene Datei. Ziehen Sie im erscheinenden Fenster das Claude-Symbol in den Ordner **Programme**.",
          "Öffnen Sie Claude aus **Programme**. Fragt Ihr Mac, ob eine aus dem Internet geladene App geöffnet werden soll, bestätigen Sie nur, wenn es Claude vom offiziellen Link oben ist.",
          "Melden Sie sich mit dem Konto aus dem vorigen Schritt an."
        ],
        "windows": [
          "Laden Sie die Datei über die Schaltfläche oben herunter. Sie landet im Ordner **Downloads**.",
          "Öffnen Sie die heruntergeladene Datei. Fragt Windows nach einer Erlaubnis, prüfen Sie, dass der Herausgeber Anthropic ist, und erlauben Sie es dann.",
          "Warten Sie, bis die Installation fertig ist. Claude öffnet sich von selbst; sonst finden Sie **Claude** im Startmenü.",
          "Melden Sie sich mit dem Konto aus dem vorigen Schritt an."
        ],
        "doneWhen": "**Fertig, wenn:** die Claude-App geöffnet ist und Sie angemeldet sind.",
        "diagram": ["Herunterladen", "Installieren", "Anmelden"]
      },
      "openai": {
        "title": "Installieren Sie die ChatGPT-App",
        "download": {
          "macArm": "ChatGPT für Mac mit Apple-Chip (M1 oder neuer) herunterladen",
          "macIntel": "ChatGPT für Mac mit Intel-Prozessor herunterladen",
          "windows": "ChatGPT für Windows aus dem Microsoft Store holen"
        },
        "short": [
          "Laden Sie die App mit der Schaltfläche oben herunter und installieren Sie sie.",
          "Öffnen Sie ChatGPT, melden Sie sich an und wählen Sie **Codex**.",
          "Schalten Sie unter **Settings → Data controls** **Improve the model for everyone** aus, wenn Ihre Chats nicht zum Training von KI-Modellen genutzt werden sollen."
        ],
        "macWhich": "Welchen Mac habe ich? Öffnen Sie das Apple-Menü und wählen Sie **Über diesen Mac**. **Chip: Apple M…** bedeutet Apple-Chip; **Prozessor: Intel** bedeutet Intel.",
        "mac": [
          "Laden Sie die passende Datei für Ihren Mac über eine Schaltfläche oben herunter. Sie landet im Ordner **Downloads**.",
          "Öffnen Sie die heruntergeladene Datei. Ziehen Sie im erscheinenden Fenster das App-Symbol (ChatGPT oder Codex) in den Ordner **Programme**.",
          "Öffnen Sie die App aus **Programme**. Fragt Ihr Mac, ob eine aus dem Internet geladene App geöffnet werden soll, bestätigen Sie nur, wenn es ChatGPT vom offiziellen Link oben ist.",
          "Melden Sie sich mit dem Konto aus dem vorigen Schritt an und wählen Sie **Codex**."
        ],
        "windows": [
          "Wählen Sie die Schaltfläche oben und öffnen Sie das heruntergeladene Installationsprogramm.",
          "Folgen Sie den Schritten im Microsoft-Store-Fenster und warten Sie, bis die Installation fertig ist.",
          "Öffnen Sie **ChatGPT** über das Startmenü.",
          "Melden Sie sich mit dem Konto aus dem vorigen Schritt an und wählen Sie **Codex**."
        ],
        "doneWhen": "**Fertig, wenn:** die ChatGPT-App geöffnet ist, Sie angemeldet sind und **Codex** wählen können.",
        "diagram": ["Herunterladen", "Installieren", "Anmelden"]
      }
    },
    "safety": {
      "title": "Vor dem Start lesen",
      "lead": "Lesen Sie das einmal, bevor der Assistent echte Unterlagen sieht. Es dauert etwa fünf Minuten. Es sind allgemeine Hinweise, keine Rechtsberatung.",
      "warnings": [
        "KI kann Fehler machen, auch bei Beträgen und Fristen. Prüfen Sie alles, bevor Sie etwas senden, unterschreiben oder bezahlen.",
        "Dateien, die der Assistent liest, werden zur Verarbeitung an {provider} gesendet.",
        "German Business Kit ist keine Steuerberatung und keine Rechtsberatung."
      ],
      "boxNote": "Lesen Sie den folgenden Text. Scrollen Sie nach unten, um alles zu sehen.",
      "license": "German Business Kit ist freie Software unter der MIT-Lizenz. Sie wird ohne Mängelgewähr und ohne jegliche Garantie bereitgestellt.",
      "question": "Haben Sie diese Punkte verstanden? Um fortzufahren, wählen Sie „Ich habe gelesen und verstanden“.",
      "understand": "Ich habe gelesen und verstanden",
      "decline": "Ich stimme nicht zu",
      "selfTest": "Selbsttest…",
      "risksTitle": "Was KI falsch machen kann",
      "risks": [
        {"title": "Selbstsichere Fehler", "text": "Sie kann ein Dokument falsch lesen, Regeln des falschen Jahres anwenden oder eine Quelle nennen, die es nicht gibt – und trotzdem überzeugt klingen."},
        {"title": "Beträge und Fristen", "text": "Beträge, Umsatzsteuer und Fristen können falsch sein. Vergleichen Sie sie mit dem Originaldokument und einer offiziellen Quelle."},
        {"title": "Kein Steuerberater", "text": "German Business Kit ist Selbsthilfe-Software, kein Steuerberater und keine Anwaltskanzlei. Durch die Nutzung entsteht kein Beratungsverhältnis."},
        {"title": "Sie entscheiden", "text": "Der Assistent bereitet Entwürfe vor. Prüfen Sie sie, bevor Sie etwas senden, unterschreiben, bezahlen oder einreichen. Ein sauberer Entwurf beweist nicht, dass etwas eingereicht wurde."}
      ],
      "flowTitle": "Wohin Ihre Daten gehen",
      "flow": ["Ihre Dateien", "KI-App", "Server des Anbieters", "Im Konto gespeichert"],
      "flowText": [
        "Wenn der Assistent eine Datei liest, kann ihr Inhalt zur Verarbeitung an {provider} gesendet werden. Ein Ordner auf Ihrem Computer bedeutet nicht, dass die KI nur auf Ihrem Computer arbeitet.",
        "Aufgaben, Chats und ihr Inhalt können in Ihrem Konto gespeichert bleiben. Wenn Sie eine Datei auf Ihrem Computer löschen, werden sie nicht gelöscht.",
        "Verbundene Dienste wie Cloud-Speicher oder E-Mail verarbeiten Daten nach ihren eigenen Bedingungen."
      ],
      "either": "Anthropic oder OpenAI",
      "gdprTitle": "Datenschutz (DSGVO) in einfachen Worten",
      "gdpr": [
        "**Ihre eigenen Unterlagen**, etwa Ihre Belege oder Steuerbriefe, betreffen vor allem Sie. Prüfen Sie trotzdem die Datenschutz-Einstellungen unten, bevor der Assistent sie liest.",
        "**Daten anderer Menschen**, zum Beispiel von Kundschaft, Ansprechpersonen oder Beschäftigten, sind personenbezogene Daten im Sinne der DSGVO. Nutzen Sie sie nur für einen klaren geschäftlichen Zweck und geben Sie nur weiter, was die Aufgabe braucht.",
        "**Private Tarife sind keine Geschäftsverträge.** Tarife wie Claude Pro oder ChatGPT Plus enthalten keinen Auftragsverarbeitungsvertrag (AVV, Art. 28 DSGVO). Business-Tarife wie Claude Team oder Enterprise und ChatGPT Business oder Enterprise bieten einen an. Prüfen Sie das, bevor der Assistent Daten von Kundschaft oder Beschäftigten verarbeitet.",
        "**Gesundheitsdaten**, etwa eine Krankmeldung, sind eine besondere Kategorie (Art. 9 DSGVO). Verwenden Sie ein erfundenes Beispiel oder nur die wenigen Angaben, die die Aufgabe braucht.",
        "**Entfernen Sie Angaben vorher.** Schwärzen Sie Namen, Adressen und Ausweis- oder Steuernummern in einer Kopie auf Ihrem Computer, bevor der Assistent sie liest. Die KI darum zu bitten, ist zu spät: Sie hat sie dann schon gelesen.",
        "**Wenn andere für Sie arbeiten**, erklären Sie ihnen diese Regeln. Die EU-KI-Verordnung (AI Act) verlangt von Unternehmen, die KI einsetzen, die KI-Kompetenz ihrer Beschäftigten zu fördern (Art. 4)."
      ],
      "gdprNote": "Diese Seite ist keine Rechtsberatung und keine DSGVO-Konformitätsbescheinigung.",
      "aiActLink": "EU-Kommission: Fragen und Antworten zur KI-Kompetenz (auf Englisch)",
      "fullLink": "Ausführliche Hinweise: KI-Grenzen und Ihre Daten (auf Englisch)",
      "settingsTitle": "Prüfen Sie Ihre Datenschutz-Einstellungen",
      "settingsLead": "Tun Sie das einmal in der App oder auf der Website. Menünamen stehen hier auf Englisch und können in einer anderen App-Sprache anders heißen. Diese Anleitung kann Ihre Einstellungen weder sehen noch ändern.",
      "claude": {
        "name": "Claude",
        "steps": [
          "Öffnen Sie **Settings → Privacy** in der Claude-App oder auf claude.ai.",
          "Suchen Sie **Help improve our AI models**. Solange der Schalter an ist, darf Anthropic Ihre Chats und Coding-Sitzungen zum Training seiner Modelle nutzen. Entscheiden Sie, ob Sie ihn ausschalten.",
          "Nutzen Sie in Chats mit echten Daten nicht die Daumen-hoch/runter-Tasten: Feedback sendet das ganze Gespräch an Anthropic, wo es bis zu fünf Jahre gespeichert werden kann."
        ],
        "link": "Anthropic: Einstellung zur Modellverbesserung ändern (auf Englisch)",
        "business": "Sie nutzen Claude Team oder Enterprise? Dann gelten die gewerblichen Bedingungen Ihrer Organisation, und standardmäßig werden diese Inhalte nicht zum Training genutzt."
      },
      "openai": {
        "name": "ChatGPT",
        "steps": [
          "Öffnen Sie **Settings → Data controls** in der ChatGPT-App oder auf chatgpt.com.",
          "Suchen Sie **Improve the model for everyone**. Bei Free, Plus und Pro ist die Option standardmäßig an und gilt auch für Ihre Codex-Aufgaben. Entscheiden Sie, ob Sie sie ausschalten.",
          "Das Ausschalten löscht keine gespeicherten Chats. Löschen Sie Chats mit echten Daten, die Sie nicht mehr brauchen."
        ],
        "link": "OpenAI: Datenkontrollen in ChatGPT (auf Englisch)",
        "business": "Sie nutzen ChatGPT Business oder Enterprise? Dann gelten die Einstellungen Ihres Workspace, und standardmäßig trainiert OpenAI nicht mit diesen Inhalten."
      },
      "quizTitle": "Kurzer Check: Würden Sie das teilen?",
      "quizLead": "Wählen Sie für jede Karte eine Antwort. Es wird nichts gesendet; das ist nur eine Übung.",
      "quizChoices": {"ok": "Ausprobieren", "check": "Erst prüfen", "never": "Niemals"},
      "quizRight": "Richtig.",
      "quizWrong": "Nicht ganz. Besser: {answer}.",
      "quizScore": "{answered} von {total} beantwortet, {right} richtig",
      "quiz": {
        "demo": {"item": "Die erfundenen Belege aus den Beispielen dieser Anleitung", "why": "Erfundene Daten sind der sicherste Weg, den Assistenten kennenzulernen."},
        "question": {"item": "Eine allgemeine Frage: „Was ist die Kleinunternehmerregelung?“", "why": "Allgemeine Fragen ohne persönliche Angaben sind in Ordnung. Prüfen Sie die Antwort trotzdem an einer offiziellen Quelle."},
        "customer": {"item": "Eine Rechnung mit Name und Adresse Ihrer Kundin oder Ihres Kunden", "why": "Das sind Daten einer anderen Person im Sinne der DSGVO. Prüfen Sie Tarif und Einstellungen und geben Sie nur weiter, was die Aufgabe braucht."},
        "letter": {"item": "Ein Brief des Finanzamts an Sie", "why": "Er enthält Ihre Steuernummer und persönliche Angaben. Prüfen Sie zuerst Ihre Datenschutz-Einstellungen und schwärzen Sie, was die Aufgabe nicht braucht."},
        "elster": {"item": "Ihre ELSTER-Zertifikatsdatei mit Passwort", "why": "Zugangsdaten, Zertifikate, TANs und Wiederherstellungscodes gehören nie in einen Chat. Melden Sie sich selbst auf der offiziellen Website an."},
        "banking": {"item": "Ihr Online-Banking-Login, damit die KI Zahlungen selbst prüft", "why": "Geben Sie nie Zugang zu Ihrem Bankkonto. Laden Sie selbst einen Kontoauszug herunter und geben Sie nur die nötigen Zeilen weiter."}
      },
      "askTitle": "Vor Ihrem ersten echten Dokument",
      "askLead": "Bitten Sie den Assistenten, den Datenweg für Ihre Einrichtung zu erklären:",
      "askLabel": "Frage zu Ihren Daten",
      "ask": "Nutze de-business-kit. Erkläre mir, bevor du meine echten Dokumente liest, welche Daten an welchen Anbieter oder verbundenen Dienst gehen, welche Kontoeinstellungen wichtig sind und was ich vorher lokal entfernen kann. Wenn du eine Einstellung nicht prüfen kannst, sag das. Beginne mit einem erfundenen Beispiel."
    },
    "skills": {
      "listTitle": "Die sieben Skills, die Sie erhalten",
      "list": {
        "de-business-kit": "Starten, fortsetzen, die nächste Aufgabe wählen",
        "de-business-start": "Eine Tätigkeit vorbereiten und eröffnen",
        "de-business-operations": "Angebote, Rechnungen und alltägliche Korrespondenz",
        "de-business-accounting": "Belege und Buchhaltungsaufzeichnungen",
        "de-business-tax": "Steuerfragen, Meldungen und Briefe vom Finanzamt",
        "de-business-services": "Bank, Versicherung, Software und Zugänge zu Diensten",
        "de-business-changes": "Änderungen, Einstellungen, Pause und Aufgabe der Tätigkeit"
      },
      "once": "Installieren Sie das Kit nur einmal pro App. Zwei Kopien derselben Skills führen zu Doppelungen.",
      "stuck": "Sieht etwas anders aus?",
      "stuckLink": "Abschnitt „If you get stuck“ in der Installationsanleitung (auf Englisch)",
      "claude": {
        "title": "Fügen Sie German Business Kit zu Claude hinzu",
        "lead": "Bitten Sie Claude, das Kit für Sie zu installieren. Dafür reicht eine Anfrage.",
        "short": [
          "Öffnen Sie Claude, wechseln Sie zu **Cowork** und starten Sie eine neue Aufgabe.",
          "Kopieren Sie diese Anfrage, fügen Sie sie in die Aufgabe ein und senden Sie sie:",
          "Folgen Sie der Antwort von Claude. Wählen Sie selbst **Install** oder bestätigen Sie die Aktion, wenn Claude darum bittet."
        ],
        "steps": [
          "Öffnen Sie die Claude-App, wechseln Sie zu **Cowork** und starten Sie eine neue Aufgabe.",
          "Kopieren Sie die Anfrage unten, fügen Sie sie in die Aufgabe ein und senden Sie sie.",
          "Folgen Sie der Antwort von Claude. Wenn Claude Sie bittet, unter **Plugins** **Install** zu wählen oder eine Aktion zu bestätigen, tun Sie das selbst: Claude zeigt Ihnen, wo, kann aber nicht für Sie klicken.",
          "Starten Sie eine **neue Aufgabe** und prüfen Sie, dass die sieben Skills unten verfügbar sind: Öffnen Sie German Business Kit und den Reiter **Skills** oder fragen Sie Claude, welche Skills von German Business Kit verfügbar sind."
        ],
        "promptLabel": "Anfrage für Claude",
        "prompt": "Installiere German Business Kit von https://github.com/ilyafedotov-ops/german-business-skills und zeig mir, wie ich es nutze. Folge den Installationsanweisungen des Repositorys für meine App, prüfe, ob das vollständige Kit verfügbar ist, und hilf mir, ein kleines Beispiel auszuprobieren.",
        "manualTitle": "Manuell installieren…",
        "result": {
          "alt": "Seite von German Business Kit in der Claude-App nach Add: Status Added und die Skills des Kits",
          "caption": "Die echte Claude-App am 21. November 2026. In Ihrer Version kann es anders aussehen."
        },
        "manualSteps": [
          "Öffnen Sie in der Claude-App in der Seitenleiste **Customize** und dann **Plugins**. Zeigt Ihre Version einen eigenen **Cowork**-Umschalter, wechseln Sie zuerst zu Cowork.",
          "Wählen Sie **Add** und dann **Add marketplace**. Falls angeboten, wählen Sie **Add from a repository**. Fügen Sie die Adresse unten ein und wählen Sie **Sync**.",
          "Suchen Sie **German Business Kit** in der Liste (falls nötig unter **Discover**) und wählen Sie **Install**. Manche Versionen zeigen **Add**.",
          "Öffnen Sie German Business Kit und den Reiter **Skills**. Prüfen Sie, dass die sieben Skills unten aufgeführt sind."
        ],
        "addressLabel": "Marketplace-Adresse",
        "github": "Das ist die öffentliche Projektseite auf GitHub. Ein GitHub-Konto brauchen Sie nicht.",
        "review": "Anthropic prüft Plugins im eigenen Verzeichnis, nicht per Adresse hinzugefügte Plugins. Diese Adresse installiert die geprüfte Veröffentlichung des Projekts.",
        "shotAlt": "Claude-Dialog zum Hinzufügen eines Marketplace mit eingetragener Projektadresse und der Schaltfläche Sync",
        "shotCaption": "Echte Claude-Desktop-App 3.6556.2 unter macOS, aufgenommen am 26. Oktober 2026 vor dem Auswählen von Sync. Bezeichnungen können in Ihrer Version abweichen.",
        "diagram": ["Cowork", "Anfrage einfügen", "Install", "Neue Aufgabe"]
      },
      "openai": {
        "title": "Fügen Sie German Business Kit zu Codex hinzu",
        "lead": "Bitten Sie Codex, das Kit für Sie zu installieren. Dafür reicht eine Anfrage.",
        "short": [
          "Legen Sie einen leeren Ordner **Business Assistant** an, zum Beispiel unter Dokumente.",
          "Wählen Sie in ChatGPT **Codex**, öffnen Sie diesen Ordner als Projekt und starten Sie einen **New chat**.",
          "Kopieren Sie diese Anfrage, fügen Sie sie in Codex ein und senden Sie sie:",
          "Folgen Sie der Antwort von Codex. Erlauben Sie Internetzugriff und Dateiänderungen nur für dieses Projekt."
        ],
        "steps": [
          "Legen Sie an einem privaten Ort, zum Beispiel unter Dokumente, einen neuen Ordner **Business Assistant** an. Er enthält nur das Kit, nicht Ihre Geschäftsunterlagen.",
          "Wählen Sie in der ChatGPT-App **Codex**, öffnen Sie den Ordner **Business Assistant** als Projekt und starten Sie einen **New chat** (neuen Chat). Werden Sie gefragt, ob Sie einem Ordner vertrauen, bestätigen Sie nur diesen.",
          "Kopieren Sie die Anfrage unten, fügen Sie sie in Codex ein und senden Sie sie. Fragt Codex nach Internetzugriff oder der Erlaubnis, Dateien zu ändern, erlauben Sie das nur für dieses Projekt.",
          "Starten Sie einen **neuen Chat im selben Projekt**. Öffnen Sie **Skills** in der Seitenleiste und prüfen Sie, dass die sieben Skills unten aufgeführt sind. Fehlen sie, schließen Sie die App und öffnen Sie sie erneut."
        ],
        "promptLabel": "Anfrage für Codex",
        "prompt": "Installiere German Business Kit von https://github.com/ilyafedotov-ops/german-business-skills und zeig mir, wie ich es nutze. Folge den Installationsanweisungen des Repositorys für meine App, prüfe, ob das vollständige Kit verfügbar ist, und hilf mir, ein kleines Beispiel auszuprobieren.",
        "manualTitle": "Manuell installieren…",
        "result": {
          "alt": "Codex zeigt die sieben Skills von German Business Kit in einer Tabelle",
          "caption": "Die echte ChatGPT-App mit Codex am 21. November 2026. Ihre Antwort sieht anders aus."
        },
        "manualSteps": [
          "Laden Sie diese zwei Dateien in denselben Ordner herunter, zum Beispiel Downloads.",
          "Kopieren Sie den vollständigen Pfad jeder Datei. Windows: Rechtsklick auf die Datei und **Als Pfad kopieren** wählen. Mac: Datei im Finder auswählen, die **Wahltaste (Option)** gedrückt halten und **Bearbeiten → „…“ als Pfadname kopieren** wählen.",
          "Kopieren Sie die Anfrage unten, fügen Sie sie in Codex ein, ersetzen Sie die zwei Teile in eckigen Klammern durch Ihre Pfade und senden Sie sie.",
          "Starten Sie einen neuen Chat im selben Projekt. Öffnen Sie **Skills** in der Seitenleiste und prüfen Sie, dass die sieben Skills unten aufgeführt sind."
        ],
        "zip": "{file} herunterladen",
        "checksums": "{file} herunterladen (Prüfsummenliste)",
        "releasePage": "Veröffentlichungsseite öffnen",
        "manualPromptLabel": "Anfrage mit Dateipfaden",
        "manualPrompt": "Ich richte German Business Kit in diesem lokalen Projekt Business Assistant in Codex ein. Mein ZIP liegt unter [vollständiger ZIP-Pfad] und SHA256SUMS unter [vollständiger Pfad der Prüfsummendatei]. Prüfe das ZIP anhand der Prüfsumme und brich ab, wenn sie nicht übereinstimmt. Entpacke es in einen neuen Ordner und kopiere dann alle sieben vollständigen Skill-Ordner in .agents/skills dieses Projekts. Verwende normale Dateiwerkzeuge, erhalte vorhandene Dateien und brich ab, wenn ein Zielordner bereits existiert. Installiere keine Laufzeitumgebungen und ändere weder Sicherheitseinstellungen noch die globale App-Konfiguration. Nenne mir die sieben installierten Namen und erkläre, wie ich eine neue Sitzung starte.",
        "checksumNote": "Mit der Prüfsummenliste kann Codex prüfen, ob der Download vollständig und unverändert ist. Sie beweist nicht, wer die Datei veröffentlicht hat.",
        "manual": "Codex konnte die Dateien nicht kopieren? Folgen Sie den manuellen Schritten in der Installationsanleitung (auf Englisch).",
        "diagram": ["Projektordner", "Anfrage einfügen", "Zugriff erlauben", "Neuer Chat"]
      }
    },
    "demos": {
      "title": "Probieren Sie erste Aufgaben mit erfundenen Beispielen aus",
      "doneTitle": "Die Einrichtung ist abgeschlossen",
      "doneLead": "German Business Kit ist bereit. Probieren Sie eine erste Aufgabe mit erfundenen Daten: Wählen Sie das Beispiel, das am besten zu Ihnen passt, und fügen Sie es in eine neue Aufgabe in Claude oder einen neuen Chat in Codex ein.",
      "more": "Weitere Beispiele…",
      "result": {
        "claudeAlt": "Claude beantwortet das Content-Creator-Beispiel mit einem kleinen ersten Schritt",
        "openaiAlt": "Codex beantwortet das Programmier-Beispiel mit einem kleinen ersten Schritt",
        "caption": "Echte Antworten vom 21. November 2026 auf die erfundenen Beispiele. Ihre Antwort sieht anders aus."
      },
      "lead": "Jedes Beispiel verwendet nur erfundene Angaben. Kopieren Sie eine Anfrage, fügen Sie sie in eine **neue Aufgabe** in Claude oder einen **neuen Chat im Projekt Business Assistant** in Codex ein und vergleichen Sie die Antwort mit der Checkliste.",
      "callTitle": "So rufen Sie das Kit auf",
      "call": {
        "claude": "Geben Sie in Claude **/** ein oder öffnen Sie **+** und wählen Sie **de-business-kit**, oder beginnen Sie Ihre Nachricht mit **Nutze de-business-kit**.",
        "openai": "Beginnen Sie Ihre Nachricht in Codex mit **Nutze de-business-kit** oder **$de-business-kit**."
      },
      "privacy": "Beginnen Sie mit erfundenen Daten. Lesen Sie vor echten Unterlagen, welche Inhalte an den KI-Dienst gehen.",
      "open": "Beispiel öffnen",
      "tried": "Ausprobiert",
      "back": "Alle Beispiele",
      "markTried": "Ich habe dieses Beispiel ausprobiert",
      "prepareTitle": "Vorbereitung",
      "promptTitle": "Diese Anfrage einfügen",
      "answersTitle": "Wenn der Assistent nachfragt",
      "checkTitle": "Antwort prüfen",
      "checkNote": "Eine nützliche Antwort kann anders aussehen. Diese Punkte helfen bei der Einschätzung.",
      "nextTitle": "Eine Folgeanfrage ausprobieren",
      "promptLabel": "Anfrage zum Einfügen",
      "answersLabel": "Erfundene Antworten",
      "nextLabel": "Folgeanfrage",
      "prototype": "Möchten Sie zuerst einen Beispiel-Arbeitsbereich sehen?",
      "prototypeLink": "Interaktive Demo mit erfundenen Daten öffnen (nur Englisch)",
      "finishTitle": "Sie sind startklar",
      "finish": "Beschreiben Sie beim nächsten Mal das gewünschte Ergebnis in normalen Worten: einen Brief verstehen, ein Formular vorbereiten, Unterlagen ordnen oder eine Änderung planen. Bleiben Sie bei erfundenen Daten, bis Sie sich sicher fühlen.",
      "guideLink": "Deutsche Startanleitung öffnen",
      "items": {
        "first": {
          "title": "Erster Schritt: Programmierung als Freelancer",
          "summary": "Fragen Sie nach einem kleinen nächsten Schritt für eine erfundene freiberufliche Programmiertätigkeit.",
          "time": "Etwa 5 Minuten",
          "prepare": ["Starten Sie eine **neue Aufgabe** in Claude oder einen **neuen Chat** in Ihrem Projekt Business Assistant in Codex. Ein Ordner ist nicht nötig."],
          "prompt": "Nutze de-business-kit. Ich probiere den Assistenten mit einem erfundenen Beispiel aus: Ich bin Programmierer und möchte in Deutschland als Freelancer Websites und Apps für kleine Unternehmen entwickeln. Ich weiß nicht, wo ich anfangen soll. Hilf mir, einen kleinen ersten Schritt zu wählen. Frag nur, was du für diesen Schritt brauchst.",
          "answers": "Das ist ein erfundenes Beispiel. Ich wohne in Berlin, habe noch nichts angemeldet und erwarte meinen ersten Auftrag im nächsten Monat.",
          "check": [
            "Ein verständlicher nächster Schritt statt eines langen Vortrags.",
            "Rückfragen nur, wo eine Angabe wirklich nötig ist.",
            "Noch keine Bitte, private Unterlagen hochzuladen oder eine Buchhaltungssoftware zu wählen.",
            "Keine Behauptung, dass etwas angemeldet oder eingereicht wurde."
          ],
          "next": "Erkläre das in einfachen Worten und nenne mir nur den nächsten Schritt."
        },
        "creator": {
          "title": "Erster Schritt: Content Creator",
          "summary": "Fragen Sie nach einem kleinen nächsten Schritt für einen erfundenen Instagram- und YouTube-Kanal.",
          "time": "Etwa 5 Minuten",
          "prepare": ["Starten Sie eine **neue Aufgabe** in Claude oder einen **neuen Chat** in Ihrem Projekt Business Assistant in Codex. Ein Ordner ist nicht nötig."],
          "prompt": "Nutze de-business-kit. Ich probiere den Assistenten mit einem erfundenen Beispiel aus: Ich mache Videos für Instagram und YouTube, und erste Marken möchten mich für Beiträge bezahlen. Ich wohne in Deutschland und habe noch nichts angemeldet. Hilf mir, einen kleinen ersten Schritt zu wählen. Frag nur, was du für diesen Schritt brauchst.",
          "answers": "Das ist ein erfundenes Beispiel. Ich wohne in München, studiere, und eine Marke hat mir für ein Video im nächsten Monat 300 EUR und ein kostenloses Produkt angeboten.",
          "check": [
            "Ein verständlicher nächster Schritt statt eines langen Vortrags.",
            "Rückfragen nur, wo eine Angabe wirklich nötig ist.",
            "Das kostenlose Produkt der Marke wird als zu klärender Punkt behandelt, nicht übergangen.",
            "Keine Behauptung, dass etwas angemeldet oder eingereicht wurde."
          ],
          "next": "Erkläre das in einfachen Worten und nenne mir nur den nächsten Schritt."
        },
        "records": {
          "title": "Belege im ersten Monat",
          "summary": "Ordnen Sie drei erfundene Belege in einem getrennten Übungsordner.",
          "time": "Etwa 10 Minuten",
          "prepare": [
            "Legen Sie einen neuen, leeren Ordner **Übungsfirma** an. Er liegt nicht im Ordner Business Assistant.",
            "Claude: Starten Sie eine neue Aufgabe in Cowork und wählen Sie diesen Ordner. Codex: Lassen Sie Ihr Projekt Business Assistant geöffnet und erlauben Sie den Zugriff auf den Übungsordner, wenn danach gefragt wird."
          ],
          "prompt": "Nutze de-business-accounting. Das ist eine erfundene Übung. Verwende nur meinen ausgewählten Ordner Übungsfirma. Lege drei erfundene Belege aus November 2026 für eine freiberufliche Programmiertätigkeit an: USB-C-Kabel 19,90 EUR, Bahnfahrt zu einem Kunden 49,00 EUR und ein Cloud-Hosting-Abo 11,90 EUR. Ordne sie für meinen ersten Monat, zeige, was noch unklar ist, und speichere eine kurze lesbare Zusammenfassung mit dem nächsten Schritt. Verwende keine echten Daten und verbinde keinen Dienst.",
          "answers": "Das ist eine Übung. In diesem Beispiel bin ich Kleinunternehmer und habe noch keine Buchhaltungssoftware gewählt. Lass Unklares als offene Frage stehen.",
          "check": [
            "Neue Dateien und eine Zusammenfassung erscheinen nur im Übungsordner.",
            "Beträge und Daten stimmen mit dem Beispiel überein.",
            "Unklare Punkte wie private Nutzung oder Umsatzsteuer bleiben offene Fragen statt Vermutungen.",
            "Nichts wird gesendet, verbunden oder eingereicht."
          ],
          "next": "Nutze de-business-kit. Lies die gespeicherte Zusammenfassung in meinem Übungsordner und zeige mir den nächsten Schritt."
        },
        "invoice": {
          "title": "Eine Rechnung vorbereiten",
          "summary": "Ein Rechnungsentwurf für einen erfundenen Kunden, ohne Versand.",
          "time": "Etwa 10 Minuten",
          "prepare": ["Verwenden Sie denselben Ordner **Übungsfirma** oder starten Sie ohne Ordner."],
          "prompt": "Nutze de-business-operations. Erfundenes Beispiel: Bereite einen Rechnungsentwurf für eine erledigte Programmierarbeit vor. Kunde: Beispiel Shop GmbH (erfunden). Leistung: Entwicklung eines Kontaktformulars für die Website des Kunden, 8 Stunden zu je 50 EUR, erbracht am 3. November 2026. Vereinbarter Preis: 400 EUR. In diesem Beispiel bin ich Kleinunternehmer. Verwende deutlich markierte Platzhalter für meine Anschrift, Steuernummer und Bankverbindung. Versende nichts.",
          "answers": "Das ist eine Übung. Behalte deutlich markierte Platzhalter statt echter persönlicher Angaben.",
          "check": [
            "Ein lesbarer Entwurf mit Kunde, Leistung, Leistungsdatum und Betrag.",
            "Wird Umsatzsteuer erwähnt, wird erklärt, warum in diesem Kleinunternehmer-Beispiel keine berechnet wird.",
            "Platzhalter statt echter Anschriften, Steuer- oder Bankdaten.",
            "Es wird gesagt, dass der Entwurf weder ausgestellt noch versendet ist."
          ],
          "next": "Zeige mir, was noch fehlt, bevor eine solche Rechnung an einen echten Kunden gehen könnte."
        },
        "continue": {
          "title": "Beim nächsten Mal fortsetzen",
          "summary": "Später zurückkommen und dort weitermachen, wo Sie aufgehört haben.",
          "time": "Etwa 5 Minuten",
          "prepare": [
            "Probieren Sie zuerst **Belege im ersten Monat** aus.",
            "Starten Sie eine neue Aufgabe in Claude oder einen neuen Chat im selben Codex-Projekt, mit demselben Übungsordner."
          ],
          "prompt": "Nutze de-business-kit. Lies die gespeicherten Angaben und den Fortschritt in meinem Ordner Übungsfirma und zeige dann, was erledigt ist, was noch offen ist und was als Nächstes kommt.",
          "answers": "Verwende den Ordner Übungsfirma. Alles darin ist erfunden.",
          "check": [
            "Die gespeicherte Zusammenfassung wird gelesen, statt alles neu zu erfragen.",
            "Erledigtes und Offenes werden getrennt aufgeführt.",
            "Es wird ein nächster Schritt vorgeschlagen."
          ],
          "next": "Speichere eine kurze Fortsetzungsnotiz mit dem nächsten Schritt und verlinke die Datei."
        }
      }
    }
  }
};
