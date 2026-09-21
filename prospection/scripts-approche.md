# Scripts d'approche — Directeurs des Études

## 1. WhatsApp (premier contact — le plus efficace en CI)

> Bonjour Monsieur/Madame,
> Je suis [NOM], de BIG RÉUSSITE. Je m'adresse à vous en tant que Directeur des Études de [ÉCOLE].
>
> Nous animons des **sessions d'initiation à l'intelligence artificielle** directement dans les
> classes — une séance pratique de 2h, avec les téléphones des élèves, sans besoin de salle informatique.
>
> L'objectif est simple : que vos étudiants de [FILIÈRE] sachent utiliser l'IA pour leurs travaux
> et pour leur employabilité, au lieu de la subir.
>
> Puis-je vous envoyer le programme en 1 page ? Et seriez-vous disponible 15 minutes cette semaine
> pour en parler ?
>
> Cordialement,
> [NOM] — [TÉLÉPHONE]

**Règle :** un seul message. Pas de relance avant 48h. Relance n°1 à J+2, relance n°2 à J+7, puis stop.

## 2. Appel au standard (quand on n'a que le fixe)

> « Bonjour, [NOM] de BIG RÉUSSITE. Je souhaite joindre **le Directeur des Études**, s'il vous plaît.
> C'est au sujet d'un programme d'initiation à l'IA pour vos classes de BTS. »

Si indisponible : **« Pouvez-vous me donner son numéro direct ou son WhatsApp ? Je lui envoie le
programme, il verra en 2 minutes si ça l'intéresse. »**
→ Noter le nom du DE dans la colonne `interlocuteur_cible` du CSV. C'est l'info qui manque aujourd'hui.

## 3. E-mail (trace formelle, après le WhatsApp)

**Objet :** Initiation à l'IA pour vos classes — une séance de 2h par classe

> Madame, Monsieur le Directeur des Études,
>
> BIG RÉUSSITE propose aux grandes écoles de Côte d'Ivoire un module court d'**initiation à
> l'intelligence artificielle**, conçu pour les étudiants et animé en présentiel dans vos locaux.
>
> **Format :** une séance de 2h par classe · **Matériel :** téléphones des étudiants + un vidéoprojecteur
> · **Livrable :** kit de prompts + attestation de participation.
>
> Le module couvre l'usage professionnel de l'IA (travaux, exposés, recherche documentaire),
> les cas d'usage propres à chaque filière, et les règles d'usage responsable — un point que
> beaucoup d'établissements souhaitent aujourd'hui cadrer auprès de leurs étudiants.
>
> Je me tiens à votre disposition pour vous présenter le programme détaillé et convenir
> d'un créneau test sur une classe.
>
> Cordialement,
> [NOM] — BIG RÉUSSITE — [TÉLÉPHONE] — [EMAIL]

## 4. Traitement des objections qui reviennent

| Objection | Réponse |
|---|---|
| « On n'a pas de salle informatique » | Pas nécessaire. Les étudiants travaillent sur leur téléphone. Il faut juste une salle et un vidéoprojecteur. |
| « Ce n'est pas au programme officiel » | C'est un module hors cursus, sur un créneau libre ou un samedi. Aucune modification de maquette, aucune validation ministérielle requise. |
| « Qui paie ? » | L'établissement fixe une somme par élève et la collecte, soit via les frais annexes, soit via les délégués de classe. On ne facture qu'une fois la classe confirmée. |
| « Une seule séance, ça suffit ? » | La séance est conçue pour être autonome : à la fin, chaque étudiant a fait tourner l'outil lui-même et repart avec son kit. **Une seconde séance est possible, on en discute une fois la première programmée.** Ne jamais l'offrir à ce stade. |
| « C'est cher pour nos étudiants » | Descendre le montant par élève de 10 000 à 5 000 — jamais le nombre de séances, jamais le seuil de 20 élèves. Et ne descendre qu'en échange d'un engagement sur d'autres classes. |

## 5. Ordre d'attaque

L'ordre d'appel est porté par **`suivi-appels.csv`**, trié par vague :

- **Vague 1 (30 écoles)** — privé, Abidjan, coordonnées vérifiées sur site officiel.
  Décision rapide, interlocuteur joignable. C'est là qu'on décroche les premiers marchés.
- **Vague 2 (57 écoles)** — privé, contact à qualifier ou hors Abidjan. Un appel de
  qualification en plus avant de proposer.
- **Vague 3 (19 écoles)** — public : universités, lycées techniques, INP-HB, AGEFOP.
  Gros effectifs mais circuit administratif long : à lancer en parallèle, sans compter
  dessus pour le chiffre du mois.

**Règle de rythme :** 15 contacts WhatsApp par jour sur la vague 1, relance à J+2 puis J+7,
puis on passe à la suivante. Renseigner le nom du Directeur des Études à chaque appel —
c'est cette colonne qui fera la valeur de la base dans un mois.
