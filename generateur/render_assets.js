const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const S = path.join(__dirname, '..', 'site');
  const mono = fs.readFileSync(S + '/assets/img/tl-monogram.svg', 'utf8');
  const monoW = fs.readFileSync(S + '/assets/img/tl-monogram-white.svg', 'utf8');
  const wordW = fs.readFileSync(S + '/assets/img/tl-wordmark-white.svg', 'utf8');
  const logo = fs.readFileSync(S + '/assets/img/tl-logo.svg', 'utf8');
  const lyon = 'data:image/jpeg;base64,' + fs.readFileSync(S + '/assets/img/lyon-1280.jpg').toString('base64');
  const font = 'data:font/woff2;base64,' + fs.readFileSync(S + '/assets/fonts/bodoni-moda.woff2').toString('base64');
  const jost = 'data:font/woff2;base64,' + fs.readFileSync(S + '/assets/fonts/jost.woff2').toString('base64');
  const b = await chromium.launch();
  const shot = async (w, h, html, out, type) => {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await p.setContent(`<style>@font-face{font-family:B;src:url(${font})}@font-face{font-family:J;src:url(${jost})}html,body{margin:0;width:${w}px;height:${h}px;overflow:hidden}svg{width:100%;height:100%}</style>${html}`);
    await p.waitForTimeout(300);
    await p.screenshot({ path: out, type: type || 'png', quality: type === 'jpeg' ? 88 : undefined, omitBackground: !type || type === 'png' ? false : undefined });
    await p.close();
  };
  // icônes : monogramme bleu sur carré blanc
  const icon = (pad) => `<div style="width:100%;height:100%;background:#fff;display:flex;align-items:center;justify-content:center"><div style="height:${100 - pad * 2}%;aspect-ratio:1175/1435">${mono}</div></div>`;
  await shot(32, 32, icon(8), S + '/favicon-32.png');
  await shot(180, 180, icon(14), S + '/apple-touch-icon.png');
  await shot(512, 512, `<div style="width:100%;height:100%;background:#fff;display:flex;align-items:center;justify-content:center"><div style="height:80%;aspect-ratio:1167/1800">${logo}</div></div>`, S + '/assets/img/tl-logo-512.png');
  // image de partage 1200x630
  await shot(1200, 630, `<div style="position:relative;width:1200px;height:630px;background:#070C2B url(${lyon}) center 70%/cover;font-family:J,sans-serif;color:#fff">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,12,43,.92) 0%,rgba(7,12,43,.72) 46%,rgba(7,12,43,.15) 100%)"></div>
    <div style="position:absolute;left:84px;top:86px;width:86px;height:105px">${monoW}</div>
    <div style="position:absolute;left:190px;top:128px;width:150px;height:22px">${wordW}</div>
    <div style="position:absolute;left:84px;top:250px;width:620px;font-family:B,serif;font-size:62px;line-height:1.06;letter-spacing:-0.5px">L’exigence du propre, jusque dans les détails.</div>
    <div style="position:absolute;left:86px;bottom:72px;font-size:24px;opacity:.88">Copropriétés, bureaux, commerces et hôtels à Lyon</div>
  </div>`, S + '/og-cover.jpg', 'jpeg');
  await b.close();
})();
