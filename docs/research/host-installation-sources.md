> Dated research, not current implementation status. Original source-check dates are retained. See [current status](../project-status.md) for delivery and acceptance.

# Host installation evidence — 2026-10-26

Maintainer research for the beginner installation guides. Checked against the
linked provider documents on **2026-10-26**; these are documentation findings,
not completed desktop installations or account acceptance tests. No host was
installed, account changed, or global setting edited during this research.

## Recommendation and terminology

Prefer a provider's desktop interface for someone starting without terminal
experience, then a project-scoped copy of this repository's complete seven-skill
bundle. This is an editorial recommendation, based on the documented local
folder and skill support below; it does not establish that the complete beginner
journey has passed on either operating system.

- **Codex** is OpenAI's agent for working with local files and commands. Its CLI
  runs in a terminal. The current official desktop documentation calls the host
  the **ChatGPT desktop app**, with a choice of ChatGPT or Codex. Older download
  and introduction pages still say **Codex app**. Guide readers to the official
  download and the Codex experience they actually see rather than promising an
  identical standalone app name on every machine.
- **Claude Code** is Anthropic's local agent, available in the Claude desktop
  app's **Code** tab and as a separately installed terminal CLI. Ordinary Claude
  chat and **Cowork** are separate surfaces with different skill discovery.
- Installing a host and installing German Business Kit are separate steps. A
  provider account, a supported computer and internet access remain necessary;
  installing these skills supplies no subscription, API credits or connectors.

## OpenAI: desktop, sign-in and local skills

| Primary source | Checked claim | Consequence for the guide |
| --- | --- | --- |
| [Desktop documentation](https://developers.openai.com/codex/app/) → [current app page](https://learn.chatgpt.com/docs/app), also read as its official `.md` representation | The former Codex app URL redirects to ChatGPT desktop documentation. The quickstart says to download for macOS/Windows, open the app, sign in with a ChatGPT account, open a folder or project, choose ChatGPT or Codex, and start a Codex **New chat**. | Account sign-in is the beginner route; do not require an API key. Explain that an opened local folder supplies the working location. The source does not establish one universal folder-selector button label. |
| [Windows desktop documentation](https://learn.chatgpt.com/docs/app/windows) | Windows uses a native agent with PowerShell by default; WSL is another configuration. The page documents **Add new project** or **Ctrl+O** for opening a WSL folder. | A beginner with native Windows folders need not install WSL. Do not turn the WSL-specific selector example into an assertion about every desktop layout. |
| [Codex account availability](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) | The current help page includes Codex across ChatGPT plans, including Free and Go, with usage limits varying by plan. Codex Cloud has separate eligibility and workspace restrictions. | Say that access and limits depend on the current account/plan and workspace policy. Do not promise unlimited or permanently free use, or require buying a particular plan without checking the reader's account. No price amount is established here. |
| [Local skill discovery](https://developers.openai.com/codex/skills/) → [Build skills](https://learn.chatgpt.com/docs/build-skills) | Standalone skills work in the desktop app, CLI and IDE extension. Codex reads `.agents/skills` at the working directory and up through a Git repository; `~/.agents/skills` is user-wide. The docs support symlinks, **Skills** in the desktop sidebar, `/skills` or `$` in CLI/IDE, and restarting if changes do not appear. | Use `<project>/.agents/skills/<skill>/SKILL.md` for this guide's bounded local route. Copy complete sibling directories, preserving references/assets/scripts. Do not call project installation account-wide or cloud installation. A fresh host session and actual skill listing are acceptance steps. |

The official skill docs describe skills as instructions/resources with optional
scripts, automatically chosen when relevant or explicitly invoked. Recognition
in a skill picker proves discovery, not correct business advice, working utility
execution or a successful tax submission. The repository's catalog, not provider
docs, establishes the seven members:
[`skill-set.json`](../../skills/de-business-kit/assets/skill-set.json).

## OpenAI: optional terminal and local plugin routes

- [CLI installation](https://developers.openai.com/codex/cli/) redirects to
  [current CLI docs](https://learn.chatgpt.com/docs/codex/cli). Read the official
  [Markdown representation](https://learn.chatgpt.com/docs/codex/cli.md) for all
  installation tabs. It documents standalone macOS/Linux and Windows installers,
  npm (`npm install -g @openai/codex`), and Homebrew. Launch `codex` from the
  project directory and choose **Sign in with ChatGPT** on first launch. The
  Windows standalone example contains an execution-policy bypass; repository
  rules prohibit prescribing such bypasses. Keep desktop installation primary;
  do not silently install Node.js merely to make the npm alternative work.
- [Official plugin packaging/local marketplace guidance](https://developers.openai.com/plugins/build/plugins)
  supports `codex plugin marketplace add ./local-marketplace-root`, but instructs
  users to install/test a local plugin in the desktop app. It documents a
  repository catalog at `.agents/plugins/marketplace.json`, restarting the app,
  opening **Plugins Directory**, selecting the marketplace and installing its
  plugin. A catalog entry makes a plugin discoverable; it does not by itself
  install/enable it. This is a supported advanced route, not evidence that a ZIP
  can be directly uploaded or that a GUI can select any arbitrary local folder.

## Anthropic: desktop and local skills

| Primary source | Checked claim | Consequence for the guide |
| --- | --- | --- |
| [Desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart) | Download/run the appropriate installer, launch Claude from Applications on macOS or Start on Windows, sign in, and open **Code** at the top of the sidebar. Claude Code requires Pro, Max, Team or Enterprise. Desktop includes Claude Code; neither Node.js nor the CLI is needed. In the current layout, select the top **Local** environment, then the project folder control → **Open folder…**. An earlier layout is documented separately. | This is the clearest documented beginner GUI route. Link official downloads from this page rather than pinning architecture-specific binary URLs. No API key is required for this subscription sign-in route. Do not promise the free chat plan unlocks Code. Explain layouts can differ. |
| [Desktop installation requirements](https://support.claude.com/en/articles/10065433-install-claude-desktop) | Desktop is available on macOS 13+ and Windows 10+; the page distinguishes Chat, Code and Cowork availability by plan. | Check the host's actual OS and plan before continuing. Ability to open Claude chat does not prove Code access. |
| [Desktop skill/plugin reference](https://code.claude.com/docs/en/desktop#use-skills) | In Code, type `/` or use **+ → Slash commands** to browse available commands/skills, including project skills. Local sessions read personal `~/.claude/skills/`. **+ → Add plugins** opens the plugin browser; another layout uses **Plugins → Browse plugins**. Desktop plugins support user, project or local-only scopes. | Use the skill browser as a discovery check. Avoid silently selecting a cloud, SSH or WSL environment for a private native folder. |
| [Skill location contract](https://code.claude.com/docs/en/skills#choose-where-skills-load) | Project skills are `.claude/skills/<skill-name>/SKILL.md`; personal skills are `~/.claude/skills/`. Local project and personal skills differ from account-synced skills. Cowork/cloud do not read the machine's personal skill directory. Plugins namespace commands as `/plugin-name:skill-name`. | Use `<project>/.claude/skills/` for all seven sibling skill directories. For a standalone installation, invoke `/de-business-kit`; for the packaged plugin, use `/de-business-kit:de-business-kit`. Do not describe local project copying as installing into Claude chat or Cowork. |

## Anthropic: optional terminal and plugin routes

- [CLI quickstart](https://code.claude.com/docs/en/quickstart) documents native
  install commands for macOS (`curl -fsSL https://claude.ai/install.sh | bash`)
  and Windows PowerShell (`irm https://claude.ai/install.ps1 | iex`). Then open a
  terminal in the project and run `claude`. This route is optional for a desktop
  Code user; installing the desktop app does not provide a terminal command.
- [Advanced setup](https://code.claude.com/docs/en/setup) gives CLI requirements:
  macOS 13+, Windows 10 1809+/Server 2019+, x64/ARM64, 4 GB+ RAM, internet and a
  supported country. Native Windows needs no administrator installation. Git for
  Windows is optional; without it Claude Code uses the PowerShell tool. Do not
  repeat older claims that native Claude Code always requires Git Bash or WSL.
- [Authentication](https://code.claude.com/docs/en/authentication) describes browser
  sign-in on first CLI launch with an eligible Claude subscription, team account,
  Console account or supported provider. The ordinary subscription route does not
  require creating an API key. Authentication details and credentials belong in
  provider sign-in screens, not business chat prompts.
- [Install/manage plugins](https://code.claude.com/docs/en/discover-plugins) supports
  a local marketplace via `/plugin marketplace add` plus the directory containing
  `.claude-plugin/marketplace.json`. The desktop plugin browser supports choosing
  a project/local-only scope. The same page documents CLI
  `claude plugin install <plugin>@<marketplace> --scope project`; do not rely on
  the default scope. Local marketplace registration is documented as a command;
  no verified graphical local-directory picker was established in this research.

## Acceptance boundaries and unresolved details

The expected first run for this project is a fresh local session in the intended
folder, discovery of all seven catalog skills, explicit invocation of
`de-business-kit`, and a guided reply that asks for unknown business facts rather
than inventing them. This is a proposed acceptance check, not a completed model
trial. Installation must preserve the existing private workspace and should not
create tax facts, post records, connect banking or submit anything to an authority.

No exact OpenAI desktop minimum OS/CPU requirement was established from the pages
above; follow the live official download's compatibility information rather than
copying requirements from an older ChatGPT or Codex release. No signed-in desktop
screens, fresh Windows/macOS account setup, local GUI marketplace selection or
end-to-end seven-skill invocation was exercised here. Provider policy can hide or
disable skills/plugins. Source review and package validation cannot establish
native desktop acceptance or current account entitlement.

## Guide artwork and review

The guide includes editable `setup-map.en.svg` and `setup-map.ru.svg` diagrams,
plus `entrepreneur-journey.png`, generated with the built-in imagegen tool on
2026-10-26 and visually inspected. All three assets ship inside the shared skill.
They are illustrations, not screenshots, installation recordings or evidence of
host acceptance. No real business records or account screens were used.

Generation prompt:

> Create a refined, friendly editorial illustration for the beginner guide of German Business Kit, a set of AI assistant skills helping a solo entrepreneur in Germany. Landscape 3:2 composition, ivory background, deep navy, muted teal and warm coral accents, simple flat vector-like shapes with gentle texture, generous whitespace. On left a person at an open laptop; center seven small distinct cards arranged as a path (lightbulb, signpost, document, receipt, calendar, service connection, growing plant); right organized folders and a small completed checklist. Calm, approachable, practical, not futuristic. No text, no letters, no logos, no app screenshots, no money values, no government seals. Avoid robot imagery. This is explicitly an illustration, not a mockup of any software interface.

Independent review confirmed the documented desktop **Skills** sidebar in the
OpenAI source and the Claude Code local project path/invocation. The copied setup
request pins the expected repository, release tag and verification procedure.
Current guide source is newer than immutable 0.8.0-preview.1; no published archive
was replaced to add these materials.


## Explicit invocation and current host distinctions — 2026-10-26

This additional source check supports the simplified prompt examples. It is
provider-documentation research, not an observed desktop invocation or install.
Earlier findings above retain their original scope.

| Host | Documented route | Practical guide consequence |
| --- | --- | --- |
| Claude chat and Cowork | [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) documents typing `/` or opening `+` to see plugin skills in both surfaces. | Select `de-business-kit` from **German Business Kit**, then add the task. Selection avoids guessing how a particular app version displays the plugin namespace. |
| Claude chat and Claude Code | [Plugin overview](https://claude.com/docs/plugins/overview) documents filtering chat's `/` menu by `plugin-name:skill-name`; Code accepts `/plugin-name:skill-name`. Cowork's typed example is `/plugin-name:command`, alongside automatic skill selection. | For this manifest, the Code plugin invocation is `/de-business-kit:de-business-kit`. Do not present `/de-business-kit` as the universal plugin command. Use the Cowork picker for explicit skill selection. |
| Codex and ChatGPT desktop | [Build skills](https://learn.chatgpt.com/docs/build-skills) documents the desktop **Skills** sidebar. Its explicit selector instructions distinguish ChatGPT (`@`) from Codex CLI/IDE (`/skills` or `$`). The same page gives `$skill-creator` as a Codex invocation and says explicit `$skill` invocation works. | Show the skill's name and a plain-language request to use it. If documenting `$de-business-kit`, identify it as Codex syntax; do not promise `$` autocomplete or `/skills` in every desktop version. A ChatGPT `@` instruction must not be relabelled as a Codex desktop instruction. |

When the picker does not list the skill, check that the complete bundle is
installed/enabled in the intended host and project, start a fresh task, and
restart if necessary. A sentence such as “Use de-business-kit” requests the
installed skill; it cannot install missing instructions or prove discovery.
OpenAI's source explicitly recommends restarting Codex if a skill change does
not appear. The existing installation checks remain necessary.

The same-account Claude plugin-sync claim is supported, with qualifications:
[Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
requires Claude Code **2.1.273 or newer**, Claude account sign-in and plugin sync
to be enabled; API-key and cloud-provider sign-in do not receive account plugins.
The [overview](https://claude.com/docs/plugins/overview) scopes installation to
the current account's organization and distinguishes account-installed plugins
from machine-local CLI installation. Preserve these distinctions in technical
help; do not imply that copying local skill folders syncs them to an account.

Paid-plan guidance remains supported: the plugin help page lists Pro, Max, Team
and Enterprise. [Cowork getting started](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)
also lists paid plans, describes a rolling unified Chat/Cowork interface and
desktop local-file access alongside cloud sessions. Consequently a separate
**Cowork** selector may be absent, and a folder-based journey must verify access
to the intended folder. These sources do not justify assuming that every
Cowork session is a particular Linux VM or can run this kit's Python writers.

## Actual Claude dialog capture — 2026-10-26

Observed in the installed **Claude Desktop 3.6556.2** on macOS using native UI
controls: **Customize → Plugins → Add → Add marketplace → Add from a repository**.
The repository selector accepted the project's public GitHub URL; selecting
**Use …** left a **Sync** button available. The
[unmodified screenshot](../../skills/de-business-kit/guides/images/claude-marketplace.jpg)
was captured at that point, with the personal sidebar hidden and the repository
suggestions closed. The dialog was then cancelled and the sidebar restored.
No Sync, marketplace addition or plugin installation was performed. This is
visual evidence of the entry screen on this host/version, not proof of discovery,
installation, account eligibility or a complete beginner journey. The EN/RU
installation text now includes the observed repository-choice and Sync steps;
other versions may use different labels.

## Capable models and reasoning effort — 2026-10-26

Checked current primary sources on **2026-10-26** for the maintainer's requested
recommendation: use a capable reasoning model for complex business work, with
**Claude Opus 5.5 + High effort** or **GPT-6 Astra + High reasoning effort** as
examples when the user's actual host/account offers them. This is a product
recommendation, not a German Business Kit benchmark or a claim that model choice
establishes accounting/tax correctness.

| Primary source | Checked claim | Practical guide consequence |
| --- | --- | --- |
| [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5) | Confirms the model name and release; Anthropic says it is available across platforms. | Name Opus 5.5 as an example, while checking the user's actual account rather than promising universal access. |
| [Change the model, effort, and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings) | Explicitly includes Opus 5.5 among models with an effort selector; documents model menu beside Send → **Effort** → choose a level. **High** balances quality and speed; higher effort takes longer and consumes more usage. Enterprise administrators can restrict model/effort access. | Recommend **High** for demanding tasks and explain the time/usage tradeoff. Do not infer that typing “think harder” changes the setting. Routine tasks can use a lower effort. |
| [Claude Academy: effort for Cowork and chat](https://academy.claude.com/tutorials/how-to-select-the-right-effort-setting-for-claude-cowork-and-chat) | Explains effort in Chat/Cowork and its effect on checking, time and usage; points to the model menu's Effort control. | The effort advice applies to the conversational workflow, not only the API. Labels/layout can change; no new desktop selection was performed in this research. |
| [Models for Work and Codex](https://learn.chatgpt.com/docs/models) | Documents the desktop model/reasoning control below the composer. A newer layout offers **Power → Advanced** for explicit model/effort choice. Astra is listed for complex work; access depends on rollout, sign-in and client. Higher effort takes longer and uses more tokens. | Tell users to choose Astra and **High** where offered; use the actual model/settings controls rather than hardcoding one universal UI path. |
| [GPT-6 Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra) and [ChatGPT model availability](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt) | Astra supports `high` reasoning effort in the API. The Help Center describes Astra in Work/Codex on eligible plans and account/workspace restrictions. Chat's generic GPT-6 **High** can use Sol, while Chat's Pro option uses Astra. | Do not equate Chat's generic High with Astra, or use API support as proof of every desktop account's picker. State both the model and effort, qualified by availability. |

No model, effort, plan or application setting was changed. Exact UI selection and
availability were not exercised on a new host during this source check. The
recommendation does not replace task prerequisites, current official-source
research, executed calculations or independent checks; the skill cannot certify
or silently change its host model. Avoid adding a model-selection gate to every
simple question or claiming that more effort guarantees a correct result.

## AI limitations and provider data processing — 2026-10-26

Checked primary sources on **2026-10-26** for a visible user notice. The practical
message is that the kit supplies AI instructions and preparation, not a licensed
Steuerberater relationship or a guarantee of correct calculations, deadlines or
filings. Users should review consequential results and obtain qualified help for
a specific unresolved professional issue. A disclaimer does not grant permission
to provide regulated individual advice to others: [StBerG §2](https://www.gesetze-im-internet.de/stberg/__2.html)
addresses authorized businesslike assistance in other people's tax affairs,
including unpaid activity. This source check is not a legal review of every
possible use of the project.

| Primary source | Checked claim | Practical notice consequence |
| --- | --- | --- |
| [OpenAI data controls](https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt) | Personal Free/Plus/Pro workspaces have model-improvement sharing enabled by default. Disabling **Improve the model for everyone** excludes new ChatGPT conversations and Codex tasks from training. Codex **Include environments** is a separate setting. Disabling training does not delete saved chats. | Tell personal-account users to inspect both the account control and relevant Codex environment-sharing control. Do not describe a paid personal subscription as business privacy. |
| [OpenAI business data](https://openai.com/business-data/) and [API data controls](https://developers.openai.com/api/docs/guides/your-data) | Business/Enterprise and API inputs/outputs are not used for model training by default; explicit sharing opt-in can change this. API abuse monitoring and application state can retain content, with feature-specific controls and eligibility requirements. | Distinguish no training from no processing, storage, safety review or retention. Check the actual workspace, contract, feature and settings; API conditions do not automatically apply to a personal desktop account. |
| [OpenAI DPA](https://openai.com/policies/data-processing-addendum/) | The DPA supplements the Services Agreement for processing customer data on the customer's behalf. It includes customer responsibilities and transfer safeguards. | Check that the applicable service/contract covers the intended processing; a DPA alone does not establish a lawful purpose or settle all GDPR obligations. |
| [Anthropic consumer training](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training) | Consumer Free/Pro/Max use, including Claude Code under those accounts, follows the user's model-improvement choice. Safety-review and other explicit opt-in/feedback routes have additional provisions. | Ask users to inspect **Privacy** settings before real documents; do not promise that consumer content can never be used for training or review. |
| [Anthropic commercial training](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training) and [Claude Code data usage](https://code.claude.com/docs/en/data-usage) | Commercial Work/API content is not used for training by default; explicit feedback/reporting or other opted-in sharing can permit use. Retention and local session logs are distinct from training settings. Claude Code sends prompts and outputs over the network even when tools run locally. | Qualify the commercial default, warn that submitted feedback can include conversation content, and distinguish local files from local-only AI processing. |
| [Anthropic DPA](https://support.claude.com/en/articles/7996862-how-do-i-view-and-sign-your-data-processing-addendum-dpa) | Anthropic's DPA and SCCs are incorporated into its Commercial Terms; third-party platform access follows that platform's terms. | Check the actual account and service route. Do not assume Free/Pro/Max has the same processor contract as commercial/API service. |
| [Cowork architecture](https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview) | Current Cowork sessions run in the cloud by default; sessions and files are saved to the Claude account. Existing local deployments have a different execution route. | Explain what is actually shared before access to real files. A private folder on the computer does not imply that prompts, extracted content, screenshots or outputs remain on that computer. |
| [Claude connector privacy](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities) | Connected services process data on their own infrastructure under their own terms. Claude inference-residency settings do not control third-party infrastructure. | Include connected services in the data-flow explanation; review their access, terms and retention separately. |

Keep the beginner notice short: AI can make mistakes; review drafts, figures,
periods and deadlines; share only necessary material; check the actual provider,
plan, training/retention settings and relevant processing agreement before real
client/employee data. Prefer fictional or locally redacted examples while the
route is unresolved. Redacting after a full file has entered model context does
not undo disclosure. Never request passwords, tax-portal certificates, API keys
or TANs in chat. These precautions support useful self-help without requiring a
blanket risk-acceptance checkbox or compulsory adviser handoff for every task.

No user account, privacy setting, contract or live document processing was
inspected or changed in this source check. No universal retention duration,
EU-only processing promise or automatic GDPR-compliance claim is established.

## Optional browser and computer assistance — 2026-10-26

Checked current provider documentation on **2026-10-26** after inspecting the
host/tool instructions available in this maintenance session. This session exposes
native CUA and Playwright browser operations, but that inventory establishes only
this host's capabilities. An installed skill is instructions, not an enabled
browser, a site login, a tool permission or evidence that upload/download works.
The existing [assisted-service contract](../../skills/de-business-kit/references/assisted-services.md)
already distinguishes connection, browser, desktop and guided-manual routes.

| Primary source | Checked route and setup | Consequence for business-user guidance |
| --- | --- | --- |
| [OpenAI built-in Browser](https://learn.chatgpt.com/docs/browser) | Desktop Work/Codex can open, inspect, click and type in the built-in browser; invoke with **@Browser**. It is included with the app. Its profile is separate from the user's regular browser. **Settings → Browser → Agent permissions** controls browsing/downloads/site exceptions. The documentation says automated file uploads are unavailable in this browser. | Offer the built-in browser when available for an appropriate page/draft and inspect the actual result. Prepare a user upload step when needed; do not advertise automatic upload merely because the browser can type. Rollout/admin restrictions can affect availability. |
| [OpenAI browser extension](https://learn.chatgpt.com/docs/chrome-extension) | Supported desktop browsers include Chrome, Edge, Brave, Opera and Vivaldi. In **Settings → Computer Use**, select the browser, follow the plugin prompt, select **Install** for its official extension, return to confirm **Manage**, and start Work/Codex with the browser **@** mention. Use the profile containing the extension. | This is an optional route to existing signed-in tabs, not a requirement for all kit users. Review requested site permissions; do not silently enable broad all-site access. |
| [OpenAI Computer Use](https://learn.chatgpt.com/docs/computer-use) | In supported regions on macOS/Windows, Work/Codex offers **Plugins → Computer Use → Install plugin/Enable**; turn on its server and skill toggles, then **Try now**. Review app access in **Settings → Computer use**. macOS requires prompted Screen Recording/Accessibility permissions; Windows operates on the active visible desktop. | Native UI control is optional for installed apps or workflows without a suitable structured/browser route. The user must review actual permissions; kit installation does not grant them. Availability and admin controls must be checked locally. |
| [Claude built-in Cowork browser](https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork) | Cowork has an interactive browser in Desktop, with no extension installation. The app must be open/online. The documented platform scope includes macOS/Windows and Linux beta, paid plans and organization controls. **Settings → Cowork → Preferred browser** chooses **Built-in browser** or **Chrome (Claude in Chrome)**. It has a separate profile unless logins are deliberately imported or entered. | Prefer an already available suitable browser over requiring Chrome. Check the actual account/rollout/owner restrictions. High-risk sites are blocked; Anthropic strongly advises against browser action involving financial accounts, medical information or other people's personal data. Do not position it as unrestricted bank/tax-portal automation. |
| [Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome) | Paid-plan extension for Google Chrome (not other Chromium browsers/mobile). Desktop setup: **Settings → Customize → Connectors → Claude in Chrome → Configure**, enable and install the official extension; enable it for the relevant conversation. Organization availability may require an owner. | Useful for an appropriate page already open in the user's signed-in Chrome profile. It is optional where the built-in browser suffices and does not bypass sensitive-site restrictions. |
| [Claude native computer use](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork) | Beta on Pro/Max in macOS/Windows Desktop Cowork/Code; current page says Team/Enterprise do not have native computer use. Update Desktop; **Settings → Capabilities**, or **Settings → System → This computer** if absent, then **Enable computer use**. App access is separately approved. Device must remain awake and Desktop open. | Distinguish native screen control from browser use. Anthropic advises against giving native control of banking, healthcare or government apps and against sensitive-data actions. Use another suitable route or guided manual steps instead of treating native control as a workaround for blocked browser access. |

For public research, web search retrieves current source information; it does not
establish interactive access to the user's selected page, saved draft, login,
upload control or export. A browser/computer helper skill can improve how existing
tools are used, but its presence does not grant those tools or permissions.

A practical setup request should name the target operation and user-held boundary:
“Use de-business-kit. Check whether this app can help with a fictional practice
form in the browser. Explain the supported setup and permissions if needed, fill
only the agreed draft fields, and show what you verified. I will handle login and
final submission.” For real operations, first check the provider's restrictions,
data-processing route and the actual site's behavior. Keep unsupported parts as
short user steps or selected-file work; never bypass a blocked site or security
control. No extension, plugin, permission, account or live form was changed in
this research; these are documented routes, not completed host acceptance trials.
