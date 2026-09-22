#!/usr/bin/env python3
"""Classe chaque etablissement dans un segment de filiere, et fournit le texte propre a ce segment.

Le segment est deduit de la colonne `type` de la base. Il sert a personnaliser le mail :
le travail que rendent reellement leurs etudiants, et ce que la seance leur apporte a eux.
"""
import re
import unicodedata


def _sans_accent(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


# L'ordre compte : un mot-cle tres specifique doit l'emporter sur un mot-cle general.
_REGLES = [
    ("sante",        r"sante|paramedical|infirmier|sage-femme|soins"),
    ("btp",          r"batiment|travaux publics|genie civil|topographie|geometre|geomatique|mines|petrole|\bbtp\b"),
    ("logistique",   r"logistique|transport|transit|maritime|navigation|douane"),
    ("hotellerie",   r"hotelier|hotellerie|tourisme|restauration"),
    ("agro",         r"agronomie|agro|agri"),
    ("lycee",        r"lycee|college"),
    ("universite",   r"universit"),
    ("communication", r"communication|\barts\b|culturelle|audiovisuel|multimedia"),
    ("numerique",    r"informatique|\btic\b|numerique|reseaux|cybersecurite|telecom|digital|codage|electronique|technolog"),
    ("ingenieur",    r"ingenieur|polytechnique|industriel|industrie"),
    ("commerce",     r"commerce|gestion|management|affaires|comptabilite|finance|banque|assurance|marketing|tertiaire|business|secretariat|administration"),
    ("formation",    r"formation|agree|pedagogique"),
]


def segment(type_etablissement):
    t = _sans_accent(type_etablissement)
    for nom, motif in _REGLES:
        if re.search(motif, t):
            return nom
    return "defaut"


# travaux : ce que leurs etudiants rendent vraiment, cite dans la question d'ouverture
# apport  : ce que la seance couvre pour cette filiere precisement
TEXTES = {
    "sante": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "un mémoire de fin de cycle ou un rapport de stage clinique",
        "apport": "Dans une filière de santé, la limite est capitale et la séance la traite "
                  "explicitement : une information clinique produite par une intelligence "
                  "artificielle se vérifie toujours avant d'être reprise dans un travail ou "
                  "appliquée à un patient.",
    },
    "btp": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "un rapport de chantier, un métré ou une note de calcul",
        "apport": "Pour vos filières techniques, la séance montre où l'IA fait gagner du temps "
                  "— rédaction de dossiers, comptes rendus, recherche de normes — et pourquoi un "
                  "résultat de calcul produit par une IA ne se recopie jamais sans être refait.",
    },
    "logistique": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "une étude de cas transport ou un rapport de stage",
        "apport": "Pour vos filières logistique et transit, la séance descend au concret : "
                  "préparer une cotation, une étude de flux ou un dossier client avec l'IA, "
                  "et repérer les erreurs qu'elle commet sur les chiffres et les incoterms.",
    },
    "hotellerie": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "un rapport de stage ou un projet d'établissement",
        "apport": "Pour vos filières hôtellerie et tourisme, la séance traite les usages qui "
                  "servent dès le premier stage : réponse aux avis clients, supports d'accueil, "
                  "communication d'établissement, préparation d'une carte.",
    },
    "agro": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "un rapport de stage ou un mémoire technique",
        "apport": "Pour vos filières agronomiques, la séance montre l'IA appliquée à la "
                  "recherche documentaire, à la rédaction technique et à l'analyse de données "
                  "d'essai — ainsi que la vérification qu'aucun résultat ne doit contourner.",
    },
    "numerique": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "un rapport de projet ou une documentation technique",
        "apport": "Vos étudiants du numérique sont les plus exposés : beaucoup produisent déjà du "
                  "code écrit par une IA. La séance porte précisément là-dessus — livrer du code "
                  "que l'on est capable de relire, d'expliquer et de défendre devant un jury ou "
                  "un employeur, et non l'inverse.",
    },
    "ingenieur": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "un rapport de projet ou une note technique",
        "apport": "Pour vos filières d'ingénierie, la séance sépare nettement ce que l'IA fait "
                  "bien — structurer, rédiger, chercher — de ce qu'elle fait mal, à commencer "
                  "par tout calcul qu'un étudiant reprendrait sans le refaire.",
    },
    "commerce": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "une étude de marché, un business plan ou un rapport de stage",
        "apport": "Pour vos filières commerce et gestion, la séance va au concret : construire "
                  "une étude de marché, une proposition commerciale ou un tableau de bord avec "
                  "l'IA, et reconnaître les chiffres qu'elle invente.",
    },
    "communication": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "un dossier de production ou un mémoire",
        "apport": "Pour vos filières communication et création, la séance traite l'IA comme un "
                  "outil de production — écriture, recherche d'angle, déclinaison de formats — "
                  "et pose la question des droits et du crédit, que vos étudiants rencontreront "
                  "dès leur premier employeur.",
    },
    "universite": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "un exposé, un rapport de stage ou un mémoire",
        "apport": "La séance s'adapte à la filière de chaque groupe : les cas d'usage montrés à "
                  "des étudiants de gestion ne sont pas ceux d'étudiants de sciences ou de droit.",
    },
    "lycee": {
        "public": "élèves",
        "corpus": "dossiers",
        "travaux": "un exposé ou un dossier de projet",
        "apport": "Pour des élèves de l'enseignement technique, la séance reste très concrète : "
                  "ils manipulent eux-mêmes, sur leur téléphone, et repartent avec des règles "
                  "d'usage simples qu'ils peuvent appliquer dès le devoir suivant.",
    },
    "formation": {
        "public": "apprenants",
        "corpus": "projets",
        "travaux": "un projet de fin de formation ou un rapport de stage",
        "apport": "Pour des apprenants en formation professionnelle, l'angle est l'employabilité "
                  "immédiate : se servir de l'IA dans le métier visé, et savoir le dire en "
                  "entretien sans se faire piéger.",
    },
    "defaut": {
        "public": "étudiants",
        "corpus": "mémoires",
        "travaux": "un exposé ou un rapport de stage",
        "apport": "La séance s'adapte à la filière de chaque groupe : les cas d'usage montrés à "
                  "une classe de gestion ne sont pas ceux d'une classe technique.",
    },
}


def civilite(interlocuteur_cible):
    """Un lycee a un proviseur, pas un directeur des etudes : l'en-tete doit le refleter."""
    return "Madame, Monsieur le Proviseur," if "Proviseur" in interlocuteur_cible \
        else "Madame, Monsieur le Directeur des Études,"


# --- nom d'etablissement tel qu'il doit apparaitre dans une phrase ------------- #

_ACCENTS = {
    "Ecole": "École", "Ecoles": "Écoles", "Superieure": "Supérieure", "Superieur": "Supérieur",
    "Superieures": "Supérieures", "Universite": "Université", "Cote": "Côte", "Etudes": "Études",
    "Specialites": "Spécialités", "Pole": "Pôle", "Academie": "Académie", "Regionale": "Régionale",
    "Lycee": "Lycée", "College": "Collège", "Institut": "Institut", "Hotellerie": "Hôtellerie", "Hoteliere": "Hôtelière", "Hotelier": "Hôtelier",
    "Genie": "Génie", "Elites": "Élites", "Pedagogique": "Pédagogique", "Numerique": "Numérique",
    "Sante": "Santé", "Geomatique": "Géomatique", "Guede": "Guédé", "Methodiste": "Méthodiste",
    "Electroniques": "Électroniques", "Specialisee": "Spécialisée", "Technologie": "Technologie",
    "Professionnalise": "Professionnalisé", "Metiers": "Métiers", "Federal": "Fédéral",
    "Internationale": "Internationale", "Systemes": "Systèmes", "Theodore": "Théodore",
}


def nom_affiche(nom):
    """Nom lisible dans une phrase : sans le rappel entre parentheses, sans le
    developpement apres le tiret quand le sigle suffit, et correctement accentue."""
    court = re.sub(r"\s*\([^)]*\)\s*$", "", nom).strip()
    if " - " in court:
        prefixe = court.split(" - ")[0].strip()
        if len(prefixe) <= 28:          # un sigle ou un nom court : le developpement est superflu
            court = prefixe
    return re.sub(r"\b[A-Za-z]+\b", lambda m: _ACCENTS.get(m.group(0), m.group(0)), court)
