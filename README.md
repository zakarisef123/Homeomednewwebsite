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
assets/fonts/        ← police auto-hébergée (Manrope — licence OFL)
index.html, */index.html, sitemap.xml, robots.txt, _redirects  ← fichiers générés
```

## Modifier le site

1. Modifier le texte dans `src/pages/<page>.html` (ou le menu / pied de page dans `build.py`).
2. Régénérer : `python3 build.py`
3. Vérifier en local : `python3 -m http.server` puis ouvrir http://localhost:8000

Gabarits utilisables dans les pages : `{{rdv}}` (bouton rendez-vous), `{{cta}}`, `{{contact}}`, `{{reviews}}`, `{{disclaimer}}`, `{{icon:nom}}`, `{{phone}}`, `{{email}}`, `{{root}}`.

## Points forts

- Accueil au format « présentation des services » : héro plein écran, bandeau défilant, grille des accompagnements, aperçus en escalier vers chaque page.
- Redirections 301 depuis les anciennes adresses (ancien site WordPress et anciennes pages de ce site) → pas de perte de référencement.
- SEO : balises title/description, Open Graph, données structurées (MedicalBusiness, FAQPage), sitemap.
- Respect de la vie privée : aucune police Google, aucun traceur ; les cartes Google ne se chargent qu’au clic → plus besoin de bandeau cookies.
- Responsive (barre d’action « Appeler / Prendre RDV » sur mobile), accessible (navigation clavier, contrastes, `prefers-reduced-motion`).

## À valider par Paola avant mise en ligne

- **Nouveaux services** (textes rédigés, à relire) : `accompagnement-tdah`, `tcc-sommeil`, `bebe-allaitement-sommeil` — formations, format/durée des séances et **tarifs**.
- **Mentions légales & CGU** réécrites pour le nouveau site (l’ancien texte des CGU citait « Marie Pascale Rumeau » et l’ancienne déclaration de confidentialité un autre numéro : +41 21 566 16 25).
- FAQ : durée de la 1ère consultation harmonisée sur 75–90 min (l’ancienne FAQ indiquait « 1h30 » et des suivis d’« 1h00 », la page tarifs 45–60 min).

## Deux cabinets = deux établissements pour Google

- Chaque page cabinet déclare son propre établissement (données structurées `MedicalBusiness`) : adresse, horaires, zone desservie, lien vers sa fiche Google Maps.
  - Pully : `/cabinet-pully/` — lun, mar, mer 8h–18h, ven 8h–13h — fiche `maps.google.com/?cid=4980652819741660907`
  - Fribourg : `/cabinet-fribourg/` — jeudi 9h–18h — fiche `maps.google.com/?cid=13756565993613354598`
- Les deux sont reliés à l’organisation HOMEOMED et à Paola Orlando.

**À régler dans Google Business Profile (par Paola) :**
1. Fiche **Pully** → Modifier le profil → Site web : `https://homeomed.ch/cabinet-pully/`
2. Fiche **Fribourg** → Site web : `https://homeomed.ch/cabinet-fribourg/`
3. Sur chaque fiche, lien de prise de rendez-vous : `https://homeomed.ch/prendre-rdv/`
4. Vérifier que les horaires des fiches sont identiques à ceux du site.

## Version anglaise (FR | EN)

- Pages anglaises : `src/pages-en/*.html` → générées sous `/en/` avec des adresses anglaises (`/en/about/`, `/en/homeopath-fribourg/`…).
- `i18n.py` : correspondance des adresses FR → EN et traductions des blocs communs (menus, pied de page, bandeaux, avis…).
  Dans les pages anglaises, on peut écrire les liens avec les adresses **françaises** (`{{root}}qui-suis-je/`) : ils sont convertis automatiquement.
- Chaque page déclare sa version dans l’autre langue (`hreflang`), le sélecteur **FR | EN** mène à la page équivalente, le sitemap liste les deux langues.
- Les avis Google restent dans leur langue d’origine (français), avec une mention ; les témoignages du site sont traduits avec la mention « translated from French ».
- Pour ajouter une page : créer la version FR dans `src/pages/`, la version EN dans `src/pages-en/`, et ajouter la paire d’adresses dans `PATHS` (`i18n.py`).

## Refonte 2026 : trois univers

Marque ombrelle **HOMEOMED · Paola Orlando** (logo sans « Homéopathe »), trois univers bien séparés :

| Univers | Adresses | Signature sous le logo |
|---|---|---|
| Homéopathie | `/homeopathie/` + `enfant-et-adolescent/`, `equilibre-feminin-et-hormonal/`, `orl-allergies-peau/`, `soins-support-oncologie/` | « Homéopathie » |
| Accompagnement parental | `/accompagnement-parental/` (page pivot) + `tdah-methode-barkley/`, `sommeil-enfant-0-3-ans/`, `allaitement/` | « Accompagnement parental » (couleur d’accent chaude) |
| Insomnie | `/insomnie-tcc-i/` | « Insomnie – TCC-i » |

- Menu unique : Accueil · Qui suis-je ? · Homéopathie ▾ · Accompagnement parental ▾ · Insomnie – TCC-i · Tarifs · Le cabinet ▾ · Blog · [Prendre RDV].
- Les pages parentales et insomnie n’affichent ni homéopathie, ni avis ; le pied de page et l’avertissement s’adaptent à l’univers (`"nav": "parent"` / `"insomnie"` / `"homeo"` dans le bloc meta).
- Accueil : trois cartes d’entrée sous le titre principal (`{{universes}}`).
- Redirections 301 (`REDIRECTS` dans `build.py`, fichier `_redirects` + pages de repli) : `/mes-specialites/…`, anciennes pages à la racine, `/tcc-sommeil/`, `/bebe-allaitement-sommeil/`, et leurs équivalents anglais.

### Style « Clinique » (refonte de novembre 2026)

Direction **A · Clinique** retenue parmi les trois maquettes du dossier `propositions/` (non indexé).

- **Charte homeomed.ch conservée** : bleu `#1C75BB`, turquoise `#69C3CB`, blanc, gris clair `#FAFAFA`, texte `#313131`
  (+ bleu nuit `#0b365a` dérivé du bleu pour les titres et les fonds sombres). Tokens en tête de `assets/css/style.css`.
- **Typographie** : Manrope (titres et texte), auto-hébergée.
- **Barre d'information** en haut (cabinets, horaires, e-mail, FR | EN), en-tête blanc avec « Secrétariat » et bouton « Prendre rendez-vous ».
- **Accueil** : photo du cabinet plein écran sous voile bleu, bandeau défilant des garanties, « Qui sommes-nous », grille des soins,
  parcours en 4 étapes, avis, praticienne, deux cabinets avec horaires, FAQ, bandeau RDV et logos.
- **Pages de soins** : un seul en-tête `phero` (photo plein cadre + voile bleu, texte blanc) pour toutes les pages ;
  la photo est celle indiquée dans `<img class="phero-bg">` en tête de chaque page.
- Les styles de la refonte sont regroupés à la fin de `style.css` (« REFONTE 2026 · CLINIQUE » et « Accueil Clinique »).

### Prise de rendez-vous : uniquement OneDoc

- Tous les boutons « Prendre rendez-vous » mènent à `/prendre-rdv/`, qui affiche directement le calendrier OneDoc (`ONEDOC` dans `build.py`).
- Plus de formulaire : l'ancien tunnel « Rendez-vous express » est supprimé. Les marqueurs `{{funnel…}}` encore présents
  dans les pages affichent désormais le bandeau d'appel à l'action (`cta_band`).

### Programme Barkley® (page TDAH) : prête, pas encore publiée

`BARKLEY_LIVE = False` en haut de `build.py`. Tant que la formation n’est pas terminée, la page
`/accompagnement-parental/tdah-methode-barkley/` existe mais est en **noindex**, hors sitemap et hors menu ; la page pivot affiche « Bientôt ».

Une fois la formation terminée : mettre `BARKLEY_LIVE = True`, compléter l’âge / le rythme / le contenu des séances si besoin, puis `python3 build.py`.
La page est alors indexée et ajoutée au menu, au pied de page et aux tarifs ; l’ancienne page homéopathique `/accompagnement-tdah/` est redirigée (301) vers elle.
Dans les pages, `<!--IF:barkley-->…<!--ENDIF:barkley-->` et `<!--IFNOT:barkley-->…<!--ENDIFNOT:barkley-->` affichent un contenu selon ce réglage.

Bouton « Réserver mon appel découverte gratuit » : `APPEL_URL` dans `build.py` (actuellement la page Prendre RDV ; à remplacer par le lien OneDoc dédié).

### Photos à remplacer (même nom de fichier, format WebP)

Copies provisoires d’images existantes, à écraser par les photos définitives :

- `assets/img/tdah-hero.webp` — en-tête TDAH : parent et enfant qui rient, lisent ou cuisinent ensemble, lumière naturelle.
- `assets/img/paola-parental.webp` — photo professionnelle de Paola, souriante, au cabinet.
- `assets/img/parental-hero.webp` — en-tête de la page pivot.
- `assets/img/sommeil-enfant.webp`, `assets/img/allaitement.webp` — pages Sommeil 0–3 ans et Allaitement.
- Section 2 de la page TDAH : illustration provisoire d’un tableau de motivation (SVG) ; idéalement une photo de votre propre tableau.

### À faire ensuite

- Textes définitifs Sommeil 0–3 ans et Allaitement (textes actuels repris de l’ancienne page, sans homéopathie).
- Landing pages publicitaires `/lp/…` (noindex, sans menu).

### Améliorations de novembre 2026 (audit design)

- **Accueil** : nouvel en-tête « La praticienne » (portrait de Paola, titre « Homéopathe diplômée fédérale à Pully, Lausanne et Fribourg »),
  bandeau de garanties fixe (plus de défilement), note Google affichée une seule fois, encadré « Votre praticienne » sans photo en double.
- **Prendre RDV** : en-tête réduit, prix / remboursement / annulation et les trois lieux affichés juste au-dessus du calendrier OneDoc.
- **Mobile** : WhatsApp intégré à la barre du bas (Appeler · WhatsApp · Prendre RDV), plus de bulle flottante qui cache le texte.
- **Accessibilité** : turquoise foncé `#257880` pour le texte (5,1:1), badges bleus plus foncés, cibles FR | EN et liens du pied de page agrandis,
  niveaux de titres corrigés (pied de page en `h2`, bloc contact en `h3`), contenu toujours visible même avant l'animation d'apparition.
- **SEO** : H1, titres et méta-descriptions de l'accueil, Homéopathie, Qui suis-je ? et Insomnie réécrits avec le métier et les villes (FR + EN).
- **À vérifier par Paola** : l'adresse de Fribourg sur OneDoc (« Avenue de la Gare 1 » ?) doit être identique à celle du site (« Rue de la Banque 4 »).
