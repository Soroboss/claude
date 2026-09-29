# -*- coding: utf-8 -*-
"""Regenere les fichiers ouvrables dans Google Sheets depuis la base.

Ces fichiers etaient tenus a la main : ils sont restes a 105 ecoles quand la base
en comptait 690. Ils sont desormais generes, donc toujours a jour.

La saisie manuelle (nom du directeur, statut, montants, notes) est RELUE et reportee :
regenerer ne doit jamais effacer le travail de prospection deja fait.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generer_envois import vague

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..")
BASE = os.path.join(RACINE, "ecoles-ci-contacts.csv")
SHEETS = os.path.join(RACINE, "sheets")

SUIVI = ["vague", "ecole", "ville_commune", "telephone_1", "whatsapp", "email",
         "etat_email", "segment", "nom_du_directeur_des_etudes", "date_1er_contact",
         "statut", "montant_par_eleve", "nb_eleves", "nb_seances_negocie",
         "nb_classes", "date_seance", "montant_attendu", "notes"]
# Colonnes remplies a la main pendant la prospection : a preserver coute que coute.
SAISIE = SUIVI[8:]
# Valeurs que le generateur pose lui-meme : les relire comme de la saisie ferait
# ecraser une vraie valeur par un defaut au passage suivant.
DEFAUTS = {"statut": "A contacter", "nb_seances_negocie": "1"}


def lire_saisie():
    """Releve ce qui a deja ete saisi, indexe par nom d'ecole."""
    garde = {}
    for chemin, sep in ((os.path.join(RACINE, "suivi-appels.csv"), ";"),
                        (os.path.join(SHEETS, "suivi-appels.csv"), ",")):
        if not os.path.exists(chemin):
            continue
        with open(chemin, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f, delimiter=sep):
                vals = {k: (r.get(k) or "").strip() for k in SAISIE}
                reel = {k: v for k, v in vals.items() if v and v != DEFAUTS.get(k)}
                if reel:
                    garde.setdefault((r.get("ecole") or "").strip(), {}).update(reel)
    return garde


def ecrire(chemin, entete, lignes, sep, bom):
    enc = "utf-8-sig" if bom else "utf-8"
    with open(chemin, "w", encoding=enc, newline="") as f:
        w = csv.writer(f, delimiter=sep, lineterminator="\n")
        w.writerow(entete)
        w.writerows(lignes)


def main():
    os.makedirs(SHEETS, exist_ok=True)
    with open(BASE, encoding="utf-8") as f:
        tout = list(csv.reader(f, delimiter=";"))
    entete_base, base = tout[0], [l for l in tout[1:] if l and l[0].strip()]
    garde = lire_saisie()

    suivi = []
    for l in base:
        d = {"vague": str(vague(l)), "ecole": l[0], "ville_commune": l[3],
             "telephone_1": l[5], "whatsapp": l[7], "email": l[8],
             "etat_email": l[14], "segment": l[15], "statut": "A contacter",
             "nb_seances_negocie": "1"}
        d.update(garde.get(l[0], {}))
        suivi.append([d.get(c, "") for c in SUIVI])

    ecrire(os.path.join(SHEETS, "base-contacts.csv"), entete_base, base, ",", True)
    ecrire(os.path.join(SHEETS, "suivi-appels.csv"), SUIVI, suivi, ",", True)
    ecrire(os.path.join(RACINE, "suivi-appels.csv"), SUIVI, suivi, ";", False)
    print(f"sheets/base-contacts.csv : {len(base)} ecoles")
    print(f"sheets/suivi-appels.csv  : {len(suivi)} ecoles "
          f"({len(garde)} avec saisie reportee)")
    print(f"suivi-appels.csv         : {len(suivi)} ecoles")


if __name__ == "__main__":
    main()
