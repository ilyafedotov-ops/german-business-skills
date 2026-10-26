/* Synthetic interaction prototype. All actions stay inside this browser. */
(() => {
  'use strict';
  let storage;
  try { storage = window.localStorage; } catch (_) { storage = { getItem() { throw new Error('unavailable'); } }; }
  const store = DemoState.openStore(storage), state = store.state;
  const main = document.querySelector('main');
  const escape = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  let route = 'home', step = state.onboarding.step, selected = new Set(state.onboarding.selected);
  let goal = state.onboarding.goal, source = state.onboarding.source, formError = '', search = '', filter = 'all';
  let helpOpener;
  const docs = [
    { id: 'invoice', name: 'October studio supplies.pdf', type: 'Invoice', date: '8 Oct 2026', amount: '€119.80', detail: 'Papier & Form · Total needs checking' },
    { id: 'receipt', name: 'Parcel receipt.pdf', type: 'Receipt', date: '10 Oct 2026', amount: '€12.00', detail: 'Paket Beispiel · Possible payment match' },
    { id: 'statement', name: 'October bank export.csv', type: 'Bank export', date: 'October 2026', amount: '1 example payment', detail: 'Sample account · EUR' }
  ];
  const button = (text, action, primary = false, extra = '') => `<button ${extra} class="${primary ? 'primary' : ''}" data-action="${action}">${text}</button>`;
  const intro = (eyebrow, title, description) => `<div class="heading-row"><div class="page-intro"><h1>${title}</h1><p>${description}</p></div><button class="text-button" data-action="help">Help me with this</button></div>`;
  const badge = (text, kind = '') => `<span class="badge ${kind}">${text}</span>`;
  function save() {
    Object.assign(state.onboarding, { step, selected: [...selected], goal, source });
    const result = store.save();
    document.querySelector('#save-status').textContent = result.message;
    const warning = document.querySelector('#storage-warning');
    warning.hidden = result.ok;
    warning.textContent = result.ok ? '' : result.message;
    return result.ok;
  }
  function go(next) {
    if (location.hash === `#${next}`) render();
    else location.hash = next;
  }
  function resume() {
    return ['review', 'payment', 'documents', 'month', 'taxes', 'accounts', 'onboard'].includes(state.resume) ? state.resume : 'documents';
  }
  function home() {
    const imported = state.imported.length > 0;
    const next = !imported ? 'onboard' : state.imported.includes('invoice') && !state.invoice.reviewed ? 'review' : state.imported.includes('statement') && !state.payment.matched ? 'payment' : 'month';
    return intro('A CLEARER DAY', imported ? 'Welcome back to your business.' : 'A place for your business to make sense.', 'Your documents, decisions and next steps, together. You stay in control of your own accounting.') +
      `<section class="hero card"><div><h2>${!imported ? 'Turn a folder of records into a clear starting point.' : next === 'review' ? 'One invoice needs a closer look.' : next === 'payment' ? 'Find the receipt for a €12.00 payment.' : 'See what is ready — and what is still open.'}</h2><p>${!imported ? 'Try a three-file example. Preview the contents, choose what to include and see what needs your attention.' : 'Take one small step. Your progress stays here so you can pick it up again.'}</p><div class="actions">${button(!imported ? 'Organize existing records' : next === 'review' ? 'Review the invoice' : next === 'payment' ? 'Investigate payment' : 'Review this month', next, true)}${button(imported ? 'Continue where I stopped' : 'Start a business', imported ? 'resume' : 'start-business')}</div></div></section>` +
      `<div class="stats"><div class="stat"><span class="count">${state.imported.length}</span><p>documents in your demo</p></div><div class="stat"><span class="count">${state.imported.includes('invoice') && !state.invoice.reviewed ? 1 : 0}</span><p>invoice to check</p></div><div class="stat"><span class="count">${state.imported.includes('statement') && !state.payment.matched ? 1 : 0}</span><p>payment to investigate</p></div></div>` +
      `<div class="grid"><section class="card"><h2>Small steps, clear outcomes.</h2>${!imported ? '<p class="muted">Nothing is waiting yet. Add the example records to discover your first tasks.</p>' : `<div class="task"><div><h3>Check the invoice total</h3><p class="hint">Compare the suggestion with the original.</p>${badge(state.invoice.reviewed ? 'Document reviewed' : state.imported.includes('invoice') ? 'Needs review' : 'Not imported', state.invoice.reviewed ? 'green' : '')}</div>${state.imported.includes('invoice') ? button('Open invoice', 'review') : ''}</div><div class="task"><div><h3>Find the parcel receipt</h3><p class="hint">A match does not create an accounting entry.</p>${badge(state.payment.matched ? 'Linked in demo' : state.imported.includes('statement') ? 'Unmatched' : 'Not imported', state.payment.matched ? 'green' : '')}</div>${state.imported.includes('statement') ? button('Open payment', 'payment') : ''}</div>`}</section><section class="card"><h2>No need to remember a prompt.</h2><p class="muted">Your corrections and notes are saved in this browser when storage is available. Come back to the task you last opened.</p>${button('Continue my work', 'resume')}<details><summary>Where is my work saved?</summary><p>This is a fictional demo, stored only in this browser. It is not synced or backed up. Moving the files, switching browsers or clearing browser data can remove access to this progress.</p></details></section></div>`;
  }
  function onboarding() {
    const steps = ['Choose a starting point', 'Preview records', 'Review import'];
    let body;
    if (step === 0) {
      body = `<h2>What would you like to do?</h2><div class="choices">${[['organize', 'Organize existing records', 'Start with documents or exports you already have.'], ['start', 'Start a business', 'Explore the setup questions without guessing your tax status.'], ['continue', 'Continue my work', 'Return to the last saved task in this demo.']].map(([id, title, hint]) => `<label class="choice"><input type="radio" name="goal" value="${id}" ${goal === id ? 'checked' : ''}><span><strong>${title}</strong><small>${hint}</small></span></label>`).join('')}</div><div class="field"><label for="source">Where are your records?</label><select id="source"><option value="folder" ${source === 'folder' ? 'selected' : ''}>A folder on my computer — sample folder</option><option value="service" ${source === 'service' ? 'selected' : ''}>Gmail or accounting software</option></select><p class="hint">This prototype uses fictional files. It never opens a real folder or account.</p></div><details><summary>Why not ask all my business questions now?</summary><p>Business type, VAT treatment and reporting obligations matter when deciding accounting or tax treatment. You can organize records first without inventing those facts.</p></details>${button('Continue', 'onboard-next', true)}`;
    } else if (step === 1) {
      body = `<h2>Here is what the sample folder contains.</h2><p class="muted">Select the records to include. The original examples stay unchanged.</p><div class="choices">${docs.map(d => `<label class="choice"><input type="checkbox" name="import" value="${d.id}" ${selected.has(d.id) ? 'checked' : ''}><span><strong>${d.name}</strong><small>${d.type} · ${d.date} · ${d.amount}${state.imported.includes(d.id) ? ' · Already imported; no second copy will be added' : ''}</small></span></label>`).join('')}</div><div class="notice"><strong>1 example file excluded:</strong> old-backup.exe is not a supported document. Nothing will be opened or executed.</div><details><summary>What happens to the bank export?</summary><p>This demo has a fixed EUR payment. A production import needs a reviewed mapping of dates, signs, amounts, currencies and transaction IDs before reconciliation.</p></details><div class="actions">${button('Back', 'onboard-back')}${button('Review selection', 'onboard-next', true)}</div>`;
    } else {
      body = `<h2>Ready to add ${selected.size} example records?</h2><p>Destination: <strong>Studio Beispiel · October 2026 demo</strong></p><ul>${docs.filter(d => selected.has(d.id)).map(d => `<li>${d.name}</li>`).join('')}</ul><p class="hint">Previously imported examples are kept once. This adds fictional catalog items, not reviewed documents or accounting entries.</p><div class="actions">${button('Back', 'onboard-back')}${button('Add selected examples', 'import', true)}${button('Cancel import', 'cancel-import')}</div>`;
    }
    return intro('GET STARTED', 'Bring your records together.', 'A short guided walkthrough. No setup commands, credentials or real documents needed.') + `<ol class="stepper">${steps.map((s, i) => `<li ${step === i ? 'aria-current="step"' : ''}>${i + 1}. ${s}</li>`).join('')}</ol><section class="card">${formError ? `<div class="error" role="alert">${formError}</div>` : ''}${body}</section>`;
  }
  function documents() {
    return intro('YOUR RECORDS', 'Documents', 'Find the original, inspect a suggestion and make a correction. Your files remain the source of truth.') + `<div class="actions">${button('Add example files', 'onboard', true)}</div><section class="card"><div class="filters"><div><label for="search">Search documents</label><input id="search" type="search" placeholder="Try “studio” or “parcel”" value="${escape(search)}"></div><div><label for="filter">Review status</label><select id="filter"><option value="all" ${filter === 'all' ? 'selected' : ''}>All documents</option><option value="needs" ${filter === 'needs' ? 'selected' : ''}>Needs review</option><option value="reviewed" ${filter === 'reviewed' ? 'selected' : ''}>Reviewed</option></select></div></div><div id="document-list">${documentList()}</div></section>`;
  }
  function documentList() {
    const rows = docs.filter(d => state.imported.includes(d.id) && `${d.name} ${d.type}`.toLowerCase().includes(search.toLowerCase()) && (filter === 'all' || (filter === 'reviewed' ? d.id === 'invoice' && state.invoice.reviewed : d.id !== 'invoice' || !state.invoice.reviewed)));
    if (!rows.length) return `<div class="empty"><h2>${state.imported.length ? 'No matching documents.' : 'Your next step starts with a document.'}</h2><p class="muted">${state.imported.length ? 'Try another search or choose “All documents”.' : 'Add the sample folder to see a mixed set of records.'}</p></div>`;
    return `<p class="search-count" role="status">${rows.length} ${rows.length === 1 ? 'document' : 'documents'} shown</p>` + rows.map(d => `<article class="document-row"><div><h3>${d.name}</h3><p>${d.type} · ${d.date} · ${d.amount}</p><p class="muted">${d.detail}</p>${badge(d.id === 'invoice' && state.invoice.reviewed ? 'Document reviewed' : 'Needs review', d.id === 'invoice' && state.invoice.reviewed ? 'green' : '')}</div>${button(d.id === 'invoice' ? 'Review invoice' : 'Inspect example', d.id === 'invoice' ? 'review' : `inspect-${d.id}`)}</article>`).join('');
  }
  function invoice() {
    if (!state.imported.includes('invoice')) return missing('invoice');
    return intro('DOCUMENT REVIEW', 'Check one thing at a time.', 'Compare the original with the suggested information. You can leave the category unresolved and return later.') + `<div class="grid equal"><section class="preview" aria-label="Original example invoice"><div class="paper"><div class="paper-header"><strong>Papier & Form<br><small>Fictional supplier</small></strong><span>DEMO<br>Not a valid invoice</span></div><h2>Rechnung</h2><p>Example INV-2026-108<br>Rechnungsdatum: <strong>08.10.2026</strong><br>Studio Beispiel · fictional customer</p><div class="invoice-line"><span>Studio supplies</span><span>€100.67</span></div><div class="invoice-line"><span>Example VAT (19%)</span><span>€19.13</span></div><div class="invoice-line total"><span>Gesamtbetrag</span><span>€119.80</span></div><p class="hint">Synthetic visual fixture. No real tax number, bank details or personal data.</p></div></section><section class="card"><div class="heading-row"><h2>Your proposed information</h2>${badge(state.invoice.reviewed ? 'Document reviewed' : 'Needs review', state.invoice.reviewed ? 'green' : '')}</div><p class="hint">No accounting entry has been recorded.</p><div id="review-error" class="error" tabindex="-1" hidden></div><div class="field"><label for="invoice-amount">Total amount · EUR</label><input id="invoice-amount" data-field="amount" inputmode="decimal" value="${escape(state.invoice.amount)}" aria-describedby="amount-hint amount-source"><p id="amount-hint" class="hint">Use 119.80 or 119,80. The initial suggestion may be wrong.</p><p id="amount-source" class="source">Source: page 1, “Gesamtbetrag 119,80 EUR”. Initial extraction: 119.00 EUR. Check against the original.</p></div><div class="field"><label for="invoice-date">Invoice date</label><input id="invoice-date" data-field="date" type="date" value="${escape(state.invoice.date)}"><p class="source">Source: page 1, “Rechnungsdatum: 08.10.2026”.</p></div><div class="field"><label for="invoice-category">Proposed category</label><select id="invoice-category" data-field="category"><option value="" ${!state.invoice.category ? 'selected' : ''}>Leave unresolved</option><option value="supplies" ${state.invoice.category === 'supplies' ? 'selected' : ''}>Office supplies — needs accounting review</option><option value="other" ${state.invoice.category === 'other' ? 'selected' : ''}>Something else — describe below</option></select><p class="hint">A suggestion, not a tax conclusion. You can review the source fields while leaving accounting treatment open.</p><details><summary>Why is the category uncertain?</summary><p>The example describes supplies, but does not establish business use, deductibility or VAT treatment. Those require your actual facts and applicable rules.</p></details></div><div class="field"><label for="invoice-note">Note for later</label><textarea id="invoice-note" data-field="note" rows="3" placeholder="What would you like to check?">${escape(state.invoice.note)}</textarea></div><div class="actions">${button('Save draft', 'save-draft')}${button('Mark document reviewed', 'review-complete', true)}</div><p id="review-result" role="status" class="hint"></p></section></div>`;
  }
  function missing(kind) {
    return intro('EXAMPLE NOT IMPORTED', 'Start with the sample folder.', `The ${kind} is not in your demo yet. Choose the relevant example in the preview.`) + button('Choose example files', 'onboard', true);
  }
  function month() {
    const checked = Number(state.invoice.reviewed && state.imported.includes('invoice')) + Number(state.payment.matched);
    return intro('OCTOBER 2026 · FICTIONAL PERIOD', 'This month · October 2026', 'See the evidence you have and what still needs a decision. This is not a tax-return completion score.') + `<div class="grid"><section class="card"><h2>Your example review tasks</h2><label for="progress">${checked} of 2 example checks completed</label><progress id="progress" value="${checked}" max="2">${checked} of 2</progress><ul class="checklist"><li><strong>${state.invoice.reviewed ? 'Completed:' : 'To do:'} Check the studio invoice</strong><span>${state.invoice.reviewed ? 'Document reviewed. Accounting treatment remains separate.' : 'Compare the total and date with the original.'}</span></li><li><strong>${state.payment.matched ? 'Completed:' : 'To do:'} Investigate the €12.00 payment</strong><span>${state.payment.matched ? 'Receipt linked in the demo. No accounting entry recorded.' : 'Find a supporting receipt, or keep a note about what is missing.'}</span></li></ul><div class="actions">${button('Review invoice', 'review')}${button('Investigate payment', 'payment', true)}</div></section><section class="card"><h2>What this does not tell you yet</h2><p class="muted">These examples do not establish that all your accounts or documents were supplied.</p><ul><li>Accounting entries: not recorded by this demo.</li><li>Tax treatment: unresolved.</li><li>Return: not prepared or submitted.</li></ul><details><summary>What comes after document review?</summary><p>Choose your authoritative accounting system, review the actual accounting treatment, record entries and reconcile all relevant accounts. Tax preparation and submission remain separate steps.</p></details></section></div>`;
  }
  function payment() {
    if (!state.imported.includes('statement')) return missing('bank export');
    return intro('PAYMENT INVESTIGATION', 'What is this €12.00 payment for?', 'Compare the statement with the receipt. A matching amount is a clue, not proof by itself.') + `<div class="grid equal"><section class="card"><h2>− €12.00</h2><p>10 October 2026 · Sample EUR account</p><div class="source">Transaction DEMO-PAY-010<br>Counterparty: Paket Beispiel<br>Reference: Parcel DEMO-010</div>${badge(state.payment.matched ? 'Receipt linked in demo' : 'Unmatched', state.payment.matched ? 'green' : '')}<details><summary>Where did these details come from?</summary><p>Fixed synthetic row in “October bank export.csv”. No live bank connection or real CSV parsing is implemented in this prototype.</p></details></section><section class="card"><h2>${state.imported.includes('receipt') ? 'Parcel receipt · €12.00' : 'A receipt is still missing.'}</h2><p>${state.imported.includes('receipt') ? 'Paket Beispiel · 10 October 2026<br>Reference: Parcel DEMO-010<br>Service: domestic parcel delivery' : 'Add the sample receipt from the folder preview, or leave the payment unresolved.'}</p><p class="hint">Fictional receipt. Check the counterparty, date, reference and business purpose before linking.</p><div class="field"><label for="payment-note">Investigation note</label><textarea id="payment-note" rows="3" placeholder="What is missing or what did you check?">${escape(state.payment.note)}</textarea></div><div class="actions">${state.imported.includes('receipt') ? button(state.payment.matched ? 'Remove demo link' : 'Link this example receipt', 'match-payment', true) : button('Choose example files', 'onboard', true)}${button('Keep open and return later', 'defer-payment')}</div><p id="payment-result" role="status"></p></section></div>`;
  }
  function taxes() {
    return intro('A SEPARATE STEP', 'Taxes and letters', 'Preparation, your approval, submission and the Finanzamt’s response are different states.') + `<div class="grid"><section class="card"><h2>Start with the right facts.</h2>${badge('Not prepared', 'neutral')}<p class="muted">An ELSTER worksheet needs your actual period, activity, accounting method and VAT position. This fictional demo cannot infer them.</p><ul class="checklist"><li>Prepare a return<span>Not available in this prototype.</span></li><li>Review and approve the exact version<span>No return or authorization exists.</span></li><li>Submit and retain the receipt<span>No transmission integration is connected.</span></li></ul>${button('Help me prepare the next step', 'help')}</section><section class="card"><h2>Authority correspondence</h2><p>No authority letters in this sample folder.</p><p class="hint">A real task should link its deadline to the inspected letter or applicable official source. No legal deadline is invented for this demo.</p><details><summary>What should I keep from a letter?</summary><p>Preserve the original, sender, date, reference, exact request, source for any deadline and your response. A submission receipt is distinct from an authority decision.</p></details></section></div>`;
  }
  function accounts() {
    return intro('USE WHAT ALREADY WORKS', 'Accounts and services', 'Start with the systems you already use. A connection should say what it can read or change.') + `<div class="grid equal"><section class="card"><h2>Bring existing records</h2><div class="task"><div><h3>A folder on your computer</h3><p class="hint">Preview a mixed sample before importing.</p>${badge('Sample available', 'green')}</div>${button('Preview folder', 'onboard')}</div>${['Gmail', 'Lexware / sevdesk', 'WISO — identify the exact product'].map(name => `<div class="task"><div><h3>${name}</h3>${badge('Not connected', 'neutral')}<p class="hint">No plugin, API or browser session has been verified.</p></div>${button('Explore connection', 'connection-help', false, `data-service="${escape(name)}"`)}</div>`).join('')}</section><section class="card"><h2>Start with your needs, not a ranking.</h2><p class="muted">Compare banking, insurance or payment services against your activity, countries, currencies, volume and existing cover.</p><ul><li>Keep your current service as an option.</li><li>Check eligibility, total costs and exclusions.</li><li>Use dated, primary-source evidence.</li></ul><p class="hint">No provider is recommended or purchased in this demo.</p>${button('Help me compare services', 'service-help')}<details><summary>Why ask about my existing services?</summary><p>A new subscription may add cost without fixing the problem. First identify what is missing, what can be retained and any cancellation or migration constraints.</p></details></section></div>`;
  }
  function settings() {
    return intro('OUTSIDE THE EVERYDAY WORK', 'Settings and demo information', 'A prototype for trying a workflow, not a production accounting application.') + `<section class="card"><h2>About this demo</h2><p>Plain local HTML, CSS and JavaScript. No Python, installation, login, analytics or network calls. The prototype interface is currently in English; English and Russian guides are included.</p><p>Only fictional state is saved in browser storage. Do not enter real personal or business data. Stored data is not encrypted, synced or backed up.</p><p>The original visual is synthetic. No OCR, real folder access, accounting posting, bank connection, payment initiation or ELSTER submission is implemented here.</p><details><summary>Saving and recovery</summary><p>“Saved” appears only after browser storage accepts the write. If storage fails, keep this page open and copy your edits. If another tab changes the demo, your edits stay here and overwrite is blocked. A reset explicitly replaces this demo’s saved state.</p></details><div class="actions">${button('Reset fictional demo data', 'reset')}</div></section>`;
  }
  function render() {
    route = location.hash.slice(1) || 'home';
    let renderScreen = home;
    switch (route) {
      case 'onboard': renderScreen = onboarding; break;
      case 'documents': renderScreen = documents; break;
      case 'review': renderScreen = invoice; break;
      case 'month': renderScreen = month; break;
      case 'payment': renderScreen = payment; break;
      case 'taxes': renderScreen = taxes; break;
      case 'accounts': renderScreen = accounts; break;
      case 'settings': renderScreen = settings; break;
      default: route = 'home';
    }
    if (!['home', 'settings'].includes(route)) { state.resume = route; save(); }
    document.querySelectorAll('[data-nav]').forEach(a => {
      const active = a.dataset.nav === ({ review: 'documents', onboard: 'documents', payment: 'month' }[route] || route);
      if (active) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    main.innerHTML = renderScreen();
    main.focus({ preventScroll: true });
    window.scrollTo(0, 0);
    document.title = `${main.querySelector('h1')?.textContent || 'Business workspace'} · Interactive demo`;
  }
  function help(kind, service = '') {
    const context = kind === 'connection-help' ? `I already use ${service}. Identify the exact product, edition, available plugin/API/browser/computer tools and permissions before proposing a connection. Start with read-only discovery; do not assume access or request credentials in chat.`
      : kind === 'service-help' ? 'Help me compare banking, insurance or payment services. First ask about my business needs and existing services, then research current primary sources and include keeping my current service. Do not purchase or contact providers.'
      : route === 'review' ? `In this fictional invoice demo, page 1 says “Gesamtbetrag 119,80 EUR”. My proposed amount is ${state.invoice.amount} EUR; category ${state.invoice.category || 'unresolved'}. Help me check the source fields and identify missing accounting facts. No accounting entry is recorded. Note: ${state.invoice.note}`
      : route === 'payment' ? `In this fictional demo, payment DEMO-PAY-010 is −12.00 EUR to Paket Beispiel on 10 October 2026, reference Parcel DEMO-010. A sample receipt has the same amount, date and reference. Help me check whether to link it. This is not an accounting posting. Note: ${state.payment.note}`
      : `Help me with ${route === 'taxes' ? 'tax preparation and authority correspondence' : route === 'onboard' && goal === 'start' ? 'starting a business in Germany' : 'organizing existing business records'}. Ask only for facts relevant to the next step. Keep self-managed accounting primary. Distinguish preparation, review, authorization, submission and response. This is a fictional prototype, not a real workspace.`;
    document.querySelector('#help-explanation').textContent = 'The request below carries the current task context. Review it before copying. No assistant is connected to this page.';
    document.querySelector('#help-prompt').value = context;
    document.querySelector('#copy-status').textContent = '';
    document.querySelector('#help-dialog').showModal();
  }
  document.addEventListener('input', e => {
    if (e.target.dataset.field) {
      state.invoice[e.target.dataset.field] = e.target.value;
      state.invoice.reviewed = false;
      const reviewBadge = main.querySelector('.card .badge');
      if (reviewBadge) { reviewBadge.textContent = 'Needs review'; reviewBadge.className = 'badge'; }
      const result = document.querySelector('#review-result');
      if (result) result.textContent = 'Draft changed. Review the document again when ready.';
      save();
    }
    if (e.target.id === 'payment-note') { state.payment.note = e.target.value; save(); }
    if (e.target.id === 'search') { search = e.target.value; document.querySelector('#document-list').innerHTML = documentList(); }
  });
  document.addEventListener('change', e => {
    if (e.target.name === 'goal') goal = e.target.value;
    if (e.target.id === 'source') source = e.target.value;
    if (e.target.name === 'import') e.target.checked ? selected.add(e.target.value) : selected.delete(e.target.value);
    if (e.target.name === 'goal' || e.target.id === 'source' || e.target.name === 'import') save();
    if (e.target.id === 'filter') { filter = e.target.value; document.querySelector('#document-list').innerHTML = documentList(); }
  });
  document.addEventListener('click', async e => {
    const target = e.target.closest('[data-action]');
    if (!target) return;
    const action = target.dataset.action;
    if (!target.closest('dialog')) helpOpener = target;
    if (['home', 'documents', 'review', 'month', 'payment', 'taxes', 'accounts', 'settings'].includes(action)) return go(action);
    if (action === 'onboard' || action === 'start-business') {
      if (['documents', 'review', 'month', 'payment', 'taxes', 'accounts'].includes(state.resume)) state.onboarding.previousTask = state.resume;
      step = 0; goal = action === 'start-business' ? 'start' : 'organize'; formError = ''; return go('onboard');
    }
    if (action === 'resume') return go(resume());
    if (action === 'onboard-next') {
      formError = '';
      if (step === 0 && goal === 'continue') return go(state.onboarding.previousTask);
      if (step === 0 && goal === 'start') return help('help');
      if (step === 0 && source === 'service') return go('accounts');
      if (step === 1 && !selected.size) formError = 'Choose at least one example file, or go back to cancel.';
      else step++;
      return render();
    }
    if (action === 'onboard-back') { step = Math.max(0, step - 1); formError = ''; return render(); }
    if (action === 'cancel-import') { step = 0; goal = 'organize'; source = 'folder'; selected = new Set(['invoice', 'receipt', 'statement']); state.resume = state.onboarding.previousTask; save(); return go('home'); }
    if (action === 'import') {
      state.imported = [...new Set([...state.imported, ...selected])];
      // Keep the store's state object stable; route persistence handles the write.
      state.resume = 'documents';
      step = 0; goal = 'organize'; source = 'folder'; selected = new Set(['invoice', 'receipt', 'statement']);
      save();
      return go('documents');
    }
    if (action === 'save-draft') {
      const ok = save();
      document.querySelector('#review-result').textContent = ok ? 'Draft saved. Document review and accounting treatment remain separate.' : 'Your draft is still here, but was not saved. See the warning above.';
    }
    if (action === 'review-complete') {
      const errors = [];
      if (DemoState.money(state.invoice.amount) !== 11980) errors.push('<a href="#invoice-amount">Check the total: the original example shows 119.80 EUR.</a>');
      if (state.invoice.date !== '2026-10-08') errors.push('<a href="#invoice-date">Check the date: the original example shows 8 October 2026.</a>');
      const error = document.querySelector('#review-error');
      error.hidden = !errors.length;
      if (errors.length) { error.innerHTML = `<strong>Check the highlighted information</strong><ul>${errors.map(x => `<li>${x}</li>`).join('')}</ul><p>You can save a draft and leave this unresolved.</p>`; error.focus(); return; }
      state.invoice.reviewed = true;
      const ok = save();
      if (!ok) state.invoice.reviewed = false;
      render();
      document.querySelector('#review-result').textContent = ok ? `Document reviewed and saved. ${state.invoice.category ? 'Category is a proposal, not confirmed accounting treatment.' : 'Category remains unresolved.'} No accounting entry recorded.` : 'Review was not saved. Your draft remains here.';
    }
    if (action === 'match-payment') {
      const previous = state.payment.matched;
      state.payment.matched = !previous;
      if (!save()) state.payment.matched = previous;
      render();
      document.querySelector('#payment-result').textContent = state.payment.matched ? 'Receipt linked in this demo. No accounting entry recorded.' : 'Payment remains open.';
    }
    if (action === 'defer-payment') {
      if (save()) go('home');
    }
    if (action.startsWith('inspect-')) {
      if (state.imported.includes('statement')) go('payment');
      else { help('help'); document.querySelector('#help-explanation').textContent = 'Example parcel receipt: Paket Beispiel, 10 October 2026, 12.00 EUR, reference Parcel DEMO-010. Import the example bank export to investigate a payment match.'; }
    }
    if (['help', 'connection-help', 'service-help'].includes(action)) help(action, target.dataset.service);
    if (action === 'close-help') document.querySelector('#help-dialog').close();
    if (action === 'copy-help') {
      try { await navigator.clipboard.writeText(document.querySelector('#help-prompt').value); document.querySelector('#copy-status').textContent = 'Copied. Nothing has been sent.'; }
      catch (_) { document.querySelector('#help-prompt').select(); document.querySelector('#copy-status').textContent = 'Automatic copy is unavailable. Copy the selected text using your browser or keyboard.'; }
    }
    if (action === 'reset') document.querySelector('#reset-dialog').showModal();
    if (action === 'cancel-reset') document.querySelector('#reset-dialog').close();
    if (action === 'confirm-reset') {
      const result = store.reset();
      document.querySelector('#reset-dialog').close();
      if (result.ok) { step = 0; goal = 'organize'; source = 'folder'; search = ''; filter = 'all'; selected = new Set(['invoice', 'receipt', 'statement']); save(); go('home'); }
      else { document.querySelector('#storage-warning').hidden = false; document.querySelector('#storage-warning').textContent = result.message; }
    }
  });
  document.querySelector('#help-dialog').addEventListener('close', () => {
    if (helpOpener?.isConnected) helpOpener.focus();
  });
  document.querySelector('.skip').addEventListener('click', e => {
    e.preventDefault();
    main.focus();
  });
  // Error-summary links focus fields without changing the application route.
  main.addEventListener('click', e => {
    const link = e.target.closest('a[href^="#invoice-"]');
    if (link) { e.preventDefault(); document.querySelector(link.getAttribute('href')).focus(); }
  });
  window.addEventListener('hashchange', render);
  if (store.warning) { document.querySelector('#storage-warning').hidden = false; document.querySelector('#storage-warning').textContent = store.warning; }
  render();
})();
