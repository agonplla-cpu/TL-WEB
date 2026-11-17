# -*- coding: utf-8 -*-
"""Génère le site statique TL Propreté dans le dossier site/ du dépôt."""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import *

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site"))
YEAR = 2026
VERSION = "20261117"
LASTMOD = "2026-11-17"


# ------------------------------------------------------------------ typographie française
def fr(s):
    s = s.replace("'", "’")
    s = re.sub(r" ([:])", " \\1", s)
    s = re.sub(r" ([;?!])", " \\1", s)
    s = s.replace("« ", "« ").replace(" »", " »")
    return s


def typeset(doc):
    """Applique fr() au texte visible uniquement (hors balises, scripts et styles)."""
    out, skip = [], False
    for part in re.split(r"(<[^>]+>)", doc):
        if part.startswith("<"):
            low = part.lower()
            if low.startswith("<script") or low.startswith("<style"):
                skip = True
            elif low.startswith("</script") or low.startswith("</style"):
                skip = False
            out.append(part)
        else:
            out.append(part if skip else fr(part))
    return "".join(out)


def a(s):  # valeur d'attribut
    return html.escape(fr(s), quote=True)


# ------------------------------------------------------------------ morceaux communs
NAV = [("Prestations", "/#prestations"), ("Copropriétés", "/nettoyage-copropriete-lyon/"),
       ("Zones", "/#zones"), ("Contact", "/contact/")]


def header(current):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{n}</a></li>' for n, h in NAV)
    svc = "".join(f'<li><a href="/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    return f'''<a class="skip-link" href="#contenu">Aller au contenu</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="TL Propreté, accueil">
      <img class="brand-mono" src="/assets/img/tl-monogram.svg" alt="" width="33" height="40">
      <img class="brand-word" src="/assets/img/tl-wordmark.svg" alt="" width="111" height="16">
    </a>
    <nav class="main-nav" aria-label="Navigation principale"><ul>{links}</ul></nav>
    <a class="header-tel" href="tel:{PHONE_INTL}">{PHONE}</a>
    <a class="btn header-cta" href="/contact/">Demander un devis</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu-mobile"><span class="menu-toggle-bars" aria-hidden="true"></span><span class="menu-toggle-label">Menu</span></button>
  </div>
</header>
<div class="mobile-menu on-dark" id="menu-mobile">
  <nav aria-label="Menu mobile">
    <ul class="mm-main"><li><a href="/">Accueil</a></li><li><a href="/#prestations">Prestations</a></li><li><a href="/#zones">Zones d'intervention</a></li><li><a href="/contact/">Contact</a></li></ul>
  </nav>
  <ul class="mm-sub">{svc}</ul>
  <div class="btn-row"><a class="btn btn-light" href="/contact/">Demander un devis</a><a class="btn btn-ghost-light" href="tel:{PHONE_INTL}">{PHONE}</a></div>
</div>'''


def footer():
    svc = "".join(f'<li><a href="/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES)
    phone = f'<a href="tel:{PHONE_INTL}">{PHONE}</a>' if PHONE else ""
    return f'''<footer class="site-footer on-dark">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="/assets/img/tl-logo-white.svg" alt="TL Propreté" width="92" height="142">
        <p>Entreprise de propreté à Lyon depuis 2021 : copropriétés, bureaux, commerces et hôtels.</p>
      </div>
      <div><h2>Prestations</h2><ul>{svc}</ul></div>
      <div><h2>Entreprise</h2><ul><li><a href="/#zones">Zones d'intervention</a></li><li><a href="/contact/">Demander un devis</a></li><li><a href="/mentions-legales/">Mentions légales</a></li><li><a href="/confidentialite/">Confidentialité</a></li></ul></div>
      <div><h2>Contact</h2>
        <address>
          <span>TL Propreté<br>{STREET}<br>{POSTCODE} {CITY}</span>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          {phone}
          <span>{HOURS}</span>
        </address>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© {YEAR} TL Propreté</p>
      <ul><li><a href="/mentions-legales/">Mentions légales</a></li><li><a href="/confidentialite/">Confidentialité</a></li></ul>
    </div>
  </div>
</footer>'''


def business_ld():
    d = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": SITE + "/#entreprise",
        "name": "TL Propreté",
        "description": "Entreprise de propreté à Lyon : nettoyage de copropriétés, bureaux, commerces et hôtels, fin de chantier, vitrerie, remise en état, remplacement de gardien.",
        "url": SITE + "/",
        "logo": SITE + "/assets/img/tl-logo-512.png",
        "image": SITE + "/og-cover.jpg",
        "email": EMAIL,
        "foundingDate": "2021",
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": POSTCODE,
                    "addressLocality": CITY, "addressRegion": "Auvergne-Rhône-Alpes", "addressCountry": "FR"},
        "areaServed": [{"@type": "City", "name": n} for n in AREA_SERVED],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "08:00", "closes": "18:00"}],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["h1"], "url": f'{SITE}/{s["slug"]}/'}} for s in SERVICES],
    }
    if PHONE_INTL:
        d["telephone"] = PHONE_INTL
    return d


def page(path, title, desc, body, *, current=None, ld=None, body_class="", noindex=False, preload=""):
    canonical = SITE + path
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    doc = f'''<!doctype html>
<html lang="fr" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.remove("no-js")</script>
<title>{a(title)}</title>
<meta name="description" content="{a(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="TL Propreté">
<meta property="og:title" content="{a(title)}">
<meta property="og:description" content="{a(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="/assets/css/site.css?v={VERSION}">
{lds}
</head>
<body class="{body_class}">
{header(current)}
{body}
{footer()}
<script src="/assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
'''
    return typeset(doc)


def write(path, doc):
    fp = os.path.join(OUT, path.lstrip("/"))
    if fp.endswith("/"):
        fp += "index.html"
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(doc)


def faq_html(items):
    return "".join(f'<details><summary>{q}</summary><div class="faq-a"><p>{r}</p></div></details>' for q, r in items)


def cta_block(title="Parlons de votre immeuble",
              text="Décrivez le lieu et la fréquence souhaitée : nous revenons vers vous sous 24 heures pour fixer une visite.",
              href="/contact/"):
    return f'''<div class="cta-band">
  <div><h2>{title}</h2><p>{text}</p></div>
  <div class="cta-actions"><a class="btn btn-light" href="{href}">Demander un devis</a><p>ou appelez le <a href="tel:{PHONE_INTL}">{PHONE}</a><br>ou écrivez à <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
</div>'''


# ------------------------------------------------------------------ accueil
def home():
    rows = "".join(f'''<li><a class="svc-row" href="/{s["slug"]}/"><h3>{s["name"]}</h3><p>{s["short"]}</p><span class="svc-go">Voir la prestation</span></a></li>''' for s in SERVICES)
    days = [("L", "Lundi"), ("M", "Mardi"), ("M", "Mercredi"), ("J", "Jeudi"), ("V", "Vendredi"), ("S", "Samedi"), ("D", "Dimanche")]
    plan = [("Entretien du hall et des paliers", [1, 1, 1, 1, 1, 0, 0]),
            ("Sortie des ordures ménagères", [1, 0, 0, 1, 0, 1, 0]),
            ("Sortie du tri sélectif", [0, 1, 0, 0, 1, 0, 0])]
    head = "".join(f'<th scope="col"><abbr title="{n}">{l}</abbr></th>' for l, n in days)
    body_rows = ""
    for task, marks in plan:
        cells = "".join(
            f'<td><span class="dot" aria-hidden="true"></span><span class="visually-hidden">{days[i][1]} : oui</span></td>' if m
            else f'<td><span class="dot dot-off" aria-hidden="true"></span><span class="visually-hidden">{days[i][1]} : non</span></td>'
            for i, m in enumerate(marks))
        body_rows += f'<tr><th scope="row">{task}</th>{cells}</tr>'
    zones = "".join(f'<div><h3>{g}</h3><ul>{"".join(f"<li>{c}</li>" for c in cs)}</ul></div>' for g, cs in ZONES)

    body = f'''<main id="contenu">
  <section class="hero">
    <div class="wrap hero-grid">
      <div class="hero-text">
        <h1>Nettoyage de copropriétés, bureaux et commerces à Lyon</h1>
        <p class="lead">Depuis 2021, TL Propreté entretient les parties communes, les locaux professionnels et les commerces de la métropole lyonnaise, avec un cahier des charges écrit pour chaque lieu.</p>
        <div class="btn-row"><a class="btn" href="/contact/">Demander un devis</a><a class="btn btn-ghost" href="tel:{PHONE_INTL}">{PHONE}</a></div>
        <ul class="hero-facts">
          <li>Visite des lieux gratuite</li>
          <li>Devis détaillé sous 24 heures</li>
          <li>Passages contrôlés par QR code</li>
        </ul>
      </div>
      <figure class="hero-photo">
        <picture><source srcset="/assets/img/lyon-800.webp 800w, /assets/img/lyon-1280.webp 1280w" sizes="(max-width: 980px) 92vw, 600px" type="image/webp"><img src="/assets/img/lyon-1280.jpg" width="1280" height="853" alt="Lyon de nuit, avec les tours du quartier de la Part-Dieu" fetchpriority="high"></picture>
      </figure>
    </div>
  </section>

  <section class="section" id="prestations">
    <div class="wrap">
      <div class="section-head"><h2>Ce que nous entretenons</h2><p>Des parties communes d'une résidence aux vitrines d'une boutique, chaque prestation part d'une visite et d'un cahier des charges écrit.</p></div>
      <ul class="svc-list">{rows}</ul>
    </div>
  </section>

  <section class="section section-alt" id="coproprietes">
    <div class="wrap copro">
      <div class="copro-text">
        <h2>Pour les copropriétés, un planning écrit et tenu</h2>
        <p class="lead">La plupart de nos contrats sont des résidences gérées par des syndics lyonnais. Chaque immeuble a son cahier des charges : ce qui est fait, quel jour, à quelle fréquence.</p>
        <ul class="copro-points">
          <li><strong>Un cahier des charges par résidence</strong><span>Validé avec le syndic et le conseil syndical avant le premier passage.</span></li>
          <li><strong>Lavage des bacs suivi par QR code</strong><span>L'agent valide chaque lavage en scannant le code affiché dans le local : chaque passage est daté.</span></li>
          <li><strong>Remplacement du gardien</strong><span>Pendant ses congés, un arrêt ou un recrutement, la résidence reste tenue.</span></li>
          <li><strong>Reprise d'un contrat en cours</strong><span>Nous repartons du planning existant, sans interruption pour les résidents.</span></li>
        </ul>
        <p style="margin-top:32px"><a href="/nettoyage-copropriete-lyon/">La prestation copropriété en détail</a></p>
      </div>
      <div class="planning">
        <h3>Une semaine type</h3>
        <p>Planning d'une résidence que nous entretenons à Lyon.</p>
        <table>
          <caption class="visually-hidden">Passages hebdomadaires par tâche, du lundi au dimanche</caption>
          <thead><tr><th scope="col">Tâche</th>{head}</tr></thead>
          <tbody>{body_rows}</tbody>
        </table>
        <ul class="planning-extra">
          <li><span>Prestations mensuelles, le lundi</span><b>1 fois par mois</b></li>
          <li><span>Pelouses et parkings, le mardi</span><b>1 fois par mois</b></li>
          <li><span>Vitrerie du hall</span><b>4 fois par an</b></li>
          <li><span>Vitrerie des escaliers</span><b>1 fois par an</b></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section" id="methode">
    <div class="wrap">
      <div class="section-head"><h2>Comment nous travaillons</h2><p>De la première visite au suivi des passages, la même méthode pour chaque lieu.</p></div>
      <ol class="steps">
        <li><h3>Visite des lieux</h3><p>Nous venons voir les surfaces, les accès et vos contraintes d'horaires. La visite est gratuite.</p></li>
        <li><h3>Devis sous 24 heures</h3><p>Un devis détaillé poste par poste, avec les fréquences proposées.</p></li>
        <li><h3>Cahier des charges</h3><p>Les tâches et leurs fréquences sont écrites. Elles servent de référence à nos agents comme à vous.</p></li>
        <li><h3>Passages et suivi</h3><p>Les interventions suivent le planning. Vous avez un interlocuteur direct pour tout ajustement.</p></li>
      </ol>
    </div>
  </section>

  <section class="section" id="zones">
    <div class="wrap">
      <div class="section-head"><h2>Lyon et sa métropole, depuis <span style="white-space:nowrap">Tassin-la-Demi-Lune</span></h2><p>Notre équipe intervient dans toute la métropole lyonnaise, à partir de nos locaux de l'Ouest lyonnais.</p></div>
      <div class="zones">{zones}</div>
      <p class="zones-note">Votre commune n'est pas dans la liste ? <a href="/contact/">Demandez-nous</a>.</p>
    </div>
  </section>

  <section class="section section-alt" id="questions">
    <div class="wrap faq-layout">
      <h2>Questions fréquentes</h2>
      <div class="faq">{faq_html(HOME_FAQ)}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">{cta_block()}</div>
  </section>
</main>'''
    ld = [business_ld(), {"@context": "https://schema.org", "@type": "WebSite", "name": "TL Propreté", "url": SITE + "/", "inLanguage": "fr-FR"}]
    write("/", page("/", "Entreprise de nettoyage à Lyon : copropriétés, bureaux, commerces | TL Propreté",
                    "TL Propreté, entreprise de propreté à Lyon depuis 2021 : nettoyage de copropriétés, bureaux, commerces et hôtels, fin de chantier, vitrerie. Devis gratuit sous 24 heures.",
                    body, current="/", ld=ld, body_class="home"))


# ------------------------------------------------------------------ pages prestations
def service(s):
    items = "".join(f'<li><strong>{t}</strong> : {d}</li>' for t, d in s["items"])
    freqs = "".join(f'<li class="freq">{f}</li>' for f in s["freqs"])
    sections = ""
    for h, ps in s["body"]:
        sections += f'<h2>{h}</h2>' + "".join(f"<p>{p}</p>" for p in ps)
    fig = ''
    if s.get("image"):
        fig = '''<figure class="figure-hall"><picture><source srcset="/assets/img/hall-400.webp" type="image/webp"><img src="/assets/img/hall-400.jpg" width="399" height="501" alt="Hall d'entrée de résidence : lambris en chêne, boîtes aux lettres, sol en marbre blanc bordé de marbre noir" loading="eager"></picture><figcaption>Hall d'une résidence entretenue par TL Propreté.</figcaption></figure>'''
    others = [o for o in SERVICES if o["slug"] != s["slug"]]
    rel = "".join(f'<li><a href="/{o["slug"]}/">{o["name"]}</a></li>' for o in others)
    body = f'''<main id="contenu">
  <section class="page-hero">
    <div class="wrap">
      <nav aria-label="Fil d'Ariane"><ol class="breadcrumb"><li><a href="/">Accueil</a></li><li><a href="/#prestations">Prestations</a></li><li aria-current="page">{s["name"]}</li></ol></nav>
      <div class="page-hero-grid">
        <div>
          <h1>{s["h1"]}</h1>
          <p class="lead">{s["lead"]}</p>
          <div class="btn-row"><a class="btn" href="/contact/?prestation={s["slug"]}">Demander un devis</a><a class="btn btn-ghost" href="mailto:{EMAIL}">Nous écrire</a></div>
        </div>
        {fig}
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap content-grid">
      <div class="prose">
        <h2>Ce que comprend la prestation</h2>
        <ul class="checklist">{items}</ul>
        {sections}
      </div>
      <aside class="aside-card" aria-label="En bref">
        <h2>En bref</h2>
        <ul class="freqs" aria-label="Fréquences possibles">{freqs}</ul>
        <dl>
          <div><dt>Pour qui</dt><dd>{s["for"]}</dd></div>
          <div><dt>Où</dt><dd>Lyon et la métropole lyonnaise</dd></div>
          <div><dt>Devis</dt><dd>Gratuit, après une visite des lieux, sous 24 heures</dd></div>
        </dl>
        <a class="btn" href="/contact/?prestation={s["slug"]}">Demander un devis</a>
      </aside>
    </div>
  </section>
  <section class="section">
    <div class="wrap faq-layout"><h2>Questions fréquentes</h2><div class="faq">{faq_html(s["faq"])}</div></div>
  </section>
  <section class="section">
    <div class="wrap">{cta_block("Une visite, puis un devis détaillé", "Dites-nous où se trouve le lieu et ce que vous attendez : nous revenons vers vous sous 24 heures pour fixer une visite.", f"/contact/?prestation={s['slug']}")}</div>
  </section>
  <section class="section">
    <div class="wrap"><h2 class="related-title">Autres prestations</h2><ul class="related">{rel}</ul></div>
  </section>
</main>'''
    url = f'{SITE}/{s["slug"]}/'
    ld = [
        {"@context": "https://schema.org", "@type": "Service", "name": s["h1"], "serviceType": s["name"],
         "description": s["desc"], "url": url, "provider": {"@id": SITE + "/#entreprise", "@type": "LocalBusiness", "name": "TL Propreté"},
         "areaServed": [{"@type": "City", "name": n} for n in AREA_SERVED]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": s["name"], "item": url}]},
    ]
    write(f'/{s["slug"]}/', page(f'/{s["slug"]}/', s["title"], s["desc"], body, ld=ld))


# ------------------------------------------------------------------ contact
def contact():
    opts_who = ["Syndic ou gestionnaire", "Membre d'un conseil syndical", "Entreprise", "Commerce ou hôtel",
                "Promoteur ou entreprise du bâtiment", "Particulier", "Autre"]
    opts_freq = ["À définir ensemble", "Ponctuelle", "Hebdomadaire", "Plusieurs fois par semaine", "Quotidienne"]
    o = lambda xs: "".join(f'<option>{x}</option>' for x in xs)
    svc_opts = "".join(f'<option value="{s["slug"]}">{s["name"]}</option>' for s in SERVICES) + '<option value="autre">Autre besoin</option>'
    phone = f'<div><dt>Téléphone</dt><dd><a href="tel:{PHONE_INTL}">{PHONE}</a></dd></div>' if PHONE else ""
    body = f'''<main id="contenu">
  <section class="page-hero">
    <div class="wrap">
      <nav aria-label="Fil d'Ariane"><ol class="breadcrumb"><li><a href="/">Accueil</a></li><li aria-current="page">Demander un devis</li></ol></nav>
      <h1>Demander un devis</h1>
      <p class="lead">Décrivez votre lieu en quelques lignes : nous vous répondons sous 24 heures ouvrées pour convenir d'une visite, gratuite et sans engagement.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap contact-grid">
      <form class="form" id="form-devis" action="/devis.php" method="post" novalidate>
        <div class="field"><label for="f-qui">Vous êtes</label><select id="f-qui" name="qui">{o(opts_who)}</select></div>
        <div class="field"><label for="f-prestation">Prestation</label><select id="f-prestation" name="prestation">{svc_opts}</select></div>
        <div class="field"><label for="f-nom">Nom et prénom</label><input id="f-nom" name="nom" autocomplete="name" required maxlength="120"></div>
        <div class="field"><label for="f-societe">Société ou résidence <span class="opt">(facultatif)</span></label><input id="f-societe" name="societe" autocomplete="organization" maxlength="160"></div>
        <div class="field"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="160"></div>
        <div class="field"><label for="f-tel">Téléphone <span class="opt">(facultatif)</span></label><input id="f-tel" name="telephone" type="tel" autocomplete="tel" maxlength="40"></div>
        <div class="field"><label for="f-lieu">Adresse ou commune du lieu</label><input id="f-lieu" name="lieu" autocomplete="street-address" required maxlength="200"></div>
        <div class="field"><label for="f-taille">Surface ou nombre de logements <span class="opt">(facultatif)</span></label><input id="f-taille" name="taille" maxlength="80" placeholder="ex. 350 m², 42 logements"></div>
        <div class="field full"><label for="f-freq">Fréquence souhaitée</label><select id="f-freq" name="frequence">{o(opts_freq)}</select></div>
        <div class="field full"><label for="f-message">Votre besoin</label><textarea id="f-message" name="message" required maxlength="4000" placeholder="Espaces à entretenir, contraintes d'horaires, date de démarrage souhaitée…"></textarea></div>
        <div class="hp" aria-hidden="true"><label for="f-site">Ne pas remplir</label><input id="f-site" name="site_web" tabindex="-1" autocomplete="off"></div>
        <input type="hidden" name="t" value="">
        <p class="form-note full">Vos informations servent uniquement à répondre à votre demande. <a href="/confidentialite/">Politique de confidentialité</a>.</p>
        <div class="full"><button class="btn" type="submit">Envoyer ma demande</button></div>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
      <aside class="contact-aside" aria-label="Coordonnées">
        <dl>
          <div><dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          {phone}
          <div><dt>Adresse</dt><dd>{STREET}<br>{POSTCODE} {CITY}</dd></div>
          <div><dt>Horaires du bureau</dt><dd>{HOURS}</dd></div>
          <div><dt>Zone d'intervention</dt><dd>Lyon et la métropole lyonnaise. <a href="/#zones">Voir les communes</a></dd></div>
        </dl>
      </aside>
    </div>
  </section>
</main>'''
    write("/contact/", page("/contact/", "Demander un devis de nettoyage à Lyon | TL Propreté",
                            "Demandez un devis gratuit à TL Propreté pour le nettoyage de votre copropriété, de vos bureaux ou de votre commerce à Lyon. Réponse sous 24 heures ouvrées.",
                            body, current="/contact/", ld=[business_ld()]))


# ------------------------------------------------------------------ pages simples
def simple(path, title, h1, text, links, noindex=True):
    body = f'''<main id="contenu" class="simple-page"><div class="wrap"><h1>{h1}</h1><p class="lead">{text}</p><div class="btn-row" style="margin-top:28px">{links}</div></div></main>'''
    return page(path, title, text, body, noindex=noindex)


def legal():
    ml = f'''<main id="contenu">
  <section class="page-hero"><div class="wrap"><h1>Mentions légales</h1></div></section>
  <section class="section"><div class="wrap legal">
    <h2>Éditeur du site</h2>
    <p>{LEGAL_NAME}, {LEGAL_FORM} au capital de {CAPITAL}.<br>Siège social : {STREET}, {POSTCODE} {CITY}.<br>SIRET : {SIRET}. {RCS}.<br>TVA intracommunautaire : {TVA}.<br>E-mail : <a href="mailto:{EMAIL}">{EMAIL}</a>. Téléphone : <a href="tel:{PHONE_INTL}">{PHONE}</a>.</p>
    <h2>Directeur de la publication</h2>
    <p>{PUBLISHER}.</p>
    <h2>Hébergement</h2>
    <p>{HOST}</p>
    <h2>Propriété intellectuelle</h2>
    <p>Les textes, le logo, les photographies et la présentation de ce site sont la propriété de TL Propreté ou sont utilisés avec l'accord de leurs auteurs. Toute reproduction sans autorisation écrite est interdite.</p>
    <h2>Données personnelles et cookies</h2>
    <p>Le traitement des informations envoyées par le formulaire de devis est décrit dans la <a href="/confidentialite/">politique de confidentialité</a>. Ce site n'utilise ni cookie publicitaire ni outil de mesure d'audience.</p>
  </div></section>
</main>'''
    write("/mentions-legales/", page("/mentions-legales/", "Mentions légales | TL Propreté", "Mentions légales du site de TL Propreté, entreprise de propreté à Tassin-la-Demi-Lune.", ml))

    pc = f'''<main id="contenu">
  <section class="page-hero"><div class="wrap"><h1>Politique de confidentialité</h1><p class="lead">Ce que deviennent les informations que vous nous envoyez.</p></div></section>
  <section class="section"><div class="wrap legal">
    <h2>Responsable du traitement</h2>
    <p>TL Propreté, {STREET}, {POSTCODE} {CITY}. Contact : <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <h2>Données collectées</h2>
    <p>Par le formulaire de devis : nom, société ou résidence, adresse e-mail, téléphone, adresse du lieu, informations sur votre besoin et votre message. Aucune donnée n'est collectée à votre insu.</p>
    <h2>Pourquoi</h2>
    <p>Pour répondre à votre demande, organiser une visite, établir un devis et assurer le suivi de la relation commerciale. Base légale : mesures précontractuelles prises à votre demande (article 6.1.b du RGPD).</p>
    <h2>Qui y a accès</h2>
    <p>Uniquement l'équipe de TL Propreté. Votre demande nous parvient par e-mail depuis le serveur qui héberge le site. Vos données ne sont ni vendues ni cédées.</p>
    <h2>Combien de temps</h2>
    <p>Trois ans après notre dernier échange si vous ne devenez pas client. Pour les clients, pendant la durée du contrat puis le temps imposé par nos obligations légales et comptables.</p>
    <h2>Vos droits</h2>
    <p>Vous pouvez accéder à vos données, les faire rectifier ou effacer, limiter ou refuser leur traitement, et demander leur portabilité, en écrivant à <a href="mailto:{EMAIL}">{EMAIL}</a>. Vous pouvez aussi adresser une réclamation à la CNIL (<a href="https://www.cnil.fr">cnil.fr</a>).</p>
    <h2>Cookies</h2>
    <p>Ce site n'utilise ni cookie publicitaire ni outil de mesure d'audience. Seuls des cookies techniques, nécessaires à la sécurité du site, peuvent être déposés par l'hébergeur.</p>
    <p class="muted">Mise à jour : novembre {YEAR}.</p>
  </div></section>
</main>'''
    write("/confidentialite/", page("/confidentialite/", "Politique de confidentialité | TL Propreté", "Comment TL Propreté traite les informations envoyées par le formulaire de devis.", pc))


def build():
    home()
    for s in SERVICES:
        service(s)
    contact()
    legal()
    write("/merci/", simple("/merci/", "Demande envoyée | TL Propreté", "Demande envoyée",
                            "Merci. Nous vous répondons sous 24 heures ouvrées pour convenir d'une visite.",
                            '<a class="btn" href="/">Retour à l\'accueil</a><a class="btn btn-ghost" href="/#prestations">Nos prestations</a>'))
    write("/404.html", simple("/404.html", "Page introuvable | TL Propreté", "Cette page n'existe pas",
                              "L'adresse a peut-être changé. Revenez à l'accueil ou consultez nos prestations.",
                              '<a class="btn" href="/">Retour à l\'accueil</a><a class="btn btn-ghost" href="/#prestations">Nos prestations</a>'))
    # sitemap + robots
    urls = ["/"] + [f'/{s["slug"]}/' for s in SERVICES] + ["/contact/", "/mentions-legales/", "/confidentialite/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        pr = "1.0" if u == "/" else ("0.8" if "lyon" in u else ("0.6" if u == "/contact/" else "0.2"))
        sm += f"  <url><loc>{SITE}{u}</loc><lastmod>{LASTMOD}</lastmod><priority>{pr}</priority></url>\n"
    sm += "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /merci/\n\nSitemap: {SITE}/sitemap.xml\n")
    print("pages:", len(urls) + 2)


if __name__ == "__main__":
    build()
