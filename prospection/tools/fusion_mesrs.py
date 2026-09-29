# -*- coding: utf-8 -*-
"""Fusionne la liste officielle MESRS dans ecoles-ci-contacts.csv.

Deux operations :
  - les 30 etablissements deja connus sont ENRICHIS (mail, tel, adresse, site
    recuperes sans ecraser ce qui a ete verifie empiriquement) ;
  - les autres sont AJOUTES comme nouveaux prospects.
"""
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rapprocher_mesrs import rapprocher, BASE
from parse_mesrs import type_email

ENTETE = open(BASE, encoding="utf-8").readline().rstrip("\n")


def fusionner():
    base, mesrs, apparies = rapprocher()
    partagees = {m for m, n in Counter(
        l[8].strip().lower() for l in base if l[8].strip()).items() if n > 1}

    journal = {"mail_recupere": [], "mail_remplace": [], "mail_conserve": [],
               "tel_recupere": [], "adresse_recuperee": []}

    for i, (j, pts, _r) in apparies.items():
        b, n = base[i], mesrs[j]
        mb = b[8].strip()
        # --- e-mail ---
        if not mb and n[8]:
            b[8], b[13], b[14] = n[8], type_email(n[8]), "a verifier"
            journal["mail_recupere"].append((b[0], n[8]))
        elif mb and n[8] and mb.lower() != n[8].lower():
            # 'valide' atteste qu'une boite accepte le courrier, pas qu'elle appartient
            # a CE campus : une adresse partagee par deux etablissements de la base est
            # une deduction d'agent, pas un constat. La liste officielle tranche.
            if b[14] == "valide" and mb.lower() not in partagees:
                journal["mail_conserve"].append((b[0], mb, n[8]))
            else:
                journal["mail_remplace"].append((b[0], mb, n[8]))
                b[8], b[13], b[14] = n[8], type_email(n[8]), "a verifier"
        # --- champs factuels : on ne comble que les vides ---
        for idx, nom in ((5, "tel_recupere"), (6, None), (7, None),
                         (4, "adresse_recuperee"), (9, None), (1, None), (15, None)):
            vide = not b[idx].strip()
            # 'defaut' n'est pas un classement, c'est l'absence de classement : les
            # filieres officielles le remplacent utilement.
            if idx == 15 and b[idx].strip() == "defaut":
                vide = True
            if vide and n[idx].strip():
                b[idx] = n[idx]
                if nom:
                    journal[nom].append((b[0], n[idx]))
        b[11] = "Haute"
        if "MESRS" not in b[12]:
            b[12] = (b[12] + " + MESRS").strip(" +")

    pris = {v[0] for v in apparies.values()}
    nouveaux = [n for j, n in enumerate(mesrs) if j not in pris]
    return base, nouveaux, journal


def main():
    base, nouveaux, journal = fusionner()
    out = BASE
    with open(out, "w", encoding="utf-8") as f:
        f.write(ENTETE + "\n")
        for l in base + nouveaux:
            f.write(";".join(l) + "\n")
    print(f"base enrichie : {len(base)} | nouveaux : {len(nouveaux)} "
          f"| total : {len(base) + len(nouveaux)}\n")
    for cle, items in journal.items():
        print(f"-- {cle} : {len(items)}")
        for it in items[:6]:
            print("     ", " | ".join(str(x)[:46] for x in it))
    return base, nouveaux


if __name__ == "__main__":
    main()
