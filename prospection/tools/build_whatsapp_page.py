#!/usr/bin/env python3
"""Genere la page HTML d'envoi WhatsApp depuis la base de contacts.

Usage: python3 tools/build_whatsapp_page.py
Sortie : envois/whatsapp.html
"""
import csv
import json
import pathlib
import re
import unicodedata

RACINE = pathlib.Path(__file__).resolve().parent.parent
PREFIXES_MOBILES = ("01", "05", "07")


def chiffres(numero):
    return numero.replace("+225", "").replace(" ", "").strip()


def est_mobile(numero):
    d = chiffres(numero)
    return len(d) == 10 and d[:2] in PREFIXES_MOBILES


def premier_mobile(ligne):
    for numero in (ligne[7], ligne[6], ligne[5]):
        if numero and est_mobile(numero):
            return numero
    return ""


def slug(nom):
    s = unicodedata.normalize("NFKD", nom.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


def vague(l):
    prive, abidjan, haute = l[2].startswith("Prive"), "Abidjan" in l[3], l[11] == "Haute"
    if prive and abidjan and haute:
        return 1
    return 2 if prive else 3


def main():
    base = list(csv.reader(open(RACINE / "ecoles-ci-contacts.csv", encoding="utf-8"), delimiter=";"))[1:]
    base.sort(key=lambda l: (vague(l), l[0].lower()))

    ecoles, vus = [], set()
    for l in base:
        numero = premier_mobile(l)
        if not numero:
            continue
        identifiant = slug(l[0])
        while identifiant in vus:          # deux campus d'un meme groupe ne doivent pas partager un id
            identifiant += "-2"
        vus.add(identifiant)
        ecoles.append({
            "id": identifiant,
            "nom": l[0],
            "lieu": l[3],
            "tel": numero,
            "num": chiffres(numero),
            "vague": vague(l),
            "sansmail": l[14] == "sans email",   # aucune adresse exploitable : WhatsApp est le seul canal
        })

    gabarit = (RACINE / "tools" / "whatsapp_page.html").read_text(encoding="utf-8")
    sortie = gabarit.replace("__ECOLES__", json.dumps(ecoles, ensure_ascii=False))
    (RACINE / "envois" / "whatsapp.html").write_text(sortie, encoding="utf-8")
    print(f"envois/whatsapp.html : {len(ecoles)} ecoles, {len(sortie) // 1024} Ko")


if __name__ == "__main__":
    main()
