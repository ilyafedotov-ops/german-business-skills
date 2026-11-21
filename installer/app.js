/* Static guided setup. No network access, no text inputs and no credentials: the
   page only links to official provider pages and copies fixed text. */
'use strict';
(() => {
  const TEXT = window.INSTALLER_TEXT;
  const LINKS = window.INSTALLER_LINKS;
  const LANGUAGES = ['en', 'ru', 'de'];
  const STEPS = ['welcome', 'assistant', 'account', 'app', 'safety', 'skills', 'demos'];
  const PROVIDERS = ['claude', 'openai'];
  const MAKERS = { claude: 'Anthropic', openai: 'OpenAI' };
  // Practice answers for "would you share this?"; tests/test_installer.py reads this table.
  const QUIZ = { demo: 'ok', question: 'ok', customer: 'check', letter: 'check', elster: 'never', banking: 'never' };
  const VERDICTS = ['ok', 'check', 'never'];
  const SYSTEMS = ['windows', 'mac'];
  const DEMOS = Object.keys(TEXT.en.demos.items);
  // Routes are compared with this fixed list, never looked up as object properties.
  const ROUTES = [...STEPS, 'examples', ...DEMOS.map(id => `demo-${id}`)];
  const NEEDS_ASSISTANT = ['account', 'app', 'skills'];
  const FIRST_EXAMPLES = ['first', 'creator'];
  // Like a licence agreement: these steps wait until the data notes are accepted.
  const NEEDS_ACCEPT = ['skills', 'demos'];
  const KEY = 'gbk-installer-v1';
  const ICONS = {
    page: 'M4 4h16v16H4zM4 9h16M7 6.5h1',
    mail: 'M3 6h18v12H3zM3 7l9 6 9-6',
    phone: 'M8 2h8v20H8zM11 18h2',
    card: 'M3 6h18v12H3zM3 10h18M7 15h4',
    download: 'M12 3v12M7 10l5 5 5-5M4 20h16',
    box: 'M4 8l8-4 8 4v8l-8 4-8-4zM4 8l8 4 8-4M12 12v8',
    person: 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21c1-4 4-6 8-6s7 2 8 6',
    sliders: 'M4 7h10M18 7h2M4 17h4M12 17h8M16 5v4M10 15v4',
    puzzle: 'M5 8h4a2 2 0 1 1 4 0h4v4a2 2 0 1 1 0 4v4H5v-4a2 2 0 1 0 0-4z',
    plus: 'M12 5v14M5 12h14',
    check: 'M5 12l5 5 9-10',
    folder: 'M3 6h6l2 2h10v11H3z',
    chat: 'M4 5h16v11H9l-5 4z',
    cloud: 'M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.2 8.6 4.7 4.7 0 0 0 7 18z',
    archive: 'M3 4h18v4H3zM5 8v12h14V8M10 12h4',
    alert: 'M12 3l9.5 17h-19zM12 10v4M12 17h.01',
    calc: 'M6 3h12v18H6zM9 7h6M9 11h.01M12 11h.01M15 11h.01M9 14h.01M12 14h.01M15 14h.01M9 17h.01M12 17h.01M15 17h.01',
  };
  const DIAGRAMS = {
    account: ['page', 'mail', 'phone', 'card'],
    app: ['download', 'box', 'person'],
    claude: ['chat', 'page', 'puzzle', 'check'],
    openai: ['folder', 'page', 'sliders', 'check'],
    safety: ['folder', 'chat', 'cloud', 'archive'],
    risks: ['alert', 'calc', 'person', 'check'],
  };

  const $ = id => document.getElementById(id);
  const main = $('main');
  const select = $('language');
  const system = detectSystem();
  let storageOk = probeStorage();
  const state = load();
  let t = TEXT[state.lang];
  let current = 'welcome';
  let lastHash = null;
  let copies = 0;

  function detectSystem() {
    // The user can always override this guess on the app step.
    const agent = navigator.userAgent || '';
    if (/iPhone|iPad|iPod|Android/i.test(agent)) return { os: null, mobile: true };
    if (/Windows/i.test(agent)) return { os: 'windows', mobile: false };
    if (/Macintosh|Mac OS X/i.test(agent)) return { os: 'mac', mobile: false };
    return { os: null, mobile: false };
  }

  function probeStorage() {
    try {
      localStorage.setItem(`${KEY}-probe`, '1');
      localStorage.removeItem(`${KEY}-probe`);
      return true;
    } catch (error) { return false; }
  }

  function initialLanguage() {
    for (const tag of navigator.languages || [navigator.language || 'en']) {
      const base = String(tag).slice(0, 2).toLowerCase();
      if (LANGUAGES.includes(base)) return base;
    }
    return 'en';
  }

  function load() {
    const fresh = { lang: initialLanguage(), assistant: null, os: system.os, done: {}, accepted: false, quiz: {}, route: 'welcome' };
    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (error) { saved = null; }
    if (!saved || typeof saved !== 'object') return fresh;
    if (LANGUAGES.includes(saved.lang)) fresh.lang = saved.lang;
    fresh.accepted = saved.accepted === true;
    if (PROVIDERS.includes(saved.assistant)) fresh.assistant = saved.assistant;
    if (SYSTEMS.includes(saved.os)) fresh.os = saved.os;
    if (ROUTES.includes(saved.route)) fresh.route = saved.route;
    if (saved.done && typeof saved.done === 'object') {
      // Finished steps and tried demos only, never arbitrary saved keys.
      for (const [key, value] of Object.entries(saved.done)) {
        if (value === true && (STEPS.includes(key) || (key.startsWith('demo:') && DEMOS.includes(key.slice(5))))) fresh.done[key] = true;
      }
    }
    if (saved.quiz && typeof saved.quiz === 'object') {
      // Read only the fixed card ids, never arbitrary saved keys.
      for (const id of Object.keys(QUIZ)) if (VERDICTS.includes(saved.quiz[id])) fresh.quiz[id] = saved.quiz[id];
    }
    return fresh;
  }

  function save() {
    if (!storageOk) return;
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (error) { storageOk = false; chrome(); }
  }

  function h(tag, attributes = {}, ...children) {
    const element = document.createElement(tag);
    for (const [name, value] of Object.entries(attributes)) {
      if (value === null || value === undefined || value === false) continue;
      if (name === 'class') element.className = value;
      else if (name.startsWith('on')) element.addEventListener(name.slice(2), value);
      else element.setAttribute(name, value === true ? '' : String(value));
    }
    for (const child of children.flat(Infinity)) {
      if (child !== null && child !== undefined && child !== false) element.append(child instanceof Node ? child : String(child));
    }
    return element;
  }

  const fill = (text, values) => text.replace(/\{(\w+)\}/g, (match, key) =>
    (Object.prototype.hasOwnProperty.call(values, key) ? String(values[key]) : match));
  // Locale strings may mark interface labels with **bold**; everything else is text.
  const rich = text => text.split('**').map((part, index) => (index % 2 ? h('strong', {}, part) : document.createTextNode(part)));
  const eyebrow = step => fill(t.ui.stepOf, { current: STEPS.indexOf(step) + 1, total: STEPS.length });
  const fileName = url => decodeURIComponent(new URL(url).pathname.split('/').pop());

  function external(href, label, className) {
    return h('a', { href, target: '_blank', rel: 'noopener noreferrer', class: className },
      rich(label), h('span', { class: 'visually-hidden' }, ` (${t.ui.newTab})`));
  }

  function icon(name) {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('focusable', 'false');
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', ICONS[name]);
    svg.append(path);
    return svg;
  }

  function diagram(labels, icons, caption = t.ui.illustration) {
    // The class sets one row per diagram on wide screens and avoids a lone tile on phones.
    return h('figure', { class: `flow n${labels.length}` },
      h('ol', {}, labels.map((label, index) => h('li', {},
        h('span', { class: 'flow-number', 'aria-hidden': 'true' }, String(index + 1)),
        h('span', { class: 'flow-icon', 'aria-hidden': 'true' }, icon(icons[index])),
        h('span', {}, label)))),
      caption ? h('figcaption', { class: 'hint' }, caption) : null);
  }

  // Numbered instructions without checkboxes: moving on with Next is enough.
  function steps(items, extras = {}) {
    return h('ol', { class: 'steps' }, items.map((item, index) => h('li', {}, h('p', {}, rich(item)), extras[index] || null)));
  }

  // Details stay one click away, so each step's page stays short.
  function more(label, ...children) {
    return h('details', { class: 'card more' }, h('summary', {}, label), children);
  }

  async function copyText(value, area) {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(value);
        return true;
      }
    } catch (error) { /* Fall back to the selected text below. */ }
    try {
      area.focus();
      area.select();
      if (document.execCommand && document.execCommand('copy')) return true;
    } catch (error) { /* The user can still copy the selected text. */ }
    area.focus();
    area.select();
    return false;
  }

  function copyBox(label, value) {
    const id = `copy-${++copies}`;
    const area = h('textarea', { id, readonly: true, rows: Math.min(9, Math.max(1, Math.ceil(value.length / 64))), spellcheck: 'false' });
    area.value = value;
    const status = h('p', { role: 'status', class: 'copy-status' });
    const button = h('button', { type: 'button', 'aria-label': `${t.ui.copy}: ${label}`, onclick: async () => {
      const copied = await copyText(value, area);
      status.textContent = copied ? t.ui.copied : t.ui.copyFailed;
      status.classList.toggle('warn', !copied);
    } }, t.ui.copy);
    return h('div', { class: 'copy' }, h('label', { for: id }, label), area, h('div', { class: 'copy-actions' }, button, status));
  }

  function heading(title, small) {
    return [small ? h('p', { class: 'eyebrow' }, small) : null, h('h1', { tabindex: '-1' }, title)];
  }

  function stepNav(step) {
    const index = STEPS.indexOf(step);
    const blocked = step === 'safety' && !state.accepted;
    return h('div', { class: 'step-nav' },
      index > 0 ? h('button', { type: 'button', onclick: () => go(STEPS[index - 1]) }, t.ui.back) : null,
      index < STEPS.length - 1 ? h('button', { type: 'button', class: 'primary', 'data-next': '', disabled: blocked, onclick: () => {
        state.done[step] = true;
        go(STEPS[index + 1]);
      } }, step === 'welcome' ? t.ui.start : t.ui.next) : null);
  }

  function rerender(focusSelector) {
    render(false);
    const target = focusSelector && main.querySelector(focusSelector);
    if (target) target.focus();
  }

  const mobileNotice = () => (system.mobile ? h('p', { class: 'notice' }, t.ui.mobile) : null);

  function welcomeView() {
    const w = t.welcome;
    return [
      ...heading(w.title, w.eyebrow),
      mobileNotice(),
      h('p', { class: 'lead' }, w.lead),
      h('section', { class: 'card' }, h('h2', {}, w.needTitle), h('ul', { class: 'ticks' }, w.need.map(item => h('li', {}, rich(item))))),
      h('p', { class: 'safety' }, w.aiShort),
      more(t.ui.more, h('h2', {}, w.aiTitle), h('p', {}, rich(w.ai)), h('p', {}, external(LINKS.docs[state.lang].risks, w.aiLink)), h('p', { class: 'hint' }, t.ui.safety)),
      stepNav('welcome'),
    ];
  }

  function providerCard(provider) {
    const info = t.assistant[provider];
    const selected = state.assistant === provider;
    return h('section', { class: selected ? 'card provider selected' : 'card provider', 'aria-labelledby': `provider-${provider}` },
      h('p', { class: 'maker' }, info.maker),
      h('h2', { id: `provider-${provider}` }, info.name),
      h('p', {}, rich(info.summary)),
      h('div', { class: 'actions' },
        h('button', { type: 'button', class: selected ? 'primary' : null, 'data-provider': provider, 'aria-pressed': String(selected),
          onclick: () => { state.assistant = provider; save(); rerender(`[data-provider="${provider}"]`); } },
        fill(t.assistant.choose, { name: info.name })),
        selected ? h('span', { class: 'badge' }, t.assistant.chosen) : null));
  }

  function assistantView() {
    const a = t.assistant;
    return [
      ...heading(a.title, eyebrow('assistant')),
      h('p', { class: 'lead' }, a.lead),
      h('div', { class: 'grid two' }, PROVIDERS.map(providerCard)),
      h('p', { class: 'hint' }, rich(a.unsure)),
      more(t.ui.more,
        PROVIDERS.map(provider => [
          h('h2', {}, a[provider].name),
          h('p', { class: 'muted' }, a[provider].app),
          h('ul', { class: 'ticks' }, a[provider].points.map(point => h('li', {}, rich(point)))),
          h('p', { class: 'small' }, external(LINKS[provider].pricing, a[provider].pricing)),
        ]),
        h('p', {}, fill(a.business, { name: t.steps.safety })),
        h('p', { class: 'hint' }, a.work)),
      stepNav('assistant'),
    ];
  }

  function accountView() {
    const provider = state.assistant;
    const account = t.account;
    const info = account[provider];
    return [
      ...heading(info.title, eyebrow('account')),
      h('p', {}, external(LINKS[provider].signup, info.open, 'button-link primary')),
      diagram(info.diagram, DIAGRAMS.account),
      steps(info.short),
      h('p', { class: 'hint' }, account.already),
      h('p', {}, t.ui.whenDone),
      more(t.ui.more, h('p', {}, account.lead), steps(info.steps), h('p', { class: 'hint' }, account.labelsNote),
        h('h2', {}, account.safetyTitle), h('ul', { class: 'ticks' }, account.safety.map(item => h('li', {}, rich(item))))),
      stepNav('account'),
    ];
  }

  function downloads(provider, os) {
    const info = t.app[provider].download;
    const links = LINKS[provider];
    if (provider === 'claude' && os === 'mac') return [external(links.mac, info.mac, 'button-link primary')];
    if (provider === 'claude') return [external(links.windows, info.windows, 'button-link primary'), h('p', { class: 'hint wide' }, external(links.windowsArm, info.windowsArm))];
    if (os === 'mac') {
      return [h('p', { class: 'hint wide' }, rich(t.app.openai.macWhich)),
        external(links.macArm, info.macArm, 'button-link primary'), external(links.macIntel, info.macIntel, 'button-link')];
    }
    return [external(links.windows, info.windows, 'button-link primary')];
  }

  function appView() {
    const provider = state.assistant;
    const app = t.app;
    const info = app[provider];
    const privacy = t.safety[provider];
    const os = state.os;
    return [
      ...heading(info.title, eyebrow('app')),
      mobileNotice(),
      h('section', { class: 'card', 'aria-labelledby': 'os-title' },
        h('h2', { id: 'os-title' }, app.osTitle),
        h('p', {}, system.os ? fill(app.detected, { os: app[system.os] }) : app.unknown),
        h('div', { class: 'choices' }, SYSTEMS.map(name => h('button', {
          type: 'button', class: 'choice', 'data-system': name, 'aria-pressed': String(os === name),
          onclick: () => { state.os = name; save(); rerender(`[data-system="${name}"]`); },
        }, app[name])))),
      os ? h('div', { class: 'downloads' }, downloads(provider, os)) : null,
      diagram(info.diagram, DIAGRAMS.app),
      steps(info.short),
      h('p', {}, t.ui.whenDone),
      more(t.ui.more,
        h('h2', {}, app.stepsTitle),
        os ? steps(info[os]) : null,
        h('p', {}, rich(info.doneWhen)),
        h('p', { class: 'hint' }, app.other, ' ', external(LINKS[provider].downloads, app.official)),
        h('p', { class: 'hint' }, app.blocked),
        h('h2', {}, t.safety.settingsTitle),
        h('p', { class: 'hint' }, t.safety.settingsLead),
        steps(privacy.steps),
        h('p', {}, external(LINKS.privacy[provider], privacy.link)),
        h('p', { class: 'hint' }, privacy.business)),
      stepNav('app'),
    ];
  }

  function quizView() {
    const s = t.safety;
    const ids = Object.keys(QUIZ);
    const score = h('p', { class: 'quiz-score' });
    const updateScore = () => {
      const answered = ids.filter(id => state.quiz[id]);
      const right = answered.filter(id => state.quiz[id] === QUIZ[id]).length;
      score.textContent = answered.length ? fill(s.quizScore, { answered: answered.length, total: ids.length, right }) : '';
    };
    const cards = ids.map(id => {
      const item = s.quiz[id];
      const labelId = `quiz-${id}`;
      const feedback = h('p', { class: 'quiz-feedback', role: 'status' });
      const card = h('li', { class: 'quiz-item' });
      const show = () => {
        const answer = state.quiz[id];
        const right = answer === QUIZ[id];
        buttons.forEach((button, index) => button.setAttribute('aria-pressed', String(VERDICTS[index] === answer)));
        card.classList.toggle('right', Boolean(answer) && right);
        card.classList.toggle('wrong', Boolean(answer) && !right);
        feedback.replaceChildren(...(answer ? [h('strong', {}, right ? s.quizRight : fill(s.quizWrong, { answer: s.quizChoices[QUIZ[id]] })), ` ${item.why}`] : []));
      };
      // Answers update in place so focus stays on the chosen button.
      const buttons = VERDICTS.map(verdict => h('button', { type: 'button', class: `verdict verdict-${verdict}`, onclick: () => {
        state.quiz[id] = verdict;
        save();
        show();
        updateScore();
      } }, s.quizChoices[verdict]));
      show();
      card.append(h('p', { class: 'quiz-question', id: labelId }, item.item),
        h('div', { class: 'verdicts', role: 'group', 'aria-labelledby': labelId }, buttons), feedback);
      return card;
    });
    updateScore();
    return [h('h2', {}, s.quizTitle), h('p', { class: 'hint' }, s.quizLead), h('ol', { class: 'quiz-list' }, cards), score,
      h('h2', {}, s.askTitle), h('p', {}, s.askLead), copyBox(s.askLabel, s.ask)];
  }

  // The full notes read like a licence agreement in a scrolling box.
  function agreement(s, who) {
    return h('div', { class: 'license', tabindex: '0', role: 'region', 'aria-label': s.title },
      h('p', {}, s.lead),
      h('h3', {}, s.risksTitle),
      s.risks.map(risk => h('p', {}, h('strong', {}, risk.title), ' — ', risk.text)),
      h('h3', {}, s.flowTitle),
      h('ul', {}, s.flowText.map(text => h('li', {}, fill(text, { provider: who })))),
      h('h3', {}, s.gdprTitle),
      h('ul', {}, s.gdpr.map(item => h('li', {}, rich(item)))),
      h('p', {}, s.gdprNote),
      h('p', {}, external(LINKS.privacy.aiAct, s.aiActLink)),
      h('p', {}, external(LINKS.docs[state.lang].risks, s.fullLink)),
      h('h3', {}, 'MIT License'),
      h('p', {}, s.license));
  }

  function safetyView() {
    const s = t.safety;
    const who = state.assistant ? MAKERS[state.assistant] : s.either;
    const accept = (value, label) => {
      const input = h('input', { type: 'radio', name: 'accept', id: `accept-${value}`, value, 'data-accept': value, onchange: () => {
        // Updated in place: the chosen option keeps focus and Next follows the answer.
        state.accepted = value === 'yes';
        save();
        main.querySelector('[data-next]').disabled = !state.accepted;
        main.querySelector('.notice[role=alert]')?.remove();
        progress();
      } });
      // "I do not accept" is the default answer.
      input.checked = (value === 'yes') === state.accepted;
      return h('div', { class: 'check-row' }, input, h('label', { for: `accept-${value}` }, label));
    };
    return [
      ...heading(s.title, eyebrow('safety')),
      h('ul', { class: 'warnings' }, s.warnings.map(warning => h('li', {},
        h('span', { class: 'risk-icon', 'aria-hidden': 'true' }, icon('alert')), h('span', {}, fill(warning, { provider: who }))))),
      h('p', { class: 'hint' }, s.boxNote),
      agreement(s, who),
      h('fieldset', { class: 'accept' }, h('legend', {}, s.question), accept('yes', s.understand), accept('no', s.decline)),
      more(s.selfTest, quizView()),
      stepNav('safety'),
    ];
  }

  function screenshot(info) {
    const source = LINKS.local.screenshot;
    const image = h('img', { src: source, alt: info.shotAlt, width: '4096', height: '2076', decoding: 'async' });
    const large = h('img', { src: source, alt: info.shotAlt, width: '4096', height: '2076', decoding: 'async' });
    const body = h('div', { class: 'lightbox-body' }, large);
    const zoom = h('button', { type: 'button', 'aria-pressed': 'false', onclick: () => {
      const zoomed = zoom.getAttribute('aria-pressed') !== 'true';
      zoom.setAttribute('aria-pressed', String(zoomed));
      body.classList.toggle('zoomed', zoomed);
    } }, t.ui.zoom);
    const dialog = h('dialog', { class: 'lightbox', 'aria-label': info.shotAlt },
      h('div', { class: 'lightbox-bar' }, zoom, h('button', { type: 'button', class: 'primary', onclick: () => dialog.close() }, t.ui.close)),
      body);
    const enlarge = h('button', { type: 'button', class: 'shot-enlarge', 'aria-haspopup': 'dialog', onclick: () => dialog.showModal() }, t.ui.enlarge);
    image.addEventListener('click', () => dialog.showModal());
    // A click on the dimmed backdrop closes; closing always returns focus to the button.
    dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => enlarge.focus());
    const figure = h('figure', { class: 'shot' }, image, h('figcaption', { class: 'hint' }, info.shotCaption), enlarge, dialog);
    // A copied installer folder may not include the repository image; hide only the figure.
    image.addEventListener('error', () => { figure.hidden = true; });
    return figure;
  }

  // A real screenshot of the app; a copied installer folder without images hides only the figure.
  function result(file, alt, caption) {
    const shot = h('img', { src: file, alt, loading: 'lazy', decoding: 'async' });
    const figure = h('figure', { class: 'shot' }, shot, caption ? h('figcaption', { class: 'hint' }, caption) : null);
    shot.addEventListener('error', () => { figure.hidden = true; });
    return figure;
  }

  function skillList() {
    const skills = t.skills;
    return [h('h2', {}, skills.listTitle), h('dl', { class: 'skill-list' }, Object.entries(skills.list).map(([name, description]) =>
      [h('dt', {}, h('code', {}, name)), h('dd', {}, description)]))];
  }

  // Fallback route for when the request does not work: the click-by-click steps.
  function manualRoute(provider, info) {
    const extras = {};
    let after;
    if (provider === 'claude') {
      extras[1] = [copyBox(info.addressLabel, LINKS.marketplace), h('p', { class: 'hint' }, info.github)];
      after = [screenshot(info), h('p', { class: 'hint' }, info.review)];
    } else {
      extras[0] = [
        h('div', { class: 'downloads' },
          external(LINKS.release.codexZip, fill(info.zip, { file: fileName(LINKS.release.codexZip) }), 'button-link primary'),
          external(LINKS.release.checksums, fill(info.checksums, { file: fileName(LINKS.release.checksums) }), 'button-link')),
        h('p', { class: 'hint' }, info.checksumNote, ' ', external(LINKS.release.page, info.releasePage)),
      ];
      extras[2] = copyBox(info.manualPromptLabel, info.manualPrompt);
      after = h('p', {}, external(LINKS.docs[state.lang].manual, info.manual));
    }
    return h('details', { class: 'card more manual-route' },
      h('summary', {}, info.manualTitle), steps(info.manualSteps, extras), skillList(), after);
  }

  function skillsView() {
    const provider = state.assistant;
    const skills = t.skills;
    const info = skills[provider];
    // The request goes right below the step that says to copy it.
    const extras = { [provider === 'claude' ? 1 : 2]: copyBox(info.promptLabel, info.prompt) };
    return [
      ...heading(info.title, eyebrow('skills')),
      h('p', { class: 'lead' }, info.lead),
      diagram(info.diagram, DIAGRAMS[provider]),
      steps(info.short, extras),
      h('p', {}, t.ui.whenDone),
      more(t.ui.preview, result(LINKS.local.results.skills[provider][state.lang], info.result.alt, info.result.caption)),
      manualRoute(provider, info),
      more(t.ui.more, steps(info.steps), skillList(), h('p', { class: 'hint' }, skills.once),
        h('p', {}, `${skills.stuck} `, external(LINKS.docs[state.lang].help, skills.stuckLink))),
      stepNav('skills'),
    ];
  }

  function finishView() {
    const demos = t.demos;
    return [
      ...heading(demos.doneTitle, eyebrow('demos')),
      h('p', { class: 'lead' }, demos.doneLead),
      // Two first examples: the user picks the one closest to their own work.
      FIRST_EXAMPLES.map(id => copyBox(demos.items[id].title, demos.items[id].prompt)),
      more(t.ui.preview, (state.assistant ? [state.assistant] : PROVIDERS).map(provider =>
        result(LINKS.local.results.first[provider][state.lang], demos.result[`${provider}Alt`], '')), h('p', { class: 'hint' }, demos.result.caption)),
      h('p', {}, h('a', { href: '#examples', class: 'button-link' }, demos.more)),
      stepNav('demos'),
    ];
  }

  function demoCard(id) {
    const item = t.demos.items[id];
    return h('article', { class: 'card demo' },
      h('h2', {}, item.title),
      h('p', {}, item.summary),
      h('p', { class: 'hint' }, item.time),
      h('div', { class: 'actions' },
        h('a', { href: `#demo-${id}`, class: 'button-link', 'aria-label': `${t.demos.open}: ${item.title}` }, t.demos.open),
        state.done[`demo:${id}`] ? h('span', { class: 'badge' }, t.demos.tried) : null));
  }

  function examplesView() {
    const demos = t.demos;
    const providers = state.assistant ? [state.assistant] : PROVIDERS;
    return [
      h('p', {}, h('a', { href: '#demos', class: 'back-link' }, t.ui.back)),
      ...heading(demos.title, eyebrow('demos')),
      h('p', { class: 'lead' }, rich(demos.lead)),
      h('section', { class: 'card note' }, h('h2', {}, demos.callTitle),
        providers.map(provider => h('p', {}, rich(demos.call[provider]))),
        h('p', { class: 'hint' }, `${demos.privacy} `, external(LINKS.docs[state.lang].risks, t.welcome.aiLink))),
      h('div', { class: 'grid demos' }, DEMOS.map(demoCard)),
      h('section', { class: 'card' }, h('h2', {}, demos.prototype), h('p', {}, h('a', { href: LINKS.local.prototype }, demos.prototypeLink))),
      h('section', { class: 'card finish' }, h('h2', {}, demos.finishTitle), h('p', {}, demos.finish),
        h('p', {}, external(LINKS.docs[state.lang].guide, demos.guideLink))),
    ];
  }

  function demoView(id) {
    const demos = t.demos;
    const item = demos.items[id];
    const key = `demo:${id}`;
    const tried = h('input', { type: 'checkbox', id: 'demo-tried', onchange: event => {
      if (event.target.checked) state.done[key] = true; else delete state.done[key];
      save();
    } });
    tried.checked = state.done[key] === true;
    return [
      h('p', {}, h('a', { href: '#examples', class: 'back-link' }, demos.back)),
      ...heading(item.title, item.time),
      h('p', { class: 'lead' }, item.summary),
      h('section', { class: 'card' }, h('h2', {}, demos.prepareTitle), h('ol', { class: 'ticks' }, item.prepare.map(step => h('li', {}, rich(step))))),
      h('section', { class: 'card' }, h('h2', {}, demos.promptTitle), copyBox(demos.promptLabel, item.prompt)),
      h('section', { class: 'card' }, h('h2', {}, demos.answersTitle), copyBox(demos.answersLabel, item.answers)),
      h('section', { class: 'card' }, h('h2', {}, demos.checkTitle), h('ul', { class: 'ticks' }, item.check.map(point => h('li', {}, rich(point)))), h('p', { class: 'hint' }, demos.checkNote)),
      h('section', { class: 'card' }, h('h2', {}, demos.nextTitle), copyBox(demos.nextLabel, item.next)),
      h('div', { class: 'check-row tried' }, tried, h('label', { for: 'demo-tried' }, demos.markTried)),
      h('div', { class: 'step-nav' }, h('button', { type: 'button', onclick: () => go('examples') }, t.ui.back)),
    ];
  }

  function view(route) {
    switch (route) {
      case 'welcome': return welcomeView();
      case 'assistant': return assistantView();
      case 'account': return accountView();
      case 'app': return appView();
      case 'safety': return safetyView();
      case 'skills': return skillsView();
      case 'demos': return finishView();
      case 'examples': return examplesView();
      default: return demoView(route.slice('demo-'.length));
    }
  }

  const stepFor = route => (route.startsWith('demo-') || route === 'examples' ? 'demos' : route);

  // A step is done when the user moves on with Next; nothing needs ticking.
  function complete(step) {
    switch (step) {
      case 'assistant': return Boolean(state.assistant);
      case 'safety': return state.accepted;
      case 'demos': return state.done.demos === true;
      default: return state.done[step] === true && (step === 'welcome' || Boolean(state.assistant));
    }
  }

  function progress() {
    const step = stepFor(current);
    const finished = STEPS.map(complete);
    const count = finished.filter(Boolean).length;
    $('progress-summary').textContent = fill(t.ui.progressSummary, { done: count, total: STEPS.length });
    const meter = $('progress-meter');
    meter.max = STEPS.length;
    meter.value = count;
    $('progress-list').replaceChildren(...STEPS.map((id, index) => {
      const done = finished[index];
      return h('li', {}, h('a', { href: `#${id}`, class: done ? 'done' : null, 'aria-current': id === step ? 'step' : null },
        h('span', { class: 'progress-mark', 'aria-hidden': 'true' }, done ? '✓' : String(index + 1)),
        h('span', { class: 'progress-label' }, t.steps[id]),
        done ? h('span', { class: 'visually-hidden' }, ` (${t.ui.done})`) : null));
    }));
  }

  function chrome() {
    t = TEXT[state.lang];
    document.documentElement.lang = state.lang;
    const route = current.startsWith('demo-') ? t.demos.items[current.slice(5)].title : (current === 'examples' ? t.demos.title : t.steps[current]);
    document.title = `${route} · ${t.meta.title}`;
    $('skip').textContent = t.ui.skip;
    $('brand').textContent = t.ui.brand;
    $('brand-sub').textContent = t.ui.brandSub;
    $('language-label').textContent = t.ui.languageLabel;
    select.value = state.lang;
    $('progress').setAttribute('aria-label', t.ui.progressLabel);
    const storage = $('storage-status');
    storage.textContent = storageOk ? t.ui.saved : t.ui.notSaved;
    storage.classList.toggle('warn', !storageOk);
    $('footer-text').textContent = t.ui.footer;
    const date = new Intl.DateTimeFormat(t.meta.locale, { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' })
      .format(new Date(`${LINKS.checked}T00:00:00Z`));
    $('footer-checked').textContent = fill(t.ui.checked, { date });
  }

  // Steps that need an earlier answer send the user back to that question.
  function allowed(route) {
    const step = stepFor(route);
    if (NEEDS_ASSISTANT.includes(step) && !state.assistant) return ['assistant', 'chooseFirst'];
    if (NEEDS_ACCEPT.includes(step) && !state.accepted) return ['safety', 'acceptFirst'];
    return [route, null];
  }

  function render(focus) {
    let raw = '';
    try { raw = decodeURIComponent(location.hash.slice(1)); } catch (error) { raw = '#invalid'; }
    const [route, notice] = allowed(ROUTES.includes(raw) ? raw : (raw ? 'welcome' : state.route));
    if (location.hash !== `#${route}`) history.replaceState(null, '', `#${route}`);
    lastHash = location.hash;
    current = route;
    state.route = route;
    if (route === 'demos') state.done.demos = true;
    save();
    chrome();
    progress();
    copies = 0;
    main.dataset.route = route;
    main.replaceChildren(...[notice ? h('p', { class: 'notice', role: 'alert' }, t.ui[notice]) : null, ...view(route)].flat(Infinity).filter(Boolean));
    if (focus) main.querySelector('h1').focus();
  }

  function go(route) {
    location.hash = route;
    render(true);
  }

  window.addEventListener('hashchange', () => { if (location.hash !== lastHash) render(true); });
  select.addEventListener('change', () => {
    if (!LANGUAGES.includes(select.value)) return;
    state.lang = select.value;
    save();
    render(false);
  });
  $('skip').addEventListener('click', event => { event.preventDefault(); main.focus(); });
  render(false);
})();
