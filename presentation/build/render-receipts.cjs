// Renders a receipt carousel to 1080x1350 PNGs (LinkedIn's image size) and a PDF: node render-receipts.cjs <lang>
const path = require('node:path');
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');
const playwright = require('playwright');

(async () => {
  const lang = process.argv[2] || 'en';
  const build = __dirname;
  const outDir = path.resolve(build, `../carousel-${lang}`);
  fs.rmSync(path.join(outDir, 'slides'), { recursive: true, force: true });
  fs.mkdirSync(path.join(outDir, 'slides'), { recursive: true });
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(build, `receipt-${lang}.html`)).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  console.log('Martian Mono loaded:', await page.evaluate(() => document.fonts.check('700 30px "Martian Mono"')));
  const slides = await page.$$('section.slide:not(.vonly)');
  for (const [i, s] of slides.entries()) {
    const id = await s.getAttribute('id');
    const issues = await s.evaluate(el => {
      const r = el.getBoundingClientRect();
      const rec = el.querySelector('.receipt');
      const rr = rec ? rec.getBoundingClientRect() : null;
      const out = [];
      if (rr && rr.bottom > r.bottom - 20) out.push(`receipt bottom ${Math.round(rr.bottom - r.top)} > ${r.height - 20}`);
      for (const row of el.querySelectorAll('.row')) {
        const k = row.querySelector('.k'), v = row.querySelector('.v');
        if (k && v && (k.getBoundingClientRect().height > 60 || v.getBoundingClientRect().height > 60) && !row.classList.contains('dw')) out.push('wrapped row: ' + row.textContent.slice(0, 40));
      }
      return out;
    });
    if (issues.length) console.log(`${id}:`, issues.join(' | '));
    await s.screenshot({ path: path.join(outDir, 'slides', `${String(i + 1).padStart(2, '0')}-${id}.png`) });
  }
  await page.pdf({ path: path.join(outDir, `german-business-kit-carousel-${lang}.pdf`), width: '1080px', height: '1350px', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log(`${lang}: ${slides.length} slides`);
})().catch(e => { console.error(e); process.exit(1); });
