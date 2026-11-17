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
  const font = 'data:font/woff2;base64,' + fs.readFileSync(S + '/assets/fonts/archivo.woff2').toString('base64');
  const b = await chromium.launch();
  const shot = async (w, h, html, out, type) => {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await p.setContent(`<style>@font-face{font-family:A;src:url(${font});font-weight:100 900;font-stretch:62% 125%}html,body{margin:0;width:${w}px;height:${h}px;overflow:hidden}svg{width:100%;height:100%}</style>${html}`);
    await p.waitForTimeout(300);
    await p.screenshot({ path: out, type: type || 'png', quality: type === 'jpeg' ? 88 : undefined, omitBackground: !type || type === 'png' ? false : undefined });
    await p.close();
  };
  // icônes : monogramme bleu sur carré blanc
  const icon = (pad) => `<div style="width:100%;height:100%;background:#fff;display:flex;align-items:center;justify-content:center"><div style="height:${100 - pad * 2}%;aspect-ratio:1175/1435">${mono}</div></div>`;
  await shot(32, 32, icon(8), S + '/favicon-32.png');
  await shot(180, 180, icon(14), S + '/apple-touch-icon.png');
  await shot(512, 512, `<div style="width:100%;height:100%;background:#fff;display:flex;align-items:center;justify-content:center"><div style="height:80%;aspect-ratio:1167/1800">${logo}</div></div>`, S + '/assets/img/tl-logo-512.png');
  // image de partage 1200x630 : texte sur bleu à gauche, vraie photo de Lyon à droite (taille d'origine)
  await shot(1200, 630, `<div style="position:relative;width:1200px;height:630px;background:#092094;font-family:A,sans-serif;color:#fff;display:grid;grid-template-columns:620px 580px">
    <div style="padding:70px 64px;display:flex;flex-direction:column">
      <div style="display:flex;align-items:center;gap:16px"><div style="width:56px;height:68px">${monoW}</div><div style="width:150px;height:22px">${wordW}</div></div>
      <div style="margin-top:auto;font-size:54px;font-weight:700;font-stretch:112%;line-height:1.06;letter-spacing:-0.5px">Nettoyage de copropriétés, bureaux et commerces à Lyon</div>
      <div style="margin-top:22px;font-size:24px;font-weight:500;opacity:.92">Devis gratuit sous 24 heures</div>
    </div>
    <div style="background:url(${lyon}) center/cover"></div>
  </div>`, S + '/og-cover.jpg', 'jpeg');
  await b.close();
})();
