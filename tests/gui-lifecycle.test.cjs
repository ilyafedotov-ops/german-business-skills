const test = require('node:test');
const assert = require('node:assert/strict');
const { spawn } = require('node:child_process');
const { once } = require('node:events');
const { stopChild } = require('./gui-lifecycle.cjs');

async function start(t, ignoreTermination = false) {
  const child = spawn(process.execPath, ['-e', `${ignoreTermination ? "process.on('SIGTERM',()=>{});" : ''}setInterval(()=>{},1000);process.stdout.write('ready');`], { stdio: ['ignore', 'pipe', 'pipe'] });
  t.after(async () => {
    if (child.exitCode === null && child.signalCode === null) {
      const closed = once(child, 'close');
      child.kill('SIGKILL');
      await closed;
    }
  });
  await once(child.stdout, 'data');
  return child;
}

test('workspace cleanup can start only after the server has exited', async t => {
  const child = await start(t);
  await stopChild(child, 100);
  assert.ok(child.exitCode !== null || child.signalCode !== null, 'Server still running at cleanup');
});

test('a server ignoring graceful termination is stopped within a bound', { skip: process.platform === 'win32' }, async t => {
  const child = await start(t, true);
  await stopChild(child, 100);
  assert.equal(child.signalCode, 'SIGKILL');
});

test('an already exited server needs no second close event', async t => {
  const child = await start(t);
  const closed = once(child, 'close');
  child.kill();
  await closed;
  await stopChild(child, 100);
});
