# Envoi automatique de candidatures spontanées

## 1. Installer Python
Télécharge Python 3 sur https://www.python.org/downloads/ (coche « Add Python to PATH » sous Windows).
Aucune bibliothèque supplémentaire n'est nécessaire.

## 2. Les fichiers du dossier
- `envoyer_candidatures.py` : le script
- `HOMRI_Saba_CV_IA_Data_ATS.pdf` : ton CV, joint à chaque mail
- `liste_1_banques.csv` : 34 adresses (banques et microfinance, Tunisie)
- `liste_2_it_esn.csv` : 124 adresses (entreprises IT et ESN)

## 3. Modifier les listes (facultatif)
Ouvre un fichier `liste_...csv` avec Excel pour ajouter ou retirer des lignes.
Colonnes : `entreprise` (insérée dans le mail), `email`, `contact` (nom du/de la RH, facultatif).
Enregistre en **CSV UTF-8**. Tout fichier nommé `liste_....csv` est envoyé automatiquement.

## 4. Créer un mot de passe d'application Gmail
Gmail refuse ton mot de passe habituel dans un script :
1. Active la **validation en deux étapes** : https://myaccount.google.com/security
2. Va sur https://myaccount.google.com/apppasswords
3. Crée un mot de passe nommé « Candidatures » et copie les 16 caractères
4. Colle-les dans le script, à la ligne `MOT_DE_PASSE_APPLICATION`

## 5. Tester puis envoyer (double-clic)
**Windows**
1. Double-clique sur `1_TESTER.bat` : le mail et la liste s'affichent, rien n'est envoyé.
2. Si tout est bon, double-clique sur `2_ENVOYER.bat` et laisse la fenêtre ouverte jusqu'à la fin.

**Mac** (la première fois : clic droit → Ouvrir, puis confirmer)
1. `1_TESTER_Mac.command` pour tester.
2. `2_ENVOYER_Mac.command` pour l'envoi réel.

## Bon à savoir
- Le script envoie jusqu'à **200 mails dans la journée**, avec 30 à 90 s de pause entre chaque :
  158 adresses = environ 2h40. Laisse l'ordinateur allumé et connecté pendant l'envoi.
- Si l'envoi s'arrête (coupure internet, blocage Gmail), relance le script : il reprend là où il s'était arrêté.
- `envois.log` garde la trace de chaque envoi : une entreprise déjà contactée
  ne reçoit jamais deux fois le mail.
- Chaque entreprise reçoit son propre mail (pas de copie visible aux autres).
- Ne partage jamais le fichier du script une fois ton mot de passe dedans.
