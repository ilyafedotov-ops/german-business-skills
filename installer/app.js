/* Static guided setup. No network access, no text inputs and no credentials: the
   page only links to official provider pages and copies fixed text. */
'use strict';
(() => {
  const TEXT = window.INSTALLER_TEXT;
  const LINKS = window.INSTALLER_LINKS;
  const LANGUAGES = ['en', 'ru', 'de'];
  const STEPS = ['welcome', 'assistant', 'account', 'app', 'skills', 'demos'];
  const PROVIDERS = ['claude', 'openai'];
  const SYSTEMS = ['windows', 'mac'];
  const DEMOS = Object.keys(TEXT.en.demos.items);
  // Routes are compared with this fixed list, never looked up as object properties.
  const ROUTES = [...STEPS, ...DEMOS.map(id => `demo-${id}`)];
  const NEEDS_ASSISTANT = ['account', 'app', 'skills'];
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
  };
  const DIAGRAMS = {
    account: ['page', 'mail', 'phone', 'card'],
    app: ['download', 'box', 'person'],
    claude: ['sliders', 'puzzle', 'plus', 'check'],
    openai: ['folder', 'download', 'chat', 'check'],
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
    const fresh = { lang: initialLanguage(), started: false, assistant: null, os: system.os, done: {}, route: 'welcome' };
    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (error) { saved = null; }
    if (!saved || typeof saved !== 'object') return fresh;
    if (LANGUAGES.includes(saved.lang)) fresh.lang = saved.lang;
    fresh.started = saved.started === true;
    if (PROVIDERS.includes(saved.assistant)) fresh.assistant = saved.assistant;
    if (SYSTEMS.includes(saved.os)) fresh.os = saved.os;
    if (ROUTES.includes(saved.route)) fresh.route = saved.route;
    if (saved.done && typeof saved.done === 'object') {
      for (const [key, value] of Object.entries(saved.done)) {
        if (value === true && /^[a-z]+(?::[a-z0-9]+){1,3}$/.test(key)) fresh.done[key] = true;
      }
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

  function diagram(labels, icons) {
    return h('figure', { class: 'flow' },
      h('ol', {}, labels.map((label, index) => h('li', {},
        h('span', { class: 'flow-number', 'aria-hidden': 'true' }, String(index + 1)),
        h('span', { class: 'flow-icon', 'aria-hidden': 'true' }, icon(icons[index])),
        h('span', {}, label)))),
      h('figcaption', { class: 'hint' }, t.ui.illustration));
  }

  function checklist(prefix, items, extras = {}) {
    return h('ol', { class: 'checklist' }, items.map((item, index) => {
      const key = `${prefix}:${index}`;
      const id = `check-${key.replace(/:/g, '-')}`;
      const box = h('input', { type: 'checkbox', id, onchange: event => {
        if (event.target.checked) state.done[key] = true; else delete state.done[key];
        save();
        progress();
      } });
      box.checked = state.done[key] === true;
      return h('li', {}, h('div', { class: 'check-row' }, box, h('label', { for: id }, rich(item))), extras[index] || null);
    }));
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
    return h('div', { class: 'step-nav' },
      index > 0 ? h('button', { type: 'button', onclick: () => go(STEPS[index - 1]) }, t.ui.back) : null,
      index < STEPS.length - 1 ? h('button', { type: 'button', class: 'primary', onclick: () => go(STEPS[index + 1]) }, t.ui.next) : null);
  }

  function rerender(focusSelector) {
    render(false);
    const target = focusSelector && main.querySelector(focusSelector);
    if (target) target.focus();
  }

  function welcomeView() {
    const w = t.welcome;
    return [
      ...heading(w.title, w.eyebrow),
      h('p', { class: 'lead' }, w.lead),
      h('section', { class: 'card', 'aria-labelledby': 'choose-language' },
        h('h2', { id: 'choose-language' }, w.chooseLanguage),
        h('div', { class: 'language-choices' }, LANGUAGES.map(code => h('button', {
          type: 'button', lang: code, class: 'choice', 'data-language': code, 'aria-pressed': String(code === state.lang),
          onclick: () => { state.lang = code; save(); rerender(`[data-language="${code}"]`); },
        }, TEXT[code].meta.language))),
        h('p', { class: 'hint' }, w.languageHint)),
      h('div', { class: 'grid two' },
        h('section', { class: 'card' }, h('h2', {}, w.needTitle), h('ul', { class: 'ticks' }, w.need.map(item => h('li', {}, rich(item))))),
        h('section', { class: 'card note' }, h('h2', {}, w.aiTitle), h('p', {}, rich(w.ai)), h('p', {}, external(LINKS.docs[state.lang].risks, w.aiLink)))),
      h('p', { class: 'safety' }, t.ui.safety),
      h('div', { class: 'step-nav' }, h('button', { type: 'button', class: 'primary', onclick: () => { state.started = true; save(); go('assistant'); } }, t.ui.start)),
    ];
  }

  function providerCard(provider) {
    const info = t.assistant[provider];
    const selected = state.assistant === provider;
    return h('section', { class: selected ? 'card provider selected' : 'card provider', 'aria-labelledby': `provider-${provider}` },
      h('p', { class: 'maker' }, info.maker),
      h('h2', { id: `provider-${provider}` }, info.name),
      h('p', { class: 'muted' }, info.app),
      h('ul', { class: 'ticks' }, info.points.map(point => h('li', {}, rich(point)))),
      h('div', { class: 'actions' },
        h('button', { type: 'button', class: selected ? 'primary' : null, 'data-provider': provider, 'aria-pressed': String(selected),
          onclick: () => { state.assistant = provider; save(); rerender(`[data-provider="${provider}"]`); } },
        fill(t.assistant.choose, { name: info.name })),
        selected ? h('span', { class: 'badge' }, t.assistant.chosen) : null),
      h('p', { class: 'small' }, external(LINKS[provider].pricing, info.pricing)));
  }

  function assistantView() {
    const a = t.assistant;
    return [
      ...heading(a.title, eyebrow('assistant')),
      h('p', { class: 'lead' }, a.lead),
      h('div', { class: 'grid two' }, PROVIDERS.map(providerCard)),
      h('p', { class: 'hint' }, rich(a.unsure)),
      h('p', { class: 'hint' }, a.work),
      stepNav('assistant'),
    ];
  }

  function accountView() {
    const provider = state.assistant;
    const account = t.account;
    const info = account[provider];
    return [
      ...heading(info.title, eyebrow('account')),
      h('p', { class: 'lead' }, account.lead),
      h('p', {}, external(LINKS[provider].signup, info.open, 'button-link primary')),
      diagram(info.diagram, DIAGRAMS.account),
      h('p', { class: 'hint' }, `${t.ui.checklist} ${account.already}`),
      checklist(`${provider}:account`, info.steps),
      h('p', { class: 'hint' }, account.labelsNote),
      h('section', { class: 'card note' }, h('h2', {}, account.safetyTitle), h('ul', { class: 'ticks' }, account.safety.map(item => h('li', {}, rich(item))))),
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
    const os = state.os;
    return [
      ...heading(info.title, eyebrow('app')),
      system.mobile ? h('p', { class: 'notice' }, t.ui.mobile) : null,
      h('section', { class: 'card', 'aria-labelledby': 'os-title' },
        h('h2', { id: 'os-title' }, app.osTitle),
        h('p', {}, system.os ? fill(app.detected, { os: app[system.os] }) : app.unknown),
        h('div', { class: 'choices' }, SYSTEMS.map(name => h('button', {
          type: 'button', class: 'choice', 'data-system': name, 'aria-pressed': String(os === name),
          onclick: () => { state.os = name; save(); rerender(`[data-system="${name}"]`); },
        }, app[name]))),
        h('p', { class: 'hint' }, app.other)),
      os ? h('div', { class: 'downloads' }, downloads(provider, os)) : null,
      h('p', {}, external(LINKS[provider].downloads, app.official)),
      os ? [
        h('h2', {}, app.stepsTitle),
        diagram(info.diagram, DIAGRAMS.app),
        h('p', { class: 'hint' }, t.ui.checklist),
        checklist(`${provider}:app:${os}`, info[os]),
        h('p', {}, rich(info.doneWhen)),
      ] : null,
      h('p', { class: 'hint' }, app.blocked),
      stepNav('app'),
    ];
  }

  function screenshot(info) {
    const image = h('img', { src: LINKS.local.screenshot, alt: info.shotAlt, width: '4096', height: '2076', decoding: 'async' });
    const figure = h('figure', { class: 'shot' }, image, h('figcaption', { class: 'hint' }, info.shotCaption));
    // A copied installer folder may not include the repository image; hide only the figure.
    image.addEventListener('error', () => { figure.hidden = true; });
    return figure;
  }

  function skillsView() {
    const provider = state.assistant;
    const skills = t.skills;
    const info = skills[provider];
    const extras = {};
    if (provider === 'claude') {
      extras[1] = [copyBox(info.addressLabel, LINKS.marketplace), h('p', { class: 'hint' }, info.github)];
    } else {
      extras[2] = [
        h('div', { class: 'downloads' },
          external(LINKS.release.codexZip, fill(info.zip, { file: fileName(LINKS.release.codexZip) }), 'button-link primary'),
          external(LINKS.release.checksums, fill(info.checksums, { file: fileName(LINKS.release.checksums) }), 'button-link')),
        h('p', { class: 'hint' }, info.checksumNote, ' ', external(LINKS.release.page, info.releasePage)),
      ];
      extras[4] = copyBox(info.promptLabel, info.prompt);
    }
    return [
      ...heading(info.title, eyebrow('skills')),
      h('p', { class: 'lead' }, info.lead),
      diagram(info.diagram, DIAGRAMS[provider]),
      h('p', { class: 'hint' }, t.ui.checklist),
      checklist(`${provider}:skills`, info.steps, extras),
      provider === 'claude'
        ? [screenshot(info), h('p', { class: 'hint' }, info.review)]
        : h('p', {}, external(LINKS.docs[state.lang].manual, info.manual)),
      h('section', { class: 'card' }, h('h2', {}, skills.listTitle),
        h('dl', { class: 'skill-list' }, Object.entries(skills.list).map(([name, description]) =>
          [h('dt', {}, h('code', {}, name)), h('dd', {}, description)]))),
      h('p', { class: 'hint' }, skills.once),
      h('p', {}, `${skills.stuck} `, external(LINKS.docs[state.lang].help, skills.stuckLink)),
      stepNav('skills'),
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

  function demosView() {
    const demos = t.demos;
    const providers = state.assistant ? [state.assistant] : PROVIDERS;
    return [
      ...heading(demos.title, eyebrow('demos')),
      h('p', { class: 'lead' }, rich(demos.lead)),
      h('section', { class: 'card note' }, h('h2', {}, demos.callTitle),
        providers.map(provider => h('p', {}, rich(demos.call[provider]))),
        h('p', { class: 'hint' }, `${demos.privacy} `, external(LINKS.docs[state.lang].risks, t.welcome.aiLink))),
      h('div', { class: 'grid demos' }, DEMOS.map(demoCard)),
      h('section', { class: 'card' }, h('h2', {}, demos.prototype), h('p', {}, h('a', { href: LINKS.local.prototype }, demos.prototypeLink))),
      h('section', { class: 'card finish' }, h('h2', {}, demos.finishTitle), h('p', {}, demos.finish),
        h('p', {}, external(LINKS.docs[state.lang].guide, demos.guideLink))),
      stepNav('demos'),
    ];
  }

  function demoView(id) {
    const demos = t.demos;
    const item = demos.items[id];
    const key = `demo:${id}`;
    const tried = h('input', { type: 'checkbox', id: 'demo-tried', onchange: event => {
      if (event.target.checked) state.done[key] = true; else delete state.done[key];
      save();
      progress();
    } });
    tried.checked = state.done[key] === true;
    return [
      h('p', {}, h('a', { href: '#demos', class: 'back-link' }, demos.back)),
      ...heading(item.title, item.time),
      h('p', { class: 'lead' }, item.summary),
      h('section', { class: 'card' }, h('h2', {}, demos.prepareTitle), h('ol', { class: 'ticks' }, item.prepare.map(step => h('li', {}, rich(step))))),
      h('section', { class: 'card' }, h('h2', {}, demos.promptTitle), copyBox(demos.promptLabel, item.prompt)),
      h('section', { class: 'card' }, h('h2', {}, demos.answersTitle), copyBox(demos.answersLabel, item.answers)),
      h('section', { class: 'card' }, h('h2', {}, demos.checkTitle), h('ul', { class: 'ticks' }, item.check.map(point => h('li', {}, rich(point)))), h('p', { class: 'hint' }, demos.checkNote)),
      h('section', { class: 'card' }, h('h2', {}, demos.nextTitle), copyBox(demos.nextLabel, item.next)),
      h('div', { class: 'check-row tried' }, tried, h('label', { for: 'demo-tried' }, demos.markTried)),
      h('div', { class: 'step-nav' }, h('button', { type: 'button', onclick: () => go('demos') }, t.ui.back)),
    ];
  }

  function view(route) {
    switch (route) {
      case 'welcome': return welcomeView();
      case 'assistant': return assistantView();
      case 'account': return accountView();
      case 'app': return appView();
      case 'skills': return skillsView();
      case 'demos': return demosView();
      default: return demoView(route.slice('demo-'.length));
    }
  }

  const stepFor = route => (route.startsWith('demo-') ? 'demos' : route);

  function complete(step) {
    const provider = state.assistant;
    const all = (prefix, count) => Array.from({ length: count }, (_, index) => state.done[`${prefix}:${index}`] === true).every(Boolean);
    switch (step) {
      case 'welcome': return state.started;
      case 'assistant': return Boolean(provider);
      case 'account': return Boolean(provider) && all(`${provider}:account`, TEXT.en.account[provider].steps.length);
      case 'app': return Boolean(provider && state.os) && all(`${provider}:app:${state.os}`, TEXT.en.app[provider][state.os].length);
      case 'skills': return Boolean(provider) && all(`${provider}:skills`, TEXT.en.skills[provider].steps.length);
      default: return DEMOS.some(id => state.done[`demo:${id}`] === true);
    }
  }

  function progress() {
    const step = stepFor(current);
    $('progress-list').replaceChildren(...STEPS.map((id, index) => {
      const done = complete(id);
      return h('li', {}, h('a', { href: `#${id}`, class: done ? 'done' : null, 'aria-current': id === step ? 'step' : null },
        h('span', { class: 'progress-mark', 'aria-hidden': 'true' }, done ? '✓' : String(index + 1)),
        h('span', {}, t.steps[id]),
        done ? h('span', { class: 'visually-hidden' }, ` (${t.ui.done})`) : null));
    }));
  }

  function chrome() {
    t = TEXT[state.lang];
    document.documentElement.lang = state.lang;
    const route = current.startsWith('demo-') ? t.demos.items[current.slice(5)].title : t.steps[current];
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

  function render(focus) {
    let raw = '';
    try { raw = decodeURIComponent(location.hash.slice(1)); } catch (error) { raw = '#invalid'; }
    let route = ROUTES.includes(raw) ? raw : (raw ? 'welcome' : state.route);
    const notice = NEEDS_ASSISTANT.includes(route) && !state.assistant;
    if (notice) route = 'assistant';
    if (location.hash !== `#${route}`) history.replaceState(null, '', `#${route}`);
    lastHash = location.hash;
    current = route;
    state.route = route;
    save();
    chrome();
    progress();
    copies = 0;
    main.dataset.route = route;
    main.replaceChildren(...[notice ? h('p', { class: 'notice', role: 'alert' }, TEXT[state.lang].ui.chooseFirst) : null, ...view(route)].flat(Infinity).filter(Boolean));
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
