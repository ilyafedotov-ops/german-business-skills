// Qualify browser upgrades without hiding application CSP violations.
const assert = require('node:assert/strict');
const playwright = require('playwright');
const browserName = process.argv.find(arg => arg.startsWith('--browser='))?.split('=')[1] || 'chromium';

(async () => {
  const browser = await playwright[browserName].launch();
  try {
    for (const [name, body, blocked] of [
      ['text input', '<input aria-label="Example">', false],
      ['native select', '<select aria-label="Example"><option>One</option><option>Two</option></select>', false],
      ['inline style attribute', '<p id="target" style="color:red">Example</p>', true],
      ['inline stylesheet', '<style>#target { color:red }</style><p id="target">Example</p>', true],
    ]) {
      const page = await browser.newPage();
      const errors = [];
      page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
      page.on('pageerror', error => errors.push(error.message));
      await page.route('http://csp.invalid/', route => route.fulfill({
        contentType: 'text/html',
        headers: { 'Content-Security-Policy': "default-src 'none'; style-src 'self'" },
        body: `<!doctype html><html><head><title>Synthetic CSP check</title></head><body>${body}</body></html>`,
      }));
      await page.goto('http://csp.invalid/');
      if (name === 'native select') {
        await page.getByLabel('Example').selectOption({ label: 'Two' });
        assert.equal(await page.getByLabel('Example').inputValue(), 'Two');
      }
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      if (blocked) {
        assert.ok(errors.some(error => /Content.Security.Policy/.test(error)), `${name}: missing CSP diagnostic`);
        assert.notEqual(await page.locator('#target').evaluate(el => getComputedStyle(el).color), 'rgb(255, 0, 0)', `${name}: forbidden style applied`);
      } else {
        assert.deepEqual(errors, [], `${name}: unexpected console errors`);
      }
      await page.close();
    }
    console.log(`${browserName}: native controls are CSP-clean; forbidden inline styles remain blocked and reported.`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
