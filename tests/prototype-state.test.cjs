const { test } = require('node:test');
const assert = require('node:assert/strict');
const { fresh, money, openStore } = require('../prototype/state.js');

const memory = () => {
  const values = new Map();
  return { getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value) };
};

test('invoice amounts accept decimal commas without rounding ambiguous values', () => {
  assert.equal(money('119,80'), 11980);
  assert.equal(money('119.80'), 11980);
  for (const value of ['', '1,234.56', '119.801', '-1', 'Infinity', '1e2']) {
    assert.equal(money(value), null);
  }
});

test('a corrected draft and its resume location survive reopening', () => {
  const storage = memory();
  const first = openStore(storage);
  first.state.invoice.amount = '119,80';
  first.state.invoice.category = '';
  first.state.resume = 'review';
  assert.equal(first.save().ok, true);
  const second = openStore(storage);
  assert.equal(second.state.invoice.amount, '119,80');
  assert.equal(second.state.invoice.category, '');
  assert.equal(second.state.invoice.reviewed, false);
  assert.equal(second.state.resume, 'review');
});

test('storage failure preserves an edited draft without claiming it was saved', () => {
  const store = openStore({ getItem: () => null, setItem: () => { throw new Error('quota'); } });
  store.state.invoice.amount = '119.80';
  assert.equal(store.save().ok, false);
  assert.equal(store.state.invoice.amount, '119.80');
});

test('another tab cannot silently overwrite newer work', () => {
  const storage = memory();
  const first = openStore(storage);
  const second = openStore(storage);
  first.state.invoice.amount = '119.80';
  assert.equal(first.save().ok, true);
  second.state.invoice.amount = '200';
  assert.equal(second.save().ok, false);
  assert.equal(openStore(storage).state.invoice.amount, '119.80');
  assert.equal(second.state.invoice.amount, '200');
});

test('damaged or foreign demo state is not overwritten automatically', () => {
  for (const raw of ['{bad', JSON.stringify({ ...fresh(), version: 42 }), JSON.stringify({ ...fresh(), invoice: null })]) {
    let written = false;
    const store = openStore({ getItem: () => raw, setItem: () => { written = true; } });
    assert.ok(store.warning);
    assert.equal(store.save().ok, false);
    assert.equal(written, false);
  }
});
