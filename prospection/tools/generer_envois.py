#!/usr/bin/env python3
"""Genere les fichiers d'envoi WhatsApp et e-mail a partir de la base de contacts.

Usage: python3 tools/generer_envois.py
Sorties : envois/whatsapp-envoi.csv et envois/emails-a-envoyer.csv
"""
import csv
import json
import pathlib
import sys
from urllib.parse import quote

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "tools"))
from segments import TEXTES, civilite, nom_affiche, segment  # noqa: E402
EXP = json.loads((RACINE / "expediteur.json").read_text(encoding="utf-8"))

# En Cote d'Ivoire, seuls 01 (Moov), 05 (MTN) et 07 (Orange) sont des prefixes mobiles.
# Un fixe en 27 n'a pas de compte WhatsApp : lui envoyer un lien wa.me ne mene nulle part.
PREFIXES_MOBILES = ("01", "05", "07")


def chiffres(numero):
    return numero.replace("+225", "").replace(" ", "").strip()


def est_mobile(numero):
    d = chiffres(numero)
    return len(d) == 10 and d[:2] in PREFIXES_MOBILES


def premier_mobile(ligne):
    """WhatsApp declare d'abord, puis le 2e numero, puis le 1er : le premier mobile trouve gagne."""
    for numero in (ligne[7], ligne[6], ligne[5]):
        if numero and est_mobile(numero):
            return numero
    return ""


def de(nom):
    """Elision : on ecrit d'AGITEL et non de AGITEL devant une voyelle."""
    return f"d'{nom}" if nom[:1].upper() in "AEIOUÉÈÊÀÂÎÔÛ" else f"de {nom}"


def signature():
    parties = [EXP["nom"]]
    if EXP.get("telephone"):
        parties.append(EXP["telephone"])
    return " - ".join(parties)


def qui_parle():
    return f"je suis {EXP['nom']}" if EXP["nom"] != "BIG RÉUSSITE" else "je vous écris de la part de BIG RÉUSSITE"


def message_whatsapp(ecole):
    return (
        f"Bonjour, {qui_parle()}. Je m'adresse au Directeur des Études {de(ecole)}.\n\n"
        "Vos étudiants utilisent déjà l'IA pour leurs exposés et leurs rapports, sans que "
        "personne ne leur ait appris à s'en servir. L'établissement porte le risque, plagiat "
        "et travaux uniformisés, sans en tirer le moindre bénéfice.\n\n"
        "Nous corrigeons cela en une séance de 2h, dans vos classes, sur les téléphones des "
        "étudiants. Aucune salle informatique nécessaire.\n\n"
        "Le sujet est encore neuf ici : les premiers établissements à le cadrer pourront "
        "l'annoncer à leurs futurs étudiants.\n\n"
        "Puis-je vous envoyer le programme en 1 page ?"
    )


RELANCE_J2 = (
    "Bonjour, je me permets de revenir vers vous. La question n'est pas de savoir si vos "
    "étudiants utilisent l'IA, ils le font déjà. Elle est de savoir qui leur apprend à s'en "
    "servir correctement. Souhaitez-vous que je vous envoie le programme ? Deux minutes de lecture."
)
RELANCE_J7 = (
    "Bonjour, dernière relance de ma part. Si le sujet n'est pas d'actualité pour vous cette "
    "année, dites-le moi simplement et je n'insisterai pas. Si au contraire vous voulez en "
    "parler, je reste disponible 15 minutes quand cela vous arrange."
)

OBJET = "Vos étudiants utilisent déjà l'IA — personne ne leur a appris à s'en servir"


def corps_email(ligne):
    """Le mail est personnalise sur la filiere : le travail que rendent leurs etudiants,
    et ce que la seance leur apporte a eux. Un mail generique ne se lit pas."""
    ecole = nom_affiche(ligne[0])
    textes = TEXTES[segment(ligne[1])]
    pub, corpus = textes["public"], textes["corpus"]
    lignes = [
        civilite(ligne[10]),
        "",
        f"Une question simple : combien d'{pub} {de(ecole)} ont rendu ce semestre "
        f"{textes['travaux']}, écrit en partie par une intelligence artificielle ?",
        "",
        "Vos enseignants le sentent souvent, sans pouvoir le prouver. Et c'est l'établissement "
        f"qui porte le risque — travaux uniformisés, {corpus} dont on ne sait plus qui les a "
        f"écrits, valeur du diplôme discutée — alors qu'aucun de vos {pub} n'a jamais reçu la "
        "moindre règle d'usage.",
        "",
        "Le paradoxe est là : ils se servent de cet outil tous les jours, et aucun ne sait "
        "réellement s'en servir. Ni pour produire un travail défendable devant un jury, ni "
        "pour le premier entretien d'embauche qui les attend.",
        "",
        "C'est exactement ce que BIG RÉUSSITE vient corriger. Une séance de 2h, animée en "
        "présentiel dans vos classes : ce qu'est réellement l'IA, comment l'utiliser sur un "
        f"travail sans tomber dans le plagiat, et ce qu'un recruteur attend aujourd'hui. Vos {pub} "
        "travaillent sur leur propre téléphone : aucune salle informatique, aucun "
        "investissement de votre part.",
        "",
        textes["apport"],
        "",
        "Un mot sur le calendrier. Le sujet est encore neuf en Côte d'Ivoire. L'établissement "
        "qui le cadre maintenant ne règle pas seulement un problème interne : il peut l'annoncer "
        f"à ses futurs {pub} et à leurs parents, au moment précis où la question commence à "
        "se poser partout. Dans un an, ce sera la norme, et plus personne n'en tirera d'avantage.",
        "",
        "Je vous propose de commencer par une classe test. Vous jugez sur pièce, et vous "
        "décidez ensuite.",
        "",
        "Cordialement,",
        signature(),
    ]
    return "\n".join(lignes)


def vague(l):
    prive, abidjan, haute = l[2].startswith("Prive"), "Abidjan" in l[3], l[11] == "Haute"
    if prive and abidjan and haute:
        return 1
    return 2 if prive else 3


def main():
    base = list(csv.reader(open(RACINE / "ecoles-ci-contacts.csv", encoding="utf-8"), delimiter=";"))[1:]
    base.sort(key=lambda l: (vague(l), l[0].lower()))
    dossier = RACINE / "envois"

    # --- WhatsApp ---------------------------------------------------------- #
    with open(dossier / "whatsapp-envoi.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["vague", "ecole", "numero_whatsapp", "lien_envoi_clic",
                    "message_a_copier", "relance_J2", "relance_J7",
                    "date_envoi", "reponse", "notes"])
        n = 0
        for l in base:
            numero = premier_mobile(l)
            if not numero:
                continue
            msg = message_whatsapp(nom_affiche(l[0]))
            lien = f"https://wa.me/225{chiffres(numero)}?text={quote(msg)}"
            w.writerow([vague(l), l[0], numero, lien, msg, RELANCE_J2, RELANCE_J7, "", "", ""])
            n += 1

    # --- E-mail ------------------------------------------------------------ #
    with open(dossier / "emails-a-envoyer.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["vague", "ecole", "destinataire", "type_email", "etat_email", "objet", "corps", "segment", "date_envoi"])
        m = 0
        # Une adresse morte a deja rebondi : la relancer ne fait que degrader la reputation
        # de l'expediteur. Les adresses gratuites passent en premier : sur ce lot, elles ont
        # echoue a 13 % contre 32 % pour les domaines propres.
        envoyables = [l for l in base if l[8] and l[14] != "morte"]
        envoyables.sort(key=lambda l: (0 if l[13] == "gratuite" else 1, vague(l), l[0].lower()))
        deja = set()
        for l in envoyables:
            if l[8].lower() in deja:      # meme boite pour deux campus : un seul mail
                continue
            deja.add(l[8].lower())
            w.writerow([vague(l), l[0], l[8], l[13], l[14], OBJET, corps_email(l), segment(l[1]), ""])
            m += 1

    injoignables = [l[0] for l in base if not l[8] and not premier_mobile(l)]
    print(f"envois/whatsapp-envoi.csv    : {n} ecoles avec un numero mobile")
    print(f"envois/emails-a-envoyer.csv  : {m} ecoles avec un email")
    print(f"ni email ni mobile           : {len(injoignables)} -> {', '.join(injoignables[:4])}...")
    print(f"signature utilisee           : {signature()}")


if __name__ == "__main__":
    main()
