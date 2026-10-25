/* Standalone demo state: no real documents, accounts, or accounting records. */
(function (root) {
  'use strict';
  const KEY = 'de-business-kit-synthetic-demo-v1';
  const fresh = () => ({ version: 1, imported: [], resume: 'home',
    onboarding: { step: 0, selected: ['invoice', 'receipt', 'statement'], goal: 'organize', source: 'folder', previousTask: 'documents' },
    invoice: { amount: '119.00', date: '2026-10-08', category: '', note: '', reviewed: false },
    payment: { matched: false, note: '' } });
  function money(value) {
    if (typeof value !== 'string' || !/^\d{1,9}([.,]\d{1,2})?$/.test(value.trim())) return null;
    const [whole, fraction = ''] = value.trim().split(/[.,]/);
    return Number(whole) * 100 + Number(fraction.padEnd(2, '0'));
  }
  function valid(s) {
    return s && s.version === 1 && Array.isArray(s.imported) && s.imported.every(x => ['invoice', 'receipt', 'statement'].includes(x))
      && ['home', 'documents', 'review', 'month', 'payment', 'taxes', 'accounts', 'onboard', 'settings'].includes(s.resume)
      && s.onboarding && [0, 1, 2].includes(s.onboarding.step)
      && Array.isArray(s.onboarding.selected) && s.onboarding.selected.every(x => ['invoice', 'receipt', 'statement'].includes(x))
      && ['organize', 'start', 'continue'].includes(s.onboarding.goal) && ['folder', 'service'].includes(s.onboarding.source)
      && ['documents', 'review', 'month', 'payment', 'taxes', 'accounts'].includes(s.onboarding.previousTask)
      && s.invoice && ['amount', 'date', 'category', 'note'].every(k => typeof s.invoice[k] === 'string')
      && typeof s.invoice.reviewed === 'boolean' && s.payment && typeof s.payment.note === 'string' && typeof s.payment.matched === 'boolean';
  }
  function openStore(storage) {
    let expected = null, blocked = '', state = fresh();
    try {
      expected = storage.getItem(KEY);
      if (expected !== null) {
        const parsed = JSON.parse(expected);
        if (!valid(parsed)) throw new Error('Invalid demo state');
        state = parsed;
      }
    } catch (_) { blocked = 'Saved demo data could not be read. Your previous data has not been replaced. Reset the demo in Settings to start again.'; }
    return {
      state, warning: blocked,
      save() {
        if (blocked) return { ok: false, message: blocked };
        try {
          if (storage.getItem(KEY) !== expected) return { ok: false, message: 'Another tab changed this demo. Your edits remain here, but are not saved. Copy your changes before reloading.' };
          const next = JSON.stringify(state);
          storage.setItem(KEY, next);
          expected = next;
          return { ok: true, message: 'Saved on this browser' };
        } catch (_) { return { ok: false, message: 'Not saved. Browser storage is unavailable or full. Keep this page open and copy your changes before leaving.' }; }
      },
      reset() {
        try {
          const next = fresh();
          storage.setItem(KEY, JSON.stringify(next));
          expected = JSON.stringify(next);
          Object.keys(state).forEach(k => delete state[k]);
          Object.assign(state, next);
          blocked = '';
          return { ok: true };
        } catch (_) { return { ok: false, message: 'The demo could not be reset. Your current work is still here.' }; }
      }
    };
  }
  const api = { fresh, money, openStore };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.DemoState = api;
})(typeof window === 'undefined' ? globalThis : window);
