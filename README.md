# TL Propreté — site web

Source du site [www.tlproprete.fr](https://www.tlproprete.fr), en ligne depuis le 4 novembre 2026.
Site statique (HTML, CSS, JS) généré en Python, plus `devis.php` pour le formulaire de devis.

## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `site/` | Le site tel qu'il est publié : contenu du dossier `httpdocs` sur Plesk. |
| `generateur/` | `content.py` (textes, prestations, coordonnées, communes), `build.py` (génère les pages dans `site/`), `render_assets.js` (favicon, icône Apple, image de partage). |
| `tests/` | Scripts Playwright : captures de l'intro et des pages, test du formulaire, enregistrement vidéo de l'intro. Les captures vont dans `captures/` (non versionné). |
| `outils/` | Chaîne de traitement des images : agrandissement Real-ESRGAN (`images/upscale.py`), retouche de la photo du hall (`images/retouch_hall.py`), vectorisation du logo (`logo/vectorize.py`). |

Pages publiées : accueil avec l'intro zoom (Lyon → hall d'entrée → logo), 7 pages prestations, contact,
mentions légales, confidentialité, `/merci/`, `404.html`, `sitemap.xml`, `robots.txt`.

## Modifier le site

1. Modifier les textes dans `generateur/content.py` (ou la mise en page dans `generateur/build.py`).
2. Régénérer : `python3 generateur/build.py`
3. Vérifier en local : `php -S 127.0.0.1:8080 -t site` puis ouvrir http://127.0.0.1:8080
   (l'envoi d'e-mail du formulaire ne fonctionne que sur le serveur).
4. Publier : dans Plesk > Fichiers > `httpdocs`, téléverser les fichiers modifiés de `site/`.
   Ne pas toucher aux autres fichiers et dossiers déjà présents dans `httpdocs` (ex. `wordpress/`, `nextcloud/`).

Après une modification de CSS ou de JS, augmenter `VERSION` dans `build.py` pour que les navigateurs
rechargent les fichiers (ils sont mis en cache un an).

## Formulaire de devis

`site/devis.php` envoie la demande à contact@tlproprete.fr (expéditeur site@tlproprete.fr, réponse directe au client).
Protections : champ piège, délai minimal de 3 s, 6 demandes par heure et par adresse IP.
Si les demandes n'arrivent pas : dans Plesk > Mail, désactiver le service mail local du domaine
lorsque la boîte contact@ est hébergée ailleurs.

## Tests

```
npm i -D playwright            # une seule fois
BASE_URL=http://127.0.0.1:8080 node tests/shoot_pages.js desktop /,/contact/
node tests/shoot_intro.js mobile
node tests/test_form.js        # envoie une vraie demande : à lancer en local, pas sur le site en ligne
```

## À compléter

- Téléphone : `PHONE` et `PHONE_INTL` dans `content.py` (il s'affiche alors partout).
- Mentions légales : forme juridique, capital, SIRET, RCS, TVA, directeur de publication, hébergeur
  (surlignés en jaune dans `/mentions-legales/`).
- Vérifier la liste des communes (`ZONES`) et le détail des prestations.
- Droits d'utilisation de la photo de Lyon.
- Google Search Console : déclarer `https://www.tlproprete.fr/sitemap.xml`.
