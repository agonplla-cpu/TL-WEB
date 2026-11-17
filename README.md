# TL Propreté — site web

Source du site [www.tlproprete.fr](https://www.tlproprete.fr). Version 2 (novembre 2026) : typographie Archivo, photos à leur taille d'origine, sans intro zoom.
Site statique (HTML, CSS, JS) généré en Python, plus `devis.php` pour le formulaire de devis.

## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `site/` | Le site tel qu'il est publié : contenu du dossier `httpdocs` sur Plesk. |
| `generateur/` | `content.py` (textes, prestations, coordonnées, communes), `build.py` (génère les pages dans `site/`), `render_assets.js` (favicon, icône Apple, image de partage). |
| `tests/` | Scripts Playwright : captures des pages, test du formulaire. Les captures vont dans `captures/` (non versionné). |
| `outils/` | Chaîne de traitement des images : agrandissement Real-ESRGAN (`images/upscale.py`), retouche de la photo du hall (`images/retouch_hall.py`), vectorisation du logo (`logo/vectorize.py`). |

Pages publiées : accueil, 7 pages prestations, contact,
mentions légales, confidentialité, `/merci/`, `404.html`, `sitemap.xml`, `robots.txt`.

## Photos

N'utiliser que de vraies photos, à leur taille d'origine (photo prise au téléphone, pas une capture d'écran), sans agrandissement par IA.

Les photos de chantiers de l'accueil (`/assets/img/photos/p01` à `p13`) ne sont pas dans ce dépôt : elles ont été extraites sur le serveur depuis l'ancienne page `tlproprete_v5.html` et n'existent que dans `httpdocs`. Trois photos d'illustration libres de droit (licence Unsplash) s'y ajoutent : `s1-vitres.jpg`, `s2-hall.jpg`, `s3-bureaux.jpg`.

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
node tests/test_form.js        # envoie une vraie demande : à lancer en local, pas sur le site en ligne
```

## À compléter

- Vérifier la liste des communes (`ZONES`) et le détail des prestations.
- Droits d'utilisation de la photo de Lyon.
- Google Search Console : déclarer `https://www.tlproprete.fr/sitemap.xml`.
