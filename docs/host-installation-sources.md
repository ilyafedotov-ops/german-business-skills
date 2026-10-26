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
[`skill-set.json`](../skills/de-business-kit/assets/skill-set.json).

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
