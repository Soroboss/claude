# -*- coding: utf-8 -*-
"""Extrait les 30 fiches module du catalogue de SORO Nagony Adama en donnees structurees.

Source : catalogue/source-catalogue.txt, texte du PDF
'Catalogue_Modules_Formation_SORO_Nagony_Adama.pdf' (Drive, version du 17/09/2026).
Tout ce que le catalogue Ecoles dit d'un module vient d'ici, mot pour mot :
on ne reecrit pas les objectifs d'un formateur.
"""
import json
import pathlib
import re

ICI = pathlib.Path(__file__).resolve().parent.parent / "catalogue"


def nettoyer(t):
    # pieds de page et en-tetes repetes a chaque page du PDF
    t = re.sub(r"SORO Nagony Adama · \+225[^\n]*— page \d+\n*", "", t)
    t = re.sub(r"Catalogue de modules de formation — Soro Nagony Adama\n*", "", t)
    return t.replace("\\.", ".")


def puces(bloc):
    out, cour = [], None
    for ligne in bloc.split("\n"):
        l = ligne.strip()
        if not l:
            continue
        if l.startswith("•"):
            if cour:
                out.append(cour)
            cour = l.lstrip("• ").strip()
        elif cour is not None:
            cour += " " + l                       # puce coupee sur deux lignes
    if cour:
        out.append(cour)
    return out


def entre(t, debut, fins):
    i = t.find(debut)
    if i < 0:
        return ""
    i += len(debut)
    j = min([k for k in (t.find(f, i) for f in fins) if k >= 0] or [len(t)])
    return t[i:j].strip()


def main():
    brut = (ICI / "source-catalogue.txt").read_text(encoding="utf-8")
    t = nettoyer(brut)
    # rfind : ces titres figurent aussi dans le sommaire, en tete de document
    corps = t[t.rfind("5. Fiches détaillées des modules"):t.rfind("6. Parcours combinés")]
    # une fiche commence par 'A1 — Titre' en debut de ligne
    ancres = list(re.finditer(r"^([A-G][1-5]) — (.+)$", corps, re.M))
    modules = []
    for k, a in enumerate(ancres):
        fiche = corps[a.start():ancres[k + 1].start() if k + 1 < len(ancres) else len(corps)]
        # le domaine qui suit peut s'etre glisse en fin de fiche
        fiche = re.split(r"\nDomaine [A-G] — ", fiche)[0]
        vol = re.search(r"Volume horaire\s+Présentiel À distance Total[^\n]*\n\s*(\d+) h[^\n]*?(\d+) h (\d+) h", fiche)
        titre = a.group(2).strip()
        # un titre peut deborder sur la ligne suivante
        suite = fiche.split("\n")[1].strip()
        if suite and not suite.startswith("Niveau"):
            titre += " " + suite
        modules.append({
            "code": a.group(1),
            "titre": titre,
            "niveau": entre(fiche, "Niveau :", ["\n"]),
            "public": entre(fiche, "Public visé :", ["\nPrérequis"]).replace("\n", " "),
            "prerequis": entre(fiche, "Prérequis :", ["\nObjectifs"]).replace("\n", " "),
            "objectifs": puces(entre(fiche, "l'apprenant est capable de :", ["\nProgramme"])),
            "programme": puces(entre(fiche, "\nProgramme", ["\nVolume horaire"])),
            "presentiel_h": int(vol.group(1)) if vol else None,
            "distance_h": int(vol.group(2)) if vol else None,
            "total_h": int(vol.group(3)) if vol else None,
            "evaluation": entre(fiche, "\nÉvaluation\n", ["\nLivrables"]).replace("\n", " "),
            "livrables": entre(fiche, "Livrables remis à l'apprenant\n", ["\n\n\n", "\nDomaine"]).replace("\n", " ").strip(),
        })
    (ICI / "modules.json").write_text(json.dumps(modules, ensure_ascii=False, indent=1), encoding="utf-8")
    return modules


if __name__ == "__main__":
    m = main()
    print(f"{len(m)} modules, {sum(x['total_h'] or 0 for x in m)} h "
          f"({sum(x['presentiel_h'] or 0 for x in m)} presentiel / {sum(x['distance_h'] or 0 for x in m)} distance)")
