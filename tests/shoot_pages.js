const { chromium, devices } = require('playwright');
const path = require('path');
const fs = require('fs');
const OUT = path.join(__dirname, '..', 'captures');
fs.mkdirSync(OUT, { recursive: true });
const BASE = process.env.BASE_URL || 'http://127.0.0.1:8080';
(async () => {
  const mode = process.argv[2] || 'desktop';
  const pages = (process.argv[3] || '/').split(',');
  const b = await chromium.launch();
  const ctx = mode === 'mobile' ? await b.newContext({ ...devices['iPhone 13'] }) : await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const errs = [];
  for (const u of pages) {
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(u + ' PAGEERROR ' + e.message));
    p.on('console', m => { if (m.type() === 'error') errs.push(u + ' ' + m.text()); });
    p.on('requestfailed', r => errs.push(u + ' FAILED ' + r.url()));
    p.on('response', r => { if (r.status() >= 400) errs.push(u + ' ' + r.status() + ' ' + r.url()); });
    await p.goto(BASE + u, { waitUntil: 'networkidle' });
    await p.waitForTimeout(500);
    const name = (u === '/' ? 'home' : u.replace(/\//g, '_').replace(/^_|_$/g, '')).replace(/[?=]/g, '-');
    await p.screenshot({ path: `${OUT}/page-${mode}-${name}.png`, fullPage: true });
    const w = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    if (w.sw > w.cw + 1) errs.push(u + ' HORIZONTAL OVERFLOW ' + JSON.stringify(w));
    await p.close();
  }
  console.log(JSON.stringify(errs, null, 1));
  await b.close();
})();
