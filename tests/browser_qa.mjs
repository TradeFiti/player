#!/usr/bin/env node
/*
  Real-browser QA over the Chrome DevTools Protocol. No npm dependencies (Node 22+ for global WebSocket).

    python3 -m http.server 8765            # from the repo root, in another terminal
    node tests/browser_qa.mjs              # CHROME=/path/to/chrome BASE=http://127.0.0.1:8765 to override

  Checks every route at 1440, 1024, 768, 390 and 320 px:
    root overflow, console errors, failed or external requests, above-the-fold identity/photo/CTAs,
    motion-ready after init, 44px touch targets at <=920px, reveal content reachable after scrolling.
  Then interaction checks: switcher keyboard/Escape/focus return, anchor-preserving design links,
  gallery dialog focus trap and restore, reduced motion, JS disabled.
  Screenshots go to $OUT (default /tmp/jo-qa).
*/
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const BASE = process.env.BASE || 'http://127.0.0.1:8765';
const OUT = process.env.OUT || '/tmp/jo-qa';
const PORT = 9333;
const ROUTES = ['/', ...Array.from({ length: 10 }, (_, i) => `/${i + 1}/`), '/404.html'];
const VIEWPORTS = [
  { w: 1440, h: 900, mobile: false },
  { w: 1024, h: 768, mobile: false },
  { w: 768, h: 1024, mobile: true },
  { w: 390, h: 844, mobile: true },
  { w: 320, h: 640, mobile: true },
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

mkdirSync(OUT, { recursive: true });
const profileDir = mkdtempSync(join(tmpdir(), 'jo-qa-chrome-'));
const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profileDir}`,
  '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--mute-audio', 'about:blank',
], { stdio: 'ignore' });

async function waitForChrome() {
  for (let i = 0; i < 100; i++) {
    try { return await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); } catch { await sleep(100); }
  }
  throw new Error('Chrome did not start');
}

class Page {
  constructor(ws) {
    this.ws = ws; this.id = 0; this.pending = new Map(); this.listeners = [];
    ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        msg.error ? reject(new Error(msg.error.message)) : resolve(msg.result);
      } else if (msg.method) this.listeners.forEach((fn) => fn(msg));
    });
  }
  send(method, params = {}) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject }));
  }
  on(fn) { this.listeners.push(fn); }
  async eval(expr) {
    const r = await this.send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    return r.result.value;
  }
  async goto(url) {
    const loaded = new Promise((res) => {
      const fn = (m) => { if (m.method === 'Page.loadEventFired') { this.listeners = this.listeners.filter((f) => f !== fn); res(); } };
      this.on(fn);
    });
    await this.send('Page.navigate', { url });
    await Promise.race([loaded, sleep(8000)]);
    await sleep(350);
  }
  async key(key, code, keyCode, modifiers = 0) {
    await this.send('Input.dispatchKeyEvent', { type: 'keyDown', key, code, windowsVirtualKeyCode: keyCode, modifiers });
    await this.send('Input.dispatchKeyEvent', { type: 'keyUp', key, code, windowsVirtualKeyCode: keyCode, modifiers });
    await sleep(120);
  }
}

async function openPage() {
  const target = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: 'PUT' })).json();
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener('open', r, { once: true }));
  const page = new Page(ws);
  await page.send('Page.enable');
  await page.send('Runtime.enable');
  await page.send('Network.enable');
  await page.send('Log.enable');
  return page;
}

const failures = [];
const notes = [];
const fail = (where, msg) => failures.push(`${where}: ${msg}`);

const AUDIT = `(() => {
  const vw = innerWidth, vh = innerHeight;
  const doc = document.documentElement;
  const over = doc.scrollWidth - doc.clientWidth;
  const wide = over > 0 ? [...document.querySelectorAll('body *')].filter(el => {
    const r = el.getBoundingClientRect(); return r.width && r.right > vw + 1 && getComputedStyle(el).position !== 'fixed';
  }).slice(0, 5).map(el => el.tagName.toLowerCase() + '.' + [...el.classList].join('.') + ' r=' + Math.round(el.getBoundingClientRect().right)) : [];
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const inFold = el => vis(el) && el.getBoundingClientRect().top < vh && el.getBoundingClientRect().bottom > 0;
  const hero = document.getElementById('overview') || document.querySelector('main');
  const h1 = document.querySelector('h1');
  const img = hero && [...hero.querySelectorAll('img')].find(i => /joseph/i.test(i.alt || ''));
  const ctas = hero ? [...hero.querySelectorAll('a')].filter(a => /Watch Footage|Contact Representative/.test(a.textContent)) : [];
  let small = [];
  if (vw <= 920) {
    small = [...document.querySelectorAll('a, button, input:not([type=hidden]), textarea, select')].filter(el => {
      if (!vis(el) || el.closest('.hp, dialog:not([open]), .sr-only') || el.classList.contains('skip-link')) return false;
      const r = el.getBoundingClientRect(); return r.width < 43.5 || r.height < 43.5;
    }).slice(0, 6).map(el => el.tagName.toLowerCase() + ' "' + (el.textContent || el.name || '').trim().slice(0, 30) + '" ' + Math.round(el.getBoundingClientRect().width) + 'x' + Math.round(el.getBoundingClientRect().height));
  }
  const rotated = [...document.querySelectorAll('video')].filter(v => { const t = getComputedStyle(v).transform; return t && t !== 'none' && !/^matrix\\(1, 0, 0, 1/.test(t); }).length;
  return {
    over, wide, h1: inFold(h1), img: inFold(img), ctas: ctas.length ? ctas.every(inFold) : null, ctaCount: ctas.length,
    stamp: (() => { const s = hero && hero.querySelector('.stamp'); return !s || (vis(s) && s.getBoundingClientRect().bottom <= vh); })(),
    motionReady: doc.classList.contains('motion-ready'), appReady: doc.classList.contains('app-ready'), small, rotated,
    autoplay: [...document.querySelectorAll('video')].filter(v => v.autoplay || !v.paused).length,
  };
})()`;

const SCROLL_ALL = `(async () => {
  const step = innerHeight * 0.7;
  for (let y = 0; y < document.documentElement.scrollHeight; y += step) { scrollTo({ top: y, behavior: 'instant' }); await new Promise(r => setTimeout(r, 70)); }
  await new Promise(r => setTimeout(r, 1200));
  const stuck = [...document.querySelectorAll('[data-reveal]')].filter(el => !el.closest('[hidden]') && parseFloat(getComputedStyle(el).opacity) < 0.99);
  scrollTo({ top: 0, behavior: 'instant' });
  return stuck.length;
})()`;

async function run() {
  await waitForChrome();
  const page = await openPage();
  let current = '';
  const errors = [];
  page.on((m) => {
    if (m.method === 'Runtime.exceptionThrown') errors.push([current, 'exception', m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text]);
    if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push([current, 'console', m.params.args.map((a) => a.value).join(' ')]);
    if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') errors.push([current, 'log', m.params.entry.text + ' ' + (m.params.entry.url || '')]);
    if (m.method === 'Network.requestWillBeSent' && !m.params.request.url.startsWith(BASE) && !m.params.request.url.startsWith('data:') && !m.params.request.url.startsWith('about:')) errors.push([current, 'external', m.params.request.url]);
    if (m.method === 'Network.responseReceived' && m.params.response.status >= 400 && !current.includes('404')) errors.push([current, 'http ' + m.params.response.status, m.params.response.url]);
  });

  let checks = 0;
  for (const vp of VIEWPORTS) {
    await page.send('Emulation.setDeviceMetricsOverride', { width: vp.w, height: vp.h, deviceScaleFactor: 1, mobile: vp.mobile });
    await page.send('Emulation.setTouchEmulationEnabled', { enabled: vp.mobile });
    for (const route of ROUTES) {
      current = `${route} @${vp.w}`;
      await page.goto(BASE + route);
      const a = await page.eval(AUDIT);
      checks++;
      if (a.over > 0) fail(current, `root overflow ${a.over}px ${a.wide.join(', ')}`);
      if (!a.h1) fail(current, 'h1 not in first viewport');
      if (route !== '/404.html') {
        if (!a.img) fail(current, 'player photo not in first viewport');
        if (a.ctas === false) fail(current, 'Watch/Contact CTAs not in first viewport');
        if (!a.stamp) fail(current, 'last-updated stamp not in first viewport');
      }
      if (!a.appReady) fail(current, 'app.js did not initialise');
      if (!a.motionReady && route !== '/404.html') fail(current, 'motion-ready missing');
      if (a.small.length) fail(current, `touch targets < 44px: ${a.small.join(' | ')}`);
      if (a.rotated) fail(current, 'rotated video element');
      if (a.autoplay) fail(current, 'video playing on load');
      if (vp.w === 1440 || vp.w === 390) {
        const shot = await page.send('Page.captureScreenshot', { format: 'png' });
        writeFileSync(join(OUT, `${route.replace(/\W+/g, '_') || 'root'}-${vp.w}.png`), Buffer.from(shot.data, 'base64'));
      }
      if (vp.w === 1440 || vp.w === 390) {
        const stuck = await page.eval(SCROLL_ALL);
        if (stuck) fail(current, `${stuck} reveal elements still hidden after full scroll`);
        const after = await page.eval('document.documentElement.scrollWidth - document.documentElement.clientWidth');
        if (after > 0) fail(current, `root overflow after scroll ${after}px`);
      }
    }
  }

  // ---- interaction checks at desktop size
  await page.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await page.send('Emulation.setTouchEmulationEnabled', { enabled: false });
  for (let n = 1; n <= 10; n++) {
    current = `/${n}/ interactions`;
    await page.goto(`${BASE}/${n}/`);
    // Switcher: open, focus inside, Escape closes and restores focus.
    const sw = await page.eval(`(async () => {
      const t = document.querySelector('[data-switcher-toggle]'); t.focus(); t.click();
      await new Promise(r => setTimeout(r, 50));
      const panel = document.getElementById(t.getAttribute('aria-controls'));
      return { expanded: t.getAttribute('aria-expanded'), visible: !panel.hidden, focusInside: panel.contains(document.activeElement) };
    })()`);
    if (sw.expanded !== 'true' || !sw.visible || !sw.focusInside) fail(current, `switcher open state ${JSON.stringify(sw)}`);
    await page.key('Escape', 'Escape', 27);
    const swClosed = await page.eval(`(() => { const t = document.querySelector('[data-switcher-toggle]'); return { expanded: t.getAttribute('aria-expanded'), focus: document.activeElement === t }; })()`);
    if (swClosed.expanded !== 'false' || !swClosed.focus) fail(current, `switcher Escape ${JSON.stringify(swClosed)}`);

    // Anchor preservation: jump to #data and check the design links carry it.
    await page.goto(`${BASE}/${n}/#data`);
    await sleep(500);
    const hrefs = await page.eval(`[...document.querySelectorAll('a[rel=next], a[rel=prev], [data-variant-link]')].map(a => a.getAttribute('href'))`);
    if (!hrefs.every((h) => h.endsWith('#data'))) fail(current, `design links do not preserve #data: ${hrefs.slice(0, 3).join(', ')}`);

    // Lightbox: open from the gallery, focus moves in, Tab stays in, Escape restores focus.
    await page.eval(`document.querySelector('#gallery a[data-lightbox]').scrollIntoView({block:'center'})`);
    await page.eval(`(() => { const a = document.querySelector('#gallery a[data-lightbox]'); a.focus(); a.click(); })()`);
    await sleep(250);
    const lb = await page.eval(`(() => { const d = document.querySelector('dialog.lightbox'); return { open: d.open, focusIn: d.contains(document.activeElement), src: d.querySelector('img').currentSrc }; })()`);
    if (!lb.open || !lb.focusIn) fail(current, `lightbox open ${JSON.stringify(lb)}`);
    for (let i = 0; i < 6; i++) await page.key('Tab', 'Tab', 9);
    const trapped = await page.eval(`document.querySelector('dialog.lightbox').contains(document.activeElement)`);
    if (!trapped) fail(current, 'focus escaped the lightbox');
    await page.key('ArrowRight', 'ArrowRight', 39);
    await page.key('Escape', 'Escape', 27);
    const lbClosed = await page.eval(`(() => { const d = document.querySelector('dialog.lightbox'); return { open: d.open, restored: document.activeElement === document.querySelector('#gallery a[data-lightbox]') }; })()`);
    if (lbClosed.open || !lbClosed.restored) fail(current, `lightbox close ${JSON.stringify(lbClosed)}`);

    // Pause motion toggles state and persists the choice.
    const paused = await page.eval(`(() => { const b = document.querySelector('[data-motion-toggle]'); b.click(); const r = { pressed: b.getAttribute('aria-pressed'), cls: document.documentElement.className }; b.click(); return r; })()`);
    if (paused.pressed !== 'true' || !paused.cls.includes('motion-paused') || paused.cls.includes('motion-ready')) fail(current, `pause motion ${JSON.stringify(paused)}`);
    checks += 5;
  }

  // 10: stepper is user controlled
  current = '/10/ stepper';
  await page.goto(`${BASE}/10/`);
  const st = await page.eval(`(async () => {
    const vis = () => [...document.querySelectorAll('[data-step]')].filter(s => !s.hidden).map(s => s.id);
    const a = vis(); await new Promise(r => setTimeout(r, 2500)); const b = vis();
    document.querySelector('[data-step-next]').click(); const c = vis();
    return { a, b, c, count: document.querySelector('[data-step-count]').textContent };
  })()`);
  if (st.a.join() !== 'step-1' || st.b.join() !== 'step-1' || st.c.join() !== 'step-2' || st.count !== 'Step 2 of 6') fail(current, JSON.stringify(st));
  checks++;

  // 4: trait focus
  current = '/4/ traits';
  await page.goto(`${BASE}/4/`);
  const tr = await page.eval(`(() => { const b = document.querySelector('.trait-focus'); b.click(); return { pressed: b.getAttribute('aria-pressed'), focus: document.querySelector('[data-traits]').classList.contains('has-focus') }; })()`);
  if (tr.pressed !== 'true' || !tr.focus) fail(current, JSON.stringify(tr));
  checks++;

  // Mobile menu: Escape closes and restores focus
  current = '/2/ mobile menu';
  await page.send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  await page.goto(`${BASE}/2/`);
  await page.eval(`(() => { const t = document.querySelector('[data-menu-toggle]'); t.focus(); t.click(); })()`);
  const menuOpen = await page.eval(`(() => { const n = document.getElementById('site-nav'); return getComputedStyle(n).display !== 'none' && n.contains(document.activeElement); })()`);
  await page.key('Escape', 'Escape', 27);
  const menuClosed = await page.eval(`(() => { const t = document.querySelector('[data-menu-toggle]'); return t.getAttribute('aria-expanded') === 'false' && document.activeElement === t && getComputedStyle(document.getElementById('site-nav')).display === 'none'; })()`);
  if (!menuOpen || !menuClosed) fail(current, `open=${menuOpen} closed=${menuClosed}`);
  checks++;

  // Reduced motion: no motion-ready, everything visible without scrolling.
  await page.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await page.send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  for (const route of ROUTES.slice(0, 11)) {
    current = `${route} reduced-motion`;
    await page.goto(BASE + route);
    const rm = await page.eval(`({ ready: document.documentElement.classList.contains('motion-ready'), hidden: [...document.querySelectorAll('[data-reveal]')].filter(el => parseFloat(getComputedStyle(el).opacity) < 0.99).length, smooth: getComputedStyle(document.documentElement).scrollBehavior })`);
    if (rm.ready || rm.hidden || rm.smooth === 'smooth') fail(current, JSON.stringify(rm));
    checks++;
  }
  await page.send('Emulation.setEmulatedMedia', { features: [] });

  // JavaScript disabled: content is all there and visible.
  await page.send('Emulation.setScriptExecutionDisabled', { value: true });
  for (const route of ROUTES.slice(0, 11)) {
    current = `${route} no-js`;
    await page.goto(BASE + route);
    const nj = await page.eval(`({ hidden: [...document.querySelectorAll('[data-reveal]')].filter(el => parseFloat(getComputedStyle(el).opacity) < 0.99).length, videos: document.querySelectorAll('video').length, imgs: document.querySelectorAll('main img').length, over: document.documentElement.scrollWidth - document.documentElement.clientWidth })`).catch(() => null);
    if (nj && (nj.hidden || (route !== '/' && nj.videos !== 12) || nj.over > 0)) fail(current, JSON.stringify(nj));
    checks++;
  }
  await page.send('Emulation.setScriptExecutionDisabled', { value: false });

  errors.forEach(([where, kind, text]) => fail(where, `${kind}: ${text}`));
  notes.push(`${checks} route/viewport/interaction checks run; screenshots in ${OUT}`);
  console.log(notes.join('\n'));
  if (failures.length) {
    console.log(`\n${failures.length} FAILURES`);
    failures.forEach((f) => console.log(' - ' + f));
  } else console.log('ALL BROWSER CHECKS PASSED');
}

run()
  .catch((err) => { console.error(err); failures.push(String(err)); })
  .finally(() => { chrome.kill(); process.exit(failures.length ? 1 : 0); });
