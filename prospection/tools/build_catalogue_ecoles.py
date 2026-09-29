# -*- coding: utf-8 -*-
"""Catalogue de formation destine aux ecoles, tire du catalogue de SORO Nagony Adama.

Le catalogue source (catalogue/Catalogue_Modules_Formation_SORO_Nagony_Adama.pdf) a ete
ecrit pour UN institut de formation : il s'ouvre sur « en reponse a la demande de
l'institut », exige un ordinateur par apprenant et ne contient pas la seance de 2h que
l'on prospecte. Envoye tel quel a un Directeur des Etudes, il contredirait nos messages.

Cette version :
  - part de la seance d'initiation de 2h (celle des messages WhatsApp et des e-mails) ;
  - presente les modules du catalogue comme la suite, par filiere ;
  - reprend MOT POUR MOT les fiches module depuis catalogue/modules.json ;
  - ne mentionne aucun prix, aucune statistique inventee, aucun « institut » ;
  - n'annonce pas la 2e seance d'initiation : elle reste un levier de negociation.
"""
import json
import pathlib
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, KeepTogether,
                                ListFlowable, ListItem, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.flowables import HRFlowable

RACINE = pathlib.Path(__file__).resolve().parent.parent
CAT = RACINE / "catalogue"
SORTIE = CAT / "Catalogue_Formation_IA_Etablissements_SORO_Nagony_Adama.pdf"
EXP = json.loads((RACINE / "expediteur.json").read_text(encoding="utf-8"))

# --- charte du catalogue source ------------------------------------------------ #
MARINE = colors.HexColor("#1F3864")
ORANGE = colors.HexColor("#C55A11")
TEXTE = colors.HexColor("#202020")
GRIS = colors.HexColor("#808080")
GRIS_FONCE = colors.HexColor("#404040")
FOND = colors.HexColor("#F2F2F2")
BLEU_CLAIR = colors.HexColor("#DEE6F1")
TRAIT = colors.HexColor("#BFBFBF")

_POLICES = "/usr/share/fonts/truetype/liberation/LiberationSans-{}.ttf"
for nom, fichier in (("Sans", "Regular"), ("Sans-B", "Bold"),
                     ("Sans-I", "Italic"), ("Sans-BI", "BoldItalic")):
    pdfmetrics.registerFont(TTFont(nom, _POLICES.format(fichier)))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B",
                              italic="Sans-I", boldItalic="Sans-BI")


def st(nom, **kw):
    base = dict(fontName="Sans", fontSize=10, leading=14, textColor=TEXTE)
    base.update(kw)
    return ParagraphStyle(nom, **base)


S = {
    "corps": st("corps", spaceAfter=5),
    "petit": st("petit", fontSize=8.5, leading=11.5, textColor=GRIS_FONCE),
    "h1": st("h1", keepWithNext=1, fontName="Sans-B", fontSize=17, leading=21, textColor=MARINE,
             spaceBefore=4, spaceAfter=4),
    "h2": st("h2", keepWithNext=1, fontName="Sans-B", fontSize=12.5, leading=16, textColor=MARINE,
             spaceBefore=12, spaceAfter=3),
    "h3": st("h3", keepWithNext=1, fontName="Sans-B", fontSize=10.5, leading=14, textColor=ORANGE,
             spaceBefore=8, spaceAfter=2),
    "chapo": st("chapo", fontName="Sans-I", textColor=GRIS_FONCE, spaceAfter=6),
    "cell": st("cell", fontSize=9, leading=12),
    "cell_b": st("cell_b", fontName="Sans-B", fontSize=9, leading=12),
    "cell_t": st("cell_t", fontName="Sans-B", fontSize=9, leading=12, textColor=colors.white),
    "encadre": st("encadre", fontSize=10, leading=14.5),
    # phrase d'amorce d'une liste : ne jamais la separer de sa liste
    "amorce": st("amorce", spaceAfter=5, keepWithNext=1),
}


NBSP = "\u00a0"


def typo(txt):
    """Espaces insecables francaises : '(21 h)' ne doit jamais se couper en fin de ligne."""
    txt = re.sub(r"(\d) (h|min|%)(?=[\s).,;:]|$)", r"\1" + NBSP + r"\2", txt)
    txt = re.sub(r" ([:;?!»])", NBSP + r"\1", txt)
    return txt.replace("« ", "«" + NBSP)


def P(txt, style="corps"):
    return Paragraph(typo(txt), S[style])


def E(txt):
    """Texte venu du catalogue : echappe avant d'entrer dans le balisage."""
    return escape(txt)


def filet(couleur=ORANGE, epaisseur=1.2, avant=2, apres=8):
    return HRFlowable(width="100%", thickness=epaisseur, color=couleur,
                      spaceBefore=avant, spaceAfter=apres)


def puces(items, style="corps"):
    """Liste a puces en paragraphes simples.

    Une ListFlowable est un conteneur que ReportLab refuse de regrouper avec
    l'intertitre qui la precede : « Programme » restait seul en bas de page.
    Des paragraphes a puce se lient a l'intertitre et se coupent entre deux elements.
    """
    base = S[style]
    puce = ParagraphStyle(f"puce_{style}", parent=base, leftIndent=14, bulletIndent=3,
                          bulletFontName="Sans-B", bulletFontSize=8, spaceAfter=3)
    out = [Paragraph(typo(i), puce, bulletText="•") for i in items]
    if out:
        out[-1].style = ParagraphStyle(f"puce_fin_{style}", parent=puce, spaceAfter=7)
    return out


def tableau(lignes, largeurs, entete=True, zebre=True):
    donnees = []
    for k, l in enumerate(lignes):
        style = "cell_t" if entete and k == 0 else "cell"
        donnees.append([c if not isinstance(c, str) else P(c, style) for c in l])
    t = Table(donnees, colWidths=largeurs, repeatRows=1 if entete else 0)
    cmds = [("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, TRAIT),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    if entete:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), MARINE))
    if zebre:
        for k in range(1 if entete else 0, len(lignes)):
            if k % 2 == 0:
                cmds.append(("BACKGROUND", (0, k), (-1, k), FOND))
    t.setStyle(TableStyle(cmds))
    return t


def encadre(flowables, fond=BLEU_CLAIR):
    t = Table([[flowables]], colWidths=[170 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fond),
                           ("LINEBEFORE", (0, 0), (0, -1), 3, ORANGE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


# --- donnees ----------------------------------------------------------------- #
MODULES = {m["code"]: m for m in json.loads((CAT / "modules.json").read_text(encoding="utf-8"))}

# Seance de 2h : deroule de offre-initiation-ia.md (celui qu'annoncent les messages).
SEANCE = [
    ("Ce qu'est vraiment l'IA, sans jargon", 15),
    ("Démonstration en direct : un devoir et un exposé traités devant la classe", 20),
    ("Atelier encadré : chaque étudiant fait tourner ses premiers prompts sur son téléphone", 40),
    ("Cas d'usage propres à la filière de la classe (comptabilité, logistique, BTP, "
     "communication, informatique, santé…)", 15),
    ("Les 5 pièges : hallucination, plagiat, dépendance, données personnelles, triche", 15),
    ("IA et employabilité : CV, lettre de motivation, préparation d'entretien", 10),
    ("Remise des attestations", 5),
]
assert sum(d for _, d in SEANCE) == 120, "la seance doit durer exactement 2 heures"

# Orientation par filiere : uniquement des modules du catalogue source.
FILIERES = [
    ("Toutes filières — le socle", ["A1", "A2"]),
    ("Commerce, gestion, comptabilité, marketing", ["D1", "E4", "E2", "G1"]),
    ("Informatique, réseaux, développement", ["G5", "G3", "G2"]),
    ("Communication, multimédia, arts graphiques", ["B1", "B2", "C1", "C2"]),
    ("Hôtellerie, tourisme, services", ["A3", "B1", "E3"]),
    ("Filières techniques et industrielles (BTP, génie civil, électrotechnique, agro)",
     ["A2", "G1"]),
    ("Entrepreneuriat — toutes filières, fin de cycle", ["F1", "E4"]),
]
# Les deux parcours que le catalogue source destine explicitement aux etudiants.
PARCOURS = [
    ("Parcours 1 — Créateur de contenu IA",
     "Demandeurs d'emploi, étudiants, community managers, freelances.",
     "Création graphique et vidéo en freelance, community management, studio de contenu.",
     ["A1", "A3", "B1", "B2", "C1", "C2"]),
    ("Parcours 6 — Développeur d'applications métier assisté par IA",
     "Étudiants en informatique, techniciens, porteurs de projet technologique.",
     "Développeur d'applications métier, intégrateur web, chef de projet digital.",
     ["A1", "G5", "G3", "G2"]),
]
RETENUS = []
for _, codes in FILIERES + [(p[0], p[3]) for p in PARCOURS]:
    for c in codes:
        if c not in RETENUS:
            RETENUS.append(c)
RETENUS.sort(key=lambda c: (c[0], int(c[1:])))

# Section 2.3 du catalogue source, mot pour mot (hors ligne propre aux reseaux sociaux).
EXPERIENCE = [
    "Responsable de la Jumia Académie de Côte d'Ivoire (2019) et formateur au sein de cette "
    "académie depuis 2018 : direction du département de formation des vendeurs, conception "
    "et animation des programmes destinés aux marchands de la plateforme",
    "Formateur corporate retenu par la Compagnie Ivoirienne d'Électricité (CIE) pour la "
    "formation de ses équipes à l'intelligence artificielle appliquée à la finance",
    "Animation d'ateliers de formation à l'intelligence artificielle en présentiel dans "
    "plusieurs villes de Côte d'Ivoire, notamment à Korhogo, Treichville et Yopougon",
    "Conception de deux dispositifs de formation complets — l'un destiné aux entrepreneurs, "
    "l'autre à l'administration — comprenant supports de présentation et livrets apprenants",
    "Conception et diffusion de formations numériques suivies par plusieurs centaines "
    "d'apprenants : plus de 120 apprenants sur la formation « Créer des vidéos "
    "professionnelles avec l'IA », plus de 75 sur la formation vidéo avancée, plus de 69 sur "
    "la formation aux visuels produits e-commerce",
    "Production de guides et manuels de formation, dont un guide de 230 pages consacré à "
    "l'usage de l'IA dans l'administration",
]


# --- pages ------------------------------------------------------------------- #
def pied(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 7.5)
    canvas.setFillColor(GRIS)
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 12 * mm,
                           "Catalogue de formation — Établissements d'enseignement")
    canvas.drawCentredString(
        A4[0] / 2, 11 * mm,
        f"{EXP['signataire']} · {EXP['telephone']} · {EXP['email']} — page {doc.page}")
    canvas.restoreState()


def couverture(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MARINE)
    canvas.rect(0, 0, A4[0], 9 * mm, stroke=0, fill=1)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, 9 * mm, A4[0], 1.2 * mm, stroke=0, fill=1)
    canvas.restoreState()


def page_de_garde():
    c = lambda n, **kw: st(n, alignment=TA_CENTER, **kw)
    return [
        Spacer(1, 42 * mm),
        Paragraph("BOSS IMPACT SOCIETY",
                  c("g1", fontName="Sans-B", fontSize=12, textColor=ORANGE, leading=16,
                    wordSpace=3)),
        Paragraph("BIG RÉUSSITE ACADÉMIE", c("g2", fontSize=9, textColor=GRIS_FONCE, leading=13)),
        Spacer(1, 16 * mm),
        Paragraph("L'INTELLIGENCE ARTIFICIELLE<br/>DANS VOS CLASSES",
                  c("g3", fontName="Sans-B", fontSize=25, leading=31, textColor=MARINE)),
        Spacer(1, 5 * mm),
        Paragraph("Catalogue de formation destiné aux établissements d'enseignement "
                  "supérieur, technique et professionnel",
                  c("g4", fontSize=12, leading=16, textColor=GRIS_FONCE)),
        Spacer(1, 6 * mm),
        filet(epaisseur=1.5, apres=10),
        Paragraph("Une séance d'initiation de 2 heures dans vos classes · "
                  "Des modules complets par filière · Des étudiants qui savent se servir "
                  "de l'IA pour leurs travaux et face à un recruteur",
                  c("g5", fontSize=10, leading=14.5)),
        Spacer(1, 22 * mm),
        Paragraph("FORMATEUR", c("g6", fontSize=8, textColor=GRIS)),
        Paragraph("SORO NAGONY ADAMA", c("g7", fontName="Sans-B", fontSize=14,
                                         leading=18, textColor=MARINE)),
        Paragraph("Fondateur et Directeur Général de BOSS IMPACT SOCIETY<br/>"
                  "Consultant en transformation digitale et formateur en intelligence "
                  "artificielle", c("g8", fontSize=9.5, leading=13.5)),
        Spacer(1, 8 * mm),
        filet(TRAIT, 0.6, apres=8),
        Paragraph("<b>Téléphone : +225 07 57 22 87 31 · +225 05 06 84 49 01</b><br/>"
                  "<b>Courriel : soroboss.bossimpact@gmail.com</b><br/>"
                  "www.jachete.ci · boutique.bigreussite.com",
                  c("g9", fontSize=9.5, leading=14.5, textColor=MARINE)),
        Spacer(1, 8 * mm),
        Paragraph("<i>Abidjan, Côte d'Ivoire — Septembre 2026</i>",
                  c("g10", fontSize=9, textColor=GRIS)),
    ]


def fiche(m):
    tete = [
        CondPageBreak(60 * mm),
        Paragraph(f"{E(m['code'])} — {E(m['titre'])}", S["h2"]),
        filet(avant=0, apres=5),
        P(f"<b>Niveau :</b> {E(m['niveau'])}"),
        P(f"<b>Prérequis :</b> {E(m['prerequis'])}"),
    ]
    corps = [
        P("Objectifs pédagogiques", "h3"),
        P("À l'issue du module, l'apprenant est capable de :", "amorce"),
        *puces([E(o) for o in m["objectifs"]]),
        P("Programme", "h3"),
        *puces([E(o) for o in m["programme"]]),
        KeepTogether([
            P("Volume horaire", "h3"),
            tableau([["Présentiel", "À distance", "Total"],
                     [f"{m['presentiel_h']} h", f"{m['distance_h']} h",
                      f"<b><font color='#C55A11'>{m['total_h']} h</font></b>"]],
                    [56 * mm, 56 * mm, 58 * mm], zebre=False)]),
        KeepTogether([P("Évaluation", "h3"), P(E(m["evaluation"]))]),
        KeepTogether([P("Livrables remis à l'apprenant", "h3"), P(E(m["livrables"]))]),
        Spacer(1, 6),
    ]
    return tete + corps


def contenu():
    h = []
    h += page_de_garde()
    h += [NextPageTemplate("normal"), PageBreak()]

    # 1. Constat
    h += [P("1. Pourquoi former vos étudiants maintenant", "h1"), filet(),
          P("Vos étudiants utilisent déjà l'intelligence artificielle : pour leurs exposés, "
            "leurs rapports de stage, leurs dossiers techniques. Personne ne leur a appris à "
            "s'en servir, et aucune règle d'usage ne leur a été donnée."),
          P("Deux risques en découlent, et c'est l'établissement qui les porte : des travaux "
            "dont on ne sait plus qui les a réellement écrits, et des diplômés qui arrivent "
            "sur le marché du travail sans savoir utiliser correctement un outil que les "
            "recruteurs attendent désormais d'eux."),
          P("Ce catalogue propose une réponse graduée :"),
          *puces(["<b>une séance d'initiation de 2 heures</b>, organisée classe par classe "
                 "dans vos locaux, sans salle informatique ;",
                 "<b>des modules de formation complets</b>, choisis selon la filière, pour "
                 "les établissements qui veulent aller plus loin."]),
          Spacer(1, 4),
          encadre([P("<b>Commencer par une classe test.</b> L'établissement juge sur pièce, "
                     "sur une seule classe, avant de décider de la suite.", "encadre")]),
          ]

    # 2. Seance
    h += [Spacer(1, 10), P("2. La séance d'initiation — 2 heures dans vos classes", "h1"),
          filet(),
          P("Une séance pratique, pas un cours magistral. Chaque étudiant manipule l'IA "
            "sur son propre téléphone, sur des cas tirés de sa filière, et repart en sachant "
            "l'utiliser sans tomber dans le plagiat."),
          P("Déroulé", "h3"),
          tableau([["Séquence", "Durée"]] +
                  [[f"{k}. {E(t)}", f"{d} min"] for k, (t, d) in enumerate(SEANCE, 1)] +
                  [["<b>Total</b>", "<b>120 min</b>"]],
                  [140 * mm, 30 * mm]),
          P("Ce que chaque étudiant emporte", "h3"),
          *puces(["Un kit de prompts pour ses propres travaux : rapports, exposés, "
                 "recherches, préparation d'entretien.",
                 "Une attestation de participation à la formation « Initiation à "
                 "l'intelligence artificielle »."]),
          KeepTogether([
              P("Conditions pratiques", "h3"),
              *puces(["Une salle, un vidéoprojecteur, une prise électrique.",
                     "Les étudiants travaillent sur leur propre téléphone : <b>aucune salle "
                     "informatique n'est nécessaire</b>.",
                     "Une classe entière par séance. Les exemples sont adaptés à la filière "
                     "du groupe : une classe de gestion ne voit pas les mêmes cas qu'une "
                     "classe technique."])]),
          ]

    # 3. Formateur
    h += [PageBreak(), P("3. Le formateur", "h1"), filet(),
          tableau([
              ["<b>Identité</b>", "Soro Nagony Adama, également connu sous le nom de SoroBoss"],
              ["<b>Fonction</b>", "Fondateur et Directeur Général de BOSS IMPACT SOCIETY, "
                                  "cabinet de transformation digitale et de formation en "
                                  "intelligence artificielle"],
              ["<b>Structures dirigées</b>", "BOSS IMPACT SOCIETY (conseil et formation) · "
                                             "BIG RÉUSSITE ACADÉMIE (formations digitales) · "
                                             "JACHETE.CI (plateforme de commerce en ligne)"],
              ["<b>Expérience</b>", "Plus de 15 années d'exercice dans les métiers de "
                                    "l'informatique, de la photographie et du digital, dont 12 "
                                    "années en marketing digital et commerce en ligne"],
              ["<b>Formation initiale</b>", "BTS Nouvelles Technologies de l'Information et "
                                            "de la Communication — ISTCI, Abidjan"],
              ["<b>Zone d'intervention</b>", "Abidjan, et interventions possibles à "
                                             "l'intérieur du pays"],
          ], [42 * mm, 128 * mm], entete=False),
          P("Expérience pédagogique", "h3"),
          *puces([E(x) for x in EXPERIENCE]),
          ]

    # 4. Aller plus loin
    h += [PageBreak(), P("4. Aller plus loin : les modules de formation", "h1"), filet(),
          P("Pour les établissements qui souhaitent former leurs étudiants au-delà de "
            "l'initiation, les modules ci-dessous sont extraits du catalogue professionnel de "
            "BOSS IMPACT SOCIETY. Leurs durées ne sont pas théoriques : elles ont été établies "
            "à partir du temps observé lors des sessions déjà animées."),
          P("Ces modules sont de véritables formations, distinctes de la séance "
            "d'initiation : format hybride (présentiel et accompagnement à distance), groupes "
            "de 10 à 15 apprenants, salle équipée. Les conditions sont détaillées en "
            "section 7."),
          P("Modules conseillés par filière", "h3"),
          tableau([["Filière", "Modules conseillés"]] +
                  [[f"<b>{E(f)}</b>",
                    "<br/>".join(f"<b>{c}</b> — {E(MODULES[c]['titre'])} "
                                 f"<font color='#808080'>({MODULES[c]['total_h']} h)</font>"
                                 for c in codes)]
                   for f, codes in FILIERES],
                  [52 * mm, 118 * mm]),
          ]

    # 5. Parcours
    h += [Spacer(1, 6), CondPageBreak(90 * mm),
          P("5. Deux parcours conçus pour les étudiants", "h1"), filet(),
          P("Les modules s'assemblent en parcours qualifiants. Chaque parcours conduit à une "
            "compétence professionnelle complète et à un livrable final présentable à un "
            "employeur ou à un client.")]
    for titre, public, debouches, codes in PARCOURS:
        pres = sum(MODULES[c]["presentiel_h"] for c in codes)
        dist = sum(MODULES[c]["distance_h"] for c in codes)
        h += [KeepTogether([
            P(E(titre), "h2"),
            P(f"<b>Public visé :</b> {E(public)}"),
            P(f"<b>Débouchés :</b> {E(debouches)}"),
            tableau([["Code", "Module", "Prés.", "Dist.", "Total"]] +
                    [[c, E(MODULES[c]["titre"]), f"{MODULES[c]['presentiel_h']}",
                      f"{MODULES[c]['distance_h']}", f"{MODULES[c]['total_h']} h"]
                     for c in codes] +
                    [["", "<b>Total du parcours</b>", f"<b>{pres}</b>", f"<b>{dist}</b>",
                      f"<b>{pres + dist} h</b>"]],
                    [13 * mm, 107 * mm, 16 * mm, 16 * mm, 18 * mm]),
        ])]

    # 6. Fiches
    h += [PageBreak(), P("6. Fiches détaillées des modules", "h1"), filet(),
          P("Chaque fiche précise les prérequis, les objectifs pédagogiques, le programme "
            "séquencé, le volume horaire, les modalités d'évaluation et les livrables remis à "
            "l'apprenant.", "chapo")]
    for c in RETENUS:
        h += fiche(MODULES[c])

    # 7. Organisation
    h += [PageBreak(), P("7. Organisation pratique", "h1"), filet(),
          P("Séance d'initiation ou module complet : ce qui change", "h3"),
          tableau([
              ["", "Séance d'initiation", "Module de formation"],
              ["<b>Durée</b>", "2 heures", "10 à 28 heures selon le module"],
              ["<b>Format</b>", "Présentiel, dans la classe",
               "Hybride : présentiel, puis accompagnement à distance"],
              ["<b>Effectif</b>", "Une classe entière",
               "10 à 15 apprenants par groupe ; au-delà de 15, un assistant formateur ou un "
               "présentiel majoré de 20 %"],
              ["<b>Matériel</b>", "Une salle, un vidéoprojecteur, une prise. Les étudiants "
                                  "utilisent leur téléphone.",
               "Salle équipée d'un vidéoprojecteur et d'une connexion Internet stable. Un "
               "ordinateur par apprenant pour les modules de bureautique, de développement, "
               "de commerce en ligne et de publicité ; un smartphone récent peut suffire "
               "pour les modules de production de contenu."],
              ["<b>Validation</b>", "Attestation de participation",
               "Évaluation finale sur un livrable professionnel réel, propre à chaque module"],
          ], [30 * mm, 60 * mm, 80 * mm]),
          P("Rythmes possibles pour les modules", "h3"),
          tableau([["Rythme", "Organisation"],
                   ["Soir", "Sessions de 3 h 30 en fin de journée"],
                   ["Intensif", "Journées pleines consécutives (7 h par jour)"],
                   ["Séquencé en semaine", "Une journée par semaine, distanciel entre les "
                                           "séances"],
                   ["Week-end", "Samedis pleins, distanciel en semaine"]],
                  [45 * mm, 125 * mm]),
          P("Modalités", "h3"),
          *puces(["Intervention en présentiel à Abidjan et dans les villes de l'intérieur, "
                 "sous réserve de prise en charge des déplacements.",
                 "Volet distanciel assuré par visioconférence et par un espace d'échange "
                 "dédié à chaque promotion.",
                 "Supports pédagogiques fournis : livret apprenant, présentation projetée, "
                 "fiches mémo, bibliothèques de modèles et de prompts réutilisables.",
                 "Les outils utilisés, et leurs éventuels abonnements, sont communiqués à "
                 "l'établissement avant chaque session.",
                 "Possibilité de former les enseignants de l'établissement afin qu'ils "
                 "reprennent l'animation des modules de niveau initiation."]),
          ]

    # 8. Prochaine etape : une vraie page de cloture, pas un reliquat en haut de page
    c = lambda n, **kw: st(n, alignment=TA_CENTER, **kw)
    h += [PageBreak(), Spacer(1, 38 * mm),
          Paragraph("PROCHAINE ÉTAPE", c("f0", fontName="Sans-B", fontSize=10,
                                         textColor=ORANGE, leading=14)),
          Spacer(1, 4 * mm),
          Paragraph(typo("Commençons par une classe test."),
                    c("f1", fontName="Sans-B", fontSize=22, leading=28, textColor=MARINE)),
          Spacer(1, 6 * mm), filet(epaisseur=1.5, apres=12),
          Paragraph(typo("Choisissez une classe. Nous animons la séance d'initiation de "
                         "2 heures dans vos locaux, à la date qui vous convient."),
                    c("f2", fontSize=11.5, leading=17)),
          Spacer(1, 3 * mm),
          Paragraph(typo("Vous jugez sur pièce — la réaction des étudiants, la qualité du "
                         "contenu, le retour de vos enseignants — avant de décider de la "
                         "suite."), c("f3", fontSize=11.5, leading=17)),
          Spacer(1, 18 * mm),
          Paragraph(E(EXP["signataire"]).upper(),
                    c("f4", fontName="Sans-B", fontSize=14, leading=18, textColor=MARINE)),
          Paragraph("Formateur en intelligence artificielle<br/>"
                    "BOSS IMPACT SOCIETY · BIG RÉUSSITE ACADÉMIE",
                    c("f5", fontSize=9.5, leading=13.5, textColor=GRIS_FONCE)),
          Spacer(1, 6 * mm),
          Paragraph("<b>+225 07 57 22 87 31 · +225 05 06 84 49 01</b><br/>"
                    f"<b>{E(EXP['email'])}</b>",
                    c("f6", fontSize=11, leading=16, textColor=MARINE)),
          Spacer(1, 22 * mm),
          filet(TRAIT, 0.6, apres=6),
          Paragraph(typo("Le catalogue professionnel complet — 30 modules répartis en "
                         "7 domaines — est disponible sur simple demande."),
                    c("f7", fontName="Sans-I", fontSize=9, textColor=GRIS)),
          ]
    return h


def construire():
    doc = BaseDocTemplate(
        str(SORTIE), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
        title="L'intelligence artificielle dans vos classes — Catalogue de formation",
        author="SORO Nagony Adama — BOSS IMPACT SOCIETY / BIG RÉUSSITE ACADÉMIE",
        subject="Catalogue de formation destiné aux établissements d'enseignement")
    cadre = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate("garde", [cadre], onPage=couverture),
                          PageTemplate("normal", [cadre], onPage=pied)])
    doc.build(contenu())
    return SORTIE


if __name__ == "__main__":
    s = construire()
    print(f"{s.relative_to(RACINE)} : {len(RETENUS)} fiches module "
          f"({', '.join(RETENUS)}), {s.stat().st_size // 1024} Ko")
