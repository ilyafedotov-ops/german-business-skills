// Shared only by developer checks; not part of the application runtime.
async function stopChild(child, timeoutMs = 5000) {
  if (!child.pid || child.exitCode !== null || child.signalCode !== null) return;
  let closed;
  const finished = new Promise(resolve => { closed = () => resolve(true); });
  child.once('close', closed);
  async function wait() {
    let timer;
    try {
      return await Promise.race([finished, new Promise(resolve => { timer = setTimeout(() => resolve(false), timeoutMs); })]);
    } finally { clearTimeout(timer); }
  }
  try {
    child.kill();
    if (await wait()) return;
    child.kill('SIGKILL');
    if (!await wait()) throw new Error('GUI server did not stop; its temporary workspace was retained.');
  } finally { child.removeListener('close', closed); }
}
module.exports = { stopChild };
