# Prompts — Programme premium à envoyer sur demande

Quand un Directeur des Études répond « oui, envoyez-moi le programme », il faut lui envoyer
**dans l'heure** un document d'une page qui ressemble à quelque chose. Ces prompts le fabriquent.

**Règle absolue, valable pour tous les prompts ci-dessous :** aucune statistique inventée.
Pas de « 87 % des étudiants utilisent ChatGPT ». Un Directeur des Études qui demande la source
te met en difficulté, et tu perds le marché que tu venais de décrocher.

---

## Variables à remplir avant d'envoyer le prompt

| Variable | Exemple |
|---|---|
| `{ÉCOLE}` | Groupe CSI Pôle Polytechnique |
| `{FILIÈRE}` | informatique et réseaux |
| `{PUBLIC}` | étudiants (ou élèves, ou apprenants) |
| `{TRAVAUX}` | un rapport de projet ou une documentation technique |
| `{EFFECTIF}` | 40 |
| `{MONTANT}` | 5 000 |
| `{VILLE}` | Abidjan — Cocody Riviera Bonoumin |

Tout ça se lit directement dans `ecoles-ci-contacts.csv` et dans `tools/segments.py`.

---

## Prompt 1 — Le programme d'une page *(le document principal)*

> Tu es responsable pédagogique chez BIG RÉUSSITE, organisme de formation basé à Abidjan.
> Rédige le programme d'une séance de formation, destiné à être lu par le Directeur des Études
> de {ÉCOLE}, un établissement de {VILLE} qui forme des {PUBLIC} en {FILIÈRE}.
>
> **Le format, à respecter strictement :**
> - Une seule page. 400 mots maximum, titres compris.
> - Un titre, puis 5 blocs : Le constat · L'objectif · Le déroulé · Ce que repart avec chaque
>   {PUBLIC} · Conditions pratiques.
> - Le déroulé est un tableau minuté : 7 séquences, durées en minutes, total exactement 120.
> - Ton professionnel et direct. Aucune formule creuse, aucun superlatif, aucun emoji.
>
> **Le fond :**
> - Le constat part d'un fait que le lecteur vérifie lui-même dans son établissement : ses
>   {PUBLIC} rendent déjà {TRAVAUX} écrit en partie par une IA, sans qu'aucune règle d'usage
>   ne leur ait été donnée. N'invente aucun chiffre, aucune étude, aucun pourcentage.
> - Le déroulé couvre : ce qu'est réellement l'IA, une démonstration en direct, un atelier où
>   chaque {PUBLIC} manipule sur son propre téléphone, les cas d'usage propres à la filière
>   {FILIÈRE}, les 5 pièges (hallucination, plagiat, dépendance, données personnelles, triche),
>   l'IA face à un recruteur, la remise des attestations.
> - L'atelier pratique doit être la séquence la plus longue.
> - Conditions pratiques : une salle, un vidéoprojecteur, une prise. Les {PUBLIC} utilisent leur
>   propre téléphone. Aucune salle informatique nécessaire. Effectif conseillé : 20 à {EFFECTIF}.
>
> **Interdits :** ne mentionne aucun prix, aucun tarif, aucune durée d'engagement. Le prix se
> discute de vive voix, pas dans un document qui circule.

---

## Prompt 2 — La proposition chiffrée *(à envoyer seulement s'il demande le prix)*

> Rédige une proposition commerciale d'une demi-page pour {ÉCOLE}, adressée à son Directeur
> des Études, pour une séance d'initiation à l'intelligence artificielle de 2h.
>
> - Montant : {MONTANT} FCFA par {PUBLIC}, fixé par l'établissement, qui collecte et reverse.
> - Base de calcul : une classe de {EFFECTIF} {PUBLIC} → montre le total.
> - Encaissement : 100 % avant la séance, ou 50 % à la réservation et 50 % à l'arrivée.
> - Seuil : 20 {PUBLIC} payants minimum par séance.
> - Mentionne qu'une seconde séance est possible et se discute séparément. Ne la chiffre pas.
> - Propose de commencer par une classe test.
>
> Ton factuel, sans argumentaire de vente : l'argumentaire a déjà été fait, ce document ne sert
> qu'à poser des chiffres. Pas de remise affichée, pas d'urgence artificielle, pas d'emoji.

---

## Prompt 3 — La version visuelle *(Canva, Figma, ou tout générateur de visuel)*

> Crée une mise en page d'une page A4 verticale pour un programme de formation professionnelle,
> destiné à la direction d'un établissement d'enseignement supérieur en Côte d'Ivoire.
>
> - Sobre et institutionnel. Ce document est lu par un Directeur des Études, pas par un étudiant.
> - Deux couleurs maximum plus un gris de texte. Pas de dégradé, pas de photo d'illustration
>   générique, pas d'icône décorative.
> - Hiérarchie nette : un titre fort, des intertitres discrets, un tableau pour le déroulé minuté.
> - Un bandeau de pied de page avec le nom de l'organisme, un e-mail et un numéro de téléphone.
> - Prévois la place d'un logo en haut à gauche.
> - Le texte doit rester lisible une fois le document ouvert sur un téléphone.

---

## Prompt 4 — Le kit de prompts remis aux {PUBLIC} *(le livrable de fin de séance)*

> Rédige un kit d'une page intitulé « 10 prompts pour vos travaux », destiné à des {PUBLIC} en
> {FILIÈRE} dans un établissement ivoirien.
>
> - 10 prompts prêts à copier, chacun en 2 lignes maximum, chacun avec une phrase qui dit
>   quand s'en servir.
> - Ils portent sur le travail réel de la filière : {TRAVAUX}, recherche documentaire, plan
>   détaillé, révision, préparation d'entretien.
> - Termine par 3 règles de vérification à appliquer avant de rendre quoi que ce soit.
> - Langue simple, tutoiement, aucun jargon technique.
> - Aucun prompt qui aide à tricher ou à masquer l'usage de l'IA. Le kit sert à produire un
>   travail défendable, c'est son seul objet — et c'est aussi ce qui rend le document
>   présentable à la direction de l'établissement.

---

## Prompt 5 — L'attestation de participation

> Crée le texte d'une attestation de participation nominative pour une formation
> « Initiation à l'intelligence artificielle », 2 heures, animée par BIG RÉUSSITE dans les
> locaux de {ÉCOLE}.
>
> - Champs à laisser vides : nom du participant, filière, date, lieu.
> - Une phrase qui résume les compétences abordées, sans les surévaluer : il s'agit d'une
>   initiation de 2h, pas d'une certification. Ne laisse rien dans le texte qui puisse être
>   présenté comme un diplôme ou un titre.
> - Prévoir un emplacement de signature et de cachet.

---

## Dans quel ordre s'en servir

1. Il répond « envoyez le programme » → **Prompt 1**, dans l'heure. C'est tout ce qu'il demande.
2. Il demande le prix → **Prompt 2**. Jamais avant qu'il le demande.
3. Il dit oui → **Prompt 4** pour préparer le kit, **Prompt 5** pour les attestations.
4. **Prompt 3** une seule fois, pour avoir un gabarit visuel réutilisable sur toutes les écoles.

**Ce qui fait la différence :** le programme arrive personnalisé avec le nom de l'école et les
travaux réels de sa filière. Un document générique se reconnaît en trois secondes et vaut zéro.
