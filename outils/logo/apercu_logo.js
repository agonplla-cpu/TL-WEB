const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const fs = require('fs'); const path = require('path'); const DIR = process.argv[2] || '.';
  const svgs = ['tl-logo-full.svg','tl-monogram.svg','tl-wordmark.svg'].map(n=>fs.readFileSync(path.join(DIR, n),'utf8'));
  await p.setContent(`<body style="margin:0;background:#fff;display:flex;gap:30px;align-items:flex-start;padding:20px">
   <div style="width:420px">${svgs[0]}</div><div style="width:380px;background:#c9a067;padding:20px">${svgs[1].replace('#092094','#3b2412')}</div>
   <div style="width:420px;background:#092094;padding:20px">${svgs[2].replace('#092094','#fff')}</div>
   <div style="position:absolute;left:20px;top:700px;width:1200px;height:280px;overflow:hidden"><div style="width:6000px;transform:translate(-2300px,-200px)">${svgs[1]}</div></div></body>`);
  await p.screenshot({ path: path.join(DIR, 'apercu.png') }); await b.close();
})();
