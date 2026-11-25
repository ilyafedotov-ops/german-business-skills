// Renders the YouTube profile picture (800x800) and banner (2560x1440): node render-channel-art.cjs
const path = require('node:path');
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');
const playwright = require('playwright');

(async () => {
  const out = path.resolve(__dirname, '../video');
  fs.mkdirSync(out, { recursive: true });
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2560, height: 1440 } });
  await page.goto(pathToFileURL(path.join(__dirname, 'channel-art.html')).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  // Show one graphic at a time at the top of the viewport so nothing renders off-screen.
  for (const [id, file] of [['avatar', 'youtube-avatar.png'], ['banner', 'youtube-banner.png']]) {
    await page.evaluate(show => document.querySelectorAll('section').forEach(s => { s.style.display = s.id === show ? '' : 'none'; }), id);
    await (await page.$('#' + id)).screenshot({ path: path.join(out, file) });
  }
  await browser.close();
  console.log('ok');
})().catch(e => { console.error(e); process.exit(1); });
