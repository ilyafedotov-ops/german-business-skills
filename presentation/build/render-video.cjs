// Renders the LinkedIn (4:5) or YouTube (16:9) video from HTML scenes + narration.
// node render-video.cjs linkedin|youtube [--stills 1.5,12,30] [--fps 30]
const path = require('node:path');
const fs = require('node:fs');
const fsp = require('node:fs/promises');
const { spawn, execFileSync } = require('node:child_process');
const { pathToFileURL } = require('node:url');
const playwright = require('playwright');

const build = __dirname;
const root = path.resolve(build, '..');
const audioDir = path.join(root, 'audio');
const outDir = path.join(root, 'video');
// Real app screenshots from the guided setup page; paths are relative to the scene HTML in build/.
const SHOTS = '../../installer/images/';
const shot = (file, extra) => ({ img: SHOTS + file, imgW: 1400, ...extra });
const format = process.argv[2];
const argv = process.argv.slice(3);
const opt = k => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : null; };
const FPS = +(opt('--fps') || 30);
const stills = opt('--stills');

const dur = f => parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());

// Narration text per segment, parsed from the scripts file so captions match what was spoken.
const scriptMd = fs.readFileSync(path.join(root, 'post/scripts.md'), 'utf8');
const texts = {};
for (const m of scriptMd.matchAll(/\*\*([LY]q?\d+[a-d]?) · [^*]+\*\*\n([^\n]+)/g)) texts[m[1]] = m[2].trim();

// Break captions at punctuation, else before a connecting word, never leaving a dangling "into a".
const JOIN = new Set(['and', 'or', 'but', 'so', 'into', 'in', 'to', 'for', 'with', 'that', 'until', 'from', 'of', 'on', 'then', 'instead', 'which', 'while', 'as', 'without', 'each', 'including', 'ready', 'often', 'when', 'where', 'because', 'if', 'asks', 'prepares', 'saves']);
function chunkSentence(sentence, max) {
  if (sentence.length <= max * 1.2) return [sentence];
  const words = sentence.split(/\s+/);
  const out = []; let cur = [];
  const len = a => a.join(' ').length;
  for (const w of words) {
    if (cur.length && len([...cur, w]) > max) {
      let k = -1;
      for (let j = cur.length - 1; j >= 1; j--) if (/[,:;]$/.test(cur[j - 1]) && len(cur.slice(0, j)) >= max * 0.4) { k = j; break; }
      if (k < 0) for (let j = cur.length - 1; j >= 1; j--) if (JOIN.has(cur[j].toLowerCase()) && len(cur.slice(0, j)) >= max * 0.4) { k = j; break; }
      if (k < 0) k = cur.length;
      out.push(cur.slice(0, k).join(' ')); cur = cur.slice(k);
    }
    cur.push(w);
  }
  if (cur.length) {
    // Fold a tiny remainder back into the previous line rather than flashing it alone.
    if (out.length && len(cur) < 14 && out.at(-1).length + len(cur) + 1 <= max * 1.25) out[out.length - 1] += ' ' + cur.join(' ');
    else out.push(cur.join(' '));
  }
  return out;
}
function chunk(text, max) {
  return text.split(/(?<=[.?!:])\s+(?=[A-Z"“])/).flatMap(s => chunkSentence(s, max));
}
function captions(text, audioDur, max) {
  const parts = chunk(text, max);
  const weight = p => p.length + (/[.?!]$/.test(p) ? 9 : /[,:;]$/.test(p) ? 4 : 0);
  const total = parts.reduce((a, p) => a + weight(p), 0);
  let t = 0;
  return parts.map(p => { const d = weight(p) / total * audioDur; const c = { text: p, s: t, e: t + d }; t += d; return c; });
}

// Captions print on a strip of receipt paper in the same face as the slides.
const CAPTION_CSS = { fontFamily: "'Martian Mono', monospace", fontVariationSettings: "'wdth' 87.5", fontWeight: 650, color: '#141414',
  background: '#f6f6f1', borderRadius: '2px', letterSpacing: '0', lineHeight: 1.36, boxShadow: '0 14px 28px rgba(8,10,50,.45)' };

function timeline() {
  const W = format === 'linkedin' ? 1080 : 1920, H = format === 'linkedin' ? 1350 : 1080;
  const lead = 0.4, tail = 0.6;
  let scenes;
  if (format === 'linkedin') {
    scenes = [
      { id: 'L1', el: 'r02', fadeIn: 0 }, { id: 'L2', el: 'r03' }, { id: 'L3', el: 'r04' }, { id: 'L3b', el: 'r05', tail: 1.2 }, { id: 'L4', el: 'r08' },
      // Viewport 916x740: a 1400-px screenshot shows 1131 px of height at full width.
      { id: 'L5', el: 'rdemo', zoom: 0, demo: { segments: [
        shot('claude-first-en.jpg', { dur: 3.0, title: 'Ask in your own words.', chrome: 'Claude app',
          focus: [{ at: 0, x: 0, y: 0, w: 1400 }, { at: 1, x: 0, y: 0, w: 1400 }] }),
        shot('claude-first-en.jpg', { dur: 3.0, title: 'Get one small first step.', chrome: 'Claude app',
          focus: [{ at: 0, x: 0, y: 0, w: 1400 }, { at: 1, x: 0, y: 168, w: 1400 }] }),
        shot('codex-skills-en.jpg', { dur: 2.6, title: 'All seven skills, ready.', chrome: 'Codex',
          focus: [{ at: 0, x: 0, y: -48, w: 1400 }, { at: 1, x: 0, y: -48, w: 1400 }] }),
        shot('codex-first-de.jpg', { dur: 99, title: 'In German, too.', chrome: 'Codex',
          focus: [{ at: 0, x: 400, y: 70, w: 1000 }, { at: 0.75, x: 0, y: -158, w: 1400 }, { at: 1, x: 0, y: -158, w: 1400 }] }) ] } },
      { id: 'L6', el: 'r10' }, { id: 'L7', el: 'r12', tail: 3.0, fadeOut: 0.6 },
    ];
  } else {
    // Viewport 1190x744: a 1400-px screenshot shows 875 px of height at full width.
    const d6 = (id, step, seg, extra = {}) => ({ id, el: 'y6', clone: true, step, zoom: 0, fadeIn: 0, fadeOut: 0, noIntro: true, demo: { segments: [{ dur: 99, ...seg }] }, ...extra });
    scenes = [
      { id: 'Y0', el: 'y0', fixed: 3.6, fadeIn: 0.6 },
      { id: 'Y1', el: 'y1' }, { id: 'Y2', el: 'y2' }, { id: 'Y3', el: 'y3' }, { id: 'Y4', el: 'y4' }, { id: 'Y5', el: 'y5', fadeOut: 0.3 },
      d6('Y6a', 1, shot('codex-skills-en.jpg', { chrome: 'Codex', focus: [{ at: 0, x: 0, y: 0, w: 1400 }, { at: 0.2, x: 0, y: 0, w: 1400 }, { at: 1, x: 0, y: 159, w: 1400 }] }), { fadeIn: 0.35 }),
      d6('Y6b', 2, shot('claude-first-en.jpg', { chrome: 'Claude app', focus: [{ at: 0, x: 0, y: 0, w: 1400 }, { at: 0.3, x: 0, y: 0, w: 1400 }, { at: 1, x: 0, y: 120, w: 1400 }] })),
      d6('Y6c', 3, shot('claude-first-en.jpg', { chrome: 'Claude app', focus: [{ at: 0, x: 0, y: 290, w: 1400 }, { at: 1, x: 0, y: 424, w: 1400 }] }), { tail: 1.2 }),
      d6('Y6d', 4, shot('codex-first-de.jpg', { chrome: 'Codex', focus: [{ at: 0, x: 400, y: 70, w: 1000 }, { at: 0.7, x: 0, y: -30, w: 1400 }, { at: 1, x: 0, y: -30, w: 1400 }] }), { tail: 1.2, fadeOut: 0.3 }),
      { id: 'Yq1', el: 'yq1', fadeIn: 0.35, tail: 1.4 }, { id: 'Yq2', el: 'yq2', tail: 1.4 }, { id: 'Yq3', el: 'yq3', tail: 1.6 },
      { id: 'Y7', el: 'y7', fadeIn: 0.35 }, { id: 'Y8', el: 'y8' }, { id: 'Y9', el: 'y9', tail: 1.4 },
      { id: 'Y10', el: 'y10', fixed: 5.5, fadeOut: 1.0 },
    ];
  }
  let t = 0;
  for (const sc of scenes) {
    const a = path.join(audioDir, `${sc.id}.mp3`);
    sc.text = texts[sc.id] || '';
    sc.audioDur = sc.fixed ? 0 : dur(a);
    sc.audio = sc.fixed ? null : a;
    sc.lead = sc.fixed ? 0 : (sc.lead ?? lead);
    sc.dur = sc.fixed || sc.lead + sc.audioDur + (sc.tail ?? tail);
    sc.start = t; t += sc.dur;
    sc.captions = sc.text ? captions(sc.text, sc.audioDur, format === 'linkedin' ? 46 : 64) : [];
    if (sc.demo) {
      // Distribute a "dur: 99" segment over the remaining scene time.
      const fixedSum = sc.demo.segments.filter(s => s.dur !== 99).reduce((a, s) => a + s.dur, 0);
      for (const s of sc.demo.segments) if (s.dur === 99) s.dur = sc.dur - fixedSum;
    }
  }
  const caption = format === 'linkedin'
    ? { left: 40, w: 1000, top: 1196, h: 140, size: 34, pad: '14px 26px', css: CAPTION_CSS }
    : { left: 160, w: 1600, top: 936, h: 116, size: 34, pad: '12px 30px', css: CAPTION_CSS };
  const card = format === 'linkedin' ? { left: 76, top: 24, w: 928, h: 1160, srcW: 1080, srcH: 1350, radius: 22 } : null;
  return { W, H, total: t, scenes, caption, card };
}

(async () => {
  const tl = timeline();
  console.log(`${format}: ${tl.scenes.length} scenes, ${tl.total.toFixed(2)} s`);
  for (const s of tl.scenes) console.log(`  ${s.id.padEnd(4)} ${s.start.toFixed(2).padStart(7)} +${s.dur.toFixed(2)}  captions:${s.captions.length}`);
  if (process.env.CAPS) { for (const s of tl.scenes) for (const c of s.captions) console.log(`    ${s.id} | ${c.text}`); if (process.env.CAPS === 'only') return; }

  const browser = await playwright.chromium.launch();
  const page = await browser.newPage({ viewport: { width: tl.W, height: tl.H }, deviceScaleFactor: 1 });
  page.on('console', m => { if (m.type() === 'warning' || m.type() === 'error') console.log('page:', m.text()); });
  const html = format === 'linkedin' ? 'receipt-en.html' : 'scenes-receipt-yt.html';
  await page.goto(pathToFileURL(path.join(build, html)).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => window.__fit && window.__fit());
  await page.addScriptTag({ path: path.join(build, 'engine.js') });
  const config = {
    width: tl.W, height: tl.H, caption: tl.caption, card: tl.card,
    stageBg: format === 'linkedin' ? '#14174a' : 'var(--carbon)',
    scenes: tl.scenes.map(({ id, el, clone, step, start, dur, lead, audioDur, text, captions, demo, zoom, fadeIn, fadeOut, noIntro }) => ({ id, el, clone, step, start, dur, lead, audioDur, text, captions, demo, zoom, fadeIn, fadeOut, noIntro })),
  };
  await page.evaluate(c => window.__setup(c), config);
  if (format === 'linkedin') await page.evaluate(() => window.__attachTitle('L5', '.demo-title'));
  await fsp.mkdir(outDir, { recursive: true });

  if (stills) {
    const dir = path.join(outDir, `stills-${format}`);
    await fsp.mkdir(dir, { recursive: true });
    for (const s of stills.split(',').map(Number)) {
      await page.evaluate(t => window.__render(t), s);
      await page.screenshot({ path: path.join(dir, `t${String(s).padStart(6, '0')}.png`) });
    }
    await browser.close();
    console.log('stills written to', dir);
    return;
  }

  const silent = path.join(outDir, `${format}-silent.mp4`);
  const t0 = Date.now();
  if (!(argv.includes('--mux-only') && fs.existsSync(silent))) {
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(FPS), silent], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.ceil(tl.total * FPS);
    for (let i = 0; i < n; i++) {
      await page.evaluate(t => window.__render(t), i / FPS);
      const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % (FPS * 10) === 0) console.log(`frame ${i}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
    }
    ff.stdin.end();
    await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
  }
  await browser.close();

  // Narration placed at each scene's lead, music ducked under the voice.
  // Input 0 is the silent video, input 1 the music, inputs 2.. the narration clips.
  const voiced = tl.scenes.filter(s => s.audio);
  const inputs = ['-i', path.join(audioDir, 'music.mp3'), ...voiced.flatMap(s => ['-i', s.audio])];
  const T = tl.total.toFixed(3);
  const parts = voiced.map((s, k) => `[${k + 2}:a]aresample=44100,adelay=${Math.round((s.start + s.lead) * 1000)}:all=1[v${k}]`);
  const filter = [
    ...parts,
    `${voiced.map((_, k) => `[v${k}]`).join('')}amix=inputs=${voiced.length}:normalize=0:duration=longest,apad=whole_dur=${T},atrim=0:${T},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[voice]`,
    `[voice]asplit=2[vo][sc]`,
    `[1:a]aresample=44100,atrim=0:${T},asetpts=N/SR/TB,volume=0.30,afade=t=in:st=0:d=1.5,afade=t=out:st=${(tl.total - 3.5).toFixed(2)}:d=3.5[m]`,
    `[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=30:release=500[md]`,
    `[vo][md]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[out]`,
  ].join(';');
  const final = path.join(outDir, format === 'linkedin' ? 'german-business-kit-linkedin.mp4' : 'german-business-kit-youtube.mp4');
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', silent, ...inputs, '-filter_complex', filter, '-map', '0:v', '-map', '[out]',
    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', final], { stdio: 'inherit' });
  await fsp.rm(silent);
  // Caption sidecar for YouTube / LinkedIn upload.
  const srt = tl.scenes.flatMap(s => s.captions.map(c => ({ s: s.start + s.lead + c.s, e: s.start + s.lead + c.e, text: c.text })));
  const ts = x => { const ms = Math.round(x * 1000); const h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, sec = Math.floor(ms / 1000) % 60; return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')},${String(ms % 1000).padStart(3, '0')}`; };
  fs.writeFileSync(final.replace(/\.mp4$/, '.srt'), srt.map((c, i) => `${i + 1}\n${ts(c.s)} --> ${ts(c.e)}\n${c.text}\n`).join('\n'));
  fs.writeFileSync(final.replace(/\.mp4$/, '.chapters.json'), JSON.stringify(tl.scenes.map(s => ({ id: s.id, start: +s.start.toFixed(2) })), null, 2));
  console.log('wrote', final, `in ${((Date.now() - t0) / 1000).toFixed(0)} s`);
})().catch(e => { console.error(e); process.exit(1); });
