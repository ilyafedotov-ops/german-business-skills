// Real local workspace GUI journeys; synthetic inputs only.
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const { spawn, execFileSync } = require('node:child_process');
const readline = require('node:readline');
const playwright = require('playwright');
const { stopChild } = require('./gui-lifecycle.cjs');
const browserName = process.argv.find(a => a.startsWith('--browser='))?.split('=')[1] || 'chromium';
const output = path.resolve('output/gui');
const python = process.env.GUI_PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
const capturing=new WeakSet();
let screenshotDiagnostics=0;
async function capture(page,options){capturing.add(page);try{await page.screenshot({caret:'initial',...options});}finally{capturing.delete(page);}}
const click = (page, name) => page.getByRole('button', { name, exact: true }).click();
async function fixture(root) {
  execFileSync(python, ['-B', '-c', `import sys; sys.path.insert(0, 'skills/de-business-kit/scripts'); import workspace as ws; ws.start_workspace(sys.argv[1], year=2026, language='en')`, root], { cwd: process.cwd() });
}
// Capture a source-startup stack before the existing deadline. Cancel the timer
// once binding completes so a long browser journey does not emit false traces.
const startupProbe = [
  'import faulthandler, runpy',
  'faulthandler.dump_traceback_later(10)',
  "scope = runpy.run_path('gui/server.py')",
  "original_create = scope['create_server']",
  'def observed_create(*args, **kwargs):',
  '    try: return original_create(*args, **kwargs)',
  '    finally: faulthandler.cancel_dump_traceback_later()',
  "scope['main'].__globals__['create_server'] = observed_create",
  "scope['main']()",
].join('\n');
function start(root) {
  const child = spawn(python, ['-B', '-X', 'faulthandler', '-c', startupProbe, '--root', root, '--no-browser', '--port', '0'], { cwd: process.cwd(), stdio: ['ignore', 'pipe', 'pipe'] });
  let stderr = '';
  child.stderr.on('data', chunk => { stderr += chunk; });
  const ready = new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`GUI startup timed out: ${stderr}`)), 15000);
    child.once('error', error => { clearTimeout(timer); reject(new Error(`GUI could not start: ${error.message}`)); });
    child.once('exit', code => { clearTimeout(timer); reject(new Error(`GUI exited ${code}: ${stderr}`)); });
    readline.createInterface({ input: child.stdout }).on('line', line => {
      try { const value = JSON.parse(line); if (value.url && value.token) { clearTimeout(timer); resolve(value); } } catch { /* not readiness */ }
    });
  });
  return { child, ready, stderr: () => stderr };
}
(async () => {
  const temp = await fs.realpath(await fs.mkdtemp(path.join(os.tmpdir(), 'gbk-gui-browser-')));
  const root = path.join(temp, 'business');
  await fixture(root);
  await fs.mkdir(output,{recursive:true});
  const server = start(root);
  let browser, page, failure, sessionToken = '';
  const pendingRequests = new Map(), apiResults = [], issues = [], assets = [];
  const staticRequests = new WeakMap();
  const redact = value => sessionToken ? String(value).replaceAll(sessionToken, '[redacted-session]') : String(value);
  try {
    const { url, token } = await server.ready;
    sessionToken = token;
    browser = await playwright[browserName].launch();
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, locale: 'en-GB', timezoneId: 'Europe/Berlin' });
    context.on('request', request => {
      const target = new URL(request.url());
      if (request.method() === 'GET' && target.origin === new URL(url).origin && ['/', '/app.js', '/i18n.js', '/style.css'].includes(target.pathname)) {
        const asset = { path: target.pathname, started: Date.now() };
        staticRequests.set(request, asset); assets.push(asset);
        if (assets.length > 12) assets.shift();
      }
      if (request.url() === url+'api' && request.method() === 'POST') {
        pendingRequests.set(request, { op: request.postDataJSON()?.op, started: Date.now() });
      }
    });
    context.on('response', async response => {
      const asset = staticRequests.get(response.request());
      if (asset) { asset.status = response.status(); asset.elapsedMs = Date.now()-asset.started; }
      const request = response.request(), pending = pendingRequests.get(request);
      if (!pending) return;
      const value = await response.json().catch(() => ({}));
      pendingRequests.delete(request);
      apiResults.push({ op: pending.op, elapsedMs: Date.now()-pending.started, status: response.status(), ok: value.ok, error: value.error });
      if (apiResults.length > 12) apiResults.shift();
    });
    context.on('requestfailed', request => {
      const asset = staticRequests.get(request);
      if (asset) { asset.error = request.failure()?.errorText; asset.elapsedMs = Date.now()-asset.started; }
    });
    context.on('page', p => {
      p.on('pageerror', err => issues.push(String(err)));
      p.on('requestfailed', req => issues.push(`${req.url()}: ${req.failure()?.errorText}`));
      p.on('request', req => { if (!req.url().startsWith(url) && !req.url().startsWith('blob:') && !req.url().startsWith('data:')) issues.push(`External request: ${req.url()}`); });
      p.on('console', message => { if(browserName==='webkit'&&capturing.has(p)&&message.text()==="Refused to apply a stylesheet because its hash, its nonce, or 'unsafe-inline' does not appear in the style-src directive of the Content Security Policy."){screenshotDiagnostics++;return;} if (message.type() === 'error' && !/^Failed to load resource: the server responded with a status of (400|409)/.test(message.text())) issues.push(message.text()); });
    });
    page = await context.newPage();
    await page.goto(`${url}#token=${token}`);
    await page.getByRole('heading', { name: 'Your business, one clear next step.' }).waitFor();
    await page.getByLabel('Working month').fill('2026-10');
    await page.getByLabel('Working month').press('Tab');
    await page.waitForFunction(()=>document.querySelector('main').getAttribute('aria-busy')==='false');
    assert.ok(!page.url().includes(token), 'Bootstrap token must leave URL');
    await page.getByRole('heading',{name:'What would you like to work on?'}).waitFor({timeout:3000});
    assert.equal(await page.locator('.next-step').getByRole('button',{name:'Add documents',exact:true}).count(),0,'Empty workspace must ask the desired task before importing');
    await page.locator('.next-step').getByRole('button',{name:'Help me with this',exact:true}).click();
    assert.match(await page.locator('#help-prompt').inputValue(),/What would you like to work on/);
    await click(page,'Close');
    for (const width of [1280,390]) {
      await page.setViewportSize({width,height:1000});
      await capture(page,{path:path.join(output,`${browserName}-empty-home-actual-${width}.png`),fullPage:true});
    }
    // Existing document/accounting work remains useful without active lifecycle tasks.
    const populatedRoot=path.join(temp,'populated-no-tasks');
    await fixture(populatedRoot);
    execFileSync(python,['-B','-c',`
import sys
from pathlib import Path
sys.path.insert(0, 'skills/de-business-kit/scripts')
import workspace as ws
root = Path(sys.argv[1])
source = root.parent / 'no-task-invoice.xml'
source.write_text('<invoice>Synthetic no-task invoice</invoice>', encoding='utf-8')
ws.ingest_document(root, source, '2026-10')
`,populatedRoot],{cwd:process.cwd()});
    const selectWorkspace=async destination=>{
      await page.getByRole('link',{name:'Settings and recovery',exact:true}).click();
      await click(page,'Open another workspace');
      await page.getByLabel('Workspace folder').fill(destination);
      await click(page,'Open existing workspace');
      await page.getByRole('heading',{name:'Your business, one clear next step.'}).waitFor();
    };
    await selectWorkspace(populatedRoot);
    await page.locator('.next-step').getByRole('button',{name:'Review the next document',exact:true}).waitFor({timeout:3000});
    await page.locator('.next-step').getByRole('button',{name:'Review the next document',exact:true}).click();
    await page.getByLabel('Review status').selectOption('reviewed');
    await page.getByLabel('Reviewer').fill('Synthetic owner');
    await page.getByLabel('Review note').fill('Checked no-task synthetic source.');
    await click(page,'Save document details');
    await page.getByText('Saved to your workspace.',{exact:true}).waitFor();
    await page.getByRole('link',{name:'Home',exact:true}).click();
    await page.locator('.next-step').getByRole('button',{name:'Choose where your accounts are kept',exact:true}).waitFor();
    await page.getByLabel('Working month').fill('2026-12');
    await page.getByLabel('Working month').press('Tab');
    await page.waitForFunction(()=>document.querySelector('main').getAttribute('aria-busy')==='false');
    await page.locator('.next-step').getByRole('button',{name:'Choose where your accounts are kept',exact:true}).click();
    await page.getByLabel('Accounting system').selectOption('local');
    await page.getByLabel('Accounting method').selectOption('EÜR');
    await page.getByLabel('Account reference').fill('synthetic-no-task');
    await page.getByLabel('Reviewer').fill('Synthetic owner');
    await page.getByLabel('Evidence file').selectOption({index:1});
    await click(page,'Save accounting choice');
    await click(page,'Confirm and save');
    await page.getByText('Saved to your workspace.',{exact:true}).waitFor();
    await page.getByRole('link',{name:'Home',exact:true}).click();
    await page.locator('.next-step').getByRole('button',{name:'Continue your work',exact:true}).click();
    await page.getByRole('heading',{name:'Make the month understandable.'}).waitFor();
    await selectWorkspace(root);
    await page.getByLabel('Working month').fill('2026-10');
    await page.getByLabel('Working month').press('Tab');
    await page.waitForFunction(()=>document.querySelector('main').getAttribute('aria-busy')==='false');
    // Canonical task writers preserve the sole register and its evidence history.
    execFileSync(python,['-B','-c',`
import sys
from pathlib import Path
sys.path.insert(0, 'skills/de-business-kit/scripts')
import workspace as ws
root = Path(sys.argv[1])
ws.save_entry(root, 'tasks', {'schema_version':1, 'id':'formation-undated', 'title':'Prepare my first business activity', 'owner':'Synthetic owner', 'status':'pending', 'note':'Choose the next formation step.'})
ws.save_entry(root, 'tasks', {'schema_version':1, 'id':'formation-dependent', 'title':'Register <img src=x onerror="window.taskInjected=true"> activity', 'owner':'Synthetic <owner>', 'status':'pending', 'depends_on':['formation-undated'], 'due_date':'2026-11-12', 'deadline_source':'Explicit synthetic target <source>', 'note':'Await the activity choice <note>.'})
item = {'schema_version':1, 'id':'evidence-review', 'title':'Check changed registration evidence', 'owner':'Synthetic owner', 'status':'pending', 'evidence_file':'task-evidence.txt'}
(root / 'task-evidence.txt').write_text('Synthetic original evidence', encoding='utf-8')
ws.save_entry(root, 'tasks', item)
(root / 'task-evidence.txt').write_text('Synthetic changed evidence', encoding='utf-8')
(root / 'task-completed.txt').write_text('Synthetic completion evidence', encoding='utf-8')
completed = {'schema_version':1, 'id':'completed-task', 'title':'Completed synthetic task', 'owner':'Synthetic owner', 'status':'pending'}
previous = ws.save_entry(root, 'tasks', completed)
ws.save_entry(root, 'tasks', dict(completed, status='completed', evidence_file='task-completed.txt'), previous['sha256'])
cancelled = {'schema_version':1, 'id':'cancelled-task', 'title':'Cancelled synthetic task', 'owner':'Synthetic owner', 'status':'pending'}
previous = ws.save_entry(root, 'tasks', cancelled)
ws.save_entry(root, 'tasks', dict(cancelled, status='cancelled'), previous['sha256'])
`,root],{cwd:process.cwd()});
    await click(page,'Refresh records');
    // The short render assertion starts after the filesystem snapshot is ready.
    await page.waitForFunction(()=>document.querySelector('main').getAttribute('aria-busy')==='false');
    await page.getByText('Prepare my first business activity',{exact:true}).first().waitFor({timeout:3000});
    const taskList=page.getByRole('list',{name:'Active tasks'});
    await taskList.getByText('Prepare my first business activity',{exact:true}).waitFor();
    assert.equal(await taskList.getByText('Completed synthetic task',{exact:true}).count(),0);
    assert.equal(await taskList.getByText('Cancelled synthetic task',{exact:true}).count(),0);
    await taskList.getByText('No date recorded',{exact:true}).first().waitFor();
    await taskList.getByText('Evidence not recorded',{exact:true}).first().waitFor();
    await taskList.getByText('Blocked by unfinished tasks: formation-undated',{exact:true}).waitFor();
    await taskList.getByText('Evidence needs review',{exact:true}).waitFor();
    await taskList.getByText('Explicit synthetic target <source>',{exact:true}).waitFor();
    await taskList.getByText('Register <img src=x onerror="window.taskInjected=true"> activity',{exact:true}).waitFor();
    assert.equal(await taskList.locator('img').count(),0,'Task titles must remain text');
    assert.equal(await page.evaluate(()=>window.taskInjected),undefined,'Task evidence must not execute');
    assert.equal(await page.locator('.next-step').getByRole('button',{name:'Choose where your accounts are kept',exact:true}).count(),0,'Formation tasks must not force an accounting choice');
    await page.locator('.next-step').getByRole('button',{name:'Continue with your assistant',exact:true}).focus();
    await page.keyboard.press('Enter');
    assert.match(await page.locator('#help-prompt').inputValue(),/formation-undated/);
    assert.match(await page.locator('#help-prompt').inputValue(),/Prepare my first business activity/);
    await click(page,'Close');
    await page.getByLabel('Working month').fill('2026-12');
    await page.getByLabel('Working month').press('Tab');
    await page.waitForFunction(()=>document.querySelector('main').getAttribute('aria-busy')==='false');
    assert.equal(await page.getByLabel('Working month').inputValue(),'2026-12');
    await taskList.getByText('Prepare my first business activity',{exact:true}).waitFor();
    await taskList.getByText('Blocked by unfinished tasks: formation-undated',{exact:true}).waitFor();
    for (const lang of ['en','ru','de']) {
      await page.locator('#language').selectOption(lang);
      const headings={en:'Active tasks',ru:'Текущие задачи',de:'Aktive Aufgaben'};
      await page.getByRole('heading',{name:headings[lang],exact:true}).waitFor();
      for (const width of [1280,390]) {
        await page.setViewportSize({width,height:1000});
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`${lang}/task home overflow at ${width}`);
        await capture(page,{path:path.join(output,`${browserName}-${lang}-task-home-${width}.png`),fullPage:true});
      }
    }
    await page.locator('#language').selectOption('en');
    await page.getByLabel('Working month').fill('2026-10');
    await page.getByLabel('Working month').press('Tab');
    await page.waitForFunction(()=>document.querySelector('main').getAttribute('aria-busy')==='false');
    await page.setViewportSize({width:1440,height:1000});
    await page.getByRole('link', { name: 'Documents', exact: true }).click();
    await page.getByLabel('Choose documents').setInputFiles({ name: 'synthetic-invoice.xml', mimeType: 'application/xml', buffer: Buffer.from('<invoice><total>119.80</total></invoice>') });
    await page.getByLabel('Storage month').fill('2026-10');
    await click(page, 'Import selected documents');
    await page.getByText('synthetic-invoice.xml', { exact: true }).first().waitFor();
    await click(page, 'Review details');
    await click(page, 'Open original');
    await page.locator('#original-preview pre').filter({hasText:'<invoice>'}).waitFor();
    await page.getByLabel('Readable title').fill('Reviewed synthetic invoice');
    await page.getByLabel('Document type').selectOption('invoice');
    await page.getByLabel('Review status').selectOption('reviewed');
    await page.getByLabel('Reviewer').fill('Synthetic owner');
    await page.getByLabel('Review note').fill('Checked against the original.');
    await click(page, 'Save document details');
    await page.getByText('Saved to your workspace.', { exact: true }).waitFor();
    await page.getByRole('link', { name: 'Accounts and services', exact: true }).click();
    await page.getByLabel('Accounting system').selectOption('local');
    await page.getByLabel('Accounting method').selectOption('EÜR');
    await page.getByLabel('Account reference').fill('synthetic-business');
    await page.getByLabel('Reviewer').fill('Synthetic owner');
    await page.getByLabel('Evidence file').selectOption({ index: 1 });
    await click(page, 'Save accounting choice');
    await click(page, 'Confirm and save');
    await page.getByText('Saved to your workspace.', { exact: true }).waitFor();
    await page.getByRole('link', { name: 'This month', exact: true }).click();
    await click(page, 'Add cash entry');
    await page.getByLabel('Entry date').fill('2026-10-20');
    await page.getByLabel('Account', { exact: true }).fill('bank');
    await page.getByLabel('Transaction reference').fill('synthetic-tx');
    await page.getByLabel('Total cash movement').fill('119.80');
    await page.getByLabel('Line amount').fill('119.80');
    await page.getByLabel('Movement kind').selectOption('income');
    await page.getByLabel('Category').fill('Synthetic service');
    await page.getByLabel('Activity reference').fill('activity-1');
    assert.equal(await page.getByLabel('Reviewed invoice (optional)').inputValue(),'','A cash line is not linked to an invoice by default');
    await page.getByLabel('VAT on the document').selectOption('stated');
    await page.getByLabel('Net amount (document)').fill('100,67');
    await page.getByLabel('VAT amount (document)').fill('19.13');
    await page.getByLabel('VAT rate % (document)').fill('19');
    await page.getByLabel('Reviewer').fill('Synthetic owner');
    await page.getByLabel('Evidence file').selectOption({ index: 1 });
    await page.getByLabel('Entry note').fill('Observed synthetic payment.');
    for(const width of [1440,390]) {
      await page.setViewportSize({width,height:1000});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`Entry editor overflow at ${width}`);
      await capture(page,{path:path.join(output,`${browserName}-entry-editor-${width}.png`),fullPage:true});
    }
    await page.setViewportSize({width:1440,height:1000});
    let releaseSave, saveWaiting;
    const saveGate=new Promise(resolve=>{releaseSave=resolve;});
    const saveStarted=new Promise(resolve=>{saveWaiting=resolve;});
    let delayNextDraft=true;
    const delayDraft=async requestRoute=>{
      const body=requestRoute.request().postDataJSON();
      if(body?.op==='draft-save'&&delayNextDraft){delayNextDraft=false;saveWaiting();await saveGate;}
      await requestRoute.continue();
    };
    await page.route(url+'api',delayDraft);
    await click(page,'Save draft');
    await saveStarted;
    assert.equal(await page.getByLabel('Total cash movement').isDisabled(),true);
    assert.equal(await page.locator('#language').isDisabled(),true);
    assert.equal(await page.locator('#period').isDisabled(),true);
    await page.getByRole('link',{name:'Accounts and services',exact:true}).click({force:true});
    assert.equal(await page.getByRole('heading',{name:'Record a cash movement',exact:true}).isVisible(),true,'Pending save must retain its form');
    await page.getByRole('link',{name:'Settings and recovery',exact:true}).click({force:true});
    assert.equal(await page.getByRole('heading',{name:'Record a cash movement',exact:true}).isVisible(),true);
    releaseSave();
    await page.getByText('Saved to your workspace.',{exact:true}).waitFor();
    await page.unroute(url+'api',delayDraft);
    await page.reload();
    await page.getByRole('link',{name:'Home',exact:true}).click();
    await page.locator('.next-step').getByRole('button',{name:'Continue your work',exact:true}).click();
    await page.getByRole('heading',{name:'Record a cash movement',exact:true}).waitFor();
    assert.equal(await page.getByLabel('Total cash movement').inputValue(),'119.80','Saved draft takes precedence over active tasks');
    await page.getByRole('link', { name: 'This month', exact: true }).click();
    await click(page, 'Resume entry draft');
    assert.equal(await page.getByLabel('Total cash movement').inputValue(), '119.80');
    assert.equal(await page.getByLabel('Net amount (document)').inputValue(), '100,67', 'Saved draft keeps the stated VAT');
    await click(page, 'Record cash entry');
    await page.getByRole('dialog').getByText('119.80 EUR', { exact: false }).waitFor();
    await page.getByRole('dialog').getByText('Stated: net and VAT shown: 100.67 + 19.13 (19 %)', { exact: true }).waitFor();
    await click(page, 'Confirm and save');
    await page.locator('main').getByText('synthetic-tx', { exact: true }).waitFor();
    await page.getByText('Saved to your workspace.', { exact: true }).waitFor();
    await click(page,'Reverse entry');
    await page.getByLabel('Person recording this').fill('Synthetic owner');
    await page.getByLabel('Evidence file').selectOption({index:1});
    await page.getByLabel('Reason for reversal').fill('Correcting synthetic amount after checking source.');
    await click(page,'Record reversal');
    await click(page,'Confirm and save');
    await page.getByRole('button',{name:'Create linked correction',exact:true}).waitFor();
    await page.getByText('Saved to your workspace.', { exact: true }).waitFor();
    await click(page,'Create linked correction');
    assert.equal(await page.getByLabel('Transaction reference').inputValue(),'synthetic-tx');
    await page.getByLabel('Total cash movement').fill('90.00');
    await page.getByLabel('Line amount').fill('90.00');
    await page.getByLabel('Movement kind').selectOption('income');
    await page.getByLabel('Category').fill('Corrected synthetic service');
    await page.getByLabel('Activity reference').fill('activity-1');
    await page.getByLabel('Reviewer').fill('Synthetic owner');
    await page.getByLabel('Evidence file').selectOption({index:1});
    await page.getByLabel('Entry note').fill('Linked correction; prior evidence retained.');
    await click(page,'Record cash entry');
    await click(page,'Confirm and save');
    await page.locator('main').getByText('90.00 EUR',{exact:true}).waitFor();
    await page.getByText('Saved to your workspace.', { exact: true }).waitFor();
    await page.getByRole('link', { name: 'Taxes and letters', exact: true }).click();
    await click(page, 'Create filing draft');
    await page.getByLabel('Official form').selectOption('ustva');
    await page.getByLabel('Form version or year').fill('2026');
    await page.getByLabel('Filing period').fill('2026-10');
    await page.getByLabel('Recipient').fill('Synthetic Finanzamt');
    await page.getByLabel('Exact payload file').selectOption({ index: 1 });
    const sources = page.getByLabel('Source evidence');
    await sources.selectOption([{ index: 0 }]);
    await click(page, 'Save filing version');
    await click(page, 'Confirm and save');
    await page.locator('main').getByText('Synthetic Finanzamt', { exact: false }).first().waitFor();
    await page.getByText('Saved to your workspace.', { exact: true }).waitFor();
    await click(page, 'Inspect filing');
    await page.getByLabel('Action to record').selectOption('cancel');
    await page.getByLabel('Person recording this').fill('Synthetic owner');
    await page.getByLabel('Evidence file').selectOption({ index: 1 });
    await page.getByLabel('What was actually checked or observed').fill('Synthetic draft replaced before any attempt.');
    await click(page, 'Save observed action');
    await click(page, 'Confirm and save');
    await page.locator('main').getByText('Cancelled', { exact: true }).waitFor();
    await page.getByText('Saved to your workspace.', { exact: true }).waitFor();
    assert.equal(await page.getByRole('button', { name: 'Submit', exact: true }).count(), 0);
    const inspectState=async stateName=>page.locator('tbody tr').filter({has:page.getByText(stateName,{exact:true})}).getByRole('button',{name:'Inspect filing',exact:true}).click();
    await inspectState('Cancelled');
    await click(page,'Prepare corrected version');
    await page.getByLabel('Exact payload file').selectOption({index:1});
    await page.getByLabel('Source evidence').selectOption([{index:0}]);
    await click(page,'Save filing version');
    await click(page,'Confirm and save');
    await page.getByText('Saved to your workspace.',{exact:true}).waitFor();
    const observeFiling=async(action,fromState,toState,extra={})=>{
      await inspectState(fromState);
      await page.getByLabel('Action to record').selectOption(action);
      await page.getByLabel('Person recording this').fill('Synthetic owner');
      await page.getByLabel('Evidence file').selectOption({index:1});
      await page.getByLabel('What was actually checked or observed').fill(`SYNTHETIC ONLY: ${action}; no external service contacted.`);
      if(extra.externalId) await page.getByLabel('Actual transmission reference').fill(extra.externalId);
      if(extra.responseKind) await page.getByLabel('Authority response type').selectOption(extra.responseKind);
      if(extra.dueDate) await page.getByLabel('Sourced response deadline, if any').fill(extra.dueDate);
      await click(page,'Save observed action');
      const dialog=page.getByRole('dialog');
      await dialog.getByText('Synthetic Finanzamt',{exact:true}).waitFor();
      assert.ok((await dialog.innerText()).includes('2026-10'));
      await click(page,'Confirm and save');
      await page.getByText('Saved to your workspace.',{exact:true}).waitFor();
      await page.locator('tbody tr').filter({has:page.getByText(toState,{exact:true})}).waitFor();
    };
    await observeFiling('review','Draft','Reviewed');
    await observeFiling('authorize','Reviewed','Authorized');
    await observeFiling('begin','Authorized','Submission outcome unknown');
    await page.getByRole('link',{name:'Home',exact:true}).click();
    await page.locator('.next-step').getByRole('button',{name:'Inspect filing',exact:true}).click();
    await page.getByRole('heading',{name:'Filing details and next action'}).waitFor();
    assert.equal(await page.getByText('Submission outcome unknown',{exact:true}).isVisible(),true,'Uncertain filing takes precedence over active tasks');
    assert.equal(await page.getByLabel('Action to record').locator('option[value="cancel"]').count(),0,'Attempted filing cannot be cancelled locally');
    for(const width of [1440,390]) {
      await page.setViewportSize({width,height:1000});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`Filing details overflow at ${width}`);
      await capture(page,{path:path.join(output,`${browserName}-filing-details-${width}.png`),fullPage:true});
    }
    await page.setViewportSize({width:1440,height:1000});
    await page.getByRole('link',{name:'Taxes and letters',exact:true}).click();
    await observeFiling('receipt','Submission outcome unknown','Receipt recorded',{externalId:'SYNTHETIC-TRANSMISSION-ONLY-001'});
    await observeFiling('response','Receipt recorded','Receipt recorded',{responseKind:'request_for_information',dueDate:'2026-11-20'});
    await inspectState('Receipt recorded');
    await page.getByRole('heading',{name:'Recorded actions and evidence'}).waitFor();
    await page.getByText('SYNTHETIC-TRANSMISSION-ONLY-001',{exact:true}).waitFor();
    await page.getByRole('table').getByText('Request for information',{exact:true}).waitFor();
    await page.getByText('Sourced response deadline, if any: 2026-11-20',{exact:true}).waitFor();
    await click(page,'Prepare corrected version');
    await page.getByLabel('Exact payload file').selectOption({index:1});
    await page.getByLabel('Source evidence').selectOption([{index:0}]);
    await click(page,'Save filing version');
    // Save and draft persistence precede the snapshot; give its completion the
    // existing bounded wait once that request actually starts.
    await Promise.all([
      page.waitForRequest(request => request.url()===url+'api' && request.method()==='POST' && request.postDataJSON()?.op==='status'),
      click(page,'Confirm and save'),
    ]);
    await page.waitForFunction(()=>document.querySelector('main').getAttribute('aria-busy')==='false');
    await page.getByText('Saved to your workspace.',{exact:true}).waitFor();
    assert.equal(await page.locator('tbody tr').count(),3,'Cancelled and submitted versions remain alongside linked replacement');
    await page.getByRole('link', { name: 'Settings and recovery', exact: true }).click();
    const backup=path.join(temp,'verified-backup'), restored=path.join(temp,'restored');
    await page.getByLabel('New backup folder').fill(backup);
    await click(page,'Create verified full backup');
    await page.getByText('Operation completed and verified by the workspace tools.',{exact:true}).first().waitFor();
    await page.getByLabel('Existing backup folder').fill(backup);
    await click(page,'Verify a backup');
    await page.getByText('Operation completed and verified by the workspace tools.',{exact:true}).first().waitFor();
    await page.getByLabel('Existing backup folder').fill(backup);
    await page.getByLabel('New restored workspace folder').fill(restored);
    await click(page,'Restore into a new folder');
    await click(page,'Confirm and save');
    await page.getByText('Operation completed and verified by the workspace tools.',{exact:true}).first().waitFor();
    await fs.access(path.join(restored,'.workspace-layout.json'));
    for (const lang of ['ru', 'de', 'en']) {
      await page.getByLabel(/Interface language|Язык интерфейса|Sprache der Oberfläche/).selectOption(lang);
      assert.equal(await page.locator('html').getAttribute('lang'), lang);
    }
    // A saved document draft keeps its original version guard across reloads.
    await page.getByRole('link', { name: 'Documents', exact: true }).click();
    await click(page,'Review details');
    await page.getByLabel('Readable title').fill('My pending document change');
    await click(page,'Save draft');
    await page.getByText('Saved to your workspace.',{exact:true}).waitFor();
    const publicApi=async(op,args={})=>{
      const response=await context.request.post(url+'api',{headers:{Authorization:'Bearer '+token},data:{op,args}});
      const result=await response.json();assert.equal(result.ok,true,result.error);return result.result;
    };
    const current=await publicApi('context');
    const state=await publicApi('status',{workspace_id:current.workspace.id,period:'2026-10'});
    const doc=state.documents[0];
    await publicApi('document-save',{workspace_id:current.workspace.id,request_id:require('node:crypto').randomUUID(),record:{...doc.record,title:'Another reviewed title'},expected_sha256:doc.sha256});
    await page.reload();
    await click(page,'Review details');
    assert.equal(await page.getByLabel('Readable title').inputValue(),'My pending document change');
    await click(page,'Save document details');
    await page.locator('#error').waitFor({state:'visible'});
    assert.equal(await page.getByLabel('Readable title').inputValue(),'My pending document change');
    const afterConflict=await publicApi('status',{workspace_id:current.workspace.id,period:'2026-10'});
    assert.equal(afterConflict.documents[0].record.title,'Another reviewed title');
    await click(page,'Discard unsaved changes');
    await page.getByRole('dialog').getByRole('button',{name:'Discard unsaved changes',exact:true}).click();
    await page.getByLabel('Readable title').waitFor();
    await page.waitForFunction(()=>document.getElementById('title')?.value==='Another reviewed title');
    // A corrupt snapshot exposes recovery and never pretends unknown counts are zero.
    const catalogPath=path.join(root,'.business-kit','admin','casework.json');
    const originalCatalog=await fs.readFile(catalogPath);
    await fs.writeFile(catalogPath,'{broken');
    await page.getByRole('link',{name:'Home',exact:true}).click();
    await click(page,'Refresh records');
    await page.getByRole('heading',{name:'Some records could not be checked. Inspect the problem before continuing.'}).waitFor();
    await click(page,'Help me with this');
    assert.match(await page.locator('#help-prompt').inputValue(),/Inspect the record errors/);
    assert.doesNotMatch(await page.locator('#help-prompt').inputValue(),/formation-undated/,'Failed refresh must not suggest a stale task');
    await click(page,'Close');
    await page.reload();
    await page.getByRole('heading',{name:'Some records could not be checked. Inspect the problem before continuing.'}).waitFor();
    assert.equal(await page.getByText('Documents received',{exact:true}).count(),0);
    assert.equal(await page.getByRole('heading',{name:'Active tasks',exact:true}).count(),0,'Unknown snapshot must not present tasks as valid');
    assert.equal(await page.getByRole('button',{name:'Continue with your assistant',exact:true}).count(),0);
    await page.getByRole('link',{name:'Settings and recovery',exact:true}).click();
    await page.getByRole('heading',{name:'Keep your work recoverable.'}).waitFor();
    await fs.writeFile(catalogPath,originalCatalog);
    await page.getByRole('link', { name: 'Home', exact: true }).click();
    await click(page,'Refresh records');
    await page.getByRole('heading',{name:'Your business, one clear next step.'}).waitFor();
    await page.getByRole('link', { name: 'Skip to content', exact: true }).focus();
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('main').evaluate(el => el === document.activeElement), true);
    // A lock left by a program that ended can be checked and removed without an assistant.
    const ended=spawn(process.execPath,['-e','']);
    await new Promise(resolve=>ended.on('exit',resolve));
    const lockFile=path.join(root,'.workspace.lock');
    await fs.writeFile(lockFile,JSON.stringify({pid:ended.pid,created_at:'2026-10-26T18:00:00+00:00',host:os.hostname()}));
    await click(page,'Refresh records');
    await page.getByRole('heading',{name:'Some records could not be checked. Inspect the problem before continuing.'}).waitFor();
    await click(page,'Check workspace lock');
    await page.getByText('The program that locked this workspace has ended on this computer.',{exact:false}).waitFor();
    await capture(page,{path:path.join(output,`${browserName}-left-over-lock.png`),fullPage:true});
    await click(page,'Remove left-over lock');
    await page.getByRole('dialog').getByText('Locked since',{exact:true}).waitFor();
    await click(page,'Confirm and save');
    await page.getByText('Left-over lock removed and recorded in the history.',{exact:true}).waitFor();
    await page.getByRole('heading',{name:'Your business, one clear next step.'}).waitFor();
    await assert.rejects(fs.access(lockFile),'Removed lock must not remain');

    // Settlement projection uses real writers and never claims authoritative payment.
    const settlementRoot=path.join(temp,'settlements');
    execFileSync(python,['-B','-c',`
import sys, shutil
sys.path.insert(0, 'tests')
from test_cash_vat import ProposalLinkTests, ac
f = ProposalLinkTests(); f.setUp()
try:
    f.proposal('proposal-1')
    ac.post(f.root, f.entry('first-payment', '60', f.line('60', status='none_stated', proposal='proposal-1')))
    shutil.copytree(f.root, sys.argv[1])
finally:
    f.doCleanups()
`,settlementRoot],{cwd:process.cwd()});
    await selectWorkspace(settlementRoot);
    await page.getByRole('link',{name:'This month',exact:true}).click();
    await page.locator('[data-settlements] summary').getByText('SYN-1',{exact:false}).waitFor();
    assert.match(await page.locator('[data-settlements]').innerText(),/Partly allocated/);
    await page.locator('[data-settlements] summary').press('Enter');
    await page.locator('[data-settlements]').getByText('59.00 EUR',{exact:true}).waitFor();
    const settlementContext=await publicApi('context');
    const postAllocation=async(id,amount,currency)=>publicApi('entry-post',{
      workspace_id:settlementContext.workspace.id,request_id:require('node:crypto').randomUUID(),
      value:{schema_version:2,entry_id:id,date:'2026-10-21',account:'bank',transaction_id:id,amount,currency,
        reviewer:'Synthetic owner',evidence_file:'08_correspondence/review.md',note:'Synthetic allocation',replaces:null,
        lines:[{kind:'income',amount,category:'Synthetic income',activity_id:'consulting',proposal_id:'proposal-1',
          vat:{status:'none_stated',net:null,tax:null,rate:null}}]}});
    await postAllocation('balance-payment','59','EUR');
    await page.reload();
    await page.locator('[data-settlements]').getByText('SYN-1 · Amounts match',{exact:true}).waitFor();
    await postAllocation('foreign-payment','10','USD');
    await page.reload();
    await page.locator('[data-settlements]').getByText('SYN-1 · Needs review',{exact:true}).waitFor();
    for(const lang of ['en','ru','de']) {
      await page.locator('#language').selectOption(lang);
      await page.locator('[data-settlements] summary').click();
      assert.match(await page.locator('[data-settlements]').innerText(),/10 USD/);
      for(const width of [1440,390]) {
        await page.setViewportSize({width,height:1000});
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`${lang}/settlements overflow at ${width}`);
        await capture(page,{path:path.join(output,`${browserName}-${lang}-settlements-${width}.png`),fullPage:true});
      }
    }
    await page.locator('#language').selectOption('en');
    await selectWorkspace(root);

    for (const lang of ['en','ru','de']) {
      await page.locator('#language').selectOption(lang);
      for (const destination of ['home','documents','month','taxes','accounts','settings']) {
        await page.locator(destination==='settings'?'#settings-link':`nav a[data-route="${destination}"]`).click();
        for (const width of [1440,390,320]) {
          await page.setViewportSize({width,height:1000});
          assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`${lang}/${destination} overflow at ${width}`);
          assert.equal(await page.locator('main h1').count(),1,`${lang}/${destination} heading`);
          if(destination==='home'&&(lang==='en'||width===390)) await capture(page,{path:path.join(output,`${browserName}-${lang}-home-${width}.png`),fullPage:true});
        }
      }
    }
    // Persist only session credentials/preferences in browser storage, never business drafts.
    assert.deepEqual(await page.evaluate(()=>Object.keys(localStorage)),[]);
    assert.deepEqual((await page.evaluate(()=>Object.keys(sessionStorage))).sort(),['gbk-language','gbk-session']);
    // A second tab changing the selected workspace must not redirect the first tab's draft.
    await page.locator('#language').selectOption('en');
    await page.locator('nav a[data-route="month"]').click();
    await click(page,'Add cash entry');
    await page.getByLabel('Total cash movement').fill('77.00');
    const otherRoot=path.join(temp,'other-business');
    await fixture(otherRoot);
    const otherTab=await context.newPage();
    await otherTab.goto(`${url}#token=${token}`);
    await otherTab.getByRole('heading',{name:'Your business, one clear next step.'}).waitFor();
    await otherTab.getByRole('link',{name:'Settings and recovery',exact:true}).click();
    await click(otherTab,'Open another workspace');
    await otherTab.getByLabel('Workspace folder').fill(otherRoot);
    await click(otherTab,'Open existing workspace');
    await otherTab.getByRole('heading',{name:'Your business, one clear next step.'}).waitFor();
    await page.bringToFront();
    await click(page,'Save draft');
    await page.locator('#error').waitFor({state:'visible'});
    assert.equal(await page.getByLabel('Total cash movement').inputValue(),'77.00');
    const switched=await publicApi('context');
    assert.equal(switched.workspace.root,otherRoot);
    const untouched=await publicApi('status',{workspace_id:switched.workspace.id,period:'2026-10'});
    assert.equal(untouched.drafts.entry,undefined,'Stale tab did not write into the newly selected workspace');
    await otherTab.close();
    assert.deepEqual(issues, []);
    console.log(`GUI ${browserName}: task-first empty/undated/blocked/evidence/XSS/cross-month journeys, real import/review/configuration/draft/post/reversal/filing lifecycle/recovery/stale-tab journeys, and 54 localized route-width checks plus 6 task-home checks passed; ${screenshotDiagnostics} screenshot-only WebKit CSP diagnostics.`);
    await context.close();
  } catch (error) {
    failure = error;
    // Synthetic fixtures only; never log session tokens or request bodies.
    console.error('GUI failure state:', await page?.evaluate(() => ({
      readyState: document.readyState,
      mainText: document.querySelector('main')?.textContent?.slice(0, 500),
      navigationLinks: document.querySelectorAll('nav a').length,
      translationsLoaded: typeof window.GUI_I18N,
      busy: document.querySelector('main')?.getAttribute('aria-busy'),
      error: document.querySelector('#error')?.textContent,
      errorHidden: document.querySelector('#error')?.hidden,
      notice: document.querySelector('#notice')?.textContent,
      noticeHidden: document.querySelector('#notice')?.hidden,
    })).catch(() => null));
    console.error('Recent GUI operations:', apiResults);
    console.error('Pending GUI operations:', [...pendingRequests.values()].map(item => ({ op:item.op, elapsedMs:Date.now()-item.started })));
    console.error('GUI browser errors:', issues.slice(-20).map(redact));
    console.error('GUI static requests:', assets.map(({ started, ...asset }) => ({ ...asset, elapsedMs: asset.elapsedMs ?? Date.now()-started })));
    console.error('GUI server diagnostics:', redact(server.stderr().slice(-4000)));
    if (page) await capture(page, { path: path.join(output, `${browserName}-failure.png`), fullPage: true, timeout: 5000 }).catch(() => {});
    throw error;
  } finally {
    const cleanupErrors = [];
    try { if (browser) await browser.close(); } catch (error) { cleanupErrors.push(error); }
    try {
      await stopChild(server.child);
      await fs.rm(temp, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
    } catch (error) { cleanupErrors.push(error); }
    if (cleanupErrors.length) {
      if (failure) console.error('Additional GUI cleanup errors:', ...cleanupErrors);
      else throw new AggregateError(cleanupErrors, 'GUI cleanup failed');
    }
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
