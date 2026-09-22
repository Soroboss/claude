#!/usr/bin/env python3
"""Genere les fichiers d'envoi WhatsApp et e-mail a partir de la base de contacts.

Usage: python3 tools/generer_envois.py
Sorties : envois/whatsapp-envoi.csv et envois/emails-a-envoyer.csv
"""
import csv
import json
import pathlib
from urllib.parse import quote

RACINE = pathlib.Path(__file__).resolve().parent.parent
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
        "Nous animons une séance d'initiation à l'intelligence artificielle de 2h, "
        "directement dans vos classes, avec les téléphones des élèves : aucune salle "
        "informatique nécessaire.\n\n"
        "L'objectif est que vos étudiants sachent utiliser l'IA pour leurs travaux et "
        "pour leur employabilité, au lieu de la subir.\n\n"
        "Puis-je vous envoyer le programme en 1 page ?"
    )


RELANCE_J2 = ("Bonjour, je me permets de revenir vers vous au sujet de la séance d'initiation à l'IA "
              "pour vos classes. Souhaitez-vous que je vous envoie le programme ? Cela prend 2 minutes à lire.")
RELANCE_J7 = ("Bonjour, dernière relance de ma part. Si le sujet n'est pas d'actualité cette année, "
              "dites-le moi simplement et je n'insisterai pas. Si au contraire vous souhaitez en parler, "
              "je reste disponible 15 minutes quand cela vous arrange.")

OBJET = "Initiation à l'IA pour vos classes — une séance de 2h par classe"


def corps_email(ecole):
    lignes = [
        "Madame, Monsieur le Directeur des Études,",
        "",
        f"BIG RÉUSSITE propose aux établissements comme {ecole} un module court d'initiation à "
        "l'intelligence artificielle, conçu pour les étudiants et animé en présentiel dans vos locaux.",
        "",
        "Format : une séance de 2h par classe.",
        "Matériel : les téléphones des étudiants et un vidéoprojecteur. Aucune salle informatique nécessaire.",
        "Livrable : un kit de prompts et une attestation de participation pour chaque étudiant.",
        "",
        "Le module couvre l'usage professionnel de l'IA (travaux, exposés, recherche documentaire), "
        "les cas d'usage propres à chaque filière, et les règles d'usage responsable — un point que "
        "beaucoup d'établissements souhaitent aujourd'hui cadrer auprès de leurs étudiants.",
        "",
        "Je me tiens à votre disposition pour vous présenter le programme détaillé et convenir "
        "d'un créneau test sur une classe.",
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
            msg = message_whatsapp(l[0])
            lien = f"https://wa.me/225{chiffres(numero)}?text={quote(msg)}"
            w.writerow([vague(l), l[0], numero, lien, msg, RELANCE_J2, RELANCE_J7, "", "", ""])
            n += 1

    # --- E-mail ------------------------------------------------------------ #
    with open(dossier / "emails-a-envoyer.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["vague", "ecole", "destinataire", "objet", "corps", "date_envoi", "reponse"])
        m = 0
        for l in base:
            if not l[8]:
                continue
            w.writerow([vague(l), l[0], l[8], OBJET, corps_email(l[0]), "", ""])
            m += 1

    injoignables = [l[0] for l in base if not l[8] and not premier_mobile(l)]
    print(f"envois/whatsapp-envoi.csv    : {n} ecoles avec un numero mobile")
    print(f"envois/emails-a-envoyer.csv  : {m} ecoles avec un email")
    print(f"ni email ni mobile           : {len(injoignables)} -> {', '.join(injoignables[:4])}...")
    print(f"signature utilisee           : {signature()}")


if __name__ == "__main__":
    main()
