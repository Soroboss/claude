# Prospection — Grandes écoles CI · Offre "Initiation à l'IA"

## Où tout est stocké

| Endroit | Quoi |
|---|---|
| Ce dépôt git | La source de vérité : tous les fichiers ci-dessous, versionnés |
| Google Drive — dossier *BIG REUSSITE - Prospection Ecoles IA* | `Suivi appels - Ecoles IA` (Google Sheet vivant) et `Offre et scripts - Initiation IA` (Google Doc) |
| `prospection-ecoles-ia.xlsx` | Le classeur complet, 6 onglets, avec tableau de bord et listes déroulantes. À déposer dans le dossier Drive pour l'ouvrir dans Sheets |
| `sheets/*.csv` | Les mêmes tables en CSV séparé par virgules, avec BOM UTF-8 : s'ouvrent sans réglage dans Google Sheets et Excel |

## Contenu
| Fichier | Rôle |
|---|---|
| `ecoles-ci-contacts.csv` | Base de contacts (séparateur `;`, ouvrable dans Excel / Google Sheets) |
| `offre-initiation-ia.md` | L'offre : une séance de 2h par classe, prix par élève, règles de négociation de la 2e séance, circuit de décision |
| `scripts-approche.md` | Scripts WhatsApp / appel / e-mail + traitement d'objections + ordre d'attaque |
| `suivi-appels.csv` | **Feuille de prospection à remplir** : 105 lignes classées en 3 vagues, colonnes de suivi (nom du DE, statut, montant par élève, nb d'élèves, nb de séances négocié, nb de classes, montant attendu) |
| `envois/whatsapp-envoi.csv` | **73 écoles** : lien `wa.me` cliquable avec le message déjà rédigé et personnalisé, plus les deux relances |
| `envois/emails-a-envoyer.csv` | **68 écoles** : destinataire, objet et corps prêts, pour publipostage ou copier-coller |
| `expediteur.json` | Ton identité d'expéditeur. La modifier puis relancer `tools/generer_envois.py` régénère tous les messages |
| `tools/generer_envois.py` | Génère les deux fichiers d'envoi depuis la base |
| `tools/merge_contacts.py` | Fusionne un nouveau lot de contacts dans la base : dédoublonnage, contrôle de format, normalisation des numéros |

## État de la base

**105 établissements** — 101 avec au moins un téléphone, 68 avec un e-mail, 0 doublon.

Répartition de `suivi-appels.csv` :

| Vague | Nombre | Profil | Pourquoi commencer là |
|---|---|---|---|
| 1 | 30 | Privé, Abidjan, coordonnées vérifiées sur site officiel | Décision rapide, interlocuteur joignable, effectifs payants |
| 2 | 56 | Privé, contact moyennement fiable ou hors Abidjan | Bon potentiel, un appel de qualification en plus |
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

## Le classeur `prospection-ecoles-ia.xlsx`

Six onglets : Mode d'emploi · Tableau de bord · Suivi appels · Base contacts · Offre et tarifs ·
Scripts et objections.

- **Suivi appels** est la seule feuille à remplir. Cellules jaunes = à saisir, cellule verte =
  calculée. Listes déroulantes sur Statut, Montant par élève et Nb de séances. Une ligne
  d'exemple en haut montre le format attendu — à supprimer une fois comprise.
- **Montant attendu** se calcule seul : `(montant par élève + supplément) × nb d'élèves × nb de classes`,
  le supplément étant de +3 000 F par élève si une 2e séance est négociée au palier 5 000.
- **Tableau de bord** agrège tout : CA signé, CA en négociation, taux de transformation, et le
  restant à contacter par vague.

Les formules ont été vérifiées de deux façons : contrôle statique des 130 formules (toutes les
références pointent vers un onglet et une plage existants, aucune fonction non supportée), et
rejeu de leur logique en Python sur 13 cas de test. LibreOffice n'étant pas utilisable dans
l'environnement de génération, les valeurs mises en cache sont vides : elles se calculent à
l'ouverture dans Google Sheets ou Excel.

## Canaux d'envoi

| Canal | Écoles joignables | Pourquoi ce nombre |
|---|---|---|
| E-mail | 68 | Les écoles dont un e-mail a été trouvé |
| WhatsApp | 73 | Uniquement les numéros **mobiles** : en Côte d'Ivoire seuls les préfixes 01 (Moov), 05 (MTN) et 07 (Orange) ont un compte WhatsApp. Un fixe en 27 n'en a pas — lui envoyer un lien `wa.me` ne mène nulle part |
| Ni l'un ni l'autre | 10 | Fixe seul : à traiter par appel, avec le script §2 de `scripts-approche.md` |

### Comment utiliser `whatsapp-envoi.csv`

Ouvrir le fichier dans Google Sheets sur le téléphone, cliquer sur le lien de la colonne
`lien_envoi_clic` : WhatsApp s'ouvre sur la bonne conversation avec le message déjà écrit.
Il ne reste qu'à envoyer. Les colonnes `relance_J2` et `relance_J7` contiennent les deux
relances à copier-coller aux bonnes dates.

Les 73 liens ont été contrôlés : tous bien formés, aucun ne pointe vers une ligne fixe.

### Personnaliser l'expéditeur

Les messages sont signés « BIG RÉUSSITE ». Pour signer de ton nom et ajouter ton numéro,
modifier `expediteur.json` puis relancer :

    python3 tools/generer_envois.py

Tous les messages WhatsApp et e-mail sont régénérés avec la nouvelle signature.

## Qualité des adresses e-mail — mesuré, pas supposé

Un premier envoi réel a servi de test grandeur nature. Résultat sur 68 adresses :

| Type d'adresse | Nombre | Mortes | Boîte pleine | Taux d'échec |
|---|---|---|---|---|
| Domaine propre (`info@ecole.ci`) | 53 | 12 | 5 | **32 %** |
| Gratuite (gmail, yahoo, hotmail, aviso) | 15 | 2 | 0 | **13 %** |

**Une adresse en domaine propre échoue 2,5 fois plus souvent.** Les domaines des petites écoles
ivoiriennes expirent, les boîtes `info@` sont abandonnées ou saturées, alors qu'un compte Gmail
reste relevé par une personne réelle.

**Règle retenue :** à adresse égale, toujours préférer une boîte gratuite trouvée sur une page
officielle de l'école à une adresse `contact@` trouvée sur un annuaire. Ne jamais déduire une
adresse d'un nom de domaine — c'est exactement ce qui a rebondi.

Deux colonnes portent cette information dans `ecoles-ci-contacts.csv` :

- `type_email` : `gratuite` ou `domaine propre`
- `etat_email` : `valide` (a déjà délivré), `a verifier` (trouvée après un rebond, jamais
  testée), `boite pleine` (l'adresse existe mais sature), `sans email`. Une adresse qui a
  rebondi définitivement est **retirée** du fichier, pas conservée : la garder ne pouvait que
  produire un nouveau rebond.

`tools/generer_envois.py` exclut désormais les adresses mortes, fait passer les adresses
gratuites en premier, et n'écrit qu'une fois aux établissements qui partagent une boîte.

## Lire le motif du rebond, pas seulement le rebond

Les 19 échecs recouvrent deux situations qui n'appellent pas la même suite :

**Domaine introuvable** — le domaine n'existe plus, aucune adresse dessus ne fonctionnera jamais.
Concerne `geige.ci`, `isfmi.net`, `groupeaist.net`, `uigb.org`, `isacm.ci`, `ites.ci`,
`groupelasorbonne.com`. Seule issue : une autre adresse, sur un autre domaine.

**Boîte introuvable** (`550 No Such User`, `5.1.1`) — le serveur du domaine a **répondu**, donc
le domaine est vivant : c'est la boîte seule qui n'existe pas. Concerne `cofecesa.net`,
`groupehetec.com`, `gestpci.com`, `ita-education.ci`, et deux comptes gratuits mal saisis.
Une autre boîte sur le même domaine peut parfaitement fonctionner — mais on ne la devine pas,
on la trouve publiée quelque part. Deviner `contact@` + domaine est exactement ce qui a échoué.

**Boîte pleine** — l'adresse existe et sature. Elle reste dans le fichier, en fin de file d'envoi.

## Ordre d'envoi

`tools/generer_envois.py` classe la file par probabilité de délivrance :

1. `valide` + gratuite — a déjà délivré, et sur le type d'adresse le plus fiable
2. `valide` + domaine propre
3. `a verifier` — trouvée après un rebond, jamais testée
4. `boite pleine` — en dernier, elle peut rebondir à nouveau

Un établissement qui partage sa boîte avec un autre campus ne reçoit qu'un seul mail.
