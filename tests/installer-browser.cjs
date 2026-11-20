// Developer-only checks. End users open installer/index.html without Node or Python.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const vm = require('node:vm');
const playwright = require('playwright');

const browserName = process.argv.find(a => a.startsWith('--browser='))?.split('=')[1] || 'chromium';
const url = pathToFileURL(path.resolve('installer/index.html')).href;
const output = path.resolve('output/installer');
// Assertions follow the page's own locale data, so every language is checked by meaning.
function load(file, name) {
  const sandbox = { window: {} };
  vm.runInNewContext(fs.readFileSync(path.resolve(file), 'utf8'), sandbox);
  return sandbox.window[name];
}
const TEXT = load('installer/text.js', 'INSTALLER_TEXT');
const LINKS = load('installer/links.js', 'INSTALLER_LINKS');
const AGENTS = {
  mac: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
  windows: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  iphone: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
};
const LOCALES = { en: 'en-GB', ru: 'ru-RU', de: 'de-DE' };
const ROUTES = ['welcome', 'assistant', 'account', 'app', 'safety', 'skills', 'demos',
  ...Object.keys(TEXT.en.demos.items).map(id => `demo-${id}`)];
// Expected answers to the "would you share this?" check.
const QUIZ = { demo: 'ok', question: 'ok', customer: 'check', letter: 'check', elster: 'never', banking: 'never' };
const fill = (text, values) => text.replace(/\{(\w+)\}/g, (_, key) => values[key]);
const plain = text => text.replace(/\*\*/g, '');
// Each language exercises both assistants; Windows and Mac alternate so all four
// assistant/system pairs are covered in every browser.
const JOURNEYS = [
  ['en', 'claude', 'mac'], ['en', 'openai', 'windows'],
  ['ru', 'claude', 'windows'], ['ru', 'openai', 'mac'],
  ['de', 'claude', 'mac'], ['de', 'openai', 'windows'],
];

async function context(browser, issues, { language = 'en', agent = 'mac', width = 1280, height = 900 } = {}) {
  const ctx = await browser.newContext({ viewport: { width, height }, locale: LOCALES[language], userAgent: AGENTS[agent], timezoneId: 'Europe/Berlin' });
  if (browserName === 'chromium') await ctx.grantPermissions(['clipboard-read', 'clipboard-write']);
  ctx.on('page', p => {
    p.on('pageerror', e => issues.push(String(e)));
    p.on('console', m => {
      if (m.type() !== 'error') return;
      if (browserName === 'webkit' && capturing.has(p) && m.text() === CAPTURE_DIAGNOSTIC) captureDiagnostics++;
      else issues.push(m.text());
    });
    p.on('requestfailed', r => issues.push(`${r.url()}: ${r.failure()?.errorText}`));
    p.on('request', r => { if (!r.url().startsWith('file:')) issues.push(`Unexpected network request: ${r.url()}`); });
  });
  return ctx;
}

// WebKit rejects Playwright's screenshot-only injected stylesheet under the page
// CSP (also seen in prototype-browser.cjs). Keep the CSP; ignore only that exact
// diagnostic while a capture is running and report how often it happened.
const CAPTURE_DIAGNOSTIC = "Refused to apply a stylesheet because its hash, its nonce, or 'unsafe-inline' does not appear in the style-src directive of the Content Security Policy.";
const capturing = new WeakSet();
let captureDiagnostics = 0;
async function capture(page, options) {
  capturing.add(page);
  try { await page.screenshot({ caret: 'initial', ...options }); } finally { capturing.delete(page); }
}
const heading = page => page.locator('main h1');
// Hash navigation renders after the event; wait for the requested view.
const route = (page, name) => page.locator(`main[data-route="${name}"]`).waitFor();
async function next(page, t) {
  await page.getByRole('button', { name: t.ui.next, exact: true }).click();
  await page.waitForFunction(() => document.activeElement === document.querySelector('main h1'));
}
async function noCredentialFields(page) {
  // The installer never collects passwords, codes, card details or keys.
  assert.equal(await page.locator('form, input:not([type=checkbox]), [contenteditable]').count(), 0);
  assert.equal(await page.locator('textarea:not([readonly])').count(), 0);
}
async function external(page, href) {
  const link = page.locator(`main a[href="${href}"]`).first();
  assert.equal(await link.count(), 1, `Missing official link ${href}`);
  assert.equal(await link.getAttribute('target'), '_blank');
  assert.match(await link.getAttribute('rel'), /noopener/);
  assert.match(await link.getAttribute('rel'), /noreferrer/);
}
async function allTicked(page, t, count) {
  for (const box of await page.locator('main .checklist input[type=checkbox]').all()) await box.check();
  await page.locator('main .check-count').filter({ hasText: fill(t.ui.allTicked, { total: count }) }).waitFor();
}
async function copies(page, t, label, expected) {
  const box = page.locator('.copy', { has: page.getByLabel(label, { exact: true }) });
  assert.equal(await box.getByLabel(label, { exact: true }).inputValue(), expected);
  await box.getByRole('button', { name: t.ui.copy }).click();
  const status = box.getByRole('status');
  if (browserName === 'chromium') {
    await status.filter({ hasText: plain(t.ui.copied) }).waitFor();
    assert.equal(await page.evaluate(() => navigator.clipboard.readText()), expected);
  } else {
    // WebKit automation cannot grant clipboard access; either outcome must be explained.
    await page.waitForFunction(element => element.textContent.trim().length > 0, await status.elementHandle());
    assert.ok([plain(t.ui.copied), plain(t.ui.copyFailed)].includes(await status.innerText()));
  }
}

async function journey(browser, language, assistant, os) {
  const t = TEXT[language];
  const issues = [];
  const ctx = await context(browser, issues, { language, agent: os });
  const page = await ctx.newPage();
  const shot = name => capture(page, { path: path.join(output, `${browserName}-${language}-${assistant}-${name}.png`), fullPage: true });
  try {
    await page.goto(url);
    assert.equal(await heading(page).innerText(), t.welcome.title, 'Browser language selects the initial language');
    assert.equal(await page.locator('html').getAttribute('lang'), language);
    const own = page.getByRole('button', { name: t.meta.language, exact: true });
    await own.click();
    assert.equal(await own.getAttribute('aria-pressed'), 'true');
    await external(page, LINKS.docs[language].risks);
    await noCredentialFields(page);
    await page.getByRole('button', { name: t.ui.start, exact: true }).click();

    assert.equal(await heading(page).innerText(), t.assistant.title);
    for (const provider of ['claude', 'openai']) await external(page, LINKS[provider].pricing);
    const choose = page.getByRole('button', { name: fill(t.assistant.choose, { name: t.assistant[assistant].name }), exact: true });
    await choose.click();
    assert.equal(await choose.getAttribute('aria-pressed'), 'true');
    await next(page, t);

    assert.equal(await heading(page).innerText(), t.account[assistant].title);
    await external(page, LINKS[assistant].signup);
    assert.equal(await page.locator('main input[type=checkbox]').count(), t.account[assistant].steps.length);
    await page.locator('main .check-count').filter({ hasText: fill(t.ui.ticked, { done: 0, total: t.account[assistant].steps.length }) }).waitFor();
    await allTicked(page, t, t.account[assistant].steps.length);
    await noCredentialFields(page);
    await next(page, t);

    assert.equal(await heading(page).innerText(), t.app[assistant].title);
    await page.getByText(fill(t.app.detected, { os: t.app[os] }), { exact: true }).waitFor();
    assert.equal(await page.getByRole('button', { name: t.app[os], exact: true }).getAttribute('aria-pressed'), 'true');
    const downloads = assistant === 'claude'
      ? (os === 'mac' ? ['mac'] : ['windows', 'windowsArm'])
      : (os === 'mac' ? ['macArm', 'macIntel'] : ['windows']);
    for (const key of [...downloads, 'downloads']) await external(page, LINKS[assistant][key]);
    assert.equal(await page.locator('main input[type=checkbox]').count(), t.app[assistant][os].length);
    for (const box of await page.locator('main input[type=checkbox]').all()) await box.check();
    await page.reload();
    assert.equal(await page.locator('main input[type=checkbox]:checked').count(), t.app[assistant][os].length, 'Ticks survive a reload');
    await next(page, t);

    // Data and AI risks: plain explanations, the provider's own settings and a practice check.
    assert.equal(await heading(page).innerText(), t.safety.title);
    for (const risk of t.safety.risks) await page.locator('main').getByText(risk.title, { exact: true }).waitFor();
    for (const key of [assistant, 'aiAct']) await external(page, LINKS.privacy[key]);
    await external(page, LINKS.docs[language].risks);
    assert.equal(await page.locator('main input[type=checkbox]').count(), t.safety[assistant].steps.length);
    await allTicked(page, t, t.safety[assistant].steps.length);
    const card = id => page.locator('.quiz-item', { has: page.getByText(t.safety.quiz[id].item, { exact: true }) });
    const verdict = (id, answer) => card(id).getByRole('button', { name: t.safety.quizChoices[answer], exact: true });
    const feedback = (id, text) => card(id).getByRole('status').filter({ hasText: text }).waitFor();
    // Answer with the keyboard: WebKit, like Safari, does not focus buttons on a mouse click.
    await verdict('banking', 'ok').focus();
    await page.keyboard.press('Space');
    assert.equal(await verdict('banking', 'ok').getAttribute('aria-pressed'), 'true');
    await feedback('banking', fill(t.safety.quizWrong, { answer: t.safety.quizChoices.never }));
    assert.equal(await verdict('banking', 'ok').evaluate(e => e === document.activeElement), true, 'Answering keeps keyboard focus');
    for (const [id, answer] of Object.entries(QUIZ)) await verdict(id, answer).click();
    for (const id of Object.keys(QUIZ)) await feedback(id, t.safety.quizRight);
    assert.equal(await verdict('banking', 'ok').getAttribute('aria-pressed'), 'false', 'A changed answer replaces the first one');
    const total = Object.keys(QUIZ).length;
    await page.locator('main').getByText(fill(t.safety.quizScore, { answered: total, total, right: total }), { exact: true }).waitFor();
    await copies(page, t, t.safety.askLabel, t.safety.ask);
    await noCredentialFields(page);
    await page.reload();
    await route(page, 'safety');
    assert.equal(await verdict('elster', 'never').getAttribute('aria-pressed'), 'true', 'Answers survive a reload');
    await shot('safety');
    await next(page, t);

    assert.equal(await heading(page).innerText(), t.skills[assistant].title);
    for (const [name, description] of Object.entries(t.skills.list)) {
      await page.locator('main').getByText(name, { exact: true }).waitFor();
      await page.locator('main').getByText(description, { exact: true }).waitFor();
    }
    if (assistant === 'claude') {
      await copies(page, t, t.skills.claude.addressLabel, LINKS.marketplace);
      const screenshot = page.getByRole('img', { name: t.skills.claude.shotAlt });
      assert.equal(await screenshot.evaluate(img => img.decode().then(() => img.naturalWidth > 0, () => false)), true, 'Actual marketplace screenshot loads');
      // The screenshot opens larger in a dialog; Escape closes it and returns focus.
      const enlarge = page.getByRole('button', { name: t.ui.enlarge, exact: true });
      await enlarge.click();
      const dialog = page.getByRole('dialog', { name: t.skills.claude.shotAlt });
      await dialog.waitFor();
      const zoom = dialog.getByRole('button', { name: t.ui.zoom, exact: true });
      await zoom.click();
      assert.equal(await zoom.getAttribute('aria-pressed'), 'true');
      await page.keyboard.press('Escape');
      await dialog.waitFor({ state: 'hidden' });
      assert.equal(await enlarge.evaluate(e => e === document.activeElement), true, 'Closing returns focus');
    } else {
      await copies(page, t, t.skills.openai.promptLabel, t.skills.openai.prompt);
      for (const key of ['codexZip', 'checksums', 'page']) await external(page, LINKS.release[key]);
      await external(page, LINKS.docs[language].manual);
    }
    for (const box of await page.locator('main input[type=checkbox]').all()) await box.check();
    await external(page, LINKS.docs[language].help);
    await noCredentialFields(page);
    await shot('skills');
    await next(page, t);

    assert.equal(await heading(page).innerText(), t.demos.title);
    await page.locator('main').getByText(plain(t.demos.call[assistant]), { exact: true }).waitFor();
    assert.equal(await page.getByRole('button', { name: t.ui.next, exact: true }).count(), 0, 'Last step has no Next');
    const demo = t.demos.items.invoice;
    await page.locator('a[href="#demo-invoice"]').click();
    await route(page, 'demo-invoice');
    assert.equal(await heading(page).innerText(), demo.title);
    assert.equal(await heading(page).evaluate(e => e === document.activeElement), true, 'Link navigation focuses the heading');
    await copies(page, t, t.demos.promptLabel, demo.prompt);
    assert.equal(await page.getByLabel(t.demos.answersLabel, { exact: true }).inputValue(), demo.answers);
    assert.equal(await page.getByLabel(t.demos.nextLabel, { exact: true }).inputValue(), demo.next);
    for (const item of demo.check) await page.locator('main').getByText(plain(item), { exact: true }).waitFor();
    await page.getByLabel(t.demos.markTried, { exact: true }).check();
    await page.getByRole('link', { name: t.demos.back, exact: true }).click();
    await route(page, 'demos');
    await page.locator('article', { has: page.locator('a[href="#demo-invoice"]') }).getByText(t.demos.tried, { exact: true }).waitFor();
    await page.getByRole('link', { name: t.demos.prototypeLink, exact: true }).waitFor();
    await external(page, LINKS.docs[language].guide);
    await shot('demos');

    // Every step is now complete; the progress list says so to assistive technology.
    const progress = page.getByRole('navigation', { name: t.ui.progressLabel });
    for (const step of Object.values(t.steps)) {
      await progress.getByRole('link', { name: `${step} (${t.ui.done})`, exact: true }).waitFor();
    }
    const steps = Object.keys(t.steps).length;
    await progress.getByText(fill(t.ui.progressSummary, { done: steps, total: steps }), { exact: true }).waitFor();
    assert.deepEqual(await progress.locator('progress').evaluate(e => [e.value, e.max]), [steps, steps]);

    // Switching language mid-flow keeps the place, choices and ticks.
    const other = language === 'en' ? 'de' : 'en';
    await progress.getByRole('link', { name: `${t.steps.skills} (${t.ui.done})`, exact: true }).click();
    await route(page, 'skills');
    await page.getByLabel(t.ui.languageLabel, { exact: true }).focus();
    await page.getByLabel(t.ui.languageLabel, { exact: true }).selectOption(other);
    assert.equal(await heading(page).innerText(), TEXT[other].skills[assistant].title);
    assert.equal(await page.locator('html').getAttribute('lang'), other);
    assert.equal(await page.getByLabel(TEXT[other].ui.languageLabel, { exact: true }).evaluate(e => e === document.activeElement), true);
    assert.equal(await page.locator('main input[type=checkbox]:not(:checked)').count(), 0);
    await page.reload();
    assert.equal(await heading(page).innerText(), TEXT[other].skills[assistant].title, 'Language survives a reload');
    await page.getByLabel(TEXT[other].ui.languageLabel, { exact: true }).selectOption(language);

    for (const width of [390, 320]) {
      await page.setViewportSize({ width, height: 844 });
      for (const name of ROUTES) {
        await page.goto(`${url}#${name}`);
        await route(page, name);
        await noCredentialFields(page);
        assert.equal(await heading(page).count(), 1, `One heading on ${name}`);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true, `Overflow at ${width}px on ${name}`);
      }
      await page.goto(`${url}#app`);
      await route(page, 'app');
      if (width === 390) {
        // On a phone the step list stays compact, so the step itself starts near the top.
        const top = await heading(page).evaluate(e => e.getBoundingClientRect().top + window.scrollY);
        assert.ok(top < 300, `Heading starts at ${top}px on a phone`);
      }
      await shot(`app-${width}`);
      await page.goto(`${url}#safety`);
      await route(page, 'safety');
      await shot(`safety-${width}`);
    }
    assert.deepEqual(issues, []);
  } catch (error) {
    await capture(page, { path: path.join(output, `${browserName}-${language}-${assistant}-failure.png`), fullPage: true }).catch(() => {});
    throw error;
  } finally { await ctx.close(); }
}

async function edgeCases(browser) {
  const issues = [];
  // Unknown and inherited-property routes fall back to the start; no assistant
  // means the provider steps ask for that choice first.
  let ctx = await context(browser, issues, { language: 'de' });
  let page = await ctx.newPage();
  for (const name of ['__proto__', 'constructor', 'toString', 'demo-__proto__', 'demo-unknown', 'unknown']) {
    await page.goto(`${url}#${name}`);
    await page.waitForFunction(() => location.hash === '#welcome');
    assert.equal(await heading(page).innerText(), TEXT.de.welcome.title, `Fallback for ${name}`);
  }
  await page.goto(`${url}#skills`);
  await page.waitForFunction(() => location.hash === '#assistant');
  assert.equal(await heading(page).innerText(), TEXT.de.assistant.title);
  await page.getByText(TEXT.de.ui.chooseFirst, { exact: true }).waitFor();
  await page.goto(`${url}#demos`);
  await route(page, 'demos');
  for (const provider of ['claude', 'openai']) await page.locator('main').getByText(plain(TEXT.de.demos.call[provider]), { exact: true }).waitFor();
  // The data step is readable before choosing; it shows both providers' settings.
  await page.goto(`${url}#safety`);
  await route(page, 'safety');
  for (const provider of ['claude', 'openai']) await page.locator(`main a[href="${LINKS.privacy[provider]}"]`).waitFor();
  assert.equal(await page.locator('main input[type=checkbox]').count(), TEXT.de.safety.claude.steps.length + TEXT.de.safety.openai.steps.length);
  // Keyboard users can skip to the step content.
  await page.getByRole('link', { name: TEXT.de.ui.skip, exact: true }).focus();
  await page.keyboard.press('Enter');
  assert.equal(await page.locator('main').evaluate(e => e.contains(document.activeElement)), true);
  await ctx.close();

  // Storage refusal keeps the wizard usable and says progress is not kept.
  ctx = await context(browser, issues);
  await ctx.addInitScript(() => { Storage.prototype.setItem = () => { throw new DOMException('Quota exceeded', 'QuotaExceededError'); }; });
  page = await ctx.newPage();
  await page.goto(url);
  await page.getByText(TEXT.en.ui.notSaved, { exact: true }).waitFor();
  await page.getByRole('button', { name: TEXT.en.ui.start, exact: true }).click();
  await page.getByRole('button', { name: fill(TEXT.en.assistant.choose, { name: TEXT.en.assistant.claude.name }), exact: true }).click();
  await next(page, TEXT.en);
  assert.equal(await heading(page).innerText(), TEXT.en.account.claude.title);
  await ctx.close();

  // A phone cannot install the desktop apps; the app step says so.
  ctx = await context(browser, issues, { agent: 'iphone', width: 390, height: 844 });
  page = await ctx.newPage();
  await page.goto(url);
  await page.getByRole('button', { name: TEXT.en.ui.start, exact: true }).click();
  await page.getByRole('button', { name: fill(TEXT.en.assistant.choose, { name: TEXT.en.assistant.openai.name }), exact: true }).click();
  await page.goto(`${url}#app`);
  await route(page, 'app');
  await page.getByText(TEXT.en.ui.mobile, { exact: true }).waitFor();
  await page.getByText(TEXT.en.app.unknown, { exact: true }).waitFor();
  await ctx.close();
  assert.deepEqual(issues, []);
}

(async () => {
  fs.mkdirSync(output, { recursive: true });
  const browser = await playwright[browserName].launch();
  try {
    for (const [language, assistant, os] of JOURNEYS) await journey(browser, language, assistant, os);
    await edgeCases(browser);
    console.log(`${browserName}: ${JOURNEYS.length} EN/RU/DE journeys (Claude/ChatGPT, Windows/Mac), data-and-risks step with settings checklist and share check, screenshot dialog, progress meter, language switch, reload, storage refusal, phone and fallback routes, 1280/390/320px, file opening without network requests — passed`);
    if (captureDiagnostics) console.log(`${captureDiagnostics} WebKit screenshot-injection CSP diagnostics identified separately; the page CSP was not relaxed.`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
