// Development dependencies only; generated overviews open directly in a browser.
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {execFileSync} = require('node:child_process');
const playwright = require('playwright');

(async () => {
  const browserName = process.argv.find(arg => arg.startsWith('--browser='))?.split('=')[1] || 'chromium';
  assert(['chromium','webkit'].includes(browserName));
  const output = path.resolve('output/overview');
  execFileSync(process.env.GBK_TEST_PYTHON || (process.platform === 'win32' ? 'python' : 'python3'),
    ['-B', 'tests/overview-fixtures.py', output], {stdio:'pipe'});
  const browser = await playwright[browserName].launch();
  try {
    const kinds = process.platform === 'win32' || process.env.GBK_TEST_DOCKER_IMAGE ? ['', '-native'] : [''];
    for (const kind of kinds) for (const language of ['en','ru']) for (const scenario of ['empty','blocked','corrupt','lifecycle']) {
      for (const width of [390,1280]) {
        const page = await browser.newPage({viewport:{width,height:900}});
        const issues=[];
        page.on('pageerror', e=>issues.push(e.message));
        page.on('console', m=>{if(m.type()==='error') issues.push(m.text());});
        page.on('requestfailed', r=>issues.push(r.url()));
        page.on('request', r=>{if(/^https?:/.test(r.url())) issues.push('External request: '+r.url());});
        await page.goto(pathToFileURL(path.join(output,`${language}-${scenario}${kind}.html`)).href);
        assert.equal(await page.locator('html').getAttribute('lang'),language);
        assert.equal(await page.locator('script,iframe,img').count(),0);
        if (scenario==='blocked') {
          assert((await page.locator(kind ? 'body' : '#needs-review').innerText()).includes('Clarify invoice country'));
          assert((await page.locator(kind ? 'body' : '#accounting-tax').innerText()).includes('return-1'));
          assert((await page.locator('body').innerText()).includes('<script>alert(1)</script>'));
        }
        if (scenario==='lifecycle') {
          const tasks=page.locator(kind ? 'body' : '#active-tasks');
          assert((await tasks.innerText()).includes('Prepare registration <script>alert(1)</script>'));
          assert((await tasks.innerText()).includes('Review authority reply'));
          assert((await tasks.innerText()).includes(language==='en'?'No date recorded':'Дата не задана'));
          assert((await tasks.innerText()).includes(language==='en'?'Unresolved dependencies':'Незавершённые зависимости'));
          if (!kind) {
            const taskLink=page.locator('nav a[href="#active-tasks"]');
            await taskLink.focus(); await page.keyboard.press('Enter');
            assert(page.url().endsWith('#active-tasks'));
            assert(await tasks.isVisible());
          }
        }
        if (scenario==='corrupt') {
          if (kind) assert((await page.locator('body').innerText()).includes('Accounting register is missing'));
          else assert(await page.locator('.warning').isVisible());
        }
        assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Horizontal overflow');
        if (!kind) {
        const link=page.locator('nav a[href="#accounting-tax"]');
        await link.focus(); await page.keyboard.press('Enter');
        assert(page.url().endsWith('#accounting-tax'));
        assert(await page.locator('#accounting-tax').isVisible());
        const disclosure=page.locator('#accounting-tax details summary');
        await disclosure.focus(); await page.keyboard.press('Enter');
        assert(await disclosure.evaluate(el=>el.parentElement.open));
        }
        await page.screenshot({path:path.join(output,`${browserName}-${language}-${scenario}${kind}-${width}.png`),fullPage:true});
        assert.deepEqual(issues,[]);
        await page.close();
      }
    }
    console.log(`${browserName}: real overview EN/RU, empty/blocked/corrupt/lifecycle, 390/1280, keyboard, escaping and no network/console errors passed`);
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
