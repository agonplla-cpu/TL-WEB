/* TL Propreté — intro « Regardez de plus près »
   Un seul plan-séquence piloté par le défilement : vue de Lyon → une entrée éclairée
   → le hall → le monogramme en laiton sur le chêne → écran de fin.
   Tout est dessiné dans un <canvas> à partir d'un repère commun (pixels de la vue de Lyon 1280×853). */
(function () {
  "use strict";
  var intro = document.getElementById("intro");
  if (!intro) return;

  var body = document.body;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var canvas = intro.querySelector(".intro-canvas");
  var ctx = canvas && canvas.getContext ? canvas.getContext("2d") : null;
  if (reduce || !ctx) { intro.classList.add("is-static"); return; }

  var base = intro.getAttribute("data-assets") || "assets/img/";

  /* ---- Géométrie du plan ---- */
  var W = 1280, H = 853;                                  // repère monde = vue de Lyon
  var HALL = { x: 233.2, y: 826.45, w: 8.8 };             // l'entrée éclairée, au pied de l'immeuble
  HALL.h = HALL.w * 2004 / 1596;
  var HPX = 1596 / HALL.w;                                // pixels du hall par unité monde
  var LOGO = { cx: 800, cy: 578, h: 170 };                // monogramme sur le chêne, entre plafond et appliques
  var MONO_AR = 1175 / 1435.2, WORD_AR = 1179 / 169.4;
  var T = { x: HALL.x + LOGO.cx / HPX, y: HALL.y + LOGO.cy / HPX };
  var NUIT = "7,12,43", CARRARE = "237,237,234";

  /* ---- Images ---- */
  var dprCap = 2;
  var bigScreen = Math.max(screen.width, screen.height) * Math.min(window.devicePixelRatio || 1, dprCap) > 1800;
  var IMG = {};
  var pending = 0;
  function load(key, src) {
    pending++;
    var im = new Image();
    im.decoding = "async";
    im.onload = function () { (im.decode ? im.decode() : Promise.resolve()).catch(function () {}).then(function () { IMG[key] = im; pending--; ready(); }); };
    im.onerror = function () { pending--; ready(); };
    im.src = base + src;
  }
  load("lyon", bigScreen ? "lyon-5120.webp" : "lyon-2560.webp");
  load("hall", "hall-1596.webp");
  load("brass", "tl-monogram-brass.svg");
  load("shadow", "tl-monogram-shadow.svg");
  load("blue", "tl-monogram.svg");
  load("word", "tl-wordmark.svg");

  var isReady = false;
  function ready() {
    if (pending > 0) return;
    if (!IMG.lyon || !IMG.hall) { intro.classList.add("is-static"); return; }
    isReady = true;
    intro.classList.add("is-ready");
    needsDraw = true;
  }

  /* ---- Rastérisation des SVG à la bonne taille (net à toutes les échelles) ---- */
  var cache = {};
  var cacheKeys = [];
  function raster(key, hPx) {
    var im = IMG[key];
    if (!im) return null;
    var b = Math.pow(1.18, Math.ceil(Math.log(Math.max(hPx, 8)) / Math.log(1.18)));
    var h = Math.min(Math.round(b), 2400);
    var ar = key === "word" ? WORD_AR : MONO_AR;
    var id = key + h;
    if (cache[id]) return cache[id];
    var c = document.createElement("canvas");
    c.height = h; c.width = Math.max(1, Math.round(h * ar));
    c.getContext("2d").drawImage(im, 0, 0, c.width, c.height);
    cache[id] = c; cacheKeys.push(id);
    if (cacheKeys.length > 40) delete cache[cacheKeys.shift()];
    return c;
  }
  var sheenCanvas = document.createElement("canvas");
  var canBlur = typeof ctx.filter === "string";

  /* ---- Outils ---- */
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function smooth(x, a, b) { var t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); }
  function mix(a, b, t) { return a + (b - a) * t; }

  /* ---- Taille du canvas ---- */
  var vw = 0, vh = 0, dpr = 1;
  function resize() {
    var r = intro.querySelector(".intro-stage").getBoundingClientRect();
    vw = Math.max(1, Math.round(r.width));
    vh = Math.max(1, Math.round(r.height));
    dpr = Math.min(window.devicePixelRatio || 1, vw * vh > 2200000 ? 1.5 : dprCap);
    canvas.width = Math.round(vw * dpr);
    canvas.height = Math.round(vh * dpr);
    needsDraw = true;
  }

  /* ---- Dessin d'une image placée dans le repère monde, limité à la partie visible ---- */
  function drawWorld(im, wx, wy, ww, wh, cam) {
    var sx = (wx - cam.x) * cam.z + vw / 2, sy = (wy - cam.y) * cam.z + vh / 2;
    var sw = ww * cam.z, sh = wh * cam.z;
    var x0 = Math.max(0, sx), y0 = Math.max(0, sy), x1 = Math.min(vw, sx + sw), y1 = Math.min(vh, sy + sh);
    if (x1 <= x0 || y1 <= y0) return;
    var iw = im.naturalWidth, ih = im.naturalHeight;
    var u0 = (x0 - sx) / sw * iw, v0 = (y0 - sy) / sh * ih;
    var u1 = (x1 - sx) / sw * iw, v1 = (y1 - sy) / sh * ih;
    ctx.drawImage(im, u0, v0, Math.max(u1 - u0, 0.01), Math.max(v1 - v0, 0.01), x0, y0, x1 - x0, y1 - y0);
  }

  /* ---- Une image du film, pour une progression p ∈ [0,1] ---- */
  var state = {};
  function render(p) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";

    var portrait = vh > vw;
    var Z0 = Math.max(vw / W, vh / H);
    var logoWorldH = LOGO.h / HPX;
    var Z1 = vh * (portrait ? 0.26 : 0.36) / logoWorldH;

    // zoom logarithmique : vitesse perçue constante, départ et arrivée adoucis
    var u = clamp(p / 0.86, 0, 1);
    var e = 0.3 * u + 0.7 * u * u * (3 - 2 * u);      // réagit dès le premier tour de molette
    var Z = Math.exp(Math.log(Z0) + (Math.log(Z1) - Math.log(Z0)) * e);

    // la cible glisse de sa place dans la photo vers le centre de l'écran
    // tant que le hall ne remplit pas l'écran, on vise son centre ; ensuite, le monogramme
    var g = 1 - smooth(e, 0, 0.72);
    var Zc = Math.max(vw / HALL.w, vh / HALL.h);
    var s = smooth(Z, Math.min(Zc, Z1 * 0.6), Math.min(Zc * 1.8, Z1 * 0.97));
    var tx = mix(HALL.x + HALL.w / 2, T.x, s), ty = mix(HALL.y + HALL.h / 2, T.y, s);
    var cx = tx + (W / 2 - tx) * (Z0 / Z) * g;
    var cy = ty + (H / 2 - ty) * (Z0 / Z) * g;

    var doorH = HALL.h * Z / vh;                      // part de l'écran occupée par l'entrée
    var dark = smooth(doorH, 0.07, 0.4);              // la ville s'efface dans la nuit
    var hx = vw / (2 * Z), hy = vh / (2 * Z);
    var ccx = clamp(cx, Math.min(hx, W / 2), Math.max(W - hx, W / 2));
    var ccy = clamp(cy, Math.min(hy, H / 2), Math.max(H - hy, H / 2));
    cx = mix(ccx, cx, dark); cy = mix(ccy, cy, dark);
    var cam = { x: cx, y: cy, z: Z };

    var cover = Math.min(HALL.w * Z / vw, HALL.h * Z / vh);
    var hallA = smooth(doorH, 0.04, 0.13);
    var glowA = smooth(doorH, 0.035, 0.22) * (1 - smooth(cover, 0.75, 1.05));
    var endA = smooth(p, 0.855, 0.95);

    // 1. fond nuit + Lyon
    ctx.fillStyle = "rgb(" + NUIT + ")";
    ctx.fillRect(0, 0, vw, vh);
    if (dark < 0.995) {
      // au-delà de la résolution de la photo, un léger flou (profondeur de champ) remplace la pixellisation
      var blur = canBlur ? clamp((Z / (IMG.lyon.naturalWidth / W) - 1.6) * 1.4, 0, 7) : 0;
      if (blur > 0.3) ctx.filter = "blur(" + blur.toFixed(1) + "px)";
      drawWorld(IMG.lyon, 0, 0, W, H, cam);
      if (blur > 0.3) ctx.filter = "none";
      if (dark > 0) { ctx.fillStyle = "rgba(" + NUIT + "," + (dark * 0.93).toFixed(3) + ")"; ctx.fillRect(0, 0, vw, vh); }
    }

    // 2. halo chaud qui sort de l'entrée
    var hcx = (HALL.x + HALL.w / 2 - cx) * Z + vw / 2, hcy = (HALL.y + HALL.h / 2 - cy) * Z + vh / 2;
    if (glowA > 0.002) {
      var rad = Math.max(HALL.w, HALL.h) * Z * 1.9 + 40;
      var gr = ctx.createRadialGradient(hcx, hcy, 0, hcx, hcy, rad);
      gr.addColorStop(0, "rgba(255,206,140," + (0.55 * glowA).toFixed(3) + ")");
      gr.addColorStop(0.35, "rgba(255,170,90," + (0.22 * glowA).toFixed(3) + ")");
      gr.addColorStop(1, "rgba(255,150,70,0)");
      ctx.globalCompositeOperation = "lighter";
      ctx.fillStyle = gr;
      ctx.fillRect(0, 0, vw, vh);
      ctx.globalCompositeOperation = "source-over";
    }

    // 3. le hall, à l'emplacement exact de l'entrée
    if (hallA > 0.002) {
      ctx.globalAlpha = hallA;
      drawWorld(IMG.hall, HALL.x, HALL.y, HALL.w, HALL.h, cam);
      ctx.globalAlpha = 1;
    }

    // 4. monogramme laiton incrusté dans le chêne
    var lh = logoWorldH * Z, lw = lh * MONO_AR;
    var lx = (T.x - cx) * Z + vw / 2, ly = (T.y - cy) * Z + vh / 2;
    var logoA = smooth(lh, 5, 36) * hallA;

    // 5. écran de fin
    if (endA > 0) {
      ctx.fillStyle = "rgba(" + CARRARE + "," + endA.toFixed(3) + ")";
      ctx.fillRect(0, 0, vw, vh);
    }
    var t = endA * endA * (3 - 2 * endA);
    var eh = Math.min(vh * (portrait ? 0.16 : 0.25), vw * 0.3 / MONO_AR);
    var ex = vw / 2, ey = vh * (portrait ? 0.27 : 0.37);
    var dh = mix(lh, eh, t), dx = mix(lx, ex, t), dy = mix(ly, ey, t), dw = dh * MONO_AR;

    if (logoA > 0.002 || endA > 0) {
      var swap = smooth(endA, 0.35, 0.85);                 // le laiton devient bleu TL une fois le fond posé
      var aBrass = Math.max(logoA, endA > 0 ? 1 : 0) * (1 - swap);
      var hDev = dh * dpr;
      if (aBrass > 0.002) {
        var sh = raster("shadow", hDev), br = raster("brass", hDev);
        if (sh && br) {
          var o = Math.max(0.6, dh * 0.012);
          ctx.globalAlpha = aBrass * 0.6;
          ctx.drawImage(sh, dx - dw / 2 + o, dy - dh / 2 + o * 1.4, dw, dh);
          // reflet qui glisse sur le laiton à l'approche
          var sheen = smooth(p, 0.62, 0.84);
          sheenCanvas.width = br.width; sheenCanvas.height = br.height;
          var sc = sheenCanvas.getContext("2d");
          sc.globalCompositeOperation = "source-over";
          sc.drawImage(br, 0, 0);
          if (sheen > 0 && sheen < 1) {
            sc.globalCompositeOperation = "source-atop";
            var bw = br.width, bh = br.height, pos = mix(-0.6, 1.6, sheen) * bw;
            var lg = sc.createLinearGradient(pos - bw * 0.35, 0, pos + bw * 0.35, bh * 0.4);
            lg.addColorStop(0, "rgba(255,248,225,0)");
            lg.addColorStop(0.5, "rgba(255,248,225,0.75)");
            lg.addColorStop(1, "rgba(255,248,225,0)");
            sc.fillStyle = lg; sc.fillRect(0, 0, bw, bh);
          }
          ctx.globalAlpha = aBrass;
          ctx.drawImage(sheenCanvas, dx - dw / 2, dy - dh / 2, dw, dh);
        }
      }
      if (swap > 0.002) {
        var bl = raster("blue", hDev);
        if (bl) { ctx.globalAlpha = swap; ctx.drawImage(bl, dx - dw / 2, dy - dh / 2, dw, dh); }
        var wA = smooth(p, 0.9, 0.97);
        if (wA > 0.002) {
          var wh = dh * 0.118, ww = wh * WORD_AR, wr = raster("word", wh * dpr);
          if (wr) { ctx.globalAlpha = wA; ctx.drawImage(wr, dx - ww / 2, dy - dh / 2 + dh * 1.144, ww, wh); }
        }
      }
      ctx.globalAlpha = 1;
    }

    state = { p: p, z: Z, doorH: doorH, cover: cover, dark: dark, endA: endA, lh: lh };
    return state;
  }

  /* ---- Légendes et en-tête ---- */
  var layers = [].slice.call(intro.querySelectorAll("[data-show]"));
  function updateLayers(s) {
    for (var i = 0; i < layers.length; i++) {
      var el = layers[i], k = el.getAttribute("data-show"), on = false;
      if (k === "open") on = s.p < 0.06;
      else if (k === "city") on = s.p > 0.12 && s.doorH < 0.06;
      else if (k === "door") on = s.doorH > 0.16 && s.lh < 45;
      else if (k === "detail") on = s.lh > 90 && s.endA < 0.05;
      else if (k === "end") on = s.endA > 0.85;
      el.classList.toggle("is-on", on);
      if (k === "end") el.toggleAttribute("inert", !on);
    }
    var light = s.endA > 0.5;
    intro.classList.toggle("is-light", light);
    body.classList.toggle("intro-light", light);
    intro.style.setProperty("--p", s.p.toFixed(4));
  }

  /* ---- Boucle : défilement lissé ---- */
  var target = 0, current = 0, needsDraw = true, last = 0, introTop = 0, introLen = 1;
  function measure() {
    var r = intro.getBoundingClientRect();
    introTop = r.top + window.pageYOffset;
    introLen = Math.max(1, intro.offsetHeight - window.innerHeight);
  }
  function onScroll() {
    var y = window.pageYOffset;
    target = clamp((y - introTop) / introLen, 0, 1);
    body.classList.toggle("on-intro", y < introTop + introLen + window.innerHeight * 0.25);
  }
  function tick(now) {
    var dt = Math.min(64, now - (last || now)); last = now;
    var k = 1 - Math.pow(1 - 0.12, dt / 16.67);
    var diff = target - current;
    if (Math.abs(diff) > 0.00005) { current += diff * k; needsDraw = true; }
    else if (current !== target) { current = target; needsDraw = true; }
    if (needsDraw && isReady && inView) { updateLayers(render(current)); needsDraw = false; }
    else if (needsDraw && !isReady) { updateLayers({ p: current, doorH: 0, cover: 0, lh: 0, endA: 0 }); }
    requestAnimationFrame(tick);
  }

  var inView = true;
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (en) { inView = en[0].isIntersecting; if (inView) needsDraw = true; }).observe(intro);
  }
  var rT;
  window.addEventListener("resize", function () { clearTimeout(rT); rT = setTimeout(function () { resize(); measure(); onScroll(); }, 80); });
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("load", function () { measure(); onScroll(); });

  // « Passer l'introduction » : arrivée directe sous l'intro, sans animation
  var skip = intro.querySelector(".intro-skip");
  if (skip) skip.addEventListener("click", function (ev) {
    var dest = document.getElementById("contenu");
    if (!dest) return;
    ev.preventDefault();
    window.scrollTo(0, dest.getBoundingClientRect().top + window.pageYOffset - 1);
    current = target = 1; needsDraw = true;
    var h = dest.querySelector("h2, h1"); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
  });

  resize(); measure(); onScroll(); current = target;
  requestAnimationFrame(tick);

  // outil de réglage : window.__tlIntro(0.5) dessine l'image à 50 %
  window.__tlIntro = function (p) { var s = render(p); updateLayers(s); return s; };
})();
