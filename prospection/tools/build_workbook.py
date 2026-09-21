#!/usr/bin/env python3
"""Genere le classeur de prospection a partir de la base CSV.

Usage: python3 tools/build_workbook.py
Sortie : prospection-ecoles-ia.xlsx (ouvrable tel quel dans Google Sheets)
"""
import csv
import pathlib

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

RACINE = pathlib.Path(__file__).resolve().parent.parent
POLICE = "Arial"

BLEU = "1F3864"        # en-tetes
JAUNE = "FFF2CC"       # cellules a remplir par l'utilisateur
GRIS = "F2F2F2"        # lignes de rappel non modifiables
VERT = "E2EFDA"        # resultats calcules

STATUTS = ["A contacter", "Contacte", "Relance", "RDV fixe", "En negociation",
           "Signe", "Refuse", "Injoignable"]

BORDURE = Border(*[Side(style="thin", color="D0D0D0")] * 4)


def style_entete(ws, ligne, nb_colonnes):
    for c in range(1, nb_colonnes + 1):
        cell = ws.cell(row=ligne, column=c)
        cell.font = Font(name=POLICE, bold=True, color="FFFFFF", size=10)
        cell.fill = PatternFill("solid", fgColor=BLEU)
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[ligne].height = 30


def largeurs(ws, valeurs):
    for i, l in enumerate(valeurs, start=1):
        ws.column_dimensions[get_column_letter(i)].width = l


def lire_base():
    with open(RACINE / "ecoles-ci-contacts.csv", encoding="utf-8") as f:
        return list(csv.reader(f, delimiter=";"))


def vague(l):
    """Vague 1 = prive, Abidjan, contact verifie sur site officiel."""
    prive, abidjan, haute = l[2].startswith("Prive"), "Abidjan" in l[3], l[11] == "Haute"
    if prive and abidjan and haute:
        return 1
    if prive and (abidjan or True):
        return 2
    return 3


# --------------------------------------------------------------------------- #
wb = Workbook()

# ---- 1. Mode d'emploi ----------------------------------------------------- #
ws = wb.active
ws.title = "Mode d'emploi"
largeurs(ws, [4, 34, 86])
lignes = [
    ("", "PROSPECTION GRANDES ECOLES - INITIATION A L'IA", ""),
    ("", "", ""),
    ("", "Onglet", "A quoi il sert"),
    ("", "Suivi appels", "LA feuille de travail. Une ligne par ecole. C'est le seul onglet a remplir."),
    ("", "Tableau de bord", "Se calcule tout seul depuis Suivi appels. Ne rien y saisir."),
    ("", "Base contacts", "La fiche complete de chaque ecole : adresse, 2e numero, site, source, fiabilite."),
    ("", "Offre et tarifs", "Ce qui est vendu et a quel prix. Le tableau de CA se recalcule si on change un montant."),
    ("", "Scripts et objections", "Quoi dire en WhatsApp, au telephone, par mail, et quoi repondre aux objections."),
    ("", "", ""),
    ("", "Colonnes a remplir (fond jaune)", ""),
    ("", "Nom du Directeur des Etudes", "A demander des le premier appel au standard. C'est l'information qui manque et qui fera la valeur de cette base."),
    ("", "Date 1er contact", "Format JJ/MM/AAAA."),
    ("", "Statut", "Liste deroulante. Fait vivre le tableau de bord."),
    ("", "Montant par eleve", "5000 ou 10000 FCFA. C'est l'etablissement qui le fixe."),
    ("", "Nb eleves par classe", "Effectif reel qui paiera. Seuil de rentabilite : 20."),
    ("", "Nb seances negocie", "1 par defaut. Passer a 2 seulement si la 2e seance a ete negociee."),
    ("", "Nb classes", "Nombre de classes engagees par l'etablissement."),
    ("", "Date seance", "Format JJ/MM/AAAA."),
    ("", "", ""),
    ("", "Colonne calculee (fond vert)", ""),
    ("", "Montant attendu", "= (montant par eleve + supplement) x nb eleves x nb classes."),
    ("", "", "Supplement applique : +3 000 FCFA par eleve si une 2e seance est negociee au palier 5 000."),
    ("", "", "Au palier 10 000, la 2e seance est incluse : aucun supplement. Regle definie dans Offre et tarifs."),
    ("", "", ""),
    ("", "Avertissement sur les numeros", ""),
    ("", "", "Les numeros en fiabilite Moyenne viennent d'annuaires et n'ont pas ete verifies un par un."),
    ("", "", "Les anciens numeros a 8 chiffres ont ete convertis au format post-2021. En cas d'echec, essayer le 2e numero de l'onglet Base contacts."),
]
for i, (a, b, c) in enumerate(lignes, start=1):
    ws.cell(row=i, column=2, value=b).font = Font(name=POLICE, bold=b in (
        "PROSPECTION GRANDES ECOLES - INITIATION A L'IA", "Onglet",
        "Colonnes a remplir (fond jaune)", "Colonne calculee (fond vert)",
        "Avertissement sur les numeros"), size=14 if i == 1 else 10)
    ws.cell(row=i, column=3, value=c).font = Font(name=POLICE, size=10)
    ws.cell(row=i, column=3).alignment = Alignment(wrap_text=True, vertical="top")
ws.cell(row=3, column=2).fill = ws.cell(row=3, column=3).fill = PatternFill("solid", fgColor=GRIS)
ws.sheet_view.showGridLines = False

# ---- 2. Suivi appels ------------------------------------------------------ #
base = lire_base()[1:]
base.sort(key=lambda l: (vague(l), l[0].lower()))

sv = wb.create_sheet("Suivi appels")
entetes = ["Vague", "Ecole", "Commune", "Telephone", "WhatsApp", "Email",
           "Nom du Directeur des Etudes", "Date 1er contact", "Statut",
           "Montant par eleve", "Nb eleves par classe", "Nb seances negocie",
           "Nb classes", "Date seance", "Montant attendu (FCFA)", "Notes"]
sv.append(entetes)
style_entete(sv, 1, len(entetes))
largeurs(sv, [7, 46, 30, 19, 19, 30, 28, 15, 16, 13, 12, 12, 11, 13, 20, 34])

MONTANT = ('=IF(OR($J{r}="",$K{r}="",$M{r}=""),"",'
           '($J{r}+IF(AND($L{r}>=2,$J{r}=5000),3000,0))*$K{r}*$M{r})')

# Ligne d'exemple, a supprimer par l'utilisateur une fois le fonctionnement compris
sv.append([1, "EXEMPLE - supprimer cette ligne", "Abidjan - Cocody", "+225 27 22 00 00 00",
           "+225 07 00 00 00 00", "exemple@ecole.ci", "M. KOUAME", "15/10/2026", "Signe",
           5000, 40, 2, 3, "22/10/2026", MONTANT.format(r=2),
           "2e seance negociee : +3 000 F/eleve applique automatiquement"])

for i, l in enumerate(base, start=3):
    wa = l[7] or l[6] or ""      # a defaut de WhatsApp declare, le 2e numero est souvent mobile
    sv.append([vague(l), l[0], l[3], l[5], wa, l[8], "", "", "A contacter",
               None, None, 1, None, "", MONTANT.format(r=i), ""])

derniere = sv.max_row
for r in range(2, derniere + 1):
    for c in range(1, len(entetes) + 1):
        cell = sv.cell(row=r, column=c)
        cell.font = Font(name=POLICE, size=10)
        cell.border = BORDURE
        cell.alignment = Alignment(vertical="center")
        if c in (7, 8, 9, 10, 11, 12, 13, 14, 16):
            cell.fill = PatternFill("solid", fgColor=JAUNE)
        elif c == 15:
            cell.fill = PatternFill("solid", fgColor=VERT)
    sv.cell(row=r, column=15).number_format = '#,##0 "F";-#,##0 "F";"-"'
    sv.cell(row=r, column=10).number_format = '#,##0'
for c in range(1, len(entetes) + 1):
    sv.cell(row=2, column=c).font = Font(name=POLICE, size=10, italic=True, color="808080")

sv.freeze_panes = "B2"
sv.auto_filter.ref = f"A1:P{derniere}"

dv_statut = DataValidation(type="list", formula1='"' + ",".join(STATUTS) + '"', allow_blank=True)
dv_montant = DataValidation(type="list", formula1='"5000,10000"', allow_blank=True)
dv_seances = DataValidation(type="list", formula1='"1,2"', allow_blank=True)
for dv, col in ((dv_statut, "I"), (dv_montant, "J"), (dv_seances, "L")):
    sv.add_data_validation(dv)
    dv.add(f"{col}2:{col}{derniere}")

# ---- 3. Tableau de bord --------------------------------------------------- #
tb = wb.create_sheet("Tableau de bord", 1)
largeurs(tb, [4, 40, 22, 60])
P = f"'Suivi appels'!$I$3:$I${derniere}"      # la ligne 2 est l'exemple : exclue de tous les calculs
M = f"'Suivi appels'!$O$3:$O${derniere}"
V = f"'Suivi appels'!$A$3:$A${derniere}"

tb.cell(row=1, column=2, value="TABLEAU DE BORD").font = Font(name=POLICE, bold=True, size=14)
tb.cell(row=2, column=2, value="Tout se calcule depuis l'onglet Suivi appels. La ligne d'exemple est exclue."
        ).font = Font(name=POLICE, size=9, italic=True, color="808080")

blocs = [
    (4, "Ecoles dans la base", f"=COUNTA('Suivi appels'!$B$3:$B${derniere})", "0", "Toutes vagues confondues"),
    (5, "Ecoles contactees", f'=COUNTIFS({P},"<>A contacter")', "0", "Statut different de A contacter"),
    (6, "RDV fixes", f'=COUNTIFS({P},"RDV fixe")', "0", ""),
    (7, "En negociation", f'=COUNTIFS({P},"En negociation")', "0", ""),
    (8, "Ecoles signees", f'=COUNTIFS({P},"Signe")', "0", ""),
    (9, "Taux de transformation", f'=IFERROR(COUNTIFS({P},"Signe")/COUNTIFS({P},"<>A contacter"),"")',
     "0.0%", "Signees / contactees"),
    (11, "CA signe", f'=SUMIFS({M},{P},"Signe")', '#,##0 "F"', "Somme des montants attendus au statut Signe"),
    (12, "CA en negociation", f'=SUMIFS({M},{P},"En negociation")', '#,##0 "F"', ""),
    (13, "CA potentiel total", f'=SUM({M})', '#,##0 "F"', "Tout ce qui est renseigne, tous statuts"),
    (15, "Vague 1 - restant a contacter", f'=COUNTIFS({V},1,{P},"A contacter")', "0", "Prive Abidjan, contact verifie"),
    (16, "Vague 2 - restant a contacter", f'=COUNTIFS({V},2,{P},"A contacter")', "0", "Prive, contact a qualifier"),
    (17, "Vague 3 - restant a contacter", f'=COUNTIFS({V},3,{P},"A contacter")', "0", "Public, circuit long"),
]
for r, libelle, formule, fmt, note in blocs:
    tb.cell(row=r, column=2, value=libelle).font = Font(name=POLICE, size=10, bold=True)
    c = tb.cell(row=r, column=3, value=formule)
    c.font = Font(name=POLICE, size=11)
    c.number_format = fmt
    c.fill = PatternFill("solid", fgColor=VERT)
    c.alignment = Alignment(horizontal="right")
    c.border = BORDURE
    tb.cell(row=r, column=4, value=note).font = Font(name=POLICE, size=9, color="808080")
tb.sheet_view.showGridLines = False

# ---- 4. Base contacts ----------------------------------------------------- #
bc = wb.create_sheet("Base contacts")
tete = ["Ecole", "Type", "Statut", "Ville / Commune", "Adresse", "Telephone 1",
        "Telephone 2", "WhatsApp", "Email", "Site web", "Interlocuteur cible",
        "Fiabilite", "Source"]
bc.append(tete)
style_entete(bc, 1, len(tete))
largeurs(bc, [46, 42, 18, 30, 56, 19, 19, 19, 30, 28, 32, 11, 32])
for l in sorted(base, key=lambda x: (x[3].lower(), x[0].lower())):
    bc.append(l)
for r in range(2, bc.max_row + 1):
    for c in range(1, len(tete) + 1):
        cell = bc.cell(row=r, column=c)
        cell.font = Font(name=POLICE, size=10)
        cell.border = BORDURE
    if bc.cell(row=r, column=12).value == "Haute":
        bc.cell(row=r, column=12).fill = PatternFill("solid", fgColor=VERT)
bc.freeze_panes = "A2"
bc.auto_filter.ref = f"A1:M{bc.max_row}"

# ---- 5. Offre et tarifs --------------------------------------------------- #
of = wb.create_sheet("Offre et tarifs")
largeurs(of, [4, 34, 26, 26, 46])
of.sheet_view.showGridLines = False


def titre(ws, r, texte, taille=12):
    ws.cell(row=r, column=2, value=texte).font = Font(name=POLICE, bold=True, size=taille)


def texte(ws, r, col, valeur, gras=False, italique=False):
    c = ws.cell(row=r, column=col, value=valeur)
    c.font = Font(name=POLICE, size=10, bold=gras, italic=italique)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    return c


titre(of, 1, "OFFRE - INITIATION A L'INTELLIGENCE ARTIFICIELLE", 14)
texte(of, 2, 2, "Prestation de base : UNE seance de 2h par classe. La 2e seance se negocie, elle n'est jamais promise d'emblee.", italique=True)
texte(of, 3, 2, "Aucun suivi individuel, aucun groupe WhatsApp : l'interlocuteur est l'etablissement, pas l'eleve.", italique=True)

titre(of, 5, "Les deux paliers")
for i, v in enumerate(["Montant par eleve", "Prestation de base", "2e seance"], start=2):
    texte(of, 6, i, v, gras=True).fill = PatternFill("solid", fgColor=GRIS)
of["B7"], of["B8"] = 5000, 10000
for r, presta, negoc in (
    (7, "1 seance de 2h + kit + attestation", "Facturee +3 000 F par eleve"),
    (8, "1 seance de 2h + kit + attestation", "Incluable si la classe fait 40 eleves ou plus"),
):
    of.cell(row=r, column=2).number_format = '#,##0 "F"'
    of.cell(row=r, column=2).font = Font(name=POLICE, size=11, bold=True, color="0000FF")
    of.cell(row=r, column=2).fill = PatternFill("solid", fgColor=JAUNE)
    texte(of, r, 3, presta)
    texte(of, r, 4, negoc)
texte(of, 9, 2, "Les deux montants ci-dessus sont en bleu : ce sont les seules valeurs a modifier. Le tableau ci-dessous se recalcule.", italique=True)

titre(of, 11, "Chiffre d'affaires par classe, pour 2h de presence")
texte(of, 12, 2, "Effectif de la classe", gras=True).fill = PatternFill("solid", fgColor=GRIS)
texte(of, 12, 3, "A 5 000 F par eleve", gras=True).fill = PatternFill("solid", fgColor=GRIS)
texte(of, 12, 4, "A 10 000 F par eleve", gras=True).fill = PatternFill("solid", fgColor=GRIS)
for i, effectif in enumerate([25, 40, 60, 100]):
    r = 13 + i
    of.cell(row=r, column=2, value=effectif).font = Font(name=POLICE, size=10, color="0000FF")
    of.cell(row=r, column=2).fill = PatternFill("solid", fgColor=JAUNE)
    for col, ref in ((3, "$B$7"), (4, "$B$8")):
        c = of.cell(row=r, column=col, value=f"=$B{r}*{ref}")
        c.font = Font(name=POLICE, size=10)
        c.number_format = '#,##0 "F"'
        c.fill = PatternFill("solid", fgColor=VERT)
of.cell(row=17, column=2, value="5 classes de 40 eleves").font = Font(name=POLICE, size=10, bold=True)
for col, ref in ((3, "$B$7"), (4, "$B$8")):
    c = of.cell(row=17, column=col, value=f"=5*40*{ref}")
    c.font = Font(name=POLICE, size=10, bold=True)
    c.number_format = '#,##0 "F"'
    c.fill = PatternFill("solid", fgColor=VERT)
texte(of, 18, 2, "Le volume vient du NOMBRE DE CLASSES, jamais du nombre de seances.", gras=True)

titre(of, 20, "Regles de negociation a tenir")
regles = [
    "Annoncer une seance. Une seule. Si on en annonce deux, on n'a plus rien a donner en negociation et on a divise le prix horaire par deux pour rien.",
    "La 2e seance ne se donne jamais contre rien. Elle s'echange contre un engagement sur 3 classes, un paiement integral d'avance, ou des dates bloquees et signees.",
    "Toujours presenter 10 000 F en premier, puis 5 000 F comme repli. Dans l'autre sens, aucun etablissement ne monte.",
    "Seuil minimum : 20 eleves payants. En dessous, proposer de regrouper deux classes de la meme filiere dans la meme salle.",
    "Encaissement : 100 % avant la seance, ou 50 % a la reservation et 50 % a l'arrivee. Jamais de seance entierement a credit.",
    "Classe pilote a 5 000 F uniquement si l'etablissement s'engage par ecrit sur 3 classes supplementaires le meme mois.",
]
for i, t in enumerate(regles):
    texte(of, 21 + i, 2, f"{i + 1}.")
    of.merge_cells(start_row=21 + i, start_column=3, end_row=21 + i, end_column=5)
    texte(of, 21 + i, 3, t)
    of.row_dimensions[21 + i].height = 28

titre(of, 29, "Contenu de la seance (2h)")
seance = [
    ("15 min", "Ce qu'est vraiment l'IA, sans jargon"),
    ("20 min", "Demo live : un devoir et un expose traites devant la classe"),
    ("40 min", "Atelier encadre : chaque eleve fait tourner ses premiers prompts sur son telephone"),
    ("15 min", "Cas d'usage propres a leur filiere"),
    ("15 min", "Les 5 pieges : hallucination, plagiat, dependance, donnees personnelles, triche"),
    ("10 min", "IA et employabilite : CV, lettre de motivation, preparation d'entretien"),
    ("5 min", "Remise des attestations"),
]
for i, (d, t) in enumerate(seance):
    texte(of, 30 + i, 2, d, gras=True)
    texte(of, 30 + i, 3, t)
    of.merge_cells(start_row=30 + i, start_column=3, end_row=30 + i, end_column=5)

titre(of, 38, "2e seance - uniquement si negociee")
seance2 = [
    ("35 min", "Rediger un rapport de stage ou un memoire avec l'IA sans tomber dans le plagiat"),
    ("40 min", "Atelier sur un vrai sujet donne par le professeur, de la recherche au plan detaille"),
    ("25 min", "Verifier une reponse d'IA : la methode en 3 controles"),
    ("20 min", "Les outils gratuits accessibles depuis la Cote d'Ivoire et leurs limites"),
]
for i, (d, t) in enumerate(seance2):
    texte(of, 39 + i, 2, d, gras=True)
    texte(of, 39 + i, 3, t)
    of.merge_cells(start_row=39 + i, start_column=3, end_row=39 + i, end_column=5)

texte(of, 44, 2, "Materiel demande a l'ecole : une salle, un videoprojecteur, une prise. Les eleves utilisent leur telephone.", gras=True)
of.merge_cells("B44:E44")

# ---- 6. Scripts et objections --------------------------------------------- #
sc = wb.create_sheet("Scripts et objections")
largeurs(sc, [4, 30, 96])
sc.sheet_view.showGridLines = False
titre(sc, 1, "SCRIPTS D'APPROCHE - DIRECTEURS DES ETUDES", 14)

blocs_texte = [
    ("1. WhatsApp (premier contact, le plus efficace en CI)", [
        "Bonjour Monsieur/Madame,",
        "Je suis [NOM], de BIG REUSSITE. Je m'adresse a vous en tant que Directeur des Etudes de [ECOLE].",
        "Nous animons des sessions d'initiation a l'intelligence artificielle directement dans les classes : une seance pratique de 2h, avec les telephones des eleves, sans besoin de salle informatique.",
        "L'objectif est simple : que vos etudiants de [FILIERE] sachent utiliser l'IA pour leurs travaux et pour leur employabilite, au lieu de la subir.",
        "Puis-je vous envoyer le programme en 1 page ? Et seriez-vous disponible 15 minutes cette semaine pour en parler ?",
        "Cordialement, [NOM] - [TELEPHONE]",
        "Regle : un seul message. Relance a J+2, puis a J+7, puis on arrete.",
    ]),
    ("2. Appel au standard (quand on n'a que le fixe)", [
        "Bonjour, [NOM] de BIG REUSSITE. Je souhaite joindre le Directeur des Etudes, s'il vous plait. C'est au sujet d'un programme d'initiation a l'IA pour vos classes de BTS.",
        "Si indisponible : Pouvez-vous me donner son numero direct ou son WhatsApp ? Je lui envoie le programme, il verra en 2 minutes si ca l'interesse.",
        "Noter immediatement son nom dans la colonne Nom du Directeur des Etudes de l'onglet Suivi appels.",
    ]),
    ("3. E-mail (trace formelle, apres le WhatsApp)", [
        "Objet : Initiation a l'IA pour vos classes - une seance de 2h par classe",
        "Madame, Monsieur le Directeur des Etudes,",
        "BIG REUSSITE propose aux grandes ecoles de Cote d'Ivoire un module court d'initiation a l'intelligence artificielle, concu pour les etudiants et anime en presentiel dans vos locaux.",
        "Format : une seance de 2h par classe. Materiel : telephones des etudiants et un videoprojecteur. Livrable : kit de prompts et attestation de participation.",
        "Le module couvre l'usage professionnel de l'IA, les cas d'usage propres a chaque filiere, et les regles d'usage responsable, un point que beaucoup d'etablissements souhaitent aujourd'hui cadrer aupres de leurs etudiants.",
        "Je me tiens a votre disposition pour vous presenter le programme detaille et convenir d'un creneau test sur une classe.",
        "Cordialement, [NOM] - BIG REUSSITE - [TELEPHONE] - [EMAIL]",
    ]),
]
r = 3
for titre_bloc, lignes_bloc in blocs_texte:
    titre(sc, r, titre_bloc, 11)
    r += 1
    for t in lignes_bloc:
        texte(sc, r, 3, t)
        sc.row_dimensions[r].height = 15 * (1 + len(t) // 95)
        r += 1
    r += 1

titre(sc, r, "4. Objections qui reviennent", 11)
r += 1
texte(sc, r, 2, "Objection", gras=True).fill = PatternFill("solid", fgColor=GRIS)
texte(sc, r, 3, "Reponse", gras=True).fill = PatternFill("solid", fgColor=GRIS)
r += 1
objections = [
    ("On n'a pas de salle informatique", "Pas necessaire. Les etudiants travaillent sur leur telephone. Il faut juste une salle et un videoprojecteur."),
    ("Ce n'est pas au programme officiel", "C'est un module hors cursus, sur un creneau libre ou un samedi. Aucune modification de maquette, aucune validation ministerielle requise."),
    ("Qui paie ?", "L'etablissement fixe une somme par eleve et la collecte, via les frais annexes ou via les delegues de classe. On ne facture qu'une fois la classe confirmee."),
    ("Une seule seance, ca suffit ?", "La seance est autonome : a la fin, chaque etudiant a fait tourner l'outil lui-meme et repart avec son kit. Une 2e seance est possible, on en discute une fois la premiere programmee. Ne jamais l'offrir a ce stade."),
    ("C'est cher pour nos etudiants", "Descendre le montant par eleve de 10 000 a 5 000, jamais le nombre de seances ni le seuil de 20 eleves. Et ne descendre qu'en echange d'un engagement sur d'autres classes."),
]
for o, rep in objections:
    texte(sc, r, 2, o, gras=True)
    texte(sc, r, 3, rep)
    sc.row_dimensions[r].height = 15 * (1 + len(rep) // 95)
    r += 1

r += 1
titre(sc, r, "5. Rythme", 11)
texte(sc, r + 1, 3, "15 contacts WhatsApp par jour sur la vague 1, relance a J+2 puis J+7, puis on passe a la vague suivante. Renseigner le nom du Directeur des Etudes a chaque appel : c'est cette colonne qui fera la valeur de la base dans un mois.")
sc.row_dimensions[r + 1].height = 45


print(f"Suivi appels : {derniere - 2} ecoles | Base contacts : {bc.max_row - 1} lignes")
wb.save(RACINE / "prospection-ecoles-ia.xlsx")
