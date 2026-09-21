#!/usr/bin/env python3
"""Fusionne des lignes CSV de contacts dans la base maitre, avec dedoublonnage et controle qualite.

Usage: python3 merge_contacts.py <base.csv> <nouvelles_lignes.csv> [...]
Les fichiers de nouvelles lignes sont SANS en-tete, separateur ';'.
"""
import re
import sys
import unicodedata

COLS = 13
HEADER = ("ecole;type;statut;ville_commune;adresse;telephone_1;telephone_2;"
          "whatsapp;email;site_web;interlocuteur_cible;fiabilite;source")


def cle(nom):
    """Cle de dedoublonnage : nom normalise, sans accents, sigles et bruit retires."""
    s = unicodedata.normalize("NFKD", nom.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\b(groupe|ecole|institut|superieur[e]?|universite|centre|de|du|des|d|la|le|les|et|l)\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


# Migration numerotation Cote d'Ivoire (janvier 2021) : les anciens numeros a 8 chiffres
# ne fonctionnent plus. Regle officielle : les fixes prennent le prefixe 27, les mobiles
# prennent le prefixe de leur operateur, determine par les 2 premiers chiffres.
_ORANGE = {"07", "08", "09", "47", "48", "49", "57", "58", "59", "77", "78", "79", "87", "88", "89"}
_MTN = {"04", "05", "06", "44", "45", "46", "54", "55", "56", "64", "65", "66", "74", "75", "76", "84", "85", "86"}
_MOOV = {"01", "02", "03", "40", "41", "42", "50", "51", "52", "60", "61", "62", "70", "71", "72"}


def _migrer_8_chiffres(d):
    """Convertit un ancien numero a 8 chiffres vers le format 10 chiffres post-2021."""
    if d[0] in "23":                      # ligne fixe
        return "27" + d
    prefixe = d[:2]
    if prefixe in _ORANGE:
        return "07" + d
    if prefixe in _MTN:
        return "05" + d
    if prefixe in _MOOV:
        return "01" + d
    return ""                             # operateur indetermine : on ne devine pas


def norm_tel(t):
    """Normalise un numero ivoirien au format +225 XX XX XX XX XX.

    Retourne la chaine d'origine si le numero ne peut pas etre normalise de facon sure :
    mieux vaut un numero a verifier qu'un numero invente.
    """
    t = t.strip()
    if not t:
        return ""
    d = re.sub(r"\D", "", t)
    if d.startswith("00"):                # prefixe international
        d = d[2:]
    if d.startswith("225") and len(d) in (11, 13):   # 225 + ancien 8 chiffres, ou 225 + 10 chiffres
        d = d[3:]
    if len(d) == 8:
        d = _migrer_8_chiffres(d) or d
    if len(d) != 10:
        return t
    return "+225 " + " ".join(d[i:i + 2] for i in range(0, 10, 2))


def charger(chemin, avec_entete):
    lignes = []
    with open(chemin, encoding="utf-8") as f:
        for brut in f:
            brut = brut.strip()
            if not brut:
                continue
            if avec_entete and brut.startswith("ecole;"):
                continue
            champs = brut.split(";")
            if len(champs) != COLS:
                print(f"  ! ignoree ({len(champs)} colonnes au lieu de {COLS}): {brut[:70]}", file=sys.stderr)
                continue
            lignes.append([c.strip() for c in champs])
    return lignes


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1

    base_path = sys.argv[1]
    lignes = charger(base_path, avec_entete=True)
    for l in lignes:                    # la base existante est renormalisee a chaque passage
        for i in (5, 6, 7):
            l[i] = norm_tel(l[i])
    vues = {cle(l[0]) for l in lignes}
    ajoutees = doublons = sans_contact = 0

    for chemin in sys.argv[2:]:
        for l in charger(chemin, avec_entete=True):
            if not (l[5] or l[6] or l[8]):      # ni telephone ni email
                sans_contact += 1
                continue
            k = cle(l[0])
            if k in vues:
                doublons += 1
                continue
            for i in (5, 6, 7):
                l[i] = norm_tel(l[i])
            vues.add(k)
            lignes.append(l)
            ajoutees += 1

    lignes.sort(key=lambda l: (l[3].lower(), l[0].lower()))
    with open(base_path, "w", encoding="utf-8") as f:
        f.write(HEADER + "\n")
        for l in lignes:
            f.write(";".join(l) + "\n")

    print(f"Base : {len(lignes)} etablissements "
          f"(+{ajoutees} ajoutes, {doublons} doublons ecartes, {sans_contact} sans contact ecartes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
