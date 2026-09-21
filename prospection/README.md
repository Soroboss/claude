# Prospection — Grandes écoles CI · Offre "Initiation à l'IA"

## Contenu
| Fichier | Rôle |
|---|---|
| `ecoles-ci-contacts.csv` | Base de contacts (séparateur `;`, ouvrable dans Excel / Google Sheets) |
| `offre-initiation-ia.md` | L'offre : format 2 séances/classe, contenu, grille tarifaire, circuit de décision |
| `scripts-approche.md` | Scripts WhatsApp / appel / e-mail + traitement d'objections + ordre d'attaque |

## Méthode de collecte
Recherche web (annuaires ivoiriens, sites officiels des établissements, fiches Le Grand Frère /
AnnuaireCI / Edukiya). Chaque ligne porte sa source et un niveau de fiabilité.

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
