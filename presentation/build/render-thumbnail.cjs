// Renders thumbnail.html to a 1280x720 PNG for YouTube.
const path = require('node:path');
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');
const playwright = require('playwright');
(async () => {
  const out = path.resolve(__dirname, '../video');
  fs.mkdirSync(out, { recursive: true });
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto(pathToFileURL(path.join(__dirname, process.argv[2] || 'thumbnail.html')).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(out, 'youtube-thumbnail.png') });
  await browser.close();
  console.log('ok');
})().catch(e => { console.error(e); process.exit(1); });
