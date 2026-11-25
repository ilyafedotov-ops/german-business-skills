// Deterministic frame engine: window.__setup(config) once, then await window.__render(t) per frame.
(() => {
  const ease = x => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);
  const easeInOut = x => { x = Math.min(1, Math.max(0, x)); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  let cfg, stage, capEl, capText;
  const scenes = [];

  function cueTime(sc, el) {
    const span = sc.audioDur || sc.dur * 0.8;
    if (el.dataset.at) return sc.lead + parseFloat(el.dataset.at) * span;
    const cue = el.dataset.cue;
    const i = sc.text.toLowerCase().indexOf(cue.toLowerCase());
    if (i < 0) { console.warn('cue not found', sc.id, cue); return 0; }
    // Snap to the caption line that contains the cue, staggered by position inside that line,
    // so muted viewers see each element appear together with the words they are reading.
    let pos = 0;
    for (const c of sc.captions || []) {
      const end = pos + c.text.length;
      if (i < end + 1) return Math.max(0, sc.lead + c.s - 0.1 + ((i - pos) / Math.max(1, c.text.length)) * (c.e - c.s) * 0.6);
      pos = end + 1;
    }
    return Math.max(0, sc.lead + (i / sc.text.length) * sc.audioDur - 0.45);
  }

  window.__setup = (config) => {
    cfg = config;
    document.body.style.margin = '0';
    // Carousel-only furniture has no meaning in a video.
    document.querySelectorAll('.swipe, .pageno').forEach(n => { n.style.visibility = 'hidden'; });
    stage = document.createElement('div');
    Object.assign(stage.style, { position: 'fixed', left: 0, top: 0, width: cfg.width + 'px', height: cfg.height + 'px', overflow: 'hidden', background: cfg.stageBg || 'var(--bg)', zIndex: 10 });
    document.body.appendChild(stage);

    for (const sc of cfg.scenes) {
      const src = document.getElementById(sc.el);
      const el = sc.clone ? src.cloneNode(true) : src;
      // Portrait: present the 1080x1350 slide as a scaled card above a caption band.
      const holder = document.createElement('div');
      Object.assign(holder.style, { position: 'absolute', left: 0, top: 0, width: cfg.width + 'px', height: cfg.height + 'px', opacity: 0, visibility: 'hidden' });
      const card = document.createElement('div');
      if (cfg.card) {
        Object.assign(card.style, { position: 'absolute', left: cfg.card.left + 'px', top: cfg.card.top + 'px', width: cfg.card.w + 'px', height: cfg.card.h + 'px', overflow: 'hidden', borderRadius: cfg.card.radius + 'px', boxShadow: '0 24px 70px rgba(23,48,42,.18)' });
        const inner = document.createElement('div');
        Object.assign(inner.style, { position: 'absolute', left: 0, top: 0, width: cfg.card.srcW + 'px', height: cfg.card.srcH + 'px', transformOrigin: '0 0', transform: `scale(${cfg.card.w / cfg.card.srcW})` });
        el.style.position = 'relative'; el.style.pageBreakAfter = 'auto';
        inner.appendChild(el); card.appendChild(inner);
      } else {
        Object.assign(card.style, { position: 'absolute', inset: 0 });
        card.appendChild(el);
      }
      holder.appendChild(card);
      stage.appendChild(holder);
      const items = [...el.querySelectorAll('[data-cue],[data-at]')].map(n => ({ n, t: cueTime(sc, n) }));
      // A printer only moves down: within a receipt, a line never appears before the line above it.
      for (let i = 1; i < items.length; i++) {
        const a = items[i - 1], b = items[i];
        if (b.n.dataset.fx === 'print' && a.n.dataset.fx === 'print' && b.n.closest('.receipt') === a.n.closest('.receipt')) b.t = Math.max(b.t, a.t + 0.06);
      }
      const intro = sc.noIntro ? [] : [...el.querySelectorAll('.top, .bar, h1, h2, .eyebrow, .lead')].filter(n => !n.closest('[data-cue],[data-at]') && !n.matches('[data-cue],[data-at]')).map((n, k) => ({ n, t: 0.05 + k * 0.12 }));
      const spot = [...el.querySelectorAll('[data-spotlight] > [data-cue]')].map(n => ({ n, t: cueTime(sc, n) })).sort((a, b) => a.t - b.t);
      const img = el.querySelector('.demo-img');
      if (sc.step) el.querySelectorAll('.dstep').forEach(d => { const s = +d.dataset.step; d.classList.toggle('on', s === sc.step); d.classList.toggle('done', s < sc.step); });
      scenes.push({ ...sc, holder, card, el, items: [...intro, ...items], spot, img, chromeEl: el.querySelector('.browser .chrome span'), lastSrc: null });
    }

    capEl = document.createElement('div');
    Object.assign(capEl.style, { position: 'absolute', left: cfg.caption.left + 'px', width: cfg.caption.w + 'px', top: cfg.caption.top + 'px', height: cfg.caption.h + 'px', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 20, pointerEvents: 'none' });
    capText = document.createElement('div');
    Object.assign(capText.style, { fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: cfg.caption.size + 'px', lineHeight: 1.28, color: '#fff', background: 'rgba(23,48,42,.92)', padding: cfg.caption.pad, borderRadius: '18px', textAlign: 'center', maxWidth: cfg.caption.w + 'px', letterSpacing: '-0.005em' }, cfg.caption.css || {});
    capEl.appendChild(capText);
    stage.appendChild(capEl);
    return scenes.map(s => ({ id: s.id, items: s.items.length }));
  };

  function demoSource(sc, local) {
    // Each segment shows one still screenshot; its progress u runs 0..1 over the segment.
    let acc = 0;
    for (const seg of sc.demo.segments) {
      if (local < acc + seg.dur || seg === sc.demo.segments.at(-1)) {
        const t = Math.max(0, local - acc);
        return { seg, t, u: Math.min(1, t / Math.max(0.001, seg.dur)) };
      }
      acc += seg.dur;
    }
  }

  function focusAt(keys, srcT) {
    // Keyframes {at, x, y, w}: the visible window in screenshot pixels, eased between keys.
    if (srcT <= keys[0].at) return keys[0];
    for (let i = 1; i < keys.length; i++) {
      if (srcT <= keys[i].at) {
        const a = keys[i - 1], b = keys[i];
        const k = easeInOut((srcT - a.at) / Math.max(0.001, b.at - a.at));
        return { x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, w: a.w + (b.w - a.w) * k };
      }
    }
    return keys.at(-1);
  }

  window.__render = async (t) => {
    let active = null;
    for (const sc of scenes) {
      const local = t - sc.start;
      const on = local >= 0 && local < sc.dur;
      if (!on) { if (sc.holder.style.visibility !== 'hidden') { sc.holder.style.visibility = 'hidden'; sc.holder.style.opacity = 0; } continue; }
      active = sc;
      const fin = sc.fadeIn ?? 0.35, fout = sc.fadeOut ?? 0.3;
      const op = Math.min(1, fin ? local / fin : 1) * Math.min(1, fout ? (sc.dur - local) / fout : 1);
      sc.holder.style.visibility = 'visible';
      sc.holder.style.opacity = op.toFixed(3);
      const z = 1 + (sc.zoom ?? 0.018) * (local / sc.dur);
      sc.card.style.transform = `scale(${z.toFixed(5)})`;
      sc.card.style.transformOrigin = '50% 45%';
      for (const it of sc.items) {
        const print = it.n.dataset.fx === 'print';
        const p = ease((local - it.t) / (print ? 0.16 : 0.5));
        it.n.style.opacity = p.toFixed(3);
        if (!print) it.n.style.transform = p >= 1 ? '' : `translateY(${(1 - p) * 26}px)`;
      }
      sc.spot.forEach((s, i) => {
        const next = sc.spot[i + 1];
        s.n.classList.toggle('spot', local >= s.t && (!next || local < next.t));
      });
      if (sc.demo && sc.img) {
        const { seg, t: segT, u } = demoSource(sc, local);
        const f = focusAt(seg.focus, u);
        if (sc.lastSrc !== seg.img) { sc.img.src = seg.img; sc.lastSrc = seg.img; await sc.img.decode().catch(() => {}); }
        const vw = sc.img.parentElement.clientWidth;
        const s = vw / f.w;
        sc.img.style.width = (seg.imgW * s) + 'px';
        sc.img.style.transform = `translate(${-f.x * s}px, ${-f.y * s}px)`;
        // A short fade on each cut, so screenshots do not snap into place.
        const i = sc.demo.segments.indexOf(seg), prev = sc.demo.segments[i - 1];
        sc.img.style.opacity = !prev || prev.img === seg.img ? 1 : ease(segT / 0.3).toFixed(3);
        if (seg.title && sc.titleEl) sc.titleEl.innerHTML = seg.title;
        if (seg.chrome && sc.chromeEl) sc.chromeEl.textContent = seg.chrome;
        if (seg.step) sc.el.querySelectorAll('.dstep').forEach(d => { const k = +d.dataset.step; d.classList.toggle('on', k === seg.step); d.classList.toggle('done', k < seg.step); });
      }
    }
    // Captions: scene-local audio time.
    let txt = '';
    if (active && active.captions) {
      const a = t - active.start - active.lead;
      const c = active.captions.find(c => a >= c.s && a < c.e);
      if (c) txt = c.text;
    }
    if (capText.textContent !== txt) capText.textContent = txt;
    capEl.style.opacity = txt ? 1 : 0;
    return !!active;
  };

  window.__attachTitle = (id, selector) => { const sc = scenes.find(s => s.id === id); sc.titleEl = sc.el.querySelector(selector); };
})();
