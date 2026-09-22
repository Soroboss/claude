# Scripts d'approche — Directeurs des Études

## 1. WhatsApp — page d'envoi avec suivi

**Page en ligne :** https://claude.ai/artifact/67t1cemVUbVhMmHRAAoXFE

73 écoles, le message déjà rédigé et personnalisé. On clique « Envoyer sur WhatsApp »,
WhatsApp s'ouvre sur la bonne conversation, il ne reste qu'à appuyer sur envoyer.
Le statut passe automatiquement à « Envoyé ». Compteurs, filtres par vague, champ note
par école. Le suivi est partagé entre tous tes appareils.

`envois/whatsapp-envoi.csv` contient les mêmes messages en tableau, pour un usage hors ligne.

**Message envoyé** — l'accroche change selon la filière de l'école :

> Vos étudiants livrent déjà du code écrit par une IA.
> La plupart seraient incapables de l'expliquer devant un jury.
>
> Bonjour, je m'adresse au Directeur des Études d'[ÉCOLE]. Personne ne leur a jamais donné la
> moindre règle d'usage, et c'est l'établissement qui porte le risque.
>
> BIG RÉUSSITE règle ça en une séance de 2h, dans votre classe, sur les téléphones de vos
> étudiants. Aucune salle informatique, aucun investissement.
>
> Je vous envoie le programme en 1 page ?

**Pourquoi les deux premières lignes comptent plus que tout le reste :** l'aperçu WhatsApp
n'affiche que celles-là. Si elles ne piquent pas, le message n'est jamais ouvert. Chaque filière
a donc son accroche propre — code non défendable pour le numérique, informations médicales non
vérifiées pour la santé, notes de calcul recopiées pour le BTP, chiffres inventés pour le
commerce. 13 accroches distinctes, dans `tools/segments.py`.

⚠️ **Le message promet un programme en 1 page. Il faut pouvoir l'envoyer dans l'heure.**
Les prompts qui le fabriquent sont dans `programme-premium/`.

Relance à J+2, puis à J+7, puis on arrête. Les deux textes sont dans la page et dans le CSV.

## 2. Appel au standard (quand on n'a que le fixe)

> « Bonjour, [NOM] de BIG RÉUSSITE. Je souhaite joindre **le Directeur des Études**, s'il vous plaît.
> C'est au sujet d'un programme d'initiation à l'IA pour vos classes de BTS. »

Si indisponible : **« Pouvez-vous me donner son numéro direct ou son WhatsApp ? Je lui envoie le
programme, il verra en 2 minutes si ça l'intéresse. »**
→ Noter le nom du DE dans la colonne `interlocuteur_cible` du CSV. C'est l'info qui manque aujourd'hui.

## 3. E-mail (trace formelle, après le WhatsApp)

**Objet :** Vos étudiants utilisent déjà l'IA — personne ne leur a appris à s'en servir

> Madame, Monsieur le Directeur des Études,
>
> Une question simple : combien d'étudiants d'[ÉCOLE] ont rendu ce semestre un exposé ou un
> rapport écrit, en partie, par une intelligence artificielle ?
>
> Vos enseignants le sentent souvent, sans pouvoir le prouver. Et c'est l'établissement qui porte
> le risque — travaux uniformisés, mémoires dont on ne sait plus qui les a écrits, valeur du
> diplôme discutée — alors qu'aucun étudiant n'a jamais reçu la moindre règle d'usage.
>
> Le paradoxe est là : ils se servent de cet outil tous les jours, et aucun ne sait réellement
> s'en servir. Ni pour produire un travail défendable devant un jury, ni pour le premier entretien
> d'embauche qui les attend.
>
> C'est exactement ce que BIG RÉUSSITE vient corriger. Une séance de 2h, animée en présentiel dans
> vos classes : ce qu'est réellement l'IA, comment l'utiliser sur un travail universitaire sans
> tomber dans le plagiat, les cas d'usage propres à chaque filière, et ce qu'un recruteur attend
> aujourd'hui. Les étudiants travaillent sur leur propre téléphone : aucune salle informatique,
> aucun investissement de votre part.
>
> Un mot sur le calendrier. Le sujet est encore neuf en Côte d'Ivoire. L'établissement qui le cadre
> maintenant ne règle pas seulement un problème interne : il peut l'annoncer à ses futurs étudiants
> et à leurs parents, au moment précis où la question commence à se poser partout. Dans un an, ce
> sera la norme, et plus personne n'en tirera d'avantage.
>
> Je vous propose de commencer par une classe test. Vous jugez sur pièce, et vous décidez ensuite.
>
> Cordialement,
> BIG RÉUSSITE

**La structure à ne pas casser :** un problème que le destinataire reconnaît → le risque qu'il
porte aujourd'hui → notre solution → la prime au premier qui bouge → une demande minuscule
(une classe test). Si tu réécris le mail, garde ces cinq temps.

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
