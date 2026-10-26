/* Real workspace interface: every authoritative write goes through the local API. */
'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const uuid = () => crypto.randomUUID();
  const today = () => new Date().toISOString().slice(0,10);
  let language = 'en', period = today().slice(0,7), snapshot = null, drafts = {}, draftHash = null;
  let route = 'home', editor = null, dirty = false, busy = false, preview = null, pendingConfirm = null;
  let selectedFiles = [], importOutcome = null, reportOutcome = null, recoveryOutcome = null, snapshotUnavailable = false;
  const requests = new Map();
  const mutationOps = new Set(['open','receive','document-save','configuration','entry-post','entry-reverse','filing-create','filing-action','report','overview','backup','restore','draft-save']);
  const routes = new Set(['home','documents','month','taxes','accounts','settings']);
  const icons = {home:'M3 10 12 3l9 7M5 9v12h5v-7h4v7h5V9',documents:'M6 3h9l4 4v14H6zM14 3v5h5M9 12h7M9 16h7',month:'M4 5h16v16H4zM8 3v4M16 3v4M4 10h16M8 14h3M14 14h2',taxes:'M4 5h16v14H4zM4 6l8 6 8-6',accounts:'M3 7h17l-4-4M21 17H4l4 4'};
  let token = '';
  const bootstrap = new URLSearchParams(location.hash.slice(1));
  if (bootstrap.has('token')) {
    token=bootstrap.get('token') || '';
    try { sessionStorage.setItem('gbk-session', token); } catch { /* Current session still works. */ }
    history.replaceState(null, '', location.pathname + location.search);
  } else {
    try { token=sessionStorage.getItem('gbk-session') || ''; } catch { /* Launcher required to reconnect. */ }
  }
  try { const saved=sessionStorage.getItem('gbk-language'); if (['en','ru','de'].includes(saved)) language=saved; } catch { /* Current language still works. */ }
  const t = key => window.GUI_I18N[language][key] || window.GUI_I18N.en[key] || key;
  const label = key => esc(t(key));
  const option = (value, text, current) => `<option value="${esc(value)}"${String(value) === String(current) ? ' selected' : ''}>${esc(text)}</option>`;
  function field(name, key, value='', type='text', hint='', required=true) {
    const id=name==='period'?'filing-period':name;
    return `<div class="field"><label for="${esc(id)}">${label(key)}</label><input id="${esc(id)}" name="${esc(name)}" type="${type}" value="${esc(value)}"${required?' required':''}>${hint?`<span class="hint">${label(hint)}</span>`:''}</div>`;
  }
  function select(name, key, options, value='', hint='', multiple=false) {
    return `<div class="field"><label for="${esc(name)}">${label(key)}</label><select id="${esc(name)}" name="${esc(name)}"${multiple?' multiple':''} required>${multiple?'':option('',t('choose'),value)}${options.map(item => option(item[0],item[1],value)).join('')}</select>${hint?`<span class="hint">${label(hint)}</span>`:''}</div>`;
  }
  function textarea(name,key,value='',required=true) {
    return `<div class="field"><label for="${name}">${label(key)}</label><textarea id="${name}" name="${name}"${required?' required':''}>${esc(value)}</textarea></div>`;
  }
  function evidence(name='evidence_file', key='evidence', value='') {
    return select(name,key,(snapshot?.files||[]).map(file=>[file.path,file.name+' · '+file.path]),value);
  }
  const intro = (title,text) => `<div class="intro"><h1>${label(title)}</h1><p>${label(text)}</p></div>`;
  const action = (key, name, cls='') => `<button type="button" data-action="${name}" class="${cls}">${label(key)}</button>`;
  const badge = state => `<span class="badge${['needs_review','submission_unconfirmed','unresolved'].includes(state)?' warning':''}">${esc(t(state==='reviewed'?'reviewedState':state))}</span>`;
  function showError(message) {
    $('error').textContent = `${t('error')} ${message}`;
    $('error').hidden = false;
    $('error').focus();
  }
  function notice(message) { $('notice').textContent=message; $('notice').hidden=false; }
  function clearMessages() { $('error').hidden=true; $('notice').hidden=true; }
  async function api(op,args={}) {
    if (!token) throw new Error(t('expired'));
    const key = JSON.stringify([op,args]);
    const request = {...args};
    if (snapshot?.workspace?.id && !['open','select-folder'].includes(op)) request.workspace_id=snapshot.workspace.id;
    if (mutationOps.has(op)) {
      if (!requests.has(key)) requests.set(key,uuid());
      request.request_id=requests.get(key);
    }
    let response;
    try { response=await fetch('/api',{method:'POST',headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`},body:JSON.stringify({op,args:request})}); }
    catch { throw new Error(t('network')); }
    let value;
    try { value=await response.json(); }
    catch { throw new Error(t('network')); }
    if (!response.ok || !value.ok) {
      requests.delete(key);
      throw new Error(value.error || `${response.status}`);
    }
    requests.delete(key);
    return value.result;
  }
  function setBusy(value) {
    busy=value;
    document.querySelectorAll('button,input,select,textarea').forEach(control=>{control.disabled=value;});
    document.querySelectorAll('nav a,#settings-link').forEach(link=>link.setAttribute('aria-disabled',String(value)));
    $('save-status').textContent=value?t('working'):dirty?t('unsaved'):t('refreshed');
    $('main').setAttribute('aria-busy',String(value));
  }
  async function perform(fn) {
    if (busy) return;
    clearMessages(); setBusy(true);
    try { await fn(); }
    catch (error) { showError(error.message); }
    finally { setBusy(false); }
  }
  async function refresh(keepDrafts=true) {
    let next;
    try { next=await api('status',{period,language}); }
    catch(error) { snapshotUnavailable=true; render(); throw error; }
    snapshotUnavailable=false; snapshot=next;
    if (!keepDrafts || !dirty) { drafts=structuredClone(next.drafts || {}); draftHash=next.drafts_sha256 ?? null; }
    render();
  }
  function setDirty() { dirty=true; $('notice').hidden=true; $('save-status').textContent=t('unsaved'); }
  function captureForm() {
    const form=$('work-form');
    if (!form) return;
    const result={};
    for (const control of form.elements) {
      if (!control.name) continue;
      result[control.name]=control.multiple?Array.from(control.selectedOptions).map(item=>item.value):control.value;
    }
    const key=draftKey(form.dataset.form);
    if (drafts[key] && Object.hasOwn(drafts[key],'__expected_sha256')) result.__expected_sha256=drafts[key].__expected_sha256;
    else if(form.dataset.form==='document') result.__expected_sha256=snapshot.documents.find(item=>item.record.document_id===editor.id)?.sha256 ?? null;
    else if(form.dataset.form==='filingAction') result.__expected_sha256=snapshot.accounting.filings.find(item=>item.record.filing_id===editor.id)?.sha256 ?? null;
    else if(form.dataset.form==='configuration') result.__expected_sha256=snapshot.accounting.configuration_sha256 ?? null;
    drafts[key]=result;
  }
  function draftKey(kind) { return ['document','filingAction','reversal'].includes(kind)&&editor?.id ? kind+':'+editor.id : kind; }
  async function saveDraft() {
    captureForm();
    drafts.continuation={route,editor,period};
    const result=await api('draft-save',{drafts,expected_sha256:draftHash});
    draftHash=result.sha256; dirty=false;
    notice(t('saved'));
  }
  async function leave(next) {
    captureForm();
    if (!dirty) { next(); return; }
    confirm(t('leaveTitle'),`<p>${label('leaveText')}</p>`,async()=>{dirty=false;next();},t('discard'));
  }
  function confirm(title,summary,callback,button=t('confirm')) {
    $('confirm-title').textContent=title;
    $('confirm-summary').innerHTML=summary;
    $('confirm-note').textContent=t('confirmNote');
    $('cancel-confirm').textContent=t('keepEditing');
    $('accept-confirm').textContent=button;
    pendingConfirm=callback;
    $('confirm-dialog').showModal();
  }
  function summary(pairs) { return '<dl>'+pairs.map(([key,value])=>`<dt>${esc(t(key))}</dt><dd>${esc(value)}</dd>`).join('')+'</dl>'; }
  function navigate(next) {
    route=routes.has(next)?next:'home'; editor=null; preview=null;
    history.replaceState(null,'','#'+route); render();
  }
  function chrome() {
    document.documentElement.lang=language;
    $('skip').textContent=t('skip'); $('period-label').textContent=t('monthLabel'); $('language-label').textContent=t('language');
    $('period').value=period; $('language').value=language;
    $('workspace-name').textContent=snapshot?.workspace?.name || t('workspace');
    $('sidebar-note').textContent=t('sidebar'); $('settings-link').textContent=t('settings'); $('help-button').textContent=t('help'); $('footer').textContent=t('footer');
    $('navigation').innerHTML=['home','documents','month','taxes','accounts'].map(name=>`<a href="#${name}" data-route="${name}"${route===name?' aria-current="page"':''}><svg class="nav-icon" aria-hidden="true" viewBox="0 0 24 24"><path d="${icons[name]}"/></svg>${label(name)}</a>`).join('');
    $('save-status').textContent=dirty?t('unsaved'):t('refreshed');
  }
  function render() {
    chrome();
    if (!snapshot?.workspace) { $('main').innerHTML=welcome(); setBusy(busy); return; }
    if (snapshotUnavailable && route!=='settings') { $('main').innerHTML=intro('issueUnknown','error')+`<div class="actions">${action('refresh','refresh','primary')}${action('settings','settings')}</div>`; setBusy(busy); return; }
    let content;
    if (editor?.kind==='document') content=documentEditor();
    else if (editor?.kind==='entry') content=entryEditor();
    else if (editor?.kind==='reversal') content=reversalEditor();
    else if (editor?.kind==='filing') content=filingEditor();
    else if (editor?.kind==='filingAction') content=filingDetails();
    else {
      switch(route) {
        case 'documents':content=documentsPage();break;
        case 'month':content=monthPage();break;
        case 'taxes':content=taxesPage();break;
        case 'accounts':content=accountsPage();break;
        case 'settings':content=settingsPage();break;
        default:content=homePage();
      }
    }
    $('main').innerHTML=content;
    const data=editor?.kind ? drafts[draftKey(editor.kind)] : route==='accounts' ? drafts.configuration : null;
    if (data) for (const control of $('work-form')?.elements || []) {
      if (!Object.hasOwn(data,control.name)) continue;
      if (control.multiple) { for (const opt of control.options) opt.selected=(data[control.name]||[]).includes(opt.value); }
      else control.value=data[control.name];
    }
    if ($('response_kind')) $('response_kind').required=false;
    if (preview && editor?.kind==='document') showPreview(preview);
    setBusy(busy);
  }
  function welcome() {
    return intro('welcome','welcomeText')+`<form id="open-form" class="panel">${field('workspace-path','path','','text','pathHint')}<div class="actions">${action('browse','browse-workspace')}</div><div class="form-section grid">${field('year','year',new Date().getFullYear(),'number')}${select('folder-language','folderLanguage',[['en','English'],['ru','Русский'],['de','Deutsch']],language)}</div><p class="hint">${label('createHint')}</p><div class="actions"><button type="submit" name="open" class="primary">${label('open')}</button><button type="button" data-action="create-workspace">${label('create')}</button></div></form>`;
  }
  function issues() {
    const overview=snapshot?.overview||{};
    const errors=[...(overview.errors||[]),...(snapshot.errors||[])];
    const rows=[...(overview.open_items||[]),...(overview.open_questions||overview.questions||[]).filter(item=>['open','deferred'].includes(item.status)),...(snapshot.accounting?.filings||[]).flatMap(item=>(item.check?.issues||[]).map(issue=>({...issue,ref:item.record.filing_id})))];
    return (errors.length?`<div class="warning"><strong>${label('issueUnknown')}</strong><ul>${errors.map(error=>`<li>${esc(typeof error==='string'?error:JSON.stringify(error))}</li>`).join('')}</ul></div>`:'')+(rows.length?'<ul>'+rows.map(row=>`<li>${esc(row.title||row.detail||window.GUI_I18N[language]['issue-'+row.code]||t('issueUnknown'))}${row.ref?` <span class="muted">${esc(snapshot.documents?.find(item=>item.record.document_id===row.ref)?.record.title||(row.ref===period?period:row.ref))}</span>`:''}</li>`).join('')+'</ul>':`<p class="muted">${label('noIssues')}</p>`);
  }
  function activeTasks() {
    return snapshot?.overview?.active_tasks || [];
  }
  function taskList(tasks) {
    if (!tasks.length) return '';
    return `<section class="section"><h2>${label('activeTasks')}</h2><p class="hint">${label('taskScope')}</p><ul class="file-list" aria-label="${label('activeTasks')}">${tasks.map(task=>`<li><div class="path"><h3>${esc(task.title)}</h3></div><p>${label('status')}: ${esc(t('task-'+task.status))} · ${label('taskOwner')}: ${esc(task.owner)}</p><p class="hint">${task.due_date?`${label('taskDate')}: ${esc(task.due_date)}<br>${label('taskDateSource')}: <span>${esc(task.deadline_source)}</span>`:label('taskUndated')}</p><p class="hint">${label('taskEvidence-'+task.evidence_status)}</p>${task.pending_dependencies?.length?`<p class="hint">${label('taskDependencies')}: ${esc(task.pending_dependencies.join(', '))}</p>`:''}${task.readiness!=='ready'?`<p class="hint">${label('taskReadiness-'+task.readiness)}</p>`:''}${task.note?`<p class="path">${esc(task.note)}</p>`:''}</li>`).join('')}</ul></section>`;
  }
  function hasBusinessRecords() {
    return Boolean(snapshot?.overview?.workspace_has_documents || snapshot?.documents?.length || snapshot?.accounting?.entries?.length || snapshot?.accounting?.filings?.length || snapshot?.accounting?.configuration);
  }
  function homePage() {
    const docs=snapshot.documents||[], pending=docs.filter(item=>!['reviewed','excluded'].includes(item.record.review_status));
    const empty=!hasBusinessRecords(), config=snapshot.accounting?.configuration;
    const hasDraft=drafts.continuation&&drafts[drafts.continuation.editor?.kind==='entry'?'entry':drafts.continuation.editor?.kind==='filing'?'filing':drafts.continuation.editor?.kind+':'+drafts.continuation.editor?.id];
    const errors=snapshotUnavailable||(snapshot.errors||[]).length||(snapshot.overview?.errors||[]).length;
    const tasks=errors?[]:activeTasks();
    const nextTask=tasks.find(task=>task.id===snapshot.overview?.next_task_id);
    const filingAttention=snapshot.accounting?.filings?.some(item=>item.record.state==='submission_unconfirmed'||(item.check?.issues||[]).length);
    const key=errors?'issueUnknown':hasDraft?'continueWork':filingAttention?'inspectFiling':tasks.length?'reviewTasks':empty?'askTask':pending.length?'reviewNext':!config?'chooseAccounts':'continueWork';
    const button=errors?'refresh':hasDraft?'continueWork':filingAttention?'inspectFiling':tasks.length?'continueAssistant':empty?'help':pending.length?'reviewNext':!config?'chooseAccounts':'continueWork';
    const target=errors?'refresh':hasDraft?'resume-work':filingAttention?'inspect-next-filing':tasks.length||empty?'help':pending.length?'review-next':!config?'accounts':'month';
    return intro('homeTitle','homeText')+`<section class="next-step"><h2>${nextTask&&!hasDraft&&!filingAttention?esc(nextTask.title):label(key)}</h2><p>${label(errors?'taskRepair':hasDraft||filingAttention?'coverage':tasks.length?'taskContinueHint':empty?'askTaskHint':'coverage')}</p><div class="actions">${action(button,target,'primary')}${errors?'':action('refresh','refresh')}</div></section>${taskList(tasks)}<dl class="facts"><div><dt>${label('received')}</dt><dd>${docs.length}</dd></div><div><dt>${label('reviewed')}</dt><dd>${docs.filter(item=>item.record.review_status==='reviewed').length}</dd></div><div><dt>${label('recorded')}</dt><dd>${snapshot.accounting?.entries?.length ?? '—'}</dd></div><div><dt>${label('filingCount')}</dt><dd>${snapshot.accounting?.filings?.length ?? '—'}</dd></div></dl><section class="section"><h2>${label('attention')}</h2>${issues()}</section>`;
  }
  function documentsPage() {
    return intro('documentsTitle','documentsText')+`<section class="panel"><form id="import-form"><div class="field"><label for="document-files">${label('chooseFiles')}</label><input id="document-files" type="file" multiple accept=".pdf,.xml,.png,.jpg,.jpeg,.tif,.tiff,.csv"><p class="hint">${label('importHint')}</p><p id="selected-files" class="hint">${selectedFiles.map(file=>esc(file.name)).join(', ')}</p></div><div class="grid">${field('import-period','storageMonth',period,'month')}${field('received-on','receivedOn',today(),'date')}</div><button type="submit" class="primary">${label('importFiles')}</button></form>${importOutcome?`<div class="section"><h3>${label('importResult')}</h3>${formatResult(importOutcome)}</div>`:''}</section><div class="search">${field('search','search','','search','',false)}</div><div id="document-list">${documentList('')}</div>`;
  }
  function documentList(query) {
    const docs=(snapshot.documents||[]).filter(item=>(item.record.title+' '+item.original_name).toLocaleLowerCase().includes(query.toLocaleLowerCase()));
    if (!docs.length) return `<p class="empty">${label(query?'noMatch':'noFiles')}</p>`;
    return `<div class="table-wrap"><table><thead><tr><th>${label('title')}</th><th>${label('type')}</th><th>${label('status')}</th><th></th></tr></thead><tbody>${docs.map(item=>`<tr><td>${esc(item.record.title)}<div class="path">${esc(item.original_name)}</div></td><td>${esc(t(item.record.type))}</td><td>${badge(item.record.review_status)}</td><td><button data-action="review-document" data-id="${esc(item.record.document_id)}">${label('reviewDetails')}</button></td></tr>`).join('')}</tbody></table></div>`;
  }
  function documentEditor() {
    const item=(snapshot.documents||[]).find(item=>item.record.document_id===editor.id);
    if (!item) { editor=null; return documentsPage(); }
    const record=item.record;
    return `<div class="heading-row"><h1>${label('reviewDetails')}</h1>${action('back','back')}</div><p class="hint">${label('reviewBoundary')}</p><div class="review-layout"><aside class="review-source"><h2>${label('original')}</h2><p>${esc(item.original_name)}</p><p class="path">${esc(item.path)}</p>${action('viewOriginal','preview-original')}<div id="original-preview"><p class="hint">${label('previewHint')}</p></div></aside><form id="work-form" data-form="document" class="panel">${field('title','readableTitle',record.title)}${select('type','documentType',['unknown','invoice','credit_note','bank_statement','contract','authority_letter','registration_receipt','receipt','other'].map(value=>[value,t(value)]),record.type)}${select('review_status','reviewStatus',['new','needs_review','reviewed','excluded'].map(value=>[value,t(value)]),record.review_status)}${field('reviewer','reviewer',record.reviewer||'','text','',false)}${textarea('review_note','reviewNote',record.review_note||'',false)}<div class="actions"><button type="submit" class="primary">${label('documentSave')}</button>${action('saveDraft','save-draft')}${action('discard','discard-draft')}</div></form></div>`;
  }
  function filteredEntries() { return (snapshot.accounting?.entries||[]).filter(item=>item.date?.startsWith(period)); }
  function monthPage() {
    const all=snapshot.accounting?.entries||[], reversed=new Set(all.filter(item=>item.reverses).map(item=>item.reverses));
    const entries=filteredEntries();
    const rows=entries.map(item=>`<tr><td>${esc(item.date)}<div class="path">${esc(item.transaction_id)}</div></td><td>${esc(item.amount)} ${esc(item.currency)}</td><td>${esc(item.lines?.map(line=>line.category).join(', '))}</td><td>${item.reverses?badge('reversed'):reversed.has(item.entry_id)?`${badge('reversed')}<button data-action="correct-entry" data-id="${esc(item.entry_id)}">${label('replacement')}</button>`:`<button data-action="reverse-entry" data-id="${esc(item.entry_id)}">${label('reverse')}</button>`}</td></tr>`).join('');
    return intro('monthTitle','monthText')+`<p class="hint">${label('immutable')}</p><div class="actions">${action(drafts.entry?'resumeEntry':'addEntry','new-entry','primary')}${action('report','report')}</div><section class="section">${entries.length?`<div class="table-wrap"><table><thead><tr><th>${label('entryDate')}</th><th>${label('amount')}</th><th>${label('category')}</th><th></th></tr></thead><tbody>${rows}</tbody></table></div>`:`<p class="empty">${label('noEntries')}</p>`}</section>${reportOutcome?`<section class="panel"><h2>${label('reportResult')}</h2>${formatResult(reportOutcome)}</section>`:''}<section class="section"><h2>${label('attention')}</h2>${issues()}</section>`;
  }
  function entryDefaults() { return {entry_id:'entry-'+uuid(),date:'',account:'',transaction_id:'',amount:'',currency:'EUR',reviewer:'',evidence_file:'',note:'',replaces:'',line_count:'1','kind-0':'unresolved','amount-0':'','category-0':'','activity_id-0':'','proposal_id-0':'','vat_status-0':'unresolved','net-0':'','tax-0':'','rate-0':''}; }
  const LINE_KEYS=['kind','amount','category','activity_id','proposal_id','vat_status','net','tax','rate'];
  function proposalSelect(name,current) {
    const choices=(snapshot.accounting?.proposals||[]).map(item=>[item.proposal_id,[item.invoice_number||item.proposal_id,[item.gross,item.currency].filter(Boolean).join(' '),item.activity_id].filter(Boolean).join(' · ')]);
    return `<div class="field"><label for="${esc(name)}">${label('linkedProposal')}</label><select id="${esc(name)}" name="${esc(name)}">${option('',t('noProposal'),current)}${choices.map(item=>option(item[0],item[1],current)).join('')}</select></div>`;
  }
  function lineVat(value,index) {
    const optional=text=>String(text??'').trim()?money(text):null;
    return {status:value['vat_status-'+index]||'unresolved',net:optional(value['net-'+index]),tax:optional(value['tax-'+index]),rate:optional(value['rate-'+index])};
  }
  function entryEditor() {
    const value=drafts.entry||entryDefaults(); drafts.entry=value;
    let lines='';
    for (let index=0;index<Number(value.line_count||1);index++) lines+=`<div class="line-row"><div class="grid">${select('kind-'+index,'kind',['unresolved','income','expense','transfer'].map(kind=>[kind,t(kind)]),value['kind-'+index])}${field('amount-'+index,'lineAmount',value['amount-'+index]||'')}${field('category-'+index,'category',value['category-'+index]||'')}${field('activity_id-'+index,'activity',value['activity_id-'+index]||'')}</div><div class="grid">${proposalSelect('proposal_id-'+index,value['proposal_id-'+index]||'')}${select('vat_status-'+index,'vatStatus',['unresolved','stated','none_stated'].map(status=>[status,t('vat-'+status)]),value['vat_status-'+index]||'unresolved')}${field('net-'+index,'vatNet',value['net-'+index]||'','text','',false)}${field('tax-'+index,'vatTax',value['tax-'+index]||'','text','',false)}${field('rate-'+index,'vatRate',value['rate-'+index]||'','text','',false)}</div>${index?`<button type="button" data-action="remove-line" data-index="${index}">${label('remove')}</button>`:''}</div>`;
    return `<div class="heading-row"><h1>${label('entryTitle')}</h1>${action('back','back')}</div><p class="hint">${label('entryHint')}</p><form id="work-form" data-form="entry" class="panel"><input type="hidden" name="entry_id" value="${esc(value.entry_id)}"><input type="hidden" name="replaces" value="${esc(value.replaces)}"><input type="hidden" name="line_count" value="${esc(value.line_count||1)}">${value.replaces?`<p>${label('replaces')}: ${esc(value.replaces)}</p>`:''}<div class="grid">${field('date','entryDate',value.date,'date')}${field('account','account',value.account)}${field('transaction_id','transaction',value.transaction_id)}${field('amount','amount',value.amount,'text','moneyHint')}${field('currency','currency',value.currency)}${field('reviewer','reviewer',value.reviewer)}</div><section class="form-section"><h2>${label('lines')}</h2><p class="hint">${label('vatHint')}</p>${lines}${action('addLine','add-line')}</section><section class="form-section">${evidence('evidence_file','evidence',value.evidence_file)}${textarea('note','note',value.note)}</section><div class="actions"><button type="submit" class="primary">${label('recordEntry')}</button>${action('saveDraft','save-draft')}${action('discard','discard-draft')}</div></form>`;
  }
  function reversalEditor() {
    const value=drafts[draftKey('reversal')]||{};
    return `<div class="heading-row"><h1>${label('reverseTitle')}</h1>${action('back','back')}</div><form id="work-form" data-form="reversal" class="panel"><p>${label('entryId')}: ${esc(editor.id)}</p><input type="hidden" name="reversal_id" value="${esc(value.reversal_id||'reversal-'+uuid())}">${field('actor','actor',value.actor)}${evidence('evidence_file','evidence',value.evidence_file)}${textarea('note','reversalReason',value.note)}<div class="actions"><button type="submit" class="danger">${label('confirmReverse')}</button>${action('saveDraft','save-draft')}${action('discard','discard-draft')}</div></form>`;
  }
  function accountsPage() {
    const config=snapshot.accounting?.configuration;
    const locked=(snapshot.accounting?.entries?.length||0)+(snapshot.accounting?.filings?.length||0)>0;
    const value=drafts.configuration||config||{};
    return intro('accountsTitle','accountsText')+`<section class="panel"><h2>${label('configured')}</h2>${locked?`<p>${esc(t(config?.system))} · ${esc(config?.product||'')} · ${esc(config?.method)}</p><p class="hint">${label('configLocked')}</p>`:`<form id="work-form" data-form="configuration">${select('system','accountingSystem',[['local',t('local')],['external',t('external')]],value.system||'')}${field('product','product',value.product||'','text','',false)}${select('method','method',[['unresolved',t('unresolved')],['EÜR','EÜR'],['Bilanzierung','Bilanzierung']],value.method||'')}${field('account_reference','accountRef',value.account_reference||'')}${field('reviewer','reviewer',value.reviewer||'')}${evidence('evidence_file','evidence',value.evidence_file||'')}<div class="actions"><button type="submit" class="primary">${label('saveConfig')}</button>${action('saveDraft','save-draft')}${action('discard','discard-draft')}</div></form>`}</section><section class="section"><h2>${label('services')}</h2><p>${label('servicesText')}</p>${action('help','help')}</section>`;
  }
  function taxesPage() {
    const filings=snapshot.accounting?.filings||[];
    return intro('taxesTitle','taxesText')+`<div class="actions">${action(drafts.filing?'resumeFiling':'createFiling','new-filing','primary')}</div><section class="section">${filings.length?`<div class="table-wrap"><table><thead><tr><th>${label('form')}</th><th>${label('filingPeriod')}</th><th>${label('status')}</th><th></th></tr></thead><tbody>${filings.map(item=>`<tr><td>${esc((snapshot.forms||[]).find(form=>form.id===item.record.form)?.label||item.record.form)}<div class="path">${esc(item.record.recipient)}</div></td><td>${esc(item.record.period)}</td><td>${badge(item.record.state)}</td><td><button data-action="inspect-filing" data-id="${esc(item.record.filing_id)}">${label('inspectFiling')}</button></td></tr>`).join('')}</tbody></table></div>`:`<p class="empty">${label('noFilings')}</p>`}</section>`;
  }
  function filingEditor() {
    const value=drafts.filing||{filing_id:'filing-'+uuid(),form:'',form_version:'',period,recipient:'',payload_file:'',source_files:[],unresolved_items:'',supersedes:''}; drafts.filing=value;
    return `<div class="heading-row"><h1>${label('filingTitle')}</h1>${action('back','back')}</div><p class="hint">${label('filingCorrectionHint')}</p><form id="work-form" data-form="filing" class="panel"><input type="hidden" name="filing_id" value="${esc(value.filing_id)}"><input type="hidden" name="supersedes" value="${esc(value.supersedes)}">${value.supersedes?`<p>${label('supersedes')}: ${esc(value.supersedes)}</p>`:''}${select('form','form',(snapshot.forms||[]).map(form=>[form.id,form.label]),value.form)}<div class="grid">${field('form_version','formVersion',value.form_version)}${field('period','filingPeriod',value.period)}</div>${field('recipient','recipient',value.recipient)}${evidence('payload_file','payload',value.payload_file)}${select('source_files','sources',(snapshot.files||[]).map(file=>[file.path,file.name+' · '+file.path]),'', 'sourcesHint',true)}${textarea('unresolved_items','unresolvedItems',value.unresolved_items||'',false)}<div class="actions"><button type="submit" class="primary">${label('saveFiling')}</button>${action('saveDraft','save-draft')}${action('discard','discard-draft')}</div></form>`;
  }
  function filingDetails() {
    const item=(snapshot.accounting?.filings||[]).find(item=>item.record.filing_id===editor.id);
    if (!item) { editor=null; return taxesPage(); }
    const record=item.record, check=item.check||{}, value=drafts[draftKey('filingAction')]||{};
    const transitions={draft:['review','cancel'],reviewed:['authorize','cancel'],authorized:['begin','cancel'],submission_unconfirmed:['not-submitted','receipt'],submitted:['response'],cancelled:[]};
    const acts=transitions[record.state]||[];
    const issues=check.issues||[];
    return `<div class="heading-row"><h1>${label('filingDetails')}</h1>${action('back','back')}</div><section class="panel">${summary([['filingRef',record.filing_id],['status',t(record.state==='reviewed'?'reviewedState':record.state)],['recipient',record.recipient],['filingPeriod',record.period],['payload',record.payload_file],['payloadHash',record.payload?.sha256||'']])}<h2>${label('preflight')}</h2>${issues.length?`<div class="warning"><p>${label('preflightBlocked')}</p><ul>${issues.map(issue=>`<li>${esc(issue.detail||issue.code||String(issue))}</li>`).join('')}</ul></div>`:`<p class="hint">${label('noBlockers')}</p>`}<p class="hint">${label('filingCorrectionHint')}</p>${['submitted','cancelled'].includes(record.state)?action('filingCorrection','correct-filing'):''}${filingHistory(record)}</section>${acts.length?`<form id="work-form" data-form="filingAction" class="panel">${select('action','filingAction',acts.map(act=>[act,t(act==='receipt'?'receipt-action':act)]),value.action||'')}${field('actor','actor',value.actor||'')}${evidence('evidence_file','evidence',value.evidence_file||'')}${textarea('note','actionNote',value.note||'')}${field('external_id','externalId',value.external_id||'','text','',false)}${select('response_kind','responseKind',['acknowledgement','request_for_information','assessment','rejection','other'].map(kind=>[kind,t(kind)]),value.response_kind||'')}${field('due_date','dueDate',value.due_date||'','date','',false)}<div class="actions"><button type="submit" class="primary">${label('actionSave')}</button>${action('saveDraft','save-draft')}${action('discard','discard-draft')}</div></form>`:''}`;
  }
  function filingHistory(record) {
    const events=record.events||[];
    if(!events.length) return '';
    return `<section class="form-section"><h2>${label('filingHistory')}</h2><div class="table-wrap filing-history" tabindex="0" role="region" aria-label="${label('filingHistory')}"><table><thead><tr><th>${label('recordedAt')}</th><th>${label('filingAction')}</th><th>${label('actionNote')}</th><th>${label('evidence')}</th></tr></thead><tbody>${events.map(event=>`<tr><td>${esc(event.recorded_at)}<div class="path">${esc(event.actor)}</div></td><td>${esc(t(event.action==='receipt'?'receipt-action':event.action))}${event.external_id?`<div>${esc(event.external_id)}</div>`:''}${event.response_kind?`<div>${esc(t(event.response_kind))}</div>`:''}${event.due_date?`<div>${label('dueDate')}: ${esc(event.due_date)}</div>`:''}</td><td>${esc(event.note)}</td><td>${event.evidence?.path?`<button type="button" data-action="download-file" data-path="${esc(event.evidence.path)}">${label('download')}</button>`:''}</td></tr>`).join('')}</tbody></table></div></section>`;
  }
  function settingsPage() {
    return intro('settingsTitle','settingsText')+`<section class="panel"><form id="backup-form"><h2>${label('backup')}</h2>${field('backup-destination','destination','','text','backupHint')}<div class="actions">${action('browse','browse-backup')}<button type="submit" class="primary">${label('backup')}</button></div></form></section><section class="panel"><form id="restore-form"><h2>${label('verifyBackup')}</h2>${field('backup-path','backupPath')}${field('restore-destination','restoreDestination','','text','restoreHint',false)}<div class="actions">${action('browse','browse-restore')}<button type="button" data-action="verify-backup">${label('verifyBackup')}</button><button type="submit">${label('restore')}</button></div></form></section>${recoveryOutcome?`<section class="panel"><p>${label('complete')}</p>${formatResult(recoveryOutcome)}</section>`:''}<section class="section"><h2>${label('switch')}</h2>${action('switch','switch-workspace')}<details><summary>${label('diagnostics')}</summary><p class="path">${esc(snapshot.workspace.root)}</p><p>${label('footer')}</p></details></section>`;
  }
  function formatResult(result) {
    const paths=[];
    function visit(value,key='') {
      if (Array.isArray(value)) value.forEach(item=>visit(item,key));
      else if (value && typeof value==='object') Object.entries(value).forEach(([name,item])=>visit(item,name));
      else if (typeof value==='string' && (key.endsWith('path')||key.endsWith('file'))) paths.push(value);
    }
    visit(result);
    const errors=result.errors||[];
    return (errors.length?`<div class="warning"><ul>${errors.map(item=>`<li>${esc(item.name||item.source||'')}: ${esc(item.error||String(item))}</li>`).join('')}</ul></div>`:'')+(paths.length?`<ul class="file-list">${[...new Set(paths)].map(path=>`<li><button data-action="download-file" data-path="${esc(path)}">${esc(path)}</button></li>`).join('')}</ul>`:`<p>${label('complete')}</p>`);
  }
  function showPreview(file) {
    const target=$('original-preview'); if (!target) return;
    target.replaceChildren();
    const bytes=Uint8Array.from(atob(file.content),char=>char.charCodeAt(0));
    if (['image/png','image/jpeg'].includes(file.mime)) {
      const image=document.createElement('img'), url=URL.createObjectURL(new Blob([bytes],{type:file.mime}));
      image.src=url; image.alt=file.name; image.onload=()=>URL.revokeObjectURL(url); target.append(image);
    } else if (/^(text\/|application\/(xml|json))/.test(file.mime)) {
      const text=document.createElement('pre'); text.textContent=new TextDecoder().decode(bytes); target.append(text);
    }
    const button=document.createElement('button');button.type='button';button.textContent=t('download');button.addEventListener('click',()=>download(file));target.append(button);
  }
  function download(file) {
    const bytes=Uint8Array.from(atob(file.content),char=>char.charCodeAt(0));
    const url=URL.createObjectURL(new Blob([bytes],{type:'application/octet-stream'}));
    const link=document.createElement('a');link.href=url;link.download=file.name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function money(value) { return String(value).trim().replace(',','.'); }
  function formValue(form) { const data={};for(const control of form.elements)if(control.name)data[control.name]=control.multiple?Array.from(control.selectedOptions).map(item=>item.value):control.value;return data; }
  async function completed(op,args,kind) {
    await api(op,args);
    if (kind) delete drafts[draftKey(kind)];
    delete drafts.continuation;
    dirty=false; editor=null; preview=null;
    let draftError=null;
    try { const saved=await api('draft-save',{drafts,expected_sha256:draftHash}); draftHash=saved.sha256; }
    catch(error) { draftError=error; }
    await refresh(false);
    notice(t('saved'));
    if(draftError) throw new Error(t('saved')+' '+draftError.message);
  }
  $('main').addEventListener('input',event=>{
    if(event.target.id==='search'){$('document-list').innerHTML=documentList(event.target.value);return;}
    if(event.target.closest('#work-form')){captureForm();setDirty();}
  });
  $('main').addEventListener('change',event=>{
    if(event.target.id==='document-files') {selectedFiles=Array.from(event.target.files);$('selected-files').textContent=selectedFiles.map(file=>file.name).join(', ');}
    if(event.target.closest('#work-form')){captureForm();setDirty();}
  });
  $('main').addEventListener('submit',event=>{
    event.preventDefault();const form=event.target;
    if(form.id==='open-form'){perform(()=>openWorkspace(false));return;}
    if(form.id==='import-form'){perform(importFiles);return;}
    if(form.id==='backup-form'){perform(async()=>{recoveryOutcome=await api('backup',{destination:$('backup-destination').value});render();notice(t('complete'));});return;}
    if(form.id==='restore-form') {const backup=$('backup-path').value,destination=$('restore-destination').value;confirm(t('restore'),summary([['backupPath',backup],['restoreDestination',destination]]),()=>perform(async()=>{recoveryOutcome=await api('restore',{backup,destination});render();notice(t('complete'));}));return;}
    captureForm(); const value=formValue(form), kind=form.dataset.form;
    if(kind==='document') {
      const item=snapshot.documents.find(item=>item.record.document_id===editor.id);
      const record={...structuredClone(item.record),title:value.title,type:value.type,review_status:value.review_status,reviewer:value.reviewer||null,review_note:value.review_note||null};
      perform(()=>completed('document-save',{record,expected_sha256:drafts[draftKey('document')].__expected_sha256},'document'));return;
    }
    if(kind==='configuration') {
      const config={system:value.system,product:value.system==='external'?value.product:null,method:value.method,account_reference:value.account_reference,reviewer:value.reviewer,evidence_file:value.evidence_file};
      confirm(t('confirmTitle'),summary([['accountingSystem',t(config.system)],['product',config.product||'—'],['method',config.method],['accountRef',config.account_reference],['evidence',config.evidence_file]]),()=>perform(()=>completed('configuration',{value:config,expected_sha256:drafts.configuration.__expected_sha256},'configuration')));return;
    }
    if(kind==='entry') {
      const record={schema_version:2,entry_id:value.entry_id,date:value.date,account:value.account,transaction_id:value.transaction_id,amount:money(value.amount),currency:value.currency,lines:[],reviewer:value.reviewer,evidence_file:value.evidence_file,note:value.note,replaces:value.replaces||null};
      for(let index=0;index<Number(value.line_count);index++)record.lines.push({kind:value['kind-'+index],amount:money(value['amount-'+index]),category:value['category-'+index],activity_id:value['activity_id-'+index],proposal_id:value['proposal_id-'+index]||null,vat:lineVat(value,index)});
      const vatSummary=record.lines.map(line=>t('vat-'+line.vat.status)+(line.vat.net!==null||line.vat.tax!==null?`: ${line.vat.net??'—'} + ${line.vat.tax??'—'}${line.vat.rate!==null?` (${line.vat.rate} %)`:''}`:'')).join('; ');
      confirm(t('confirmTitle'),summary([['entryDate',record.date],['transaction',record.transaction_id],['amount',record.amount+' '+record.currency],['vatStatus',vatSummary],['evidence',record.evidence_file],['reviewer',record.reviewer],['note',record.note]])+`<p class="hint">${label('immutable')}</p>`,()=>perform(()=>completed('entry-post',{value:record},'entry')));return;
    }
    if(kind==='reversal') {const entry_id=editor.id;confirm(t('reverseTitle'),summary([['entryId',entry_id],['reversalReason',value.note],['evidence',value.evidence_file]]),()=>perform(()=>completed('entry-reverse',{entry_id,reversal_id:drafts[draftKey('reversal')]?.reversal_id||'reversal-'+uuid(),...value},'reversal')));return;}
    if(kind==='filing') {
      const record={...value,source_files:value.source_files||[],unresolved_items:value.unresolved_items.split('\n').map(item=>item.trim()).filter(Boolean),supersedes:value.supersedes||null};
      confirm(t('confirmTitle'),summary([['form',record.form],['filingPeriod',record.period],['recipient',record.recipient],['payload',record.payload_file],['sources',record.source_files.join('\n')]]),()=>perform(()=>completed('filing-create',{value:record},'filing')));return;
    }
    if(kind==='filingAction') {
      const item=snapshot.accounting.filings.find(item=>item.record.filing_id===editor.id);
      if(['review','authorize','begin'].includes(value.action)&&(item.check?.issues||[]).length) {showError(t('preflightBlocked'));return;}
      const record={filing_id:editor.id,action:value.action,actor:value.actor,evidence_file:value.evidence_file,note:value.note,external_id:value.action==='receipt'?value.external_id||null:null,response_kind:value.action==='response'?value.response_kind||null:null,due_date:value.action==='response'?value.due_date||null:null};
      confirm(t('confirmTitle'),summary([['filingAction',t(record.action==='receipt'?'receipt-action':record.action)],['filingRef',record.filing_id],['recipient',item.record.recipient],['filingPeriod',item.record.period],['payload',item.record.payload_file],['payloadHash',item.record.payload?.sha256],['actionNote',record.note],['evidence',record.evidence_file],['externalId',record.external_id||'—']]),()=>perform(()=>completed('filing-action',{value:record,expected_sha256:drafts[draftKey('filingAction')].__expected_sha256},'filingAction')));
    }
  });
  async function openWorkspace(create) {
    const path=$('workspace-path').value, year=Number($('year').value), folderLanguage=$('folder-language').value;
    const opened=await api('open',{path,create,language:folderLanguage,year});snapshot={workspace:opened};dirty=false;drafts={};editor=null;route='home';history.replaceState(null,'','#home');await refresh(false);notice(t('saved'));
  }
  async function importFiles() {
    if(!selectedFiles.length)throw new Error(t('noSelection'));
    const files=[];
    for(const file of selectedFiles){const bytes=new Uint8Array(await file.arrayBuffer());let binary='';for(let index=0;index<bytes.length;index+=8192)binary+=String.fromCharCode(...bytes.subarray(index,index+8192));files.push({name:file.name,content:btoa(binary)});}
    importOutcome=await api('receive',{files,period:$('import-period').value,received_on:$('received-on').value,type:'unknown'});
    if(!(importOutcome.errors||[]).length)selectedFiles=[];
    await refresh();notice((importOutcome.errors||[]).length?t('error'):t('saved'));
  }
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[data-route]');
    if(link){event.preventDefault();if(!busy)leave(()=>navigate(link.dataset.route));return;}
    const button=event.target.closest('button[data-action]');if(!button||busy)return;
    const name=button.dataset.action;
    switch(name) {
      case 'refresh':perform(()=>refresh());break;
      case 'documents':case 'accounts':case 'month':case 'settings':leave(()=>navigate(name));break;
      case 'review-next':{const item=snapshot.documents.find(item=>!['reviewed','excluded'].includes(item.record.review_status));if(item){route='documents';editor={kind:'document',id:item.record.document_id};render();}break;}
      case 'review-document':editor={kind:'document',id:button.dataset.id};preview=null;render();break;
      case 'preview-original':perform(async()=>{const item=snapshot.documents.find(item=>item.record.document_id===editor.id);preview=await api('file',{path:item.path});showPreview(preview);});break;
      case 'download-file':perform(async()=>download(await api('file',{path:button.dataset.path})));break;
      case 'resume-work':{const point=drafts.continuation;if(point){route=routes.has(point.route)?point.route:'home';editor=point.editor||null;render();}break;}
      case 'inspect-next-filing':{const item=snapshot.accounting?.filings?.find(item=>item.record.state==='submission_unconfirmed'||(item.check?.issues||[]).length);if(item){route='taxes';editor={kind:'filingAction',id:item.record.filing_id};render();}break;}
      case 'new-entry':editor={kind:'entry'};drafts.entry ||= entryDefaults();render();break;
      case 'reverse-entry':editor={kind:'reversal',id:button.dataset.id};drafts[draftKey('reversal')] ||= {actor:'',evidence_file:'',note:'',reversal_id:'reversal-'+uuid()};render();break;
      case 'correct-entry':{const entry=snapshot.accounting.entries.find(item=>item.entry_id===button.dataset.id);drafts.entry={...entryDefaults(),date:entry.date,account:entry.account,transaction_id:entry.transaction_id,currency:entry.currency,replaces:entry.entry_id};editor={kind:'entry'};render();break;}
      case 'add-line':captureForm();drafts.entry.line_count=String(Number(drafts.entry.line_count||1)+1);render();setDirty();break;
      case 'remove-line':{captureForm();const value=drafts.entry,count=Number(value.line_count),index=Number(button.dataset.index);for(let next=index;next<count-1;next++)for(const key of LINE_KEYS)value[key+'-'+next]=value[key+'-'+(next+1)];for(const key of LINE_KEYS)delete value[key+'-'+(count-1)];value.line_count=String(count-1);render();setDirty();break;}
      case 'new-filing':editor={kind:'filing'};render();break;
      case 'inspect-filing':editor={kind:'filingAction',id:button.dataset.id};render();break;
      case 'correct-filing':{const item=snapshot.accounting.filings.find(item=>item.record.filing_id===editor.id);drafts.filing={filing_id:'filing-'+uuid(),form:item.record.form,form_version:item.record.form_version,period:item.record.period,recipient:item.record.recipient,payload_file:'',source_files:item.record.source_files,unresolved_items:'',supersedes:item.record.filing_id};editor={kind:'filing'};render();setDirty();break;}
      case 'save-draft':perform(saveDraft);break;
      case 'discard-draft':confirm(t('leaveTitle'),`<p>${label('leaveText')}</p>`,()=>perform(async()=>{const key=draftKey(editor?.kind||$('work-form')?.dataset.form);delete drafts[key];delete drafts.continuation;const result=await api('draft-save',{drafts,expected_sha256:draftHash});draftHash=result.sha256;dirty=false;await refresh();}),t('discard'));break;
      case 'back':leave(()=>{editor=null;preview=null;render();});break;
      case 'create-workspace':perform(()=>openWorkspace(true));break;
      case 'browse-workspace':perform(async()=>{const result=await api('select-folder',{purpose:'workspace'});if(result.path)$('workspace-path').value=result.path;});break;
      case 'browse-backup':perform(async()=>{const result=await api('select-folder',{purpose:'backup'});if(result.path)$('backup-destination').value=result.path+(result.path.includes('\\')?'\\':'/')+'business-backup-'+today();});break;
      case 'browse-restore':perform(async()=>{const result=await api('select-folder',{purpose:'restore'});if(result.path)$('backup-path').value=result.path;});break;
      case 'verify-backup':perform(async()=>{recoveryOutcome=await api('verify-backup',{backup:$('backup-path').value});render();notice(t('complete'));});break;
      case 'switch-workspace':leave(()=>{snapshot={workspace:null};editor=null;render();});break;
      case 'report':perform(async()=>{reportOutcome=await api('report',{period});await refresh();notice(t('saved'));});break;
      case 'help':openHelp();break;
    }
  });
  $('settings-link').addEventListener('click',event=>{event.preventDefault();if(!busy)leave(()=>navigate('settings'));});
  $('language').addEventListener('change',event=>{captureForm();language=event.target.value;try{sessionStorage.setItem('gbk-language',language);}catch{}render();});
  $('period').addEventListener('change',event=>{const chosen=event.target.value;if(!/^\d{4}-\d{2}$/.test(chosen))return;leave(()=>{period=chosen;perform(()=>refresh());});});
  $('skip').addEventListener('click',event=>{event.preventDefault();$('main').focus();});
  $('cancel-confirm').addEventListener('click',()=>{$('confirm-dialog').close();pendingConfirm=null;});
  $('accept-confirm').addEventListener('click',()=>{const callback=pendingConfirm;pendingConfirm=null;$('confirm-dialog').close();if(callback)callback();});
  $('help-button').addEventListener('click',openHelp);
  $('close-help').addEventListener('click',()=>$('help-dialog').close());
  $('copy-help').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('help-prompt').value);$('copy-status').textContent=t('copied');}catch{$('help-prompt').focus();$('help-prompt').select();$('copy-status').textContent=t('copyManual');}});
  function openHelp() {
    $('help-title').textContent=t('helpTitle');$('help-label').textContent=t('helpLabel');$('help-hint').textContent=t('helpHint');$('copy-help').textContent=t('copy');$('close-help').textContent=t('close');$('copy-status').textContent='';
    const contexts={en:`Help me continue my own German business work in ${period}. I am on “${t(route)}”${editor?`, reviewing ${editor.kind} ${editor.id||''}`:''}. Check the actual saved records and available tools. Explain the next useful step and any unresolved evidence. Keep review, accounting entries and manual ELSTER outcomes distinct. Do not send anything automatically.`,ru:`Помоги продолжить самостоятельный учёт бизнеса в Германии за ${period}. Я в разделе «${t(route)}»${editor?`, проверяю ${editor.kind} ${editor.id||''}`:''}. Проверь сохранённые записи и доступные инструменты. Объясни следующий шаг и недостающие доказательства. Разделяй проверку, записи учёта и фактический результат ручной подачи ELSTER. Ничего не отправляй автоматически.`,de:`Hilf mir, meine eigene Unternehmensarbeit in Deutschland für ${period} fortzusetzen. Ich bin auf „${t(route)}“${editor?`, bei ${editor.kind} ${editor.id||''}`:''}. Prüfe gespeicherte Daten und verfügbare Werkzeuge. Erkläre den nächsten Schritt und offene Nachweise. Halte Prüfung, Buchungen und manuelle ELSTER-Ergebnisse getrennt. Versende nichts automatisch.`};
    if (route==='home' && !editor && (snapshotUnavailable||(snapshot?.errors||[]).length||(snapshot?.overview?.errors||[]).length||activeTasks().length||!hasBusinessRecords())) {
      const errors=snapshotUnavailable||(snapshot?.errors||[]).length||(snapshot?.overview?.errors||[]).length;
      const tasks=errors?[]:activeTasks();
      const nextTask=tasks.find(task=>task.id===snapshot.overview?.next_task_id);
      const taskContext=nextTask ? `${nextTask.id}: ${nextTask.title}` : tasks.map(task=>`${task.id}: ${task.title}`).join('\n');
      const homeContexts={
        en:errors?t('taskRepair'):tasks.length?`Help me continue this German business task: ${taskContext}. Inspect its saved state, dependencies and evidence before suggesting the next step. Do not mark tasks complete or perform external actions automatically.`:`${t('askTask')} Help me choose the task I want to work on in my German business. Ask about my intended outcome and inspect existing records before proposing a route.`,
        ru:errors?t('taskRepair'):tasks.length?`Помоги продолжить задачу бизнеса в Германии: ${taskContext}. Проверь сохранённое состояние, зависимости и доказательства перед следующим шагом. Не отмечай задачи выполненными и не выполняй внешние действия автоматически.`:`${t('askTask')} Помоги выбрать задачу для моего бизнеса в Германии. Уточни желаемый результат и проверь существующие записи перед выбором маршрута.`,
        de:errors?t('taskRepair'):tasks.length?`Hilf mir bei dieser Unternehmensaufgabe in Deutschland: ${taskContext}. Prüfe gespeicherten Stand, Abhängigkeiten und Nachweise vor dem nächsten Schritt. Markiere keine Aufgabe als erledigt und führe keine externen Aktionen automatisch aus.`:`${t('askTask')} Hilf mir, meine gewünschte Unternehmensaufgabe in Deutschland zu wählen. Frage nach meinem Ziel und prüfe vorhandene Daten vor einem Routenvorschlag.`
      };
      contexts[language]=homeContexts[language];
    }
    $('help-prompt').value=contexts[language];$('help-dialog').showModal();
  }
  window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue='';}});
  window.addEventListener('hashchange',()=>{if(busy){history.replaceState(null,'','#'+route);return;}const next=location.hash.slice(1);if(routes.has(next))leave(()=>navigate(next));});
  route=routes.has(location.hash.slice(1))?location.hash.slice(1):'home';
  perform(async()=>{snapshot=await api('context');await refresh(false);});
})();
