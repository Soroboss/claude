# -*- coding: utf-8 -*-
"""Parse la liste officielle MESRS des grandes ecoles (616 etablissements)
et la convertit dans le schema 16 colonnes de ecoles-ci-contacts.csv.

Source : bac.mesrs-ci.net/offres/grdes-ecoles (donnees fournies brutes).
Format : bloc @@F = liste des filieres indexee 0..117
         bloc @@E = etablissements, 19 colonnes separees par des tabulations
         la derniere colonne pointe vers les indices du bloc @@F.
"""
import re
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_contacts import norm_tel          # migration 8 chiffres + format +225
from segments import segment, _sans_accent   # classifieur de filiere

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mesrs", "raw.txt")

# Boites gratuites : 13 % d'echec constate contre 32 % pour les domaines propres.
# On les privilegie systematiquement quand une cellule contient plusieurs adresses.
GRATUITES = {
    "gmail.com", "yahoo.fr", "yahoo.com", "yahoo.co.uk", "hotmail.com", "hotmail.fr",
    "outlook.com", "outlook.fr", "live.fr", "live.com", "ymail.com", "aviso.ci",
    "orange.ci", "msn.com", "laposte.net", "gmail.fr",
}

# Adresses deja constatees mortes lors de la premiere campagne : on ne les reprend pas.
MORTES = set()


def decouper(chemin):
    lignes = open(chemin, encoding="utf-8").read().split("\n")
    i_f = lignes.index("@@F")
    i_e = lignes.index("@@E")
    i_fin = lignes.index("@@END")
    filieres = [l for l in lignes[i_f + 1:i_e] if l.strip()]
    etabs = [l for l in lignes[i_e + 1:i_fin] if l.strip()]
    return filieres, etabs


def libelle_filiere(brut):
    """'BTS : IDA / INFORMATIQUE DEVELOPPEUR D'APPLICATIONS|BTS' -> (diplome, libelle)."""
    txt = brut.split("¦")[0].strip()
    diplome = "BTS" if txt.upper().startswith("BTS") else "Licence"
    lib = txt
    if "/" in lib:
        lib = lib.split("/", 1)[1]
    else:
        lib = re.sub(r"^(BTS|LICENCE)\s*(:|EN|DE|DES|D')?\s*", "", lib, flags=re.I)
    lib = re.sub(r"\((PRIVE|PUBLIC)\)", "", lib, flags=re.I)
    return diplome, " ".join(lib.split()).capitalize()


def _compact(t):
    return re.sub(r"[^A-Za-z0-9]", "", t).upper()


def nettoyer_nom(nom, sigle):
    """Normalise 'X -(AIST BOUAKE)' -> 'X (AIST BOUAKE)'.

    On ne supprime JAMAIS le contenu des parentheses : pour les reseaux multi-campus
    (AIST, ESCOGET, ITA...) c'est le seul element qui distingue un site d'un autre,
    et le nom sert de cle de deduplication et de cle du menu deroulant du classeur.
    """
    n = " ".join(nom.split())
    n = re.sub(r"\s*-\s*\(", " (", n)          # '-(X)' -> ' (X)'
    n = re.sub(r"\s+\(", " (", n)
    # La source repete parfois le nom entier dans le suffixe : 'GROUPE CEFIAT ABIDJAN
    # -(GROUPE CEFIAT ABIDJAN)'. On retire toute parenthese deja contenue dans le nom.
    hors_par = _compact(re.sub(r"\([^()]*\)", "", n))
    n = re.sub(r"\s*\(([^()]*)\)",
               lambda m: "" if _compact(m.group(1)) in hors_par else m.group(0), n)
    n = n.strip(" -–,")
    s = sigle.strip()
    if s and _compact(s) not in _compact(n):
        # 'PIGIER ... (PIGIER CI PLATEAU)' + sigle 'PIGIER Cl' : meme sigle a une faute
        # de frappe pres. On n'ajoute pas une seconde parenthese redondante.
        existants = re.findall(r"\(([^()]*)\)", n)
        if not (existants and s.split()[0].upper() in n.upper()):
            n = f"{n} ({s})"
    return n


def telephones(cellule):
    """Decoupe une cellule multi-numeros et normalise chacun."""
    bruts = re.split(r"[/;,]|\bet\b|\n", cellule)
    out = []
    for b in bruts:
        b = b.strip()
        if not b:
            continue
        n = norm_tel(b)
        if n.startswith("+225") and n not in out:
            out.append(n)
    return out


def est_mobile(num):
    """Seuls les prefixes 01 / 05 / 07 portent un compte WhatsApp (le 27 est fixe)."""
    d = re.sub(r"\D", "", num)[-10:]
    return d[:2] in ("01", "05", "07")


def emails(cellule):
    """Extrait les adresses, boites gratuites en tete (regle de deliverabilite)."""
    trouves = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", cellule)
    vues, propres = [], []
    for e in trouves:
        e = e.strip(" .,;").lower()
        if e in MORTES or e in vues or e in propres:
            continue
        (vues if e.split("@")[-1] in GRATUITES else propres).append(e)
    return vues + propres


def type_email(mail):
    if not mail:
        return ""
    return "gratuite" if mail.split("@")[-1] in GRATUITES else "domaine propre"


PUBLIC = re.compile(r"\bnational|\bd'etat\b|\betat\b|\binp-hb\b|\bpublic\b", re.I)


def statut(nom):
    return "Public" if PUBLIC.search(_sans_accent(nom)) else "Prive"


# Filieres que _REGLES (concu pour des TYPES d'etablissement) ne classe pas.
_FILIERE_EXTRA = [
    ("commerce",  r"assistanat|entrepreneuriat|immobilier|juridique|fiscalite|droit|statistique"),
    ("ingenieur", r"hygiene|securite|incendie|maintenance|energetique|electrotechnique|qualite"),
    ("agro",      r"environnement|ressources naturelles|developpement durable"),
]


def segment_filiere(libelle):
    s = segment(libelle)
    if s != "defaut":
        return s
    t = _sans_accent(libelle).lower()
    for nom, motif in _FILIERE_EXTRA:
        if re.search(motif, t):
            return nom
    return "defaut"


def segment_etab(nom, libelles):
    """Le nom porte l'identite de l'ecole ; les filieres ne tranchent qu'en cas de net ecart.

    Ces ecoles offrent en general 9 a 16 filieres couvrant tous les domaines : designer
    un segment 'dominant' a une voix d'ecart revient a tirer au sort (c'est ce qui gonflait
    artificiellement 'agro'). Un specialiste doit donc devancer le second de 2 voix au moins.
    A defaut l'ecole est polyvalente, et c'est le socle tertiaire - que toutes enseignent -
    qui cadre notre argumentaire.
    """
    par_nom = segment(nom)
    if par_nom not in ("defaut", "formation"):
        return par_nom
    votes = Counter(segment_filiere(l) for l in libelles)
    votes.pop("defaut", None)
    if not votes:
        return par_nom
    classement = votes.most_common()
    tete, n_tete = classement[0]
    n_second = classement[1][1] if len(classement) > 1 else 0
    if n_tete - n_second >= 2:
        return tete
    return "commerce" if "commerce" in votes else tete


def libelle_type(diplomes, libelles):
    """Colonne 'type' : lisible en une ligne dans le classeur."""
    dip = "/".join(d for d in ("BTS", "Licence") if d in diplomes) or "BTS"
    doms = []
    for l in libelles:
        court = l.split(" option ")[0].split(" et ")[0].strip()
        if court and court not in doms:
            doms.append(court)
    return f"Grande ecole {dip} - " + ", ".join(doms[:3]).lower()


def main():
    filieres_brut, etabs = decouper(RAW)
    table = [libelle_filiere(f) for f in filieres_brut]
    lignes = []
    for ligne in etabs:
        c = ligne.split("\t")
        nom = nettoyer_nom(c[2], c[7])
        ville, commune = c[3].strip().title(), c[4].strip().title()
        lieu = f"{ville} - {commune}" if commune and commune != ville else ville
        tels = telephones(c[10])
        wa = next((t for t in tels if est_mobile(t)), "")
        mails = emails(c[11])
        mail = mails[0] if mails else ""
        idx = [int(i) for i in re.findall(r"\d+", c[18])]
        libelles = [table[i][1] for i in idx if i < len(table)]
        diplomes = {table[i][0] for i in idx if i < len(table)}
        site = c[12].strip()
        if site and not site.startswith("http"):
            site = "https://" + site.lstrip("/")
        lignes.append([
            nom,
            libelle_type(diplomes, libelles),
            statut(nom),
            lieu,
            " ".join(c[9].split()),
            tels[0] if tels else "",
            tels[1] if len(tels) > 1 else "",
            wa,
            mail,
            site,
            "Directeur des Etudes",
            "Haute",
            "MESRS - liste officielle grandes ecoles",
            type_email(mail),
            "a verifier" if mail else "sans email",
            segment_etab(nom, libelles),
        ])
    # garde-fou : un ';' dans un champ decale silencieusement toute la ligne
    lignes = [[ch.replace(";", ",").strip() for ch in l] for l in lignes]
    out = os.path.join(os.path.dirname(RAW), "mesrs-parse.csv")
    with open(out, "w", encoding="utf-8") as f:
        for l in lignes:
            f.write(";".join(l) + "\n")
    print(f"{len(lignes)} etablissements -> {out}")
    return lignes


if __name__ == "__main__":
    main()
