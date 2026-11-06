#!/usr/bin/env python3
"""
Générateur statique du site HOMEOMED.

Usage :  python3 build.py

- Les contenus des pages sont dans  src/pages/*.html
  La première ligne de chaque fichier est un commentaire JSON :
  <!--meta {"title": "...", "description": "...", "path": "qui-suis-je/", "nav": "about"} -->
- L'en-tête, le pied de page et les blocs réutilisables sont définis ici.
- Les pages sont générées dans le dossier racine (ex. qui-suis-je/index.html),
  avec des liens relatifs : le site fonctionne sur n'importe quel hébergeur statique.

Aucune dépendance externe (Python 3.8+).
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "pages"
SITE_URL = "https://homeomed.ch/"

PHONE = "+41 (0)21 566 18 15"
PHONE_LINK = "tel:+41215661815"
EMAIL = "secretariat@homeomed.ch"
WHATSAPP = "https://wa.me/41767076648"
ONEDOC = "https://onedoc.ch/fr/widget/2bf549600bbfd938215e1c9f4103cc3351c24342abb15eabe0229ff39ecb2835"
GOOGLE_REVIEWS = "https://search.google.com/local/reviews?placeid=ChIJa587Df0vjEcR69Y_1lnVHkU"
GOOGLE_WRITE_REVIEW = "https://search.google.com/local/writereview?placeid=ChIJa587Df0vjEcR69Y_1lnVHkU"
MAP_PULLY = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2745.8486027979893!2d6.657421112157884!3d46.51110716286125!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x478c2ffd0d3b9f6b%3A0x451ed559d63fd6eb!2sCabinet%20HOMEOMED%20-%20Paola%20ORLANDO!5e0!3m2!1sfr!2sch!4v1752832729991!5m2!1sfr!2sch"
MAP_FRIBOURG = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d10924.077428576657!2d7.1357336871582016!3d46.8039246!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x478e6934385efac9%3A0xbee923e2c28ae666!2sCabinet%20HOMEOMED%20Paola%20Orlando%20Hom%C3%A9opathe%20Fribourg!5e0!3m2!1sfr!2sch!4v1781771720679!5m2!1sfr!2sch"
GMAPS_PULLY = "https://www.google.com/maps/search/?api=1&query=Place+Neuve+1+1009+Pully"
GMAPS_FRIBOURG = "https://www.google.com/maps/search/?api=1&query=Rue+de+la+Banque+4+1700+Fribourg"
FACEBOOK = "https://www.facebook.com/profile.php?id=61577642218751"
INSTAGRAM = "https://www.instagram.com/paolaorlando_homeopathe/"
LINKEDIN = "https://www.linkedin.com/in/paola-orlando-560369a1/"

# --------------------------------------------------------------------------
# Icônes (traits 1.8px, style "line")
# --------------------------------------------------------------------------
_P = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="3"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>',
    "phone": '<path d="M5 4h3.5l1.7 4.3-2.2 1.4a11 11 0 0 0 6.3 6.3l1.4-2.2L20 15.5V19a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "chevron": '<path d="M6 9l6 6 6-6"/>',
    "child": '<circle cx="12" cy="5.5" r="2.5"/><path d="M8 21v-5l-2-1 1.5-5h9L18 15l-2 1v5M10 21v-4h4v4"/>',
    "flower": '<circle cx="12" cy="12" r="2.5"/><path d="M12 9.5C10 6 10.5 3 12 3s2 3 0 6.5zM12 14.5c2 3.5 1.5 6.5 0 6.5s-2-3 0-6.5zM9.5 12C6 14 3 13.5 3 12s3-2 6.5 0zM14.5 12c3.5-2 6.5-1.5 6.5 0s-3 2-6.5 0z"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19l8-8"/>',
    "wind": '<path d="M3 8h11a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h7"/>',
    "ribbon": '<path d="M12 3a4 4 0 0 0-4 4c0 2.5 2 5 4 7.5 2-2.5 4-5 4-7.5a4 4 0 0 0-4-4z"/><path d="M9.5 12L6 21l3-1.5L10.5 22 14.5 12"/><path d="M14.5 12L18 21l-3-1.5"/>',
    "heart": '<path d="M12 20s-7.5-4.6-9.3-9.2C1.5 7.6 3.6 4.5 7 4.5c2 0 3.4 1.1 5 3 1.6-1.9 3-3 5-3 3.4 0 5.5 3.1 4.3 6.3C19.5 15.4 12 20 12 20z"/>',
    "brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 3V4zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 3V4z"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
    "alert": '<path d="M12 3l9.5 17h-19L12 3z"/><path d="M12 10v4.5M12 17.5v.5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    "walk": '<circle cx="13" cy="4.5" r="2"/><path d="M10 21l2-6-2.5-2.5L11 8l3 3 3 1M9.5 12.5L7 14"/><path d="M14 15l2 6"/>',
    "car": '<path d="M5 17h14v-4l-2-5H7l-2 5v4z"/><circle cx="8" cy="17" r="1.8"/><circle cx="16" cy="17" r="1.8"/><path d="M5 13h14"/>',
    "bus": '<rect x="5" y="3" width="14" height="15" rx="3"/><path d="M5 11h14M8 21v-3M16 21v-3"/><circle cx="8.5" cy="14.5" r=".8"/><circle cx="15.5" cy="14.5" r=".8"/>',
    "train": '<rect x="6" y="3" width="12" height="13" rx="3"/><path d="M6 10h12M9 20l-2 2M15 20l2 2M9 20h6"/><circle cx="9.5" cy="13" r=".8"/><circle cx="14.5" cy="13" r=".8"/>',
    "elevator": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M12 3v18M7.5 10L9 8l1.5 2M13.5 14L15 16l1.5-2"/>',
    "video": '<rect x="3" y="6" width="13" height="12" rx="2.5"/><path d="M16 10.5l5-3v9l-5-3"/>',
    "cash": '<rect x="2.5" y="6" width="19" height="12" rx="2.5"/><circle cx="12" cy="12" r="2.5"/><path d="M6 9.5v5M18 9.5v5"/>',
    "card": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19M6 15h4"/>',
    "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
    "book": '<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H20v15H5.5A1.5 1.5 0 0 0 4 19.5z"/><path d="M4 19.5A1.5 1.5 0 0 0 5.5 21H20"/>',
    "quote": '<path d="M7 7h4v4c0 3-1.5 5-4 6M14 7h4v4c0 3-1.5 5-4 6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
    "steps": '<path d="M4 20h4v-4h4v-4h4V8h4"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1-3.5 3.5-5.5 6.5-5.5s5.5 2 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14.8c1.8.7 3 2.4 3.5 5.2"/>',
    "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
}
_SOLID = {
    "whatsapp": '<path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.7 11.7 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/>',
    "facebook": '<path fill="currentColor" d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4a21 21 0 0 0-2.3-.1c-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1z"/>',
    "instagram": '<path fill="currentColor" d="M12 7.3A4.7 4.7 0 1 0 16.7 12 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 3-3 3 3 0 0 1-3 3zm4.9-8.9a1.1 1.1 0 1 0 1.1 1.1 1.1 1.1 0 0 0-1.1-1.1zM21 8.2a5.6 5.6 0 0 0-1.5-3.7A5.6 5.6 0 0 0 15.8 3C14.3 3 9.7 3 8.2 3a5.6 5.6 0 0 0-3.7 1.5A5.6 5.6 0 0 0 3 8.2C3 9.7 3 14.3 3 15.8a5.6 5.6 0 0 0 1.5 3.7A5.6 5.6 0 0 0 8.2 21c1.5.1 6.1.1 7.6 0a5.6 5.6 0 0 0 3.7-1.5 5.6 5.6 0 0 0 1.5-3.7c.1-1.5.1-6.1 0-7.6zm-2 9.3a3 3 0 0 1-1.7 1.7c-1.2.5-4 .4-5.3.4s-4.1.1-5.3-.4a3 3 0 0 1-1.7-1.7c-.5-1.2-.4-4-.4-5.3s-.1-4.1.4-5.3A3 3 0 0 1 6.7 5.2C7.9 4.7 10.7 4.8 12 4.8s4.1-.1 5.3.4A3 3 0 0 1 19 6.9c.5 1.2.4 4 .4 5.3s.1 4.1-.4 5.3z"/>',
    "linkedin": '<path fill="currentColor" d="M6.9 8.8H3.8V20h3.1V8.8zM5.3 3.8a1.8 1.8 0 1 0 1.8 1.8 1.8 1.8 0 0 0-1.8-1.8zM20 13.6c0-3-.6-5.1-4.1-5.1a3.6 3.6 0 0 0-3.2 1.8V8.8h-3V20h3.1v-5.5c0-1.5.3-2.9 2.1-2.9s1.8 1.7 1.8 3V20H20z"/>',
    "google": '<path fill="#4285F4" d="M21.6 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3z"/><path fill="#34A853" d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22z"/><path fill="#FBBC05" d="M6.4 14a6 6 0 0 1 0-3.9V7.5H3.1a10 10 0 0 0 0 9z"/><path fill="#EA4335" d="M12 6c1.5 0 2.8.5 3.8 1.5l2.9-2.9A10 10 0 0 0 3.1 7.5L6.4 10C7.2 7.8 9.4 6 12 6z"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    if name in _SOLID:
        return f'<svg{c} viewBox="0 0 24 24" aria-hidden="true" focusable="false">{_SOLID[name]}</svg>'
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_P[name]}</svg>')


# --------------------------------------------------------------------------
# Avis Google (textes d'origine)
# --------------------------------------------------------------------------
REVIEWS = [
    ("Nicole Klaus", "il y a 1 an", "Madame Paola Orlando, homéopathe, me suit depuis plusieurs années. Au mois de février de cette année 2025, on m’a diagnostiqué un cancer du sein. Madame Orlando a dressé un protocole précis et essentiel ciblé sur mon cancer. Au fur et à mesure que j’avance dans un traitement chimiothérapeutique, elle réadapte mon protocole afin que les médicaments qu’elle me prescrit correspondent à l’état sans cesse en mouvement de mon corps physique mais aussi de mon état psychique. Sur ce parcours, Madame Orlando ne m’a jamais dissuadée de suivre le protocole allopathique classique ; au contraire, elle m’y a encouragée et continue de le faire. Aujourd’hui je tiens vraiment et de tout mon cœur à remercier Madame Orlando de son professionnalisme, de ses formidables compétences, mais aussi de sa disponibilité, de sa générosité d’écoute, de son attention profonde et sincère. Elle est passionnée par son métier."),
    ("Isabelle Blatter", "il y a 10 mois", "Arrivée chez Madame Orlando tout par hasard et on dit : le hasard fait bien les choses. Je ne peux que confirmer cela. J’ai été curieuse de voir ce que l’homéopathie pourrait apporter à notre fille de 7 ans. Madame Orlando s’est montrée très à l’écoute, toujours disponible et très professionnelle. On connaît tous l’arnica ;-), mais l’homéopathie est bien plus complexe que cela, surtout personnalisée pour chacun d’entre nous et EFFICACE ! Enfin, une adresse que je vais précieusement garder. Merci Madame Orlando d’être d’une bienveillance rare et de vos conseils !"),
    ("Julian S.", "il y a 11 mois", "Paola est une femme bienveillante, à l’écoute, passionnée et investie. Très à l’aise avec les enfants, elle permet un complément parfait au suivi pédiatrique. Très disponible et prenant son travail très à cœur, je ne peux que la recommander !"),
    ("Solene Montloin", "il y a 11 mois", "Paola Orlando me suit depuis 1 an et demi maintenant et je vois une nette amélioration sur mes angoisses et mon stress, qui étaient très présents. Elle est très à l’écoute et prend son rôle à cœur. Elle trouve le traitement parfait pour chaque besoin. Je la recommande vivement."),
    ("Mallika Nadesan", "il y a 12 mois", "Mme Orlando a pris en charge la santé de mon bébé, un grand prématuré né à 29 semaines, avec beaucoup de bienveillance, d’écoute et de sérieux. Elle a su le guérir de maux de ventre, dont il souffrait depuis la naissance. Aussi, je vous recommande sincèrement cette homéopathe solaire et intelligente."),
    ("Sophie Castex", "il y a 12 mois", "J’ai eu la grande chance d’être suivie par Mme Orlando Paola avant de devoir débuter une chimiothérapie. Cet accompagnement (sur la base d’une anamnèse complète et détaillée de votre parcours de santé et votre vécu) a fait pour moi toute la différence et m’a permis de traverser cette étape sans les effets secondaires connus tels les nausées/vomissements, paresthésies etc… de ce traitement lourd. Ça a été pour moi un accompagnement important et efficace que je conseille vivement ! Et dès le premier moment, vous savez que vous avez affaire à quelqu’un d’extrêmement professionnelle, consciencieuse et humaine."),
    ("Laurianne Demarliere", "il y a 1 an", "Une praticienne exceptionnelle, à l’écoute et bienveillante. Elle prend vraiment le temps de comprendre, sans jugement, avec une grande humanité. Ses conseils m’ont énormément aidée à retrouver un équilibre dans ma santé de femme. Je la recommande du fond du cœur. Merci à vous Paola !!!"),
    ("Cécile Theumann", "il y a 5 ans", "J’ai beaucoup apprécié la grande écoute de Paola, et son empathie. Elle cherche tous les détails auxquels on ne penserait pas dans une approche globale du problème, qui s’est avéré dans mon cas très utile et bénéfique. Mille mercis Paola, je vais vraiment mieux."),
    ("Hardy Virdee", "il y a 5 ans", "Paola est vraiment professionnelle. Elle a écouté attentivement mes besoins et a abordé mon problème dans sa globalité, en examinant tous les détails de ma vie, ce qui m’a aidée à trouver la solution la plus adaptée à mes besoins. Merci beaucoup, Paola."),
]


def review_card(name, when, text):
    initials = "".join(p[0] for p in name.replace(".", "").split()[:2]).upper()
    if len(text) > 330:
        cut = text.rfind(". ", 0, 300) + 1 or 300
        body = (f"<p>{text[:cut]}</p><details><summary>Lire la suite</summary><p>{text[cut:].strip()}</p></details>")
    else:
        body = f"<p>{text}</p>"
    return f"""<article class="review">
  <div class="stars" aria-label="5 étoiles sur 5">★★★★★</div>
  {body}
  <div class="who"><span class="avatar" aria-hidden="true">{initials}</span><div><strong>{name}</strong><span>Avis Google · {when}</span></div></div>
</article>"""


def reviews_block():
    cards = "\n".join(review_card(*r) for r in REVIEWS)
    return f"""<section class="section bg-sand" aria-labelledby="avis-title">
  <div class="container">
    <div class="carousel" data-carousel>
      <div class="reviews-head">
        <div>
          <span class="eyebrow">Témoignages</span>
          <h2 id="avis-title" class="mb-0">Ce qu’ils en pensent</h2>
        </div>
        <div class="btn-row">
          <a class="rating-box" href="{GOOGLE_REVIEWS}" target="_blank" rel="noopener" style="text-decoration:none">
            {icon("google", "g-logo")}
            <span class="score">4.9</span>
            <span class="meta"><span class="stars">★★★★★</span><br>Basé sur 17 avis Google</span>
          </a>
          <div class="carousel-nav">
            <button type="button" data-prev aria-label="Avis précédents">{icon("arrow-left")}</button>
            <button type="button" data-next aria-label="Avis suivants">{icon("arrow")}</button>
          </div>
        </div>
      </div>
      <div class="carousel-track" tabindex="0" aria-label="Avis de patients">
{cards}
      </div>
      <p class="small muted mt-1"><a href="{GOOGLE_WRITE_REVIEW}" target="_blank" rel="noopener">Donner votre avis sur Google</a></p>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------
# Blocs réutilisables
# --------------------------------------------------------------------------
def rdv_btn(root, label="Je prends rendez-vous", cls="btn btn-primary"):
    return f'<a class="{cls}" href="{root}prendre-rdv/">{icon("calendar")}{label}</a>'


def hours_list():
    rows = [("Lundi", "8h – 18h"), ("Mardi", "8h – 18h"), ("Mercredi", "8h – 18h"),
            ("Jeudi", "8h – 18h <small>(Fribourg)</small>"), ("Vendredi", "8h – 13h"),
            ("Samedi", None), ("Dimanche", None)]
    out = []
    for d, h in rows:
        out.append(f'<li><span>{d}</span><span>{h}</span></li>' if h else
                   f'<li class="closed"><span>{d}</span><span>Fermé</span></li>')
    return '<ul class="hours">' + "".join(out) + "</ul>"


def cta_band(root, title="Et si on commençait&nbsp;?",
             text="La première consultation permet de poser les bases d’un suivi structuré et individualisé. Je vous reçois à Pully/Lausanne et tous les jeudis à Fribourg."):
    return f"""<section class="section tight">
  <div class="container">
    <div class="cta-band reveal">
      <div>
        <h2>{title}</h2>
        <p>{text}</p>
      </div>
      <div class="btn-row">
        {rdv_btn(root, "Prendre rendez-vous", "btn btn-light")}
        <a class="btn btn-outline-light" href="{PHONE_LINK}">{icon("phone")}{PHONE}</a>
      </div>
    </div>
  </div>
</section>"""


def contact_block(root):
    return f"""<section class="section bg-white" aria-labelledby="contact-title">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow center">Contact</span>
      <h2 id="contact-title">Comment me contacter&nbsp;?</h2>
      <p>Prise de rendez-vous en ligne 24h/24, par téléphone ou par e-mail. Si je suis en consultation, laissez un message&nbsp;: je vous rappelle dès que possible.</p>
    </div>
    <div class="contact-grid">
      <div class="contact-item reveal">
        <div class="icon-badge">{icon("phone")}</div>
        <h4>Téléphone</h4>
        <p><a href="{PHONE_LINK}">{PHONE}</a></p>
      </div>
      <div class="contact-item reveal d1">
        <div class="icon-badge">{icon("mail")}</div>
        <h4>E-mail</h4>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div class="contact-item reveal d2">
        <div class="icon-badge">{icon("pin")}</div>
        <h4>Cabinets</h4>
        <p><a href="{root}cabinet-pully/">Place Neuve 1, 1009 Pully</a><br><a href="{root}cabinet-fribourg/">Centre ITS – Rue de la Banque 4, 1700 Fribourg</a></p>
      </div>
      <div class="contact-item reveal d3">
        <div class="icon-badge">{icon("clock")}</div>
        <h4>Horaires</h4>
        <p>Lun – Jeu&nbsp;: 8h – 18h<br>Vendredi&nbsp;: 8h – 13h<br><span class="muted">Sur rendez-vous uniquement</span></p>
      </div>
    </div>
  </div>
</section>"""


def disclaimer():
    return f"""<div class="disclaimer">{icon("info")}<div><strong>Informations importantes.</strong> L’homéopathie est une médecine complémentaire. Elle ne remplace en aucun cas les traitements médicaux prescrits, ni la consultation d’un médecin ou d’un spécialiste. En cas de doute ou d’urgence, veuillez contacter votre professionnel de santé.</div></div>"""


# --------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------
# Catalogue des services : source unique pour le menu, l'accueil et le pied de page.
# Chaque service : page, libellés, description, icône, image, sous-services (ancres
# dans la page ou autres pages) et services liés.
SERVICES = [
    dict(path="enfant-et-adolescent/", short="Enfant & Ado", title="Bébé, enfant & adolescent", icon="child",
         img="spec-enfant.webp", tagline="Dès la naissance, jusqu’à 18 ans",
         desc="Otites à répétition, sommeil, digestion, eczéma, dentition, comportement, acné et troubles hormonaux de l’ado.",
         subs=[("Nouveau-né & bébé", "#bebe", "Coliques, reflux, sommeil, dentition"),
               ("Enfant", "#enfant", "ORL, peau, sommeil, digestion, concentration"),
               ("Adolescent", "#ado", "Acné, allergies, cycles, fatigue, émotions"),
               ("Questions fréquentes", "#faq", "")],
         related=[("Accompagnement TDAH", "accompagnement-tdah/"), ("Bébé : allaitement & sommeil", "bebe-allaitement-sommeil/")]),
    dict(path="equilibre-feminin-et-hormonal/", short="Femme & hormones", title="Équilibre féminin & hormonal", icon="flower",
         img="spec-femme.webp", tagline="Toutes les étapes de la vie hormonale",
         desc="Cycles douloureux, SOPK, endométriose, fertilité, grossesse, post-partum, ménopause, thyroïde.",
         subs=[("Cycles & douleurs menstruelles", "#cycles", "Règles douloureuses, SPM, cycles irréguliers"),
               ("SOPK & endométriose", "#sopk", "Douleurs pelviennes, cycles longs"),
               ("Fertilité & désir de grossesse", "#fertilite", "Projet bébé, PMA, stimulation"),
               ("Grossesse & post-partum", "#grossesse", "Nausées, accouchement, baby-blues"),
               ("Préménopause & ménopause", "#menopause", "Bouffées de chaleur, sommeil, humeur"),
               ("Thyroïde & métabolisme", "#thyroide", "Hypo/hyperthyroïdie, poids, fatigue")],
         related=[("Bébé : allaitement & sommeil", "bebe-allaitement-sommeil/"), ("TCC du sommeil", "tcc-sommeil/")]),
    dict(path="orl-allergies-peau/", short="ORL · Allergies · Peau", title="ORL, allergies, peau", icon="wind",
         img="spec-orl.webp", tagline="Chez l’enfant et l’adulte",
         desc="Eczéma, psoriasis, urticaire, rhume des foins, asthme, otites, sinusites.",
         subs=[("Peau : eczéma, psoriasis, urticaire", "#peau", "Démangeaisons, poussées, sommeil perturbé"),
               ("Allergies saisonnières", "#allergies", "Pollen, acariens, animaux, conjonctivites"),
               ("Infections ORL à répétition", "#infections-orl", "Otites, angines, sinusites, rhinites"),
               ("Asthme & troubles respiratoires", "#asthme", "Toux nocturne, essoufflement"),
               ("Questions fréquentes", "#faq", "")],
         related=[("Enfant & adolescent", "enfant-et-adolescent/")]),
    dict(path="homeopathie-soins-support-oncologie/", short="Oncologie", title="Soins de support en oncologie", icon="ribbon",
         img="spec-onco.webp", tagline="En complément de l’équipe médicale",
         desc="Pendant et après les traitements contre le cancer, pour mieux traverser les effets secondaires.",
         subs=[("Pendant les traitements", "#pendant", "Chimio, radio, hormonothérapie, immunothérapie"),
               ("Après les traitements", "#apres", "Récupération, énergie, retour au quotidien"),
               ("Formations & recherche", "#formations", "Gustave Roussy, SHISSO, publications"),
               ("Questions fréquentes", "#faq", "")],
         related=[("Mon histoire : mon papa, mon héros", "soin-de-support-en-oncologie-histoire-personnelle/"), ("TCC du sommeil", "tcc-sommeil/")]),
    dict(path="accompagnement-tdah/", short="TDAH", title="Accompagnement TDAH", icon="brain", new=True,
         img="tdah-accompagnement.webp", tagline="Enfant, parents & famille",
         desc="Un accompagnement en trois volets : l’enfant, les parents et toute la famille.",
         subs=[("Pour l’enfant", "#enfant", "Attention, agitation, sommeil, émotions"),
               ("Pour les parents", "#parents", "Écoute, repères concrets, fatigue"),
               ("Pour la famille", "#famille", "Apaiser les tensions, retrouver un rythme"),
               ("Questions fréquentes", "#faq", "")],
         related=[("Article : TDAH & homéopathie", "tdah-homeopathie-accompagnement-individualise/"), ("Enfant & adolescent", "enfant-et-adolescent/")]),
    dict(path="tcc-sommeil/", short="Sommeil", title="TCC du sommeil", icon="moon", new=True,
         img="onco-apres.webp", tagline="Thérapie comportementale et cognitive de l’insomnie",
         desc="Endormissement difficile, réveils nocturnes : retrouver des nuits réparatrices durablement.",
         subs=[("Pour qui ?", "#pour-qui", "Insomnie, réveils nocturnes, fatigue"),
               ("La méthode en 3 étapes", "#methode", "Évaluer, ajuster, apaiser le mental"),
               ("Questions fréquentes", "#faq", "")],
         related=[("Bébé : allaitement & sommeil", "bebe-allaitement-sommeil/"), ("Équilibre féminin & hormonal", "equilibre-feminin-et-hormonal/")]),
    dict(path="bebe-allaitement-sommeil/", short="Bébé & allaitement", title="Bébé : allaitement & sommeil", icon="heart", new=True,
         img="enfant-bebe.webp", tagline="Soutien aux mamans et aux tout-petits",
         desc="Soutenir les mamans dans l’allaitement et accompagner le sommeil du tout-petit.",
         subs=[("Allaitement", "#allaitement", "Douleurs, production de lait, tétées, sevrage"),
               ("Sommeil de bébé", "#sommeil-bebe", "Réveils, endormissement, rituels"),
               ("Questions fréquentes", "#faq", "")],
         related=[("Nouveau-né & bébé", "enfant-et-adolescent/#bebe"), ("Grossesse & post-partum", "equilibre-feminin-et-hormonal/#grossesse")]),
    dict(path="mes-specialites/#complementaires", short="Autres troubles", title="Autres accompagnements", icon="bolt",
         img="famille.webp", tagline="Chronique, neurologique, urgences",
         desc="Fatigue et stress chroniques, troubles digestifs, migraines, vertiges, urgences homéopathiques.",
         subs=[("Déséquilibres métaboliques chroniques", "", "Fatigue, stress, digestion, auto-immunité"),
               ("Troubles neurologiques", "", "Migraines, vertiges, tremblements"),
               ("Urgences homéopathiques", "", "Fièvre, otites, cystites, gastro, toux")],
         related=[("Toutes mes spécialités", "mes-specialites/"), ("Tarifs : urgence homéo", "tarifs-remboursements/")]),
]
# Compatibilité (pied de page, etc.)
SPECIALTIES = [(s["path"], s["title"], s["tagline"], s["icon"]) for s in SERVICES[:4]]
NEW_SERVICES = [(s["path"], s["title"], s["tagline"], s["icon"]) for s in SERVICES[4:7]]


def svc_href(root, svc, href):
    base = svc["path"].split("#")[0]
    if href.startswith("#"):
        return f"{root}{base}{href}"
    return f"{root}{href or svc['path']}"


def services_bar(root, nav_path):
    items = []
    for i, s in enumerate(SERVICES):
        cur = ' aria-current="page"' if nav_path and s["path"].split("#")[0] == nav_path else ""
        new = '<span class="dot-new" aria-label="nouveau"></span>' if s.get("new") else ""
        subs = "".join(
            f'<li><a href="{svc_href(root, s, h)}"><strong>{t}</strong>{f"<span>{d}</span>" if d else ""}</a></li>'
            for t, h, d in s["subs"])
        rel = "".join(f'<li><a href="{root}{h}">{icon("arrow")}{t}</a></li>' for t, h in s["related"])
        align = " right" if i >= len(SERVICES) - 3 else ""
        items.append(f"""<li class="svc-item{align}">
  <a class="svc-link" href="{root}{s['path']}"{cur}>{icon(s['icon'])}<span>{s['short']}</span>{new}{icon('chevron', 'chev')}</a>
  <div class="svc-panel" role="group" aria-label="{s['title']}">
    <div class="svc-panel-intro">
      <img src="{root}assets/img/{s['img']}" alt="" loading="lazy">
      <span class="eyebrow">{s['tagline']}</span>
      <h3>{s['title']}{' <span class="badge-new">Nouveau</span>' if s.get('new') else ''}</h3>
      <p>{s['desc']}</p>
      <a class="btn btn-primary btn-sm" href="{root}{s['path']}">Voir la page</a>
    </div>
    <div class="svc-panel-links">
      <p class="svc-panel-label">Ce que j’accompagne</p>
      <ul class="svc-subs">{subs}</ul>
      <p class="svc-panel-label">Services liés</p>
      <ul class="svc-related">{rel}</ul>
    </div>
  </div>
</li>""")
    return f"""<div class="svc-bar">
  <div class="container wide">
    <ul class="svc-list" aria-label="Mes services">
      {''.join(items)}
    </ul>
  </div>
</div>"""


def mobile_services(root):
    out = []
    for s in SERVICES:
        links = "".join(f'<li><a href="{svc_href(root, s, h)}">{t}</a></li>' for t, h, _ in s["subs"])
        rel = "".join(f'<li><a class="rel" href="{root}{h}">{t}</a></li>' for t, h in s["related"])
        new = ' <span class="badge-new">Nouveau</span>' if s.get("new") else ""
        out.append(f"""<details class="m-svc">
  <summary>{icon(s['icon'])}<span>{s['title']}{new}</span>{icon('chevron', 'chev')}</summary>
  <ul><li><a class="all" href="{root}{s['path']}">Voir la page {s['title']}</a></li>{links}{rel}</ul>
</details>""")
    return '<div class="mobile-services"><p class="svc-panel-label">Mes services</p>' + "".join(out) + "</div>"


# --------------------------------------------------------------------------
# Blocs « services » pour les propositions d'accueil
# --------------------------------------------------------------------------
def svc_tiles(root):
    """Proposition A — mosaïque : chaque service en tuile photo + sous-services."""
    out = []
    for i, s in enumerate(SERVICES):
        chips = "".join(f'<li><a href="{svc_href(root, s, h)}">{t}</a></li>'
                        for t, h, _ in s["subs"] if t != "Questions fréquentes")
        new = '<span class="badge-new">Nouveau</span>' if s.get("new") else ""
        out.append(f"""<article class="svc-tile reveal d{i % 4}">
  <a class="svc-tile-img" href="{root}{s['path']}" tabindex="-1" aria-hidden="true"><img src="{root}assets/img/{s['img']}" alt="" loading="lazy">{new}</a>
  <div class="svc-tile-body">
    <h3><a href="{root}{s['path']}">{icon(s['icon'])}{s['title']}</a></h3>
    <p>{s['desc']}</p>
    <ul class="svc-chips">{chips}</ul>
    <a class="preview-link" href="{root}{s['path']}">Voir la page {icon('arrow')}</a>
  </div>
</article>""")
    return '<div class="svc-tiles">' + "".join(out) + "</div>"


def svc_tabs(root):
    """Proposition B — explorateur : liste des services + panneau détaillé."""
    tabs, panels = [], []
    for i, s in enumerate(SERVICES):
        sel = "true" if i == 0 else "false"
        new = ' <span class="dot-new" aria-label="nouveau"></span>' if s.get("new") else ""
        tabs.append(f'<button class="svc-tab" role="tab" id="tab-{i}" aria-controls="panel-{i}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{icon(s["icon"])}<span>{s["title"]}</span>{new}</button>')
        subs = "".join(f'<li><a href="{svc_href(root, s, h)}"><strong>{t}</strong>{f"<span>{d}</span>" if d else ""}</a></li>'
                       for t, h, d in s["subs"] if t != "Questions fréquentes")
        rel = "".join(f'<a class="chip-link" href="{root}{h}">{t}</a>' for t, h in s["related"])
        panels.append(f"""<div class="svc-tabpanel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}"{'' if i == 0 else ' hidden'}>
  <div class="svc-tabpanel-media"><img src="{root}assets/img/{s['img']}" alt="" loading="{'eager' if i == 0 else 'lazy'}"></div>
  <div class="svc-tabpanel-body">
    <span class="eyebrow">{s['tagline']}</span>
    <h3>{s['title']}{' <span class="badge-new">Nouveau</span>' if s.get('new') else ''}</h3>
    <p class="muted">{s['desc']}</p>
    <ul class="svc-subs two">{subs}</ul>
    <div class="svc-rel"><span>Services liés&nbsp;:</span>{rel}</div>
    <div class="btn-row mt-1"><a class="btn btn-primary" href="{root}{s['path']}">Voir la page</a>{rdv_btn(root, "Prendre rendez-vous", "btn btn-ghost")}</div>
  </div>
</div>""")
    return f"""<div class="svc-explorer" data-tabs>
  <div class="svc-tablist" role="tablist" aria-label="Mes services">{''.join(tabs)}</div>
  <div class="svc-tabpanels">{''.join(panels)}</div>
</div>"""


PROFILES = [
    ("child", "Mon bébé", "0 – 2 ans", ["enfant-et-adolescent/#bebe", "bebe-allaitement-sommeil/", "orl-allergies-peau/"]),
    ("users", "Mon enfant, mon ado", "3 – 18 ans", ["enfant-et-adolescent/", "accompagnement-tdah/", "orl-allergies-peau/"]),
    ("flower", "Moi, en tant que femme", "Cycles, grossesse, ménopause", ["equilibre-feminin-et-hormonal/", "bebe-allaitement-sommeil/", "tcc-sommeil/"]),
    ("user", "Moi, adulte", "Peau, allergies, sommeil, chronique", ["orl-allergies-peau/", "tcc-sommeil/", "mes-specialites/#complementaires"]),
    ("ribbon", "Un parcours contre le cancer", "Pendant et après les traitements", ["homeopathie-soins-support-oncologie/", "tcc-sommeil/"]),
    ("heart", "Toute la famille", "Parents, fratrie, quotidien", ["accompagnement-tdah/#famille", "enfant-et-adolescent/", "bebe-allaitement-sommeil/"]),
]


def svc_profiles(root):
    """Proposition C — « Pour qui consultez-vous ? » puis catalogue complet."""
    by_path = {s["path"].split("#")[0]: s for s in SERVICES}
    cards = []
    for ic, t, sub, links in PROFILES:
        lis = []
        for l in links:
            sv = by_path.get(l.split("#")[0])
            label = sv["title"] if sv else l
            if l == "enfant-et-adolescent/#bebe":
                label = "Nouveau-né & bébé"
            if l == "accompagnement-tdah/#famille":
                label = "Accompagnement TDAH – famille"
            lis.append(f'<li><a href="{root}{l}">{label}</a></li>')
        cards.append(f"""<div class="profile-card">
  <div class="icon-badge">{icon(ic)}</div>
  <h3>{t}</h3><p class="small muted">{sub}</p>
  <ul>{''.join(lis)}</ul>
</div>""")
    return '<div class="profile-grid">' + "".join(cards) + "</div>"


def svc_catalog(root):
    rows = []
    for i, s in enumerate(SERVICES):
        subs = "".join(f'<li><a href="{svc_href(root, s, h)}">{t}</a></li>' for t, h, _ in s["subs"] if t != "Questions fréquentes")
        new = ' <span class="badge-new">Nouveau</span>' if s.get("new") else ""
        rows.append(f"""<a class="catalog-row reveal" href="{root}{s['path']}">
  <span class="catalog-num">{i + 1:02d}</span>
  <span class="catalog-img"><img src="{root}assets/img/{s['img']}" alt="" loading="lazy"></span>
  <span class="catalog-main"><span class="catalog-title">{s['title']}{new}</span><span class="catalog-desc">{s['desc']}</span></span>
  <span class="catalog-go">{icon('arrow')}</span>
</a>""")
    return '<div class="catalog">' + "".join(rows) + "</div>"


def header(root, nav, path=""):
    def cur(key):
        return ' aria-current="page"' if nav == key else ""

    cab_current = " is-current" if nav in ("cabinet",) else ""
    return f"""<a class="skip-link" href="#contenu">Aller au contenu</a>
<header class="site-header">
  <div class="container wide header-inner">
    <a class="brand" href="{root}" aria-label="HOMEOMED – Paola Orlando, homéopathe – accueil">
      <img src="{root}assets/img/logo.webp" alt="HOMEOMED – Paola Orlando Homéopathe" width="640" height="157">
    </a>
    <nav class="main-nav" id="menu" aria-label="Navigation principale">
      {mobile_services(root)}
      <ul>
        <li><a href="{root}qui-suis-je/"{cur("about")}>Qui suis-je&nbsp;?</a></li>
        <li><a href="{root}mes-specialites/"{cur("specialites") if path == "mes-specialites/" else ""}>Spécialités</a></li>
        <li><a href="{root}tarifs-remboursements/"{cur("tarifs")}>Tarifs</a></li>
        <li class="has-sub{cab_current}">
          <button class="nav-toggle-sub" type="button" aria-expanded="false">Cabinets {icon("chevron")}</button>
          <ul class="submenu">
            <li><a href="{root}cabinet-pully/">Pully – Lausanne<span>Place Neuve 1 · lun, mar, mer, ven</span></a></li>
            <li><a href="{root}cabinet-fribourg/">Fribourg<span>Centre ITS · tous les jeudis</span></a></li>
          </ul>
        </li>
        <li><a href="{root}faq/"{cur("faq")}>FAQ</a></li>
        <li><a href="{root}blog/"{cur("blog")}>Blog</a></li>
      </ul>
      <div class="mobile-nav-cta">
        {rdv_btn(root, "Prendre rendez-vous")}
        <a class="btn btn-ghost" href="{PHONE_LINK}">{icon("phone")}{PHONE}</a>
      </div>
    </nav>
    <div class="btn-row header-actions">
      <a class="header-phone" href="{PHONE_LINK}">{icon("phone")}<span>{PHONE}</span></a>
      <a class="btn btn-primary btn-sm header-cta" href="{root}prendre-rdv/">{icon("calendar")}Prendre RDV</a>
      <button class="menu-btn" type="button" aria-controls="menu" aria-expanded="false" aria-label="Ouvrir le menu"><span></span></button>
    </div>
  </div>
  {services_bar(root, path)}
</header>"""


def footer(root):
    spec = "".join(f'<li><a href="{root}{p}">{t}</a></li>' for p, t, _, _ in SPECIALTIES + NEW_SERVICES)
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{root}assets/img/logo.webp" alt="HOMEOMED" width="640" height="157" loading="lazy">
        <p>Paola Orlando, homéopathe diplômée fédérale. Homéopathie classique pour enfants, femmes et adultes à Pully/Lausanne et Fribourg.</p>
        <div class="socials">
          <a href="{FACEBOOK}" target="_blank" rel="noopener" aria-label="Facebook">{icon("facebook")}</a>
          <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram")}</a>
          <a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">{icon("linkedin")}</a>
        </div>
      </div>
      <div>
        <h4>Spécialités</h4>
        <ul>{spec}<li><a href="{root}mes-specialites/">Toutes les spécialités</a></li></ul>
      </div>
      <div>
        <h4>Le cabinet</h4>
        <ul>
          <li><a href="{root}qui-suis-je/">Qui suis-je&nbsp;?</a></li>
          <li><a href="{root}tarifs-remboursements/">Tarifs &amp; remboursements</a></li>
          <li><a href="{root}cabinet-pully/">Homéopathe Pully – Lausanne</a></li>
          <li><a href="{root}cabinet-fribourg/">Homéopathe Fribourg</a></li>
          <li><a href="{root}faq/">Questions fréquentes</a></li>
          <li><a href="{root}blog/">Blog Homeo’Conseils</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="{PHONE_LINK}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Place Neuve 1, 1009 Pully</li>
          <li>Centre ITS – Rue de la Banque 4, 1700 Fribourg</li>
        </ul>
        <p class="mt-1">{rdv_btn(root, "Prendre rendez-vous", "btn btn-light btn-sm")}</p>
      </div>
    </div>
    <div class="footer-disclaimer"><strong>Informations importantes&nbsp;:</strong> l’homéopathie est une médecine complémentaire. Elle ne remplace en aucun cas les traitements médicaux prescrits, ni la consultation d’un médecin ou d’un spécialiste. En cas de doute ou d’urgence, veuillez contacter votre professionnel de santé.</div>
    <div class="footer-bottom">
      <span>© <span data-year>{date.today().year}</span> HOMEOMED – Paola Orlando. Tous droits réservés.</span>
      <ul>
        <li><a href="{root}mentions-legales/">Mentions légales &amp; confidentialité</a></li>
        <li><a href="{root}conditions-generales-dutilisation-du-site-homeomed-ch/">Conditions d’utilisation</a></li>
      </ul>
    </div>
  </div>
</footer>
<div class="fab-wrap">
  <a class="fab wa" href="{WHATSAPP}" target="_blank" rel="noopener" aria-label="Écrire sur WhatsApp">{icon("whatsapp")}</a>
</div>
<div class="mobile-bar">
  <a class="btn btn-ghost" href="{PHONE_LINK}">{icon("phone")}Appeler</a>
  {rdv_btn(root, "Prendre RDV")}
</div>"""


SCHEMA = {
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "name": "Cabinet HOMEOMED – Paola Orlando, Homéopathe",
    "url": SITE_URL,
    "logo": SITE_URL + "assets/img/logo.png",
    "image": SITE_URL + "assets/img/paola-portrait.webp",
    "telephone": "+41215661815",
    "email": EMAIL,
    "priceRange": "CHF 90 – 230",
    "medicalSpecialty": "Homeopathic",
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "17"},
    "address": [
        {"@type": "PostalAddress", "streetAddress": "Place Neuve 1", "postalCode": "1009",
         "addressLocality": "Pully", "addressRegion": "VD", "addressCountry": "CH"},
        {"@type": "PostalAddress", "streetAddress": "Rue de la Banque 4 (Centre ITS)", "postalCode": "1700",
         "addressLocality": "Fribourg", "addressRegion": "FR", "addressCountry": "CH"},
    ],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"],
         "opens": "08:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "08:00", "closes": "13:00"},
    ],
    "founder": {"@type": "Person", "name": "Paola Orlando", "jobTitle": "Homéopathe diplômée fédérale"},
    "sameAs": [FACEBOOK, INSTAGRAM, LINKEDIN],
}


def page(meta, body):
    path = meta["path"]
    depth = 0 if path in ("", "404.html") else path.strip("/").count("/") + 1
    root = "../" * depth
    if path == "404.html":
        root = "/"
    title = meta["title"]
    desc = meta["description"]
    canonical = SITE_URL + ("" if path == "404.html" else path)
    og_img = SITE_URL + "assets/img/" + meta.get("image", "hero-granules.webp")
    schema = ""
    if meta.get("schema"):
        schema = f'<script type="application/ld+json">{json.dumps(SCHEMA, ensure_ascii=False)}</script>'
    faq_schema = ""
    if meta.get("faq_schema"):
        qa = re.findall(r'<details>\s*<summary>(.*?)</summary>\s*<div class="answer">(.*?)</div>\s*</details>', body, re.S)
        if qa:
            data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": html.unescape(re.sub(r"<[^>]+>", "", q)).strip(),
                 "acceptedAnswer": {"@type": "Answer",
                                    "text": re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", a))).strip()}}
                for q, a in qa]}
            faq_schema = f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'

    robots = '\n<meta name="robots" content="noindex">' if meta.get("noindex") else ""
    body = expand(body, root)
    return f"""<!doctype html>
<html lang="fr-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#faf7f2">{robots}
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_CH">
<meta property="og:site_name" content="HOMEOMED – Paola Orlando, Homéopathe">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="{root}assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{root}assets/img/favicon-192.png">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="preload" href="{root}assets/fonts/fraunces-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/dm-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/style.css">
{schema}{faq_schema}
</head>
<body>
{header(root, meta.get("nav", ""), path)}
<main id="contenu">
{body}
</main>
{footer(root)}
<script src="{root}assets/js/main.js" defer></script>
</body>
</html>
"""


def expand(body, root):
    """Remplace les gabarits {{...}} présents dans les pages."""
    def repl(m):
        key = m.group(1).strip()
        if key == "root":
            return root
        if key.startswith("icon:"):
            return icon(key[5:])
        if key == "rdv":
            return rdv_btn(root)
        if key.startswith("rdv:"):
            return rdv_btn(root, key[4:])
        if key == "rdv-teal":
            return rdv_btn(root, cls="btn btn-teal")
        if key == "cta":
            return cta_band(root)
        if key == "contact":
            return contact_block(root)
        if key == "reviews":
            return reviews_block()
        if key.startswith("include:"):
            return (ROOT / "src" / "partials" / f"{key[8:]}.html").read_text(encoding="utf-8")
        if key == "svc-tiles":
            return svc_tiles(root)
        if key == "svc-tabs":
            return svc_tabs(root)
        if key == "svc-profiles":
            return svc_profiles(root)
        if key == "svc-catalog":
            return svc_catalog(root)
        if key == "disclaimer":
            return disclaimer()
        if key == "hours":
            return hours_list()
        consts = {"phone": PHONE, "phone-link": PHONE_LINK, "email": EMAIL, "whatsapp": WHATSAPP,
                  "onedoc": ONEDOC, "map-pully": MAP_PULLY, "map-fribourg": MAP_FRIBOURG,
                  "gmaps-pully": GMAPS_PULLY, "gmaps-fribourg": GMAPS_FRIBOURG,
                  "google-reviews": GOOGLE_REVIEWS}
        if key in consts:
            return consts[key]
        raise KeyError(f"Gabarit inconnu : {{{{{key}}}}}")

    # deux passes : les blocs peuvent contenir eux-mêmes {{root}}
    for _ in range(3):
        body = re.sub(r"\{\{([^}]+)\}\}", repl, body)
    return body


REDIRECTS = {
    "declaration-de-confidentialite/": "mentions-legales/",
    "politique-de-cookies-ue/": "mentions-legales/",
}


def main():
    pages = []
    for f in sorted(SRC.glob("*.html")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--meta\s+(\{.*?\})\s*-->\s*", raw, re.S)
        if not m:
            raise SystemExit(f"{f.name} : bloc meta manquant")
        meta = json.loads(m.group(1))
        out = page(meta, raw[m.end():])
        path = meta["path"]
        dest = ROOT / (path if path.endswith(".html") else path + "index.html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out, encoding="utf-8")
        if path != "404.html" and not meta.get("noindex"):
            pages.append(path)
        print("✓", dest.relative_to(ROOT))

    # Redirections des anciennes adresses WordPress
    for old, new in REDIRECTS.items():
        d = ROOT / old
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(
            f'<!doctype html><html lang="fr-CH"><head><meta charset="utf-8"><title>Redirection…</title>'
            f'<meta name="robots" content="noindex"><link rel="canonical" href="{SITE_URL}{new}">'
            f'<meta http-equiv="refresh" content="0; url=../{new}"></head>'
            f'<body><p><a href="../{new}">Cette page a été déplacée.</a></p></body></html>\n', encoding="utf-8")
    (ROOT / "_redirects").write_text(
        "".join(f"/{o} /{n} 301\n/{o.rstrip('/')} /{n} 301\n" for o, n in REDIRECTS.items()), encoding="utf-8")
    print(f"✓ {len(REDIRECTS)} redirections")

    today = date.today().isoformat()
    urls = "\n".join(f"  <url><loc>{SITE_URL}{p}</loc><lastmod>{today}</lastmod></url>" for p in pages)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    print(f"✓ sitemap.xml ({len(pages)} pages)")


if __name__ == "__main__":
    main()
