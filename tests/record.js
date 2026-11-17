const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const OUT = path.join(__dirname, '..', 'captures');
fs.mkdirSync(OUT, { recursive: true });
const BASE = process.env.BASE_URL || 'http://127.0.0.1:8080';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1, recordVideo: { dir: OUT, size: { width: 1280, height: 720 } } });
  const p = await ctx.newPage();
  await p.goto(BASE + '/', { waitUntil: 'networkidle' });
  await p.waitForTimeout(2200);
  const len = await p.evaluate(() => { const i = document.getElementById('intro'); return i.offsetHeight - innerHeight; });
  const steps = 260;
  for (let k = 1; k <= steps; k++) {
    const t = k / steps, e = t;
    await p.evaluate((y) => window.scrollTo(0, y), Math.round(e * len));
    await p.waitForTimeout(10);
  }
  await p.waitForTimeout(2500);
  for (let k = 1; k <= 60; k++) { await p.evaluate((y) => window.scrollTo(0, y), len + k * 14); await p.waitForTimeout(33); }
  await p.waitForTimeout(800);
  await ctx.close(); await b.close();
})();
