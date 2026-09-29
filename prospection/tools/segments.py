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


# --- noms d'etablissement dans une phrase --------------------------------------- #
# La liste MESRS ecrit 613 noms sur 690 en CAPITALES. Recopies tels quels, ils
# donnaient « au Directeur des Etudes d'INSTITUT SUPERIEUR DE ... » : un nom crie,
# et une preposition fausse. On les remet en casse francaise, sigles conserves.

# Sigles de 5 lettres ou plus : impossibles a distinguer d'un mot sans liste.
_SIGLES = set("""
ESBTP ESCAM ESCAMT ESCOGET ESMAT ESMIT HETEC IHETT ISFCG ISFMI ISFPT ISTCI CERCO
AGEFOP AGITEL ARSTM ATSAM CAFOP CEFAT CEFIAT CFOMIS CIFEC ECOFORP EPMACI ESATIC ESCOM
ESEPT ESETEC ESFIT ESICOM ESIGE ESMCT ESTAN ESTEAI FICOGES GEIGE GESTPCI GISTECOM
ICOGES IESTP IFORAS IFPAM IIPEA IISAN IMOTEP INFAS INPRAT INSAAC INSCP INSTEC IPNETP
ISACM ISAECI ISCAE ISFIA ISTAM ISTEA MAAXIT MUPES SODEC UNIHTEC UNISAT ENSIT EYLIM
EMATECH CESTIA AVIDE UICI UIST
""".split())

# Mots de 4 lettres ou moins qui sont des mots ou des noms, pas des sigles.
_MOTS_COURTS = set("""
AND ART ARTS AUX BOWL CAMP COTE DAME DATA EURO FOI HIGH MAN MER MONT NEUF PAIX POLE
PONT PORT POUR ROI SAN SUD SUP ZONE DIVO JEAN PAUL HUGO FRED ADAM LAMA KOKO LOKO
ZADI YAPI MONA KADI ACKA AGBE AKA ATSE INZA YOH DION ONYX CITE VIE NEW THE
""".split())

_MINUSCULES = {"de", "du", "des", "la", "le", "les", "et", "en", "au", "aux", "sur",
               "pour", "par", "a", "of", "and", "the"}

# Fautes de frappe de la source, sans ambiguite possible.
_CORRECTIONS = {"INSITUT": "INSTITUT", "INSTIUT": "INSTITUT", "INSTITU": "INSTITUT",
                "SUPEREIRUR": "SUPERIEUR", "ECOEL": "ECOLE"}

# Cle : forme en capitales sans accent. Valeur : forme correcte.
_ACCENTUES = {k.upper(): v for k, v in {
    "Academie": "Académie", "Appliquee": "Appliquée", "Appliquees": "Appliquées",
    "Avancee": "Avancée", "Avancees": "Avancées", "Batiment": "Bâtiment", "Bouake": "Bouaké",
    "Bouafle": "Bouaflé", "Carrieres": "Carrières", "Chaussees": "Chaussées",
    "College": "Collège", "Competences": "Compétences", "Comptabilite": "Comptabilité",
    "Coeur": "Cœur", "Developpement": "Développement", "Duekoue": "Duékoué", "Ecole": "École",
    "Ecoles": "Écoles", "Econometrie": "Économétrie", "Economie": "Économie",
    "Economique": "Économique", "Economiques": "Économiques", "Education": "Éducation",
    "Elite": "Élite", "Elites": "Élites", "Energie": "Énergie", "Energetique": "Énergétique",
    "Esperance": "Espérance", "Etude": "Étude", "Etudes": "Études", "Galilee": "Galilée",
    "General": "Général", "Generale": "Générale", "Genie": "Génie", "Geomatique": "Géomatique",
    "Hotelier": "Hôtelier", "Hoteliere": "Hôtelière", "Hotellerie": "Hôtellerie",
    "Ingenierie": "Ingénierie", "Ingenieries": "Ingénieries", "Ingenieur": "Ingénieur",
    "Ingenieurs": "Ingénieurs", "Jaures": "Jaurès", "Mecanique": "Mécanique",
    "Metier": "Métier", "Metiers": "Métiers", "Marahoue": "Marahoué", "Numerique": "Numérique",
    "Numeriques": "Numériques", "Phenix": "Phénix", "Poincare": "Poincaré", "Pole": "Pôle",
    "Preparatoires": "Préparatoires", "Presbyterien": "Presbytérien",
    "Presentielle": "Présentielle", "Prive": "Privé", "Privee": "Privée", "Progres": "Progrès",
    "Proselyte": "Prosélyte", "Regional": "Régional", "Regionale": "Régionale",
    "Sacre": "Sacré", "Sante": "Santé", "Securite": "Sécurité", "Seguela": "Séguéla",
    "Speciale": "Spéciale", "Specialites": "Spécialités", "Strategies": "Stratégies",
    "Succes": "Succès", "Superieur": "Supérieur", "Superieure": "Supérieure",
    "Superieures": "Supérieures", "Superieurs": "Supérieurs",
    "Telecommunication": "Télécommunication", "Telecommunications": "Télécommunications",
    "Therese": "Thérèse", "Tiassale": "Tiassalé", "Universite": "Université",
    "Cote": "Côte", "Odienne": "Odienné", "Adjame": "Adjamé", "Angre": "Angré",
    "Adzope": "Adzopé", "Azaguie": "Azaguié", "Soubre": "Soubré", "Attecoube": "Attécoubé",
    "Bouet": "Bouët", "Eburnie": "Éburnie", "Etablissement": "Établissement",
    "Media": "Média", "Medias": "Médias", "Esthetique": "Esthétique", "Creation": "Création",
    "Etat": "État", "Aeronautique": "Aéronautique", "Electricite": "Électricité",
    "Electronique": "Électronique", "Electroniques": "Électroniques",
    "Electrotechnique": "Électrotechnique", "Medical": "Médical", "Medicale": "Médicale",
    "Paramedical": "Paramédical", "Paramedicale": "Paramédicale", "Veterinaire": "Vétérinaire",
    "Etoile": "Étoile", "Reussite": "Réussite", "Eveil": "Éveil", "Emergence": "Émergence",
    "Evangelique": "Évangélique", "Methodiste": "Méthodiste", "Theologie": "Théologie",
    "Republique": "République", "Geologie": "Géologie", "Systemes": "Systèmes",
    "Specialisee": "Spécialisée", "Professionnalise": "Professionnalisé",
    "Pedagogique": "Pédagogique", "Regionales": "Régionales", "Federal": "Fédéral",
    "Theodore": "Théodore", "Guede": "Guédé", "Specialites.": "Spécialités",
}.items()}


def _sans_accent_maj(t):
    return _sans_accent(t).upper()


def _mot(tok, premier):
    """Casse d'un mot isole (sans apostrophe ni trait d'union)."""
    if not tok:
        return tok
    cle = _sans_accent_maj(tok)
    if cle in _CORRECTIONS:             # faute de la source : on ecrit la forme corrigee
        cle = tok = _CORRECTIONS[cle]
    if any(ch.isdigit() for ch in tok) or cle in _SIGLES:
        return tok.upper()
    if len(cle) == 1:
        return tok.upper()
    if len(cle) <= 4 and cle not in _MOTS_COURTS and cle.lower() not in _MINUSCULES:
        return tok.upper()                                   # ESTC, ISTP, HEC...
    if cle.lower() in _MINUSCULES and not premier:
        return cle.lower()
    if cle in _ACCENTUES:
        return _ACCENTUES[cle]
    return tok[:1].upper() + tok[1:].lower()


def _jeton(tok, premier):
    """Gere apostrophes (D'ABIDJAN, N'GUESSAN, SUP'INTER) et traits d'union."""
    if "-" in tok:
        return "-".join(_jeton(p, premier and i == 0) for i, p in enumerate(tok.split("-")))
    if "'" in tok or "’" in tok:
        a, b = re.split(r"['’]", tok, maxsplit=1)
        if a.upper() in ("D", "L"):
            return ("D" if premier and a.upper() == "D" else a.lower()) + "'" + _mot(b, True)
        return _mot(a, premier) + "'" + _mot(b, True)
    return _mot(tok, premier)


def casse_francaise(nom):
    """'INSTITUT SUPERIEUR DE ... (ISTP) YOPOUGON' -> 'Institut Supérieur de ... (ISTP) Yopougon'.

    Ne touche qu'aux noms majoritairement en capitales : un nom deja saisi en casse
    mixte ('AIST Plateau', 'Groupe CSI') est suppose correct.
    """
    lettres = [c for c in nom if c.isalpha()]
    if not lettres or sum(c.isupper() for c in lettres) < 0.6 * len(lettres):
        return nom
    nom = nom.replace("_", " ")          # 'COCODY_GRANDE ECOLE' dans la source
    # 'D ENSEIGNEMENT' / 'L AGRICULTURE' : apostrophe perdue a la source
    nom = re.sub(r"\b([DL]) (?=[AEIOUYÉÈÊÂÎÔH])", r"\1'", nom)
    morceaux = re.split(r"(\s+|[()/,])", nom)
    sortie, premier = [], True
    for m in morceaux:
        if not m or m.isspace() or m in "()/,":
            sortie.append(m)
            continue
        sortie.append(_jeton(m, premier))
        premier = False
    return "".join(sortie)


def nom_affiche(nom):
    """Nom lisible dans une phrase : sans le rappel entre parentheses, sans le
    developpement apres le tiret quand le sigle suffit, en casse francaise et accentue."""
    court = re.sub(r"\s*\([^)]*\)\s*$", "", nom).strip()
    if " - " in court:
        prefixe = court.split(" - ")[0].strip()
        if len(prefixe) <= 28:          # un sigle ou un nom court : le developpement est superflu
            court = prefixe
    court = casse_francaise(court)
    return re.sub(r"\b[A-Za-z]+\b", lambda m: _ACCENTS.get(m.group(0), m.group(0)), court)


# Nom commun en tete de nom propre : il appelle un article. « du Groupe », « de l'Institut ».
_ARTICLE = {
    "ecole": "de l'", "ecoles": "des ", "institut": "de l'", "institute": "de l'",
    "universite": "de l'", "academie": "de l'", "etablissement": "de l'",
    "groupe": "du ", "lycee": "du ", "college": "du ", "centre": "du ", "cours": "du ",
    "complexe": "du ", "pole": "du ", "cabinet": "du ", "conservatoire": "du ",
    "campus": "du ", "chantiers": "des ", "grande": "de la ", "haute": "de la ",
    "hautes": "des ", "grandes": "des ",
}


def de(nom):
    """« de l'Institut X », « du Groupe Y », « d'AGITEL », « de PIGIER »."""
    premier = _sans_accent(re.split(r"[\s\-]", nom, maxsplit=1)[0]).lower().strip(",") if nom else ""
    if premier in _ARTICLE:
        return _ARTICLE[premier] + nom
    return f"d'{nom}" if nom[:1].upper() in "AEIOUYÉÈÊÀÂÎÔÛH" and not nom[:2].upper() in ("HU",) else f"de {nom}"


# --- accroches WhatsApp -------------------------------------------------------- #
# Sur WhatsApp, l'apercu ne montre que les deux premieres lignes. Si elles ne font
# pas mal, le message n'est jamais ouvert. Chaque accroche nomme le travail precis
# que rendent leurs etudiants, pas l'IA en general.

ACCROCHES = {
    "numerique": "Vos étudiants livrent déjà du code écrit par une IA.\nLa plupart seraient incapables de l'expliquer devant un jury.",
    "sante": "Vos étudiants recopient déjà des informations médicales sorties d'une IA.\nSans les vérifier une seule fois.",
    "btp": "Vos étudiants recopient déjà des notes de calcul sorties d'une IA.\nSans les refaire.",
    "logistique": "Vos étudiants rendent déjà des études de flux dont les chiffres sortent d'une IA.\nChiffres que personne n'a contrôlés.",
    "hotellerie": "Vos étudiants rédigent déjà leurs rapports de stage avec une IA.\nEt ils ne savent pas s'en servir pour le métier qui les attend.",
    "agro": "Vos étudiants rendent déjà des analyses de données produites par une IA.\nSans savoir ce qu'elles valent.",
    "commerce": "Vos étudiants rendent déjà des études de marché avec des chiffres inventés par une IA.\nEt ils ne le savent même pas.",
    "communication": "Vos étudiants produisent déjà leurs dossiers avec une IA.\nSans se douter de ce que ça pose comme problème de droits.",
    "ingenieur": "Vos étudiants rendent déjà des notes techniques écrites par une IA.\nSans savoir refaire le calcul qu'il y a derrière.",
    "universite": "Vos étudiants rendent déjà des exposés et des mémoires écrits par une IA.\nVos enseignants le voient sans pouvoir le prouver.",
    "lycee": "Vos élèves rendent déjà des exposés écrits par une IA.\nVos enseignants le voient sans pouvoir le prouver.",
    "formation": "Vos apprenants utilisent déjà l'IA tous les jours.\nAucun ne sait s'en servir pour le métier qu'il vise.",
    "defaut": "Vos étudiants rendent déjà des travaux écrits par une IA.\nVos enseignants le voient sans pouvoir le prouver.",
}
