# Prospection — Grandes écoles CI · Offre "Initiation à l'IA"

## Contenu
| Fichier | Rôle |
|---|---|
| `ecoles-ci-contacts.csv` | Base de contacts (séparateur `;`, ouvrable dans Excel / Google Sheets) |
| `offre-initiation-ia.md` | L'offre : format 2 séances/classe, contenu, grille tarifaire, circuit de décision |
| `scripts-approche.md` | Scripts WhatsApp / appel / e-mail + traitement d'objections + ordre d'attaque |
| `suivi-appels.csv` | **Feuille de prospection à remplir** : 106 lignes classées en 3 vagues, colonnes de suivi (nom du DE, statut, palier, nb de classes, montant attendu) |
| `tools/merge_contacts.py` | Fusionne un nouveau lot de contacts dans la base : dédoublonnage, contrôle de format, normalisation des numéros |

## État de la base

**106 établissements** — 102 avec au moins un téléphone, 69 avec un e-mail, 0 doublon.
43 fiches en fiabilité Haute, 63 en Moyenne.

Répartition de `suivi-appels.csv` :

| Vague | Nombre | Profil | Pourquoi commencer là |
|---|---|---|---|
| 1 | 30 | Privé, Abidjan, coordonnées vérifiées sur site officiel | Décision rapide, interlocuteur joignable, effectifs payants |
| 2 | 57 | Privé, contact moyennement fiable ou hors Abidjan | Bon potentiel, un appel de qualification en plus |
| 3 | 19 | Public (universités, lycées techniques, INP-HB, AGEFOP) | Gros volumes mais circuit administratif long |

## Méthode de collecte
Recherche web menée par 7 agents en parallèle, chacun sur un segment (Cocody/Riviera · Yopougon/Abobo/Adjamé · Plateau/Treichville/Marcory · écoles d'ingénieurs et du numérique · filières techniques santé-BTP-logistique-hôtellerie · villes de l'intérieur · universités privées et lycées techniques). Sources : sites officiels des établissements, UPESUP, Le Grand Frère, AnnuaireCI, Edukiya. Chaque ligne porte sa source et un niveau de fiabilité.

- **Haute** = coordonnées lues sur la page contact du site officiel de l'école
- **Moyenne** = coordonnées issues d'annuaires ; à confirmer au premier appel

## Limite connue — contacts nominatifs des Directeurs des Études
La colonne `interlocuteur_cible` indique la **fonction** visée, pas un nom.
Deux raisons, vérifiées :
1. La base de prospection B2B connectée (Vibe Prospecting) a **zéro couverture "personnes" pour la
   Côte d'Ivoire** — testé sans aucun filtre, 0 résultat.
2. Les annuaires ivoiriens (pratik-ci, goafricaonline, annuaireci) sont **bloqués par la politique
   réseau** de cet environnement d'exécution.

→ Le nom du Directeur des Études se récupère au premier appel. Le script §2 de
`scripts-approche.md` est fait pour ça. **Remplir la colonne au fur et à mesure** : c'est cette
colonne qui transforme la liste en base de prospection réelle.

## Numéros de téléphone — correction appliquée

Les annuaires ivoiriens publient encore beaucoup de numéros au format **8 chiffres d'avant la
migration de janvier 2021**. Ces numéros ne sonnent plus. `tools/merge_contacts.py` les convertit
automatiquement au format à 10 chiffres (lignes fixes → préfixe `27`, mobiles → préfixe de
l'opérateur d'après les deux premiers chiffres). Sans cette correction, une partie notable de la
base aurait été injoignable dès le premier appel.

Les numéros que le script n'a pas su convertir de façon sûre sont laissés tels quels plutôt que
devinés — aucun numéro n'est inventé.

## Reste à couvrir

Les recherches ont été interrompues par le quota de recherches web de la session. Établissements
repérés mais sans coordonnées exploitables, à traiter dans une prochaine passe :

- **Bouaké** : ESSECT Poincaré, ESCT-EIT-NTIC, Institut Supérieur Louis Le Grand, IES-Le Campus, AIST, IHEM-SO
- **Korhogo** : ETIC, Institut Supérieur Les Élites (ISE), CFP Korhogo
- **Yamoussoukro** : ISCAE, ISTA, IESE Eylim, EPI-Yakro
- **Abidjan** : ISP Abobo, I2SC Abobo, ES2I Yopougon, IES Le Campus Yopougon, ISTT Yopougon,
  Groupe ETEC Yopougon, ESETP Yopougon, ESSC Saint Chalmel, Université SEPI, ISSF Adjamé,
  CFP-GDS Anyama, BEFST Anyama
- **Autres** : IFPT Daloa, IUSSE San-Pédro, CFP Daloa 1 et 2, Groupe ETEC Gagnoa, Institut Supérieur Sarhaoum Man
