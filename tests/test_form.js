const { chromium, devices } = require('playwright');
const path = require('path');
const fs = require('fs');
const OUT = path.join(__dirname, '..', 'captures');
fs.mkdirSync(OUT, { recursive: true });
const BASE = process.env.BASE_URL || 'http://127.0.0.1:8080';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ ...devices['iPhone 13'] });
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(BASE + '/contact/?prestation=nettoyage-vitres-lyon', { waitUntil: 'networkidle' });
  const pre = await p.$eval('#f-prestation', s => s.value);
  // empty submit -> errors
  await p.click('button[type=submit]');
  const nErr = await p.$$eval('.field-error', e => e.length);
  await p.fill('#f-nom', 'Test Playwright'); await p.fill('#f-email', 'test@example.fr');
  await p.fill('#f-lieu', 'Villeurbanne'); await p.fill('#f-message', 'Vitrine 6 m, chaque semaine.');
  await p.waitForTimeout(3200);
  await p.click('button[type=submit]');
  await p.waitForSelector('.form-status.is-shown');
  const msg = await p.$eval('.form-status', e => e.textContent);
  await p.screenshot({ path: path.join(OUT, 'form-ok.png') });
  // mobile menu
  await p.click('.menu-toggle'); await p.waitForTimeout(400);
  await p.screenshot({ path: path.join(OUT, 'menu.png') });
  const exp = await p.$eval('.menu-toggle', e => e.getAttribute('aria-expanded'));
  console.log(JSON.stringify({ pre, nErr, msg, exp, errs }));
  await b.close();
})();
