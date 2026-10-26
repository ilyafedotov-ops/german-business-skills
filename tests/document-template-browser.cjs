/* Developer-only synthetic render/export checks; no user runtime dependency.
 * Acceptance: offline EN/RU/DE readable content, visible draft, no active source
 * markup, no horizontal clipping at 390/1280px, and A4 PDF with long tables.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium, webkit} = require('playwright');
const escape = value => value.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
(async () => {
  const output = path.resolve('output/document-template');
  await fs.mkdir(output, {recursive:true});
  const template = await fs.readFile('skills/de-business-kit/assets/readable-document.html','utf8');
  const labels = {
    en:['October 2026 — records report','DRAFT — not submitted','Result','Item','Amount','Source','Unresolved: missing receipt.','Synthetic example · version 01'],
    ru:['Октябрь 2026 — отчёт по записям','ЧЕРНОВИК — не отправлен','Результат','Позиция','Сумма','Источник','Не выяснено: отсутствует чек.','Синтетический пример · версия 01'],
    de:['Oktober 2026 — Unterlagenübersicht','ENTWURF — nicht versandt','Ergebnis','Position','Betrag','Quelle','Offen: Beleg fehlt.','Synthetisches Beispiel · Version 01']
  };
  const selected = process.argv.find(arg => arg.startsWith('--browser='))?.split('=')[1];
  if (selected && !['chromium','webkit'].includes(selected)) throw new Error('Unsupported browser: ' + selected);
  for (const engine of [chromium,webkit].filter(engine => !selected || engine.name() === selected)) {
    const browser = await engine.launch({headless:true});
    try {
      for (const [lang,t] of Object.entries(labels)) {
        const source = '<img src="https://example.invalid/track" onerror="alert(1)">';
        const rows = Array.from({length:90}, (_,i) => `<tr><td>${t[3]} ${i+1}</td><td class="amount">123,45 EUR</td><td>${escape('SYNTHETIC-'+('reference-'.repeat(i===1 ? 18 : 1))+(i+1))}</td></tr>`).join('');
        const values = {LANG:lang,TITLE:escape(t[0]),STATUS:escape(t[1]),METADATA:escape('2026-10 · v01 · 2026-10-26'),
          CONTENT:`<h2>${t[2]}</h2><p>${escape(t[6])}</p><p>${escape(source)}</p><table><thead><tr><th scope="col">${t[3]}</th><th scope="col">${t[4]}</th><th scope="col">${t[5]}</th></tr></thead><tbody>${rows}</tbody></table>`,FOOTER:escape(t[7])};
        const html = template.replace(/\{\{([A-Z]+)\}\}/g,(_,key)=>values[key]);
        assert(!html.includes('{{'));
        const file = path.join(output,lang+'.html'); await fs.writeFile(file,html);
        for (const width of [390,1280]) {
          const page = await browser.newPage({viewport:{width,height:900}});
          const errors=[]; const external=[];
          page.on('pageerror', e=>errors.push(e.message));
          page.on('console', m=>{if(m.type()==='error') errors.push(m.text());});
          page.on('request', r=>{if(/^https?:/.test(r.url())) external.push(r.url());});
          await page.goto(pathToFileURL(file).href);
          assert.equal(await page.locator('html').getAttribute('lang'),lang);
          assert.equal(await page.locator('.status').innerText(),t[1]);
          assert.equal(await page.locator('tbody tr').count(),90);
          assert(await page.locator('tbody tr').first().locator('.amount').evaluate(cell => {
            const range=document.createRange(); range.selectNodeContents(cell);
            return range.getClientRects().length<=2;
          }), 'Amount is split into unreadable fragments by long source text');
          assert.equal(await page.locator('img,script,iframe').count(),0);
          assert(await page.locator('main').innerText().then(s=>s.includes(source)));
          assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Horizontal clipping');
          await page.screenshot({path:path.join(output,`${engine.name()}-${lang}-${width}.png`)});
          if (engine===chromium && width===1280) {
            await page.emulateMedia({media:'print'});
            assert(await page.locator('.status').isVisible());
            const pdf=await page.pdf({path:path.join(output,lang+'.pdf'),preferCSSPageSize:true,printBackground:true});
            assert.equal(pdf.subarray(0,4).toString(),'%PDF');
          }
          assert.deepEqual(external,[]);assert.deepEqual(errors,[]);
          await page.close();
        }
        console.log(`${engine.name()} ${lang}: desktop/mobile readable; offline escaping${engine===chromium?'; A4 PDF generated':''}`);
      }
    } finally {await browser.close();}
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
