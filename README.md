# HOMEOMED — nouveau site

Refonte moderne du site [homeomed.ch](https://homeomed.ch/) (Paola Orlando, homéopathe diplômée fédérale, Pully/Lausanne & Fribourg).

Site **statique** : HTML/CSS/JS sans framework ni dépendance. Il peut être hébergé tel quel sur n’importe quel hébergeur (Netlify, GitHub Pages, Infomaniak…).

## Structure

```
src/pages/*.html     ← contenu de chaque page (à modifier ici)
build.py             ← en-tête, menu, pied de page, avis Google, blocs réutilisables
assets/css/style.css ← design (couleurs, typographies, composants)
assets/js/main.js    ← menu mobile, carrousel, animations, cartes au clic
assets/img/          ← photos optimisées (WebP) et logos
assets/fonts/        ← polices auto-hébergées (DM Serif Display, Nunito Sans — licence OFL)
index.html, */index.html, sitemap.xml, robots.txt, _redirects  ← fichiers générés
```

## Modifier le site

1. Modifier le texte dans `src/pages/<page>.html` (ou le menu / pied de page dans `build.py`).
2. Régénérer : `python3 build.py`
3. Vérifier en local : `python3 -m http.server` puis ouvrir http://localhost:8000

Gabarits utilisables dans les pages : `{{rdv}}` (bouton rendez-vous), `{{cta}}`, `{{contact}}`, `{{reviews}}`, `{{disclaimer}}`, `{{icon:nom}}`, `{{phone}}`, `{{email}}`, `{{root}}`.

## Points forts

- Accueil au format « présentation des services » : héro plein écran, bandeau défilant, grille des accompagnements, aperçus en escalier vers chaque page.
- Mêmes adresses (URL) que l’ancien site WordPress → pas de perte de référencement ; redirections pour les anciennes pages légales.
- SEO : balises title/description, Open Graph, données structurées (MedicalBusiness, FAQPage), sitemap.
- Respect de la vie privée : aucune police Google, aucun traceur ; les cartes Google ne se chargent qu’au clic → plus besoin de bandeau cookies.
- Responsive (barre d’action « Appeler / Prendre RDV » sur mobile), accessible (navigation clavier, contrastes, `prefers-reduced-motion`).

## À valider par Paola avant mise en ligne

- **Nouveaux services** (textes rédigés, à relire) : `accompagnement-tdah`, `tcc-sommeil`, `bebe-allaitement-sommeil` — formations, format/durée des séances et **tarifs**.
- **Mentions légales & CGU** réécrites pour le nouveau site (l’ancien texte des CGU citait « Marie Pascale Rumeau » et l’ancienne déclaration de confidentialité un autre numéro : +41 21 566 16 25).
- FAQ : durée de la 1ère consultation harmonisée sur 75–90 min (l’ancienne FAQ indiquait « 1h30 » et des suivis d’« 1h00 », la page tarifs 45–60 min).
