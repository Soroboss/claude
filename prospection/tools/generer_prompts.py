#!/usr/bin/env python3
"""Genere le prompt du programme premium, deja rempli, pour chaque etablissement.

Usage: python3 tools/generer_prompts.py
Sortie : programme-premium/prompts-par-ecole.csv
"""
import csv
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "tools"))
from segments import TEXTES, nom_affiche, segment  # noqa: E402

# Libelle de filiere lisible, deduit du segment : le type brut de la base ne se met pas
# dans une phrase ("Grande ecole publique - numerique" ne se lit pas).
FILIERES = {
    "numerique": "informatique, réseaux et numérique",
    "sante": "santé et paramédical",
    "btp": "bâtiment, travaux publics et génie civil",
    "logistique": "logistique, transport et transit",
    "hotellerie": "hôtellerie, restauration et tourisme",
    "agro": "agronomie et agro-industrie",
    "commerce": "commerce, gestion et finance",
    "communication": "communication, arts et création",
    "ingenieur": "ingénierie et sciences techniques",
    "universite": "filières universitaires",
    "lycee": "enseignement technique et professionnel",
    "formation": "formation professionnelle",
    "defaut": "filières tertiaires et techniques",
}

GABARIT = """Tu es responsable pédagogique chez BIG RÉUSSITE, organisme de formation basé à Abidjan. \
Rédige le programme d'une séance de formation, destiné à être lu par {cible} {ecole}, \
établissement situé à {ville} qui forme des {public} en {filiere}.

FORMAT, à respecter strictement : une seule page, 400 mots maximum titres compris. \
Un titre, puis 5 blocs : Le constat, L'objectif, Le déroulé, Ce que repart avec chaque {singulier}, \
Conditions pratiques. Le déroulé est un tableau minuté de 7 séquences, durées en minutes, \
total exactement 120. Ton professionnel et direct, aucune formule creuse, aucun superlatif, aucun emoji.

FOND : le constat part d'un fait que le lecteur vérifie lui-même dans son établissement, \
ses {public} rendent déjà {travaux} écrit en partie par une IA sans qu'aucune règle d'usage \
ne leur ait été donnée. N'invente aucun chiffre, aucune étude, aucun pourcentage. \
Le déroulé couvre : ce qu'est réellement l'IA, une démonstration en direct, un atelier où chaque \
{singulier} manipule sur son propre téléphone, les cas d'usage propres à {filiere}, les 5 pièges \
(hallucination, plagiat, dépendance, données personnelles, triche), l'IA face à un recruteur, \
la remise des attestations. L'atelier pratique est la séquence la plus longue. \
{apport}

CONDITIONS PRATIQUES : une salle, un vidéoprojecteur, une prise. Les {public} utilisent leur propre \
téléphone, aucune salle informatique nécessaire. Effectif conseillé 20 à 60.

INTERDITS : ne mentionne aucun prix, aucun tarif, aucune durée d'engagement."""


def main():
    base = list(csv.reader(open(RACINE / "ecoles-ci-contacts.csv", encoding="utf-8"), delimiter=";"))[1:]
    dossier = RACINE / "programme-premium"
    dossier.mkdir(exist_ok=True)

    with open(dossier / "prompts-par-ecole.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ecole", "filiere", "prompt_programme"])
        for l in base:
            seg = segment(l[1])
            t = TEXTES[seg]
            w.writerow([
                l[0],
                FILIERES[seg],
                GABARIT.format(
                    cible="le Proviseur de" if "Proviseur" in l[10] else "le Directeur des Études de",
                    ecole=nom_affiche(l[0]),
                    ville=l[3],
                    public=t["public"],
                    singulier=t["public"].rstrip("s"),   # « chaque étudiant », pas « chaque étudiants »
                    filiere=FILIERES[seg],
                    travaux=t["travaux"],
                    apport=t["apport"],
                ),
            ])
    print(f"programme-premium/prompts-par-ecole.csv : {len(base)} prompts prets a copier")


if __name__ == "__main__":
    main()
