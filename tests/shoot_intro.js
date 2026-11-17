const { chromium, devices } = require('playwright');
const path = require('path');
const fs = require('fs');
const OUT = path.join(__dirname, '..', 'captures');
fs.mkdirSync(OUT, { recursive: true });
const BASE = process.env.BASE_URL || 'http://127.0.0.1:8080';
(async () => {
  const mode = process.argv[2] || 'desktop';
  const ps = (process.argv[3] || '0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1').split(',').map(Number);
  const b = await chromium.launch();
  const ctx = mode === 'mobile' ? await b.newContext({ ...devices['iPhone 13'] }) : await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  const errs = [];
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.text()); });
  p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  await p.goto(BASE + '/', { waitUntil: 'networkidle' });
  await p.waitForTimeout(800);
  for (const v of ps) {
    await p.evaluate((v) => { const i = document.getElementById('intro'); const top = i.getBoundingClientRect().top + scrollY; const len = i.offsetHeight - innerHeight; window.scrollTo(0, top + v * len); }, v);
    await p.waitForTimeout(1600);
    const st = await p.evaluate(() => { const s = window.__tlIntroState; return null; });
    await p.screenshot({ path: `${OUT}/${mode}-${String(Math.round(v * 100)).padStart(3, '0')}.jpg`, type: 'jpeg', quality: 70 });
  }
  console.log('errors:', JSON.stringify(errs));
  await b.close();
})();
