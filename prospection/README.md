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
| `programme-premium/prompts.md` | Les 5 prompts qui fabriquent le programme promis dans les messages : programme 1 page, proposition chiffrée, gabarit visuel, kit de prompts pour les étudiants, attestation |
| `programme-premium/prompts-par-ecole.csv` | Le prompt du programme **déjà rempli** pour chacune des 105 écoles : nom, ville, filière, travaux réels, interlocuteur. Copier-coller, rien à remplir |
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

## Le message WhatsApp

L'aperçu WhatsApp n'affiche que les deux premières lignes. Le message est donc bâti autour
d'elles : une accroche qui nomme le travail réel que rendent leurs étudiants, pas l'IA en
général. **13 accroches distinctes**, une par filière, dans `tools/segments.py`.

Le message complet fait environ 475 caractères — quatre blocs courts et une seule question.
L'interlocuteur et le mot désignant le public s'adaptent : « au Proviseur… vos élèves » pour
un lycée, « au Directeur des Études… vos étudiants » ailleurs.

## Le programme premium

Le message se termine par « Je vous envoie le programme en 1 page ? ». **Ce programme doit
partir dans l'heure qui suit la réponse**, sinon l'intérêt retombe.

`programme-premium/prompts.md` contient les 5 prompts qui le produisent, et
`prompts-par-ecole.csv` les livre déjà remplis école par école.

Règle commune à tous : **aucune statistique inventée**. Un Directeur des Études qui demande la
source d'un « 87 % des étudiants » fait perdre le marché qui venait d'être décroché. L'argument
tient sur un constat qu'il vérifie lui-même dans son propre établissement.

Ordre d'usage : programme d'abord, prix seulement s'il le demande, kit et attestations une fois
la séance calée.

## Base de donnees : 690 etablissements

La base vient de deux sources :

| Source | Etablissements | Remarque |
|---|---|---|
| Recherches web (9 agents) | 104 | 47 adresses testees et confirmees en campagne |
| Liste officielle MESRS | 586 nouveaux | `bac.mesrs-ci.net/offres/grdes-ecoles` |

Couverture : **535 e-mails**, 611 telephones, 406 numeros joignables sur WhatsApp,
58 villes. Les adresses sont a **71 % des boites gratuites** (gmail, yahoo...), qui
echouent 13 % du temps contre 32 % pour les domaines propres : c'est le critere de tri
des envois.

### Chaine de traitement

```
mesrs/raw.txt                       donnees brutes MESRS (616 lignes)
  -> tools/parse_mesrs.py           -> mesrs/mesrs-parse.csv (schema 16 colonnes)
  -> tools/rapprocher_mesrs.py      rapprochement avec la base (30 correspondances)
  -> tools/fusion_mesrs.py          -> ecoles-ci-contacts.csv (690 etablissements)
  -> tools/generer_envois.py        -> envois/emails-a-envoyer.csv (475)
                                    -> envois/whatsapp-envoi.csv (456)
  -> tools/build_whatsapp_page.py   -> envois/whatsapp.html (suivi des envois)
  -> tools/build_sheets.py          -> sheets/*.csv + suivi-appels.csv
  -> tools/build_workbook.py        -> prospection-ecoles-ia.xlsx (8 onglets)
  -> tools/generer_prompts.py       -> programme-premium/prompts-par-ecole.csv
```

Tout se regenere depuis `ecoles-ci-contacts.csv`. `build_sheets.py` **relit et reporte
la saisie manuelle** (nom du directeur, statut, montants, notes) : regenerer ne detruit
jamais le travail de prospection deja fait.

### Regles de qualite appliquees

- Une adresse n'est **jamais deduite** d'un nom de domaine. Deux adresses tronquees a la
  source (`cofecesa@cofecesap`, `...@yahoo`) sont ecartees plutot que completees au hasard.
- `valide` atteste qu'une boite accepte le courrier, **pas** qu'elle appartient a ce
  campus : une adresse partagee par deux etablissements est une deduction, la liste
  officielle la remplace.
- Une boite partagee par plusieurs campus ne recoit **qu'un seul** e-mail.
- Comparaisons de `statut` / `fiabilite` insensibles a la casse : un test sensible a la
  casse renvoyait les 586 nouvelles ecoles en derniere vague.
- Segment par filiere : un specialiste ne l'emporte qu'avec 2 voix d'ecart, sinon
  l'ecole est polyvalente et c'est le socle tertiaire qui cadre l'argumentaire.

## Catalogue de formation

Deux fichiers dans `catalogue/` :

| Fichier | Pour qui | Quand l'envoyer |
|---|---|---|
| `Catalogue_Formation_IA_Etablissements_SORO_Nagony_Adama.pdf` | **les écoles** (19 pages) | une fois le Directeur des Études en ligne |
| `Catalogue_Modules_Formation_SORO_Nagony_Adama.pdf` | l'institut de formation (original, 42 pages) | **jamais aux écoles** |

L'original a été écrit pour un institut : il s'ouvre sur « en réponse à la demande de
l'institut », cite « l'institut » 14 fois, exige un ordinateur par apprenant et des groupes
de 10 à 15, et ne contient pas la séance de 2h. Envoyé à une école, il contredirait nos
messages (« aucune salle informatique, sur leurs téléphones »).

La version Écoles part de la séance d'initiation de 2h, présente 16 des 30 modules par filière
(fiches reprises **mot pour mot** : 241 éléments vérifiés), deux parcours étudiants, et se
termine sur la classe test. **Aucun prix.** La 2e séance d'initiation n'y figure pas : elle
reste un levier de négociation (voir `offre-initiation-ia.md`, règle 1).

Le PDF est aussi joint à la page WhatsApp (bouton « Ouvrir le PDF »).

```
catalogue/source-catalogue.txt      texte du PDF original (Drive, 17/09/2026)
  -> tools/extraire_catalogue.py    -> catalogue/modules.json (30 fiches structurées)
  -> tools/build_catalogue_ecoles.py -> catalogue/Catalogue_Formation_IA_Etablissements_...pdf
```

**L'ordre d'envoi :** 1) message WhatsApp — il ne demande qu'un appel ; 2) l'appel ;
3) le catalogue, pour que le Directeur des Études le fasse valider en interne ;
4) la classe test.
