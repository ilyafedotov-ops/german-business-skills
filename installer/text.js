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
      "start": "Start setup",
      "copy": "Copy",
      "copied": "Copied. Paste it with Ctrl+V (Windows) or Cmd+V (Mac).",
      "copyFailed": "Could not copy automatically. Select the text and press Ctrl+C (Windows) or Cmd+C (Mac).",
      "newTab": "opens in a new tab",
      "done": "done",
      "checklist": "Tick each step when it is done.",
      "saved": "Your progress is saved in this browser on this computer only.",
      "notSaved": "This browser does not allow saving progress. Keep this page open until you finish.",
      "checked": "Provider details checked on {date}. Plans, prices and menus can change; the provider's own page is authoritative.",
      "safety": "This guide never asks for passwords, payment details, verification codes or keys. Enter them only on the provider's own website or in its app.",
      "illustration": "Illustration. Real screens may look different.",
      "chooseFirst": "Choose your assistant first.",
      "mobile": "Setup needs a Windows PC or a Mac. Open this guide on your computer to install the app.",
      "footer": "German Business Kit is AI-assisted self-help software, not tax advice. This page sends nothing; links open official websites only when you select them."
    },
    "steps": {"welcome": "Welcome", "assistant": "Assistant", "account": "Account", "app": "App", "skills": "Skills", "demos": "First tasks"},
    "welcome": {
      "eyebrow": "Guided setup · about 30 minutes",
      "title": "Set up your AI business assistant, step by step",
      "lead": "This guide helps you create an account with Claude or ChatGPT, install the app, add German Business Kit and try first tasks with made-up examples. You do not need programming skills.",
      "chooseLanguage": "Choose your language",
      "languageHint": "You can change the language at any time at the top of the page.",
      "needTitle": "What you need",
      "need": [
        "A Windows PC or a Mac with internet access.",
        "An email address you can open now.",
        "A mobile phone that can receive text messages (SMS).",
        "For a paid plan: a bank card. You enter it only on the provider's own website, never here."
      ],
      "aiTitle": "Good to know before you start",
      "ai": "German Business Kit is AI-assisted self-help software, not a tax adviser (Steuerberater). AI can make mistakes, including in amounts and deadlines. Files the assistant reads are processed by Anthropic or OpenAI. Use made-up examples until you have read the data guidance.",
      "aiLink": "Read about AI limits and your data"
    },
    "assistant": {
      "title": "Choose your assistant",
      "lead": "German Business Kit works inside one of two AI apps. Both can do the tasks in this guide. Pick the one you prefer; you can set up the other one later.",
      "choose": "Choose {name}",
      "chosen": "Selected",
      "unsure": "Not sure? Choose **Claude** for the fewest setup steps if a paid plan is fine for you. Choose **ChatGPT with Codex** if you want to start without paying.",
      "work": "Using an account from your employer or school? Its administrator may block apps, plugins or skills. Ask them first.",
      "claude": {
        "name": "Claude",
        "maker": "by Anthropic",
        "app": "Claude desktop app with Cowork",
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
        "pricing": "ChatGPT plans and prices",
        "points": [
          "You can start on any plan, including **Free**. Paid plans give more usage.",
          "More setup steps: you download a file and Codex copies the kit into a project folder.",
          "Works with the files in a project folder on your computer."
        ]
      }
    },
    "account": {
      "lead": "You sign up on the provider's own website. This guide only opens the official page in a new tab.",
      "labelsNote": "Button names can differ by language or app version.",
      "already": "Already have an account? Tick the steps you have done and continue.",
      "safetyTitle": "Keep your account safe",
      "safety": [
        "Type passwords, codes and card details only on the provider's own page or in its app.",
        "Nobody from this project will ask you for codes or passwords.",
        "Check the address bar: **claude.ai** or **claude.com** for Claude, **chatgpt.com** or **openai.com** for ChatGPT."
      ],
      "claude": {
        "title": "Create your Claude account",
        "open": "Open the official Claude sign-up page",
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
        "steps": [
          "On the official page, choose **Sign up**. Use your email address or one of the account options the page offers.",
          "Follow the page's steps to confirm your email address.",
          "When you first use Codex, the app may ask you to add or verify a phone number. Do this only in the ChatGPT app or on chatgpt.com.",
          "Choose a plan. **Free** is enough to try; **Plus** or higher gives more Codex usage. Pay only on OpenAI's own website."
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
        "lead": "The kit is one plugin with seven connected skills. You add it once; it is saved to your Claude account and also works in Claude chat and Claude Code.",
        "steps": [
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
        "diagram": ["Customize", "Plugins", "Add marketplace", "Install"]
      },
      "openai": {
        "title": "Add German Business Kit to Codex",
        "lead": "In Codex, the kit is copied into a project folder on your computer. After you download the kit, Codex can do the copying for you.",
        "steps": [
          "Create a new folder called **Business Assistant** in a private place, for example in Documents. It holds only the kit, not your business records.",
          "In the ChatGPT app, choose **Codex**, open the **Business Assistant** folder as your project and start a **New chat**. If asked to trust a folder, confirm only this one.",
          "Download these two files into the same folder, for example Downloads.",
          "Copy the full path of each file. Windows: right-click the file and choose **Copy as path**. Mac: select the file in Finder, hold **Option** and choose **Edit → Copy … as Pathname**.",
          "Copy the request below, paste it into Codex, replace the two parts in square brackets with your paths and send it.",
          "Start a **new chat in the same project**. Open **Skills** in the sidebar and check that the seven skills below are listed. If they are missing, close and reopen the app."
        ],
        "zip": "Download {file}",
        "checksums": "Download {file} (checksum list)",
        "releasePage": "Open the release page",
        "promptLabel": "Request for Codex",
        "prompt": "I am setting up German Business Kit in this local Business Assistant project in Codex. My ZIP is at [full ZIP path] and SHA256SUMS is at [full checksum-file path]. Check the ZIP against its checksum and stop if it does not match. Extract it into a new folder, then copy all seven complete skill folders into this project's .agents/skills. Use native file tools, preserve existing files and stop if a destination already exists. Do not install runtimes, change security settings or change global app configuration. Tell me the seven installed names and how to start a fresh session.",
        "checksumNote": "The checksum list lets Codex check that the download is complete and unchanged. It does not prove who published the file.",
        "manual": "Codex could not copy the files? Follow the manual steps in the installation guide.",
        "diagram": ["Project folder", "Download", "Ask Codex", "New chat"]
      }
    },
    "demos": {
      "title": "Try your first tasks with made-up examples",
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
          "title": "Your first step",
          "summary": "Ask for one small next step for a fictional new business.",
          "time": "About 5 minutes",
          "prepare": ["Start a **new task** in Claude or a **new chat** in your Business Assistant project in Codex. No folder is needed."],
          "prompt": "Use de-business-kit. I am trying the assistant with a fictional example: I want to start working as a freelance translator in Germany. I do not know where to begin. Help me choose one small first step. Ask only what you need for that step.",
          "answers": "This is a fictional example. I live in Berlin, I have not registered anything yet and I expect my first customer next month.",
          "check": [
            "One understandable next step, not a long lecture.",
            "Questions only where a fact is really needed.",
            "No request to upload private documents or choose accounting software yet.",
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
          "prompt": "Use de-business-accounting. This is a fictional practice exercise. Use only my selected folder Practice business. Create three made-up receipts from November 2026 for a translator: printer paper EUR 23.80, a train ticket to a client EUR 49.00 and a software subscription EUR 11.90. Organize them for my first month, show what is still unclear and save a short readable summary with the next step. Do not use real data or connect any service.",
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
          "prompt": "Use de-business-operations. Fictional example: prepare a draft invoice for a translation I delivered. Customer: Beispiel Verlag GmbH (fictional). Service: translation of a 10-page brochure from English into German, delivered on 3 November 2026. Agreed price: EUR 400. In this example I am a Kleinunternehmer. Use clearly marked placeholders for my address, tax number and bank details. Do not send anything.",
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
      "start": "Начать установку",
      "copy": "Копировать",
      "copied": "Скопировано. Вставьте с помощью Ctrl+V (Windows) или Cmd+V (Mac).",
      "copyFailed": "Не удалось скопировать автоматически. Выделите текст и нажмите Ctrl+C (Windows) или Cmd+C (Mac).",
      "newTab": "откроется в новой вкладке",
      "done": "выполнено",
      "checklist": "Отмечайте каждый шаг, когда он выполнен.",
      "saved": "Ваш прогресс сохраняется только в этом браузере на этом компьютере.",
      "notSaved": "Этот браузер не разрешает сохранять прогресс. Не закрывайте страницу до конца установки.",
      "checked": "Сведения о сервисах проверены {date}; тарифы, цены и меню могут меняться, решающей остаётся страница самого сервиса.",
      "safety": "Эта инструкция никогда не спрашивает пароли, платёжные данные, коды подтверждения или ключи. Вводите их только на сайте или в приложении самого сервиса.",
      "illustration": "Схема. Настоящие экраны могут выглядеть иначе.",
      "chooseFirst": "Сначала выберите ассистента.",
      "mobile": "Для установки нужен компьютер с Windows или Mac. Откройте эту инструкцию на компьютере, чтобы установить приложение.",
      "footer": "German Business Kit — программа для самостоятельной работы с помощью AI, а не налоговая консультация. Эта страница ничего не отправляет; ссылки открывают официальные сайты, только когда вы их выбираете."
    },
    "steps": {"welcome": "Начало", "assistant": "Ассистент", "account": "Аккаунт", "app": "Приложение", "skills": "Скиллы", "demos": "Первые задачи"},
    "welcome": {
      "eyebrow": "Пошаговая установка · около 30 минут",
      "title": "Настройте AI-ассистента для бизнеса шаг за шагом",
      "lead": "Эта инструкция поможет создать аккаунт Claude или ChatGPT, установить приложение, добавить German Business Kit и попробовать первые задачи на вымышленных примерах. Навыки программирования не нужны.",
      "chooseLanguage": "Выберите язык",
      "languageHint": "Язык можно сменить в любой момент вверху страницы.",
      "needTitle": "Что понадобится",
      "need": [
        "Компьютер с Windows или Mac и доступом в интернет.",
        "Адрес электронной почты, который вы можете открыть сейчас.",
        "Мобильный телефон, принимающий SMS.",
        "Для платного тарифа — банковская карта. Её данные вводятся только на сайте самого сервиса, никогда здесь."
      ],
      "aiTitle": "Важно знать до начала",
      "ai": "German Business Kit — программа для самостоятельной работы с помощью AI, а не налоговый консультант (Steuerberater). AI может ошибаться, в том числе в суммах и сроках. Файлы, которые читает ассистент, обрабатываются Anthropic или OpenAI. Используйте вымышленные примеры, пока не прочитаете рекомендации о данных.",
      "aiLink": "Ограничения AI и ваши данные"
    },
    "assistant": {
      "title": "Выберите ассистента",
      "lead": "German Business Kit работает внутри одного из двух AI-приложений. Оба справляются с задачами из этой инструкции. Выберите удобное; второе можно настроить позже.",
      "choose": "Выбрать {name}",
      "chosen": "Выбрано",
      "unsure": "Сомневаетесь? Выберите **Claude**, если хотите меньше шагов при установке и готовы к платному тарифу. Выберите **ChatGPT с Codex**, если хотите начать бесплатно.",
      "work": "Аккаунт от работодателя или учебного заведения? Администратор может запретить приложения, плагины или скиллы. Сначала спросите у него.",
      "claude": {
        "name": "Claude",
        "maker": "от Anthropic",
        "app": "Приложение Claude для компьютера с Cowork",
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
        "pricing": "Тарифы и цены ChatGPT",
        "points": [
          "Можно начать на любом тарифе, включая **Free**. Платные тарифы дают больше использования.",
          "Больше шагов при установке: вы скачиваете файл, а Codex копирует набор в папку проекта.",
          "Работает с файлами в папке проекта на вашем компьютере."
        ]
      }
    },
    "account": {
      "lead": "Регистрация проходит на сайте самого сервиса. Эта инструкция только открывает официальную страницу в новой вкладке.",
      "labelsNote": "Названия кнопок могут отличаться в зависимости от языка или версии приложения.",
      "already": "Аккаунт уже есть? Отметьте выполненные шаги и продолжайте.",
      "safetyTitle": "Безопасность аккаунта",
      "safety": [
        "Вводите пароли, коды и данные карты только на странице самого сервиса или в его приложении.",
        "Никто из этого проекта не будет спрашивать ваши коды или пароли.",
        "Проверяйте адресную строку: **claude.ai** или **claude.com** для Claude, **chatgpt.com** или **openai.com** для ChatGPT."
      ],
      "claude": {
        "title": "Создайте аккаунт Claude",
        "open": "Открыть официальную страницу регистрации Claude",
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
        "steps": [
          "На официальной странице выберите **Sign up** (**Зарегистрироваться**). Используйте адрес почты или один из вариантов входа, которые предлагает страница.",
          "Следуйте шагам на странице, чтобы подтвердить адрес почты.",
          "При первом запуске Codex приложение может попросить добавить или подтвердить номер телефона. Делайте это только в приложении ChatGPT или на chatgpt.com.",
          "Выберите тариф. Для пробы достаточно **Free**; **Plus** или выше даёт больше использования Codex. Оплачивайте только на сайте OpenAI."
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
        "lead": "Набор — это один плагин с семью связанными скиллами. Его добавляют один раз; он сохраняется в вашем аккаунте Claude и работает также в чате Claude и в Claude Code.",
        "steps": [
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
        "diagram": ["Customize", "Plugins", "Add marketplace", "Install"]
      },
      "openai": {
        "title": "Добавьте German Business Kit в Codex",
        "lead": "В Codex набор копируется в папку проекта на вашем компьютере. Когда вы скачаете набор, Codex может скопировать его сам.",
        "steps": [
          "Создайте новую папку **Business Assistant** в приватном месте, например в «Документах». В ней будет только набор, а не ваши деловые записи.",
          "В приложении ChatGPT выберите **Codex**, откройте папку **Business Assistant** как проект и начните **New chat** (новый разговор). Если приложение спросит, доверять ли папке, подтвердите только эту.",
          "Скачайте эти два файла в одну папку, например в «Загрузки».",
          "Скопируйте полный путь к каждому файлу. Windows: щёлкните файл правой кнопкой и выберите **Копировать как путь**. Mac: выберите файл в Finder, удерживайте **Option** и выберите **Правка → Скопировать … как путь**.",
          "Скопируйте запрос ниже, вставьте его в Codex, замените две части в квадратных скобках своими путями и отправьте.",
          "Начните **новый разговор в том же проекте**. Откройте **Skills** на боковой панели и проверьте, что там семь скиллов из списка ниже. Если их нет, закройте и снова откройте приложение."
        ],
        "zip": "Скачать {file}",
        "checksums": "Скачать {file} (контрольные суммы)",
        "releasePage": "Открыть страницу выпуска",
        "promptLabel": "Запрос для Codex",
        "prompt": "Я устанавливаю German Business Kit в этот локальный проект Business Assistant в Codex. ZIP находится по пути [полный путь к ZIP], а SHA256SUMS — по пути [полный путь к файлу контрольных сумм]. Проверь ZIP по контрольной сумме и остановись, если она не совпадает. Распакуй архив в новую папку, затем скопируй все семь полных папок скиллов в .agents/skills этого проекта. Используй обычные файловые инструменты, сохраняй существующие файлы и остановись, если папка назначения уже существует. Не устанавливай среды выполнения, не меняй настройки безопасности и глобальную конфигурацию приложения. Назови семь установленных скиллов и объясни, как начать новый разговор.",
        "checksumNote": "Файл контрольных сумм позволяет Codex проверить, что загрузка полная и не изменена. Он не доказывает, кто опубликовал файл.",
        "manual": "Codex не смог скопировать файлы? Выполните ручные шаги из инструкции по установке.",
        "diagram": ["Папка проекта", "Скачать", "Попросить Codex", "Новый разговор"]
      }
    },
    "demos": {
      "title": "Попробуйте первые задачи на вымышленных примерах",
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
          "title": "Ваш первый шаг",
          "summary": "Попросите один небольшой следующий шаг для вымышленного нового бизнеса.",
          "time": "Около 5 минут",
          "prepare": ["Начните **новую задачу** в Claude или **новый разговор** в проекте Business Assistant в Codex. Папка не нужна."],
          "prompt": "Используй de-business-kit. Я пробую ассистента на вымышленном примере: хочу начать работать переводчиком-фрилансером в Германии. Не знаю, с чего начать. Помоги выбрать один небольшой первый шаг. Спрашивай только то, что нужно для этого шага.",
          "answers": "Это вымышленный пример. Я живу в Берлине, ещё ничего не регистрировал(а) и жду первого клиента в следующем месяце.",
          "check": [
            "Один понятный следующий шаг, а не длинная лекция.",
            "Вопросы только там, где действительно нужен факт.",
            "Пока нет просьбы загрузить личные документы или выбрать бухгалтерскую программу.",
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
          "prompt": "Используй de-business-accounting. Это вымышленное учебное упражнение. Используй только выбранную папку Учебный бизнес. Создай три вымышленных чека за ноябрь 2026 года для переводчика: бумага для принтера 23,80 EUR, билет на поезд к клиенту 49,00 EUR и подписка на программу 11,90 EUR. Разбери их для моего первого месяца, покажи, что ещё неясно, и сохрани короткую понятную сводку со следующим шагом. Не используй настоящие данные и не подключай никакие сервисы.",
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
          "prompt": "Используй de-business-operations. Вымышленный пример: подготовь черновик счёта за выполненный перевод. Клиент: Beispiel Verlag GmbH (вымышленный). Услуга: перевод 10-страничной брошюры с английского на немецкий, выполнен 3 ноября 2026 года. Согласованная цена: 400 EUR. В этом примере я Kleinunternehmer. Для моего адреса, налогового номера и банковских данных используй явно помеченные заполнители. Ничего не отправляй.",
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
      "start": "Einrichtung starten",
      "copy": "Kopieren",
      "copied": "Kopiert. Fügen Sie es mit Strg+V (Windows) oder Cmd+V (Mac) ein.",
      "copyFailed": "Automatisches Kopieren war nicht möglich. Markieren Sie den Text und drücken Sie Strg+C (Windows) oder Cmd+C (Mac).",
      "newTab": "öffnet in einem neuen Tab",
      "done": "erledigt",
      "checklist": "Haken Sie jeden Schritt ab, wenn er erledigt ist.",
      "saved": "Ihr Fortschritt wird nur in diesem Browser auf diesem Computer gespeichert.",
      "notSaved": "Dieser Browser erlaubt kein Speichern des Fortschritts. Lassen Sie diese Seite bis zum Ende geöffnet.",
      "checked": "Anbieterangaben geprüft am {date}. Tarife, Preise und Menüs können sich ändern; maßgeblich ist die Seite des Anbieters.",
      "safety": "Diese Anleitung fragt nie nach Passwörtern, Zahlungsdaten, Bestätigungscodes oder Schlüsseln. Geben Sie diese nur auf der Website oder in der App des Anbieters ein.",
      "illustration": "Schema. Echte Bildschirme können anders aussehen.",
      "chooseFirst": "Wählen Sie zuerst Ihren Assistenten.",
      "mobile": "Für die Einrichtung brauchen Sie einen Windows-PC oder einen Mac. Öffnen Sie diese Anleitung auf Ihrem Computer, um die App zu installieren.",
      "footer": "German Business Kit ist KI-gestützte Selbsthilfe-Software und keine Steuerberatung. Diese Seite sendet nichts; Links öffnen offizielle Websites nur, wenn Sie sie auswählen."
    },
    "steps": {"welcome": "Start", "assistant": "Assistent", "account": "Konto", "app": "App", "skills": "Skills", "demos": "Erste Aufgaben"},
    "welcome": {
      "eyebrow": "Geführte Einrichtung · etwa 30 Minuten",
      "title": "Richten Sie Ihren KI-Assistenten für Ihr Unternehmen Schritt für Schritt ein",
      "lead": "Diese Anleitung hilft Ihnen, ein Konto bei Claude oder ChatGPT anzulegen, die App zu installieren, German Business Kit hinzuzufügen und erste Aufgaben mit erfundenen Beispielen auszuprobieren. Programmierkenntnisse brauchen Sie nicht.",
      "chooseLanguage": "Sprache wählen",
      "languageHint": "Sie können die Sprache jederzeit oben auf der Seite ändern.",
      "needTitle": "Das brauchen Sie",
      "need": [
        "Einen Windows-PC oder Mac mit Internetzugang.",
        "Eine E-Mail-Adresse, die Sie jetzt abrufen können.",
        "Ein Mobiltelefon, das SMS empfangen kann.",
        "Für einen kostenpflichtigen Tarif: eine Bankkarte. Sie geben sie nur auf der Website des Anbieters ein, niemals hier."
      ],
      "aiTitle": "Gut zu wissen vor dem Start",
      "ai": "German Business Kit ist KI-gestützte Selbsthilfe-Software und kein Steuerberater. KI kann sich irren, auch bei Beträgen und Fristen. Dateien, die der Assistent liest, werden von Anthropic oder OpenAI verarbeitet. Verwenden Sie erfundene Beispiele, bis Sie die Hinweise zu Ihren Daten gelesen haben.",
      "aiLink": "KI-Grenzen und Ihre Daten (auf Englisch)"
    },
    "assistant": {
      "title": "Wählen Sie Ihren Assistenten",
      "lead": "German Business Kit arbeitet in einer von zwei KI-Apps. Beide schaffen die Aufgaben in dieser Anleitung. Wählen Sie, was Ihnen lieber ist; die andere App können Sie später einrichten.",
      "choose": "{name} wählen",
      "chosen": "Ausgewählt",
      "unsure": "Unsicher? Wählen Sie **Claude** für die wenigsten Einrichtungsschritte, wenn ein kostenpflichtiger Tarif für Sie passt. Wählen Sie **ChatGPT mit Codex**, wenn Sie kostenlos beginnen möchten.",
      "work": "Nutzen Sie ein Konto Ihres Arbeitgebers oder Ihrer Hochschule? Die Verwaltung kann Apps, Plugins oder Skills sperren. Fragen Sie zuerst dort nach.",
      "claude": {
        "name": "Claude",
        "maker": "von Anthropic",
        "app": "Claude-Desktop-App mit Cowork",
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
        "pricing": "ChatGPT: Tarife und Preise",
        "points": [
          "Sie können mit jedem Tarif beginnen, auch mit **Free**. Kostenpflichtige Tarife bieten mehr Nutzung.",
          "Mehr Einrichtungsschritte: Sie laden eine Datei herunter, und Codex kopiert das Kit in einen Projektordner.",
          "Arbeitet mit den Dateien in einem Projektordner auf Ihrem Computer."
        ]
      }
    },
    "account": {
      "lead": "Die Registrierung erfolgt auf der Website des Anbieters. Diese Anleitung öffnet nur die offizielle Seite in einem neuen Tab.",
      "labelsNote": "Schaltflächen können je nach Sprache oder App-Version anders heißen.",
      "already": "Sie haben schon ein Konto? Haken Sie die erledigten Schritte ab und machen Sie weiter.",
      "safetyTitle": "So bleibt Ihr Konto sicher",
      "safety": [
        "Geben Sie Passwörter, Codes und Kartendaten nur auf der Seite oder in der App des Anbieters ein.",
        "Niemand aus diesem Projekt fragt Sie nach Codes oder Passwörtern.",
        "Prüfen Sie die Adresszeile: **claude.ai** oder **claude.com** für Claude, **chatgpt.com** oder **openai.com** für ChatGPT."
      ],
      "claude": {
        "title": "Legen Sie Ihr Claude-Konto an",
        "open": "Offizielle Claude-Registrierung öffnen",
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
        "steps": [
          "Wählen Sie auf der offiziellen Seite **Sign up** (**Registrieren**). Verwenden Sie Ihre E-Mail-Adresse oder eine der Anmeldeoptionen auf der Seite.",
          "Folgen Sie den Schritten auf der Seite, um Ihre E-Mail-Adresse zu bestätigen.",
          "Beim ersten Start von Codex kann die App Sie bitten, eine Telefonnummer hinzuzufügen oder zu bestätigen. Tun Sie das nur in der ChatGPT-App oder auf chatgpt.com.",
          "Wählen Sie einen Tarif. **Free** reicht zum Ausprobieren; **Plus** oder höher bietet mehr Codex-Nutzung. Bezahlen Sie nur auf der Website von OpenAI."
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
        "lead": "Das Kit ist ein Plugin mit sieben verbundenen Skills. Sie fügen es einmal hinzu; es wird in Ihrem Claude-Konto gespeichert und funktioniert auch im Claude-Chat und in Claude Code.",
        "steps": [
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
        "diagram": ["Customize", "Plugins", "Add marketplace", "Install"]
      },
      "openai": {
        "title": "Fügen Sie German Business Kit zu Codex hinzu",
        "lead": "In Codex wird das Kit in einen Projektordner auf Ihrem Computer kopiert. Nach dem Herunterladen kann Codex das Kopieren für Sie erledigen.",
        "steps": [
          "Legen Sie an einem privaten Ort, zum Beispiel unter Dokumente, einen neuen Ordner **Business Assistant** an. Er enthält nur das Kit, nicht Ihre Geschäftsunterlagen.",
          "Wählen Sie in der ChatGPT-App **Codex**, öffnen Sie den Ordner **Business Assistant** als Projekt und starten Sie einen **New chat** (neuen Chat). Werden Sie gefragt, ob Sie einem Ordner vertrauen, bestätigen Sie nur diesen.",
          "Laden Sie diese zwei Dateien in denselben Ordner herunter, zum Beispiel Downloads.",
          "Kopieren Sie den vollständigen Pfad jeder Datei. Windows: Rechtsklick auf die Datei und **Als Pfad kopieren** wählen. Mac: Datei im Finder auswählen, die **Wahltaste (Option)** gedrückt halten und **Bearbeiten → „…“ als Pfadname kopieren** wählen.",
          "Kopieren Sie die Anfrage unten, fügen Sie sie in Codex ein, ersetzen Sie die zwei Teile in eckigen Klammern durch Ihre Pfade und senden Sie sie.",
          "Starten Sie einen **neuen Chat im selben Projekt**. Öffnen Sie **Skills** in der Seitenleiste und prüfen Sie, dass die sieben Skills unten aufgeführt sind. Fehlen sie, schließen Sie die App und öffnen Sie sie erneut."
        ],
        "zip": "{file} herunterladen",
        "checksums": "{file} herunterladen (Prüfsummenliste)",
        "releasePage": "Veröffentlichungsseite öffnen",
        "promptLabel": "Anfrage für Codex",
        "prompt": "Ich richte German Business Kit in diesem lokalen Projekt Business Assistant in Codex ein. Mein ZIP liegt unter [vollständiger ZIP-Pfad] und SHA256SUMS unter [vollständiger Pfad der Prüfsummendatei]. Prüfe das ZIP anhand der Prüfsumme und brich ab, wenn sie nicht übereinstimmt. Entpacke es in einen neuen Ordner und kopiere dann alle sieben vollständigen Skill-Ordner in .agents/skills dieses Projekts. Verwende normale Dateiwerkzeuge, erhalte vorhandene Dateien und brich ab, wenn ein Zielordner bereits existiert. Installiere keine Laufzeitumgebungen und ändere weder Sicherheitseinstellungen noch die globale App-Konfiguration. Nenne mir die sieben installierten Namen und erkläre, wie ich eine neue Sitzung starte.",
        "checksumNote": "Mit der Prüfsummenliste kann Codex prüfen, ob der Download vollständig und unverändert ist. Sie beweist nicht, wer die Datei veröffentlicht hat.",
        "manual": "Codex konnte die Dateien nicht kopieren? Folgen Sie den manuellen Schritten in der Installationsanleitung (auf Englisch).",
        "diagram": ["Projektordner", "Herunterladen", "Codex fragen", "Neuer Chat"]
      }
    },
    "demos": {
      "title": "Probieren Sie erste Aufgaben mit erfundenen Beispielen aus",
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
          "title": "Ihr erster Schritt",
          "summary": "Fragen Sie nach einem kleinen nächsten Schritt für ein erfundenes neues Unternehmen.",
          "time": "Etwa 5 Minuten",
          "prepare": ["Starten Sie eine **neue Aufgabe** in Claude oder einen **neuen Chat** in Ihrem Projekt Business Assistant in Codex. Ein Ordner ist nicht nötig."],
          "prompt": "Nutze de-business-kit. Ich probiere den Assistenten mit einem erfundenen Beispiel aus: Ich möchte in Deutschland freiberuflich Übersetzungen anbieten. Ich weiß nicht, wo ich anfangen soll. Hilf mir, einen kleinen ersten Schritt zu wählen. Frag nur, was du für diesen Schritt brauchst.",
          "answers": "Das ist ein erfundenes Beispiel. Ich wohne in Berlin, habe noch nichts angemeldet und erwarte meinen ersten Auftrag im nächsten Monat.",
          "check": [
            "Ein verständlicher nächster Schritt statt eines langen Vortrags.",
            "Rückfragen nur, wo eine Angabe wirklich nötig ist.",
            "Noch keine Bitte, private Unterlagen hochzuladen oder eine Buchhaltungssoftware zu wählen.",
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
          "prompt": "Nutze de-business-accounting. Das ist eine erfundene Übung. Verwende nur meinen ausgewählten Ordner Übungsfirma. Lege drei erfundene Belege aus November 2026 für eine Übersetzungstätigkeit an: Druckerpapier 23,80 EUR, Bahnfahrt zu einem Kunden 49,00 EUR und ein Software-Abo 11,90 EUR. Ordne sie für meinen ersten Monat, zeige, was noch unklar ist, und speichere eine kurze lesbare Zusammenfassung mit dem nächsten Schritt. Verwende keine echten Daten und verbinde keinen Dienst.",
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
          "prompt": "Nutze de-business-operations. Erfundenes Beispiel: Bereite einen Rechnungsentwurf für eine erledigte Übersetzung vor. Kunde: Beispiel Verlag GmbH (erfunden). Leistung: Übersetzung einer 10-seitigen Broschüre aus dem Englischen ins Deutsche, geliefert am 3. November 2026. Vereinbarter Preis: 400 EUR. In diesem Beispiel bin ich Kleinunternehmer. Verwende deutlich markierte Platzhalter für meine Anschrift, Steuernummer und Bankverbindung. Versende nichts.",
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
