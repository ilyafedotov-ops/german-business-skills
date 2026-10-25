// Developer-only checks. End users open prototype/index.html without Node or Python.
const assert = require('node:assert/strict');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const fs = require('node:fs/promises');
const playwright = require('playwright');
const browserName = process.argv.find(a => a.startsWith('--browser='))?.split('=')[1] || 'chromium';
const url = pathToFileURL(path.resolve('prototype/index.html')).href;
const output = path.resolve('output/prototype');
const click = (page, name) => page.getByRole('button', { name, exact: true }).click();
const visible = async (page, text) => page.getByText(text, { exact: false }).first().waitFor({ state: 'visible' });
const saved = page => visible(page, 'Saved on this browser');
const capturing = new WeakSet();
let screenshotDiagnostics = 0;
async function capture(page, options) {
  capturing.add(page);
  try { await page.screenshot({ caret: 'initial', ...options }); }
  finally { capturing.delete(page); }
}

(async () => {
  await fs.mkdir(output, { recursive: true });
  const browser = await playwright[browserName].launch();
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, locale: 'en-GB', timezoneId: 'Europe/Berlin' });
  const issues = [];
  context.on('page', p => {
    p.on('pageerror', e => issues.push(String(e)));
    p.on('console', m => {
      if (m.type() !== 'error') return;
      // WebKit rejects Playwright's screenshot-only injected stylesheet under
      // our CSP. A minimal load+capture probe reproduced this without app actions.
      // Keep CSP intact; filter only that exact diagnostic during capture.
      if (browserName === 'webkit' && capturing.has(p) && m.text() === "Refused to apply a stylesheet because its hash, its nonce, or 'unsafe-inline' does not appear in the style-src directive of the Content Security Policy.") screenshotDiagnostics++;
      else issues.push(m.text());
    });
    p.on('requestfailed', r => issues.push(`${r.url()}: ${r.failure()?.errorText}`));
    p.on('request', r => { if (/^https?:/.test(r.url())) issues.push(`Unexpected network request: ${r.url()}`); });
  });
  const page = await context.newPage();
  try {
    await page.goto(url);
    await visible(page, 'Fictional data');
    await capture(page, { path: path.join(output, `${browserName}-home-desktop.png`), fullPage: true });
    await page.getByRole('link', { name: 'Documents', exact: true }).click();
    await visible(page, 'Your next step starts with a document.');
    await page.getByRole('link', { name: 'Skip to content', exact: true }).focus();
    await page.keyboard.press('Enter');
    assert.ok(page.url().endsWith('#documents'));
    await visible(page, 'Your next step starts with a document.');
    assert.equal(await page.locator('main').evaluate(e => e === document.activeElement), true);
    await page.getByRole('link', { name: 'Home', exact: true }).click();
    await click(page, 'Organize existing records');
    await click(page, 'Continue');
    await visible(page, 'old-backup.exe');
    await page.locator('input[name=import][value=receipt]').uncheck();
    await page.reload();
    await visible(page, 'Here is what the sample folder contains.');
    assert.equal(await page.locator('input[name=import][value=receipt]').isChecked(), false);
    for (const item of await page.locator('input[name=import]').all()) await item.uncheck();
    await click(page, 'Review selection');
    await visible(page, 'Choose at least one example file');
    for (const item of await page.locator('input[name=import]').all()) await item.check();
    await click(page, 'Review selection');
    await click(page, 'Add selected examples');
    await visible(page, '3 documents shown');
    await page.getByLabel('Search documents').fill('nothing matches');
    await visible(page, 'No matching documents.');
    await page.getByLabel('Search documents').fill('studio');
    await visible(page, '1 document shown');
    await click(page, 'Review invoice');
    await click(page, 'Mark document reviewed');
    assert.ok(await page.locator('#review-error').isVisible());
    await page.locator('#review-error a').click();
    assert.equal(await page.locator('#invoice-amount').evaluate(e => e === document.activeElement), true);
    await page.getByLabel('Total amount · EUR').fill('119,80');
    await page.getByLabel('Note for later').fill('Check business use before classifying.');
    await saved(page);
    await click(page, 'Save draft');
    await page.close();
    const resumed = await context.newPage();
    await resumed.goto(url);
    await click(resumed, 'Continue where I stopped');
    assert.equal(await resumed.getByLabel('Total amount · EUR').inputValue(), '119,80');
    assert.equal(await resumed.getByLabel('Note for later').inputValue(), 'Check business use before classifying.');
    assert.equal(await resumed.getByLabel('Proposed category').inputValue(), '');
    await click(resumed, 'Mark document reviewed');
    await visible(resumed, 'Category remains unresolved. No accounting entry recorded.');
    await capture(resumed, { path: path.join(output, `${browserName}-review-desktop.png`), fullPage: true });
    await resumed.getByRole('link', { name: 'This month', exact: true }).click();
    await visible(resumed, '1 of 2 example checks completed');
    await click(resumed, 'Investigate payment');
    await resumed.getByLabel('Investigation note').fill('Reference and date checked against sample receipt.');
    await click(resumed, 'Keep open and return later');
    await click(resumed, 'Continue where I stopped');
    await visible(resumed, 'Unmatched');
    assert.equal(await resumed.getByLabel('Investigation note').inputValue(), 'Reference and date checked against sample receipt.');
    await click(resumed, 'Link this example receipt');
    await visible(resumed, 'Receipt linked in this demo. No accounting entry recorded.');
    await resumed.locator('main').getByRole('button', { name: 'Help me with this', exact: true }).click();
    assert.match(await resumed.getByLabel('Ready-to-use assistant request').inputValue(), /DEMO-PAY-010/);
    await resumed.keyboard.press('Escape');
    assert.equal(await resumed.locator('#help-dialog').isVisible(), false);
    assert.equal(await resumed.locator('main').getByRole('button', { name: 'Help me with this', exact: true }).evaluate(e => e === document.activeElement), true);
    for (const name of ['Taxes and letters', 'Accounts and services']) await resumed.getByRole('link', { name, exact: true }).click();
    await resumed.getByRole('button', { name: 'Explore connection', exact: true }).first().click();
    assert.match(await resumed.getByLabel('Ready-to-use assistant request').inputValue(), /Gmail/);
    await click(resumed, 'Close help');
    // One tab's stale draft must never replace a newer saved correction.
    await resumed.getByRole('link', { name: 'Documents', exact: true }).click();
    await click(resumed, 'Review invoice');
    const other = await context.newPage();
    await other.goto(`${url}#review`);
    await resumed.getByLabel('Note for later').fill('Newer work in first tab');
    await other.getByLabel('Note for later').fill('Stale tab draft stays here');
    await visible(other, 'Another tab changed this demo.');
    assert.equal(await other.getByLabel('Note for later').inputValue(), 'Stale tab draft stays here');
    await other.reload();
    assert.equal(await other.getByLabel('Note for later').inputValue(), 'Newer work in first tab');
    await other.close();
    // Check every screen at narrow widths; only navigation itself may scroll.
    for (const width of [390, 320]) {
      await resumed.setViewportSize({ width, height: 844 });
      for (const route of ['home', 'documents', 'review', 'month', 'payment', 'taxes', 'accounts', 'settings', 'onboard']) {
        await resumed.goto(`${url}#${route}`);
        assert.equal(await resumed.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true, `Overflow at ${width}px on ${route}`);
      }
      await resumed.goto(`${url}#review`);
      await capture(resumed, { path: path.join(output, `${browserName}-review-${width}.png`), fullPage: true });
    }
    await resumed.getByRole('link', { name: 'Settings and demo information' }).click();
    await click(resumed, 'Reset fictional demo data');
    await click(resumed, 'Keep my demo work');
    await click(resumed, 'Reset fictional demo data');
    await click(resumed, 'Reset demo');
    await visible(resumed, 'A place for your business to make sense.');
    // Runtime storage rejection keeps fields visible and never reports success.
    const failed = await context.newPage();
    await failed.goto(`${url}#review`);
    await failed.evaluate(() => { Storage.prototype.setItem = () => { throw new DOMException('Quota exceeded', 'QuotaExceededError'); }; });
    await failed.getByRole('button', { name: 'Choose example files', exact: true }).click();
    await click(failed, 'Continue');
    await click(failed, 'Review selection');
    await click(failed, 'Add selected examples');
    await click(failed, 'Review invoice');
    await failed.getByLabel('Total amount · EUR').fill('119.80');
    await click(failed, 'Save draft');
    assert.equal(await failed.getByLabel('Total amount · EUR').inputValue(), '119.80');
    await visible(failed, 'Your draft is still here, but was not saved.');
    assert.ok(!(await failed.locator('#save-status').innerText()).startsWith('Saved'));
    await capture(failed, { path: path.join(output, `${browserName}-storage-error.png`), fullPage: true });
    assert.deepEqual(issues, []);
    console.log(`${browserName}: four journeys, empty/error/help/reset/conflict states, 1440/390/320px, direct file opening, no unexpected console errors or network requests — passed`);
    if (screenshotDiagnostics) console.log(`${screenshotDiagnostics} WebKit screenshot-injection CSP diagnostics identified separately; application CSP was not relaxed.`);
  } catch (error) {
    for (const [i, p] of context.pages().entries()) await p.screenshot({ caret: 'initial', path: path.join(output, `${browserName}-failure-${i}.png`), fullPage: true }).catch(() => {});
    throw error;
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
