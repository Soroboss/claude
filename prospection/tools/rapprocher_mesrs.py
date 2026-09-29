# -*- coding: utf-8 -*-
"""Rapproche la liste MESRS de la base existante et produit la fusion.

Les noms MESRS sont les raisons sociales completes ('GROUPE ECOLES D'INGENIEURS
AGITEL-FORMATION'), la base utilise des formes courtes ('AGITEL-FORMATION') :
aucune cle de chaine ne les relie. On score donc plusieurs signaux et on ne retient
que le meilleur candidat par ligne de base.
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from segments import _sans_accent

ICI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(ICI, "..", "ecoles-ci-contacts.csv")
MESRS = os.path.join(ICI, "..", "mesrs", "mesrs-parse.csv")

STOP = {"de", "du", "des", "la", "le", "les", "d", "l", "et", "en", "groupe", "ecole",
        "ecoles", "superieure", "superieur", "institut", "centre", "abidjan", "cote",
        "ivoire", "ci", "formation", "internationale", "international", "academie",
        "grande", "hautes", "etudes", "professionnelle", "technique", "technologie"}

COMMUNES = ["abobo", "adjame", "attecoube", "cocody", "koumassi", "marcory", "plateau",
            "port-bouet", "treichville", "yopougon", "bingerville", "anyama", "songon",
            "riviera", "angre", "bouake", "yamoussoukro", "daloa", "korhogo", "san pedro",
            "man", "gagnoa", "abengourou", "divo", "toumodi", "bouafle", "dabou",
            "grand-bassam", "agboville", "soubre", "seguela", "odienne", "bondoukou"]


def toks(n):
    n = _sans_accent(re.sub(r"\([^()]*\)", " ", n)).lower()
    return {t for t in re.findall(r"[a-z0-9]+", n) if t not in STOP and len(t) > 2}


def sigles(n):
    s = set(re.findall(r"\(([^()]+)\)", n.upper()))
    tete = n.split(" - ")[0].strip()
    if re.fullmatch(r"[A-Z0-9\-]{3,12}", tete):
        s.add(tete)
    m = re.match(r"^([A-Z]{3,10})\b", n.strip())
    if m:
        s.add(m.group(1))
    return {re.sub(r"[^A-Z0-9]", "", x) for x in s
            if len(re.sub(r"[^A-Z0-9]", "", x)) >= 3}


def communes(*textes):
    t = _sans_accent(" ".join(textes)).lower()
    return {c for c in COMMUNES if c in t}


def charger(chemin, entete):
    lg = [l.rstrip("\n").split(";") for l in open(chemin, encoding="utf-8")]
    if entete:
        lg = lg[1:]
    return [l for l in lg if l and l[0].strip()]


def score(b, n):
    """email=10 (preuve), sigle=5 (fort), commune=3 (tranche les reseaux), noms=1."""
    pts, raisons = 0, []
    mb, mn = b[8].strip().lower(), n[8].strip().lower()
    if mb and mb == mn:
        pts += 10
        raisons.append("email")
    inter = sigles(b[0]) & sigles(n[0])
    if inter:
        pts += 5
        raisons.append("sigle:" + ",".join(sorted(inter)))
    cb, cn = communes(b[0], b[3]), communes(n[0], n[3])
    if cb and cn:
        if cb & cn:
            pts += 3
            raisons.append("commune")
        else:
            pts -= 6          # campus different : c'est un autre etablissement
            raisons.append("COMMUNE DIVERGENTE")
    tb, tn = toks(b[0]), toks(n[0])
    if tb and tn and (tb <= tn or tn <= tb):
        pts += 1
        raisons.append("noms")
    return pts, raisons


def rapprocher():
    base = charger(BASE, True)
    mesrs = charger(MESRS, False)
    paires, pris = {}, {}
    for i, b in enumerate(base):
        meilleur = (0, None, None)
        for j, n in enumerate(mesrs):
            pts, r = score(b, n)
            if pts > meilleur[0]:
                meilleur = (pts, j, r)
        pts, j, r = meilleur
        if pts >= 5:                       # sigle seul suffit, nom seul jamais
            if j in pris and pris[j][0] >= pts:
                continue                   # deja pris par une meilleure ligne de base
            pris[j] = (pts, i)
            paires[i] = (j, pts, r)
    # un index MESRS ne peut servir qu'une fois
    final = {i: v for i, v in paires.items() if pris.get(v[0], (0, -1))[1] == i}
    return base, mesrs, final


if __name__ == "__main__":
    base, mesrs, final = rapprocher()
    print(f"{len(final)} rapprochements retenus sur {len(base)} lignes de base\n")
    for i in sorted(final):
        j, pts, r = final[i]
        b, n = base[i], mesrs[j]
        maj = ""
        if not b[8].strip() and n[8].strip():
            maj = f"  ==> MAIL RECUPERE : {n[8]}"
        elif b[8].strip() and n[8].strip() and b[8].lower() != n[8].lower():
            maj = f"  ==> MAIL DIFFERENT base={b[8]} mesrs={n[8]}"
        print(f"[{pts:2d}] {b[0][:44]:46s} <- {n[0][:44]:46s} {'+'.join(r)}{maj}")
