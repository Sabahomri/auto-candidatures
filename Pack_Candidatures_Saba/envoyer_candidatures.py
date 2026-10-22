"""
Envoi automatique de candidatures spontanées - Saba Homri
---------------------------------------------------------
- Lit les listes d'entreprises liste_*.csv (une par catégorie)
- Envoie un mail personnalisé (nom de l'entreprise) à chaque adresse, un par un
- Joint le CV en PDF
- Attend 1 à 3 minutes entre deux envois pour ne pas être classée en spam
- Note chaque envoi dans envois.log : on peut relancer le script sans renvoyer
  aux entreprises déjà contactées

Utilisation :
  1. Vérifier les fichiers liste_*.csv
  2. Mettre le mot de passe d'application Gmail ci-dessous (voir README)
  3. Test sans rien envoyer :   python envoyer_candidatures.py --test
  4. Un seul mail d'essai :     python envoyer_candidatures.py --essai ton.adresse@gmail.com
  5. Envoi réel :               python envoyer_candidatures.py
"""

import csv
import random
import smtplib
import ssl
import sys
import time
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

# ===================== À CONFIGURER =====================
EXPEDITEUR = "sabahomri96@gmail.com"
MOT_DE_PASSE_APPLICATION = "qiqo egad wowm jivu" \
""  # mot de passe d'application Gmail (16 caractères)
FICHIER_CV = "HOMRI_Saba_CV_IA_Data_ATS.pdf"
LISTES = "liste_*.csv"          # toutes les listes, envoyées dans l'ordre (banques, puis IT)
MAX_ENVOIS_PAR_JOUR = 200         # tout envoyer dans la journée (158 adresses)
PAUSE_MIN, PAUSE_MAX = 30, 90     # pause aléatoire entre deux mails (secondes) : ~2h40 pour 158 mails
# ========================================================

OBJET = "Candidature spontanée – Ingénieure IA & Data"

MESSAGE = """{salutation}

Ingénieure IA & Data récemment diplômée, je vous adresse ma candidature spontanée pour un poste d'Ingénieure IA, Data ou Machine Learning au sein {de_entreprise}.

Lors de mon projet de fin d'études chez VERMEG Solution, j'ai conçu et déployé une plateforme de détection de fraude bancaire. Elle s'appuie sur des modèles de Machine Learning (XGBoost, SHAP), sur un LLM avec un système RAG et sur une chaîne MLOps complète (MLflow, Docker, FastAPI, PostgreSQL). Cette expérience m'a permis de maîtriser tout le cycle d'un projet d'IA, de la préparation des données à la mise en production.

J'ai complété ce parcours par plusieurs expériences en développement full stack (Spring Boot, Angular, Node.js, React), ce qui me permet d'intégrer efficacement des solutions d'IA dans des applications réelles.

Rigoureuse, curieuse et orientée résultats, je serais ravie de mettre ces compétences au service de vos projets et de vous présenter mon parcours lors d'un entretien.

Vous trouverez mon CV en pièce jointe.

Je vous remercie de l'attention portée à ma candidature et vous prie d'agréer, {formule}, l'expression de mes salutations distinguées.

Saba Homri
Ingénieure IA & Data
+216 28 608 328
sabahomri96@gmail.com
"""

DOSSIER = Path(__file__).resolve().parent
JOURNAL = DOSSIER / "envois.log"


def deja_envoyes():
    if not JOURNAL.exists():
        return set()
    lignes = JOURNAL.read_text(encoding="utf-8").splitlines()
    return {l.split(";")[1].strip().lower() for l in lignes if ";OK" in l}


def lire_entreprises():
    toutes = []
    for fichier in sorted(DOSSIER.glob(LISTES)):
        brut = fichier.read_bytes()
        try:
            texte = brut.decode("utf-8-sig")
        except UnicodeDecodeError:  # CSV enregistré par Excel sans UTF-8
            texte = brut.decode("cp1252")
        separateur = ";" if ";" in texte.splitlines()[0] else ","
        lignes = [l for l in csv.DictReader(texte.splitlines(), delimiter=separateur)
                  if (l.get("email") or "").strip()]
        print(f"  {fichier.name} : {len(lignes)} adresses")
        toutes += lignes
    vus, uniques = set(), []
    for l in toutes:  # une adresse présente dans deux listes n'est envoyée qu'une fois
        e = l["email"].strip().lower()
        if e not in vus:
            vus.add(e)
            uniques.append(l)
    return uniques


def avec_de(nom):
    """« de Sagemcom », mais « d'Advans Tunisie » devant une voyelle."""
    if nom[:1].lower() in "aeiouyéèêàâîôûh" and not nom.lower().startswith(("la ", "le ", "les ")):
        return "d'" + nom
    return "de " + nom


def trouver_cv():
    """Le CV indiqué dans FICHIER_CV, sinon le seul PDF présent dans le dossier."""
    chemin = DOSSIER / FICHIER_CV
    if chemin.exists():
        return chemin
    pdfs = list(DOSSIER.glob("*.pdf"))
    if len(pdfs) == 1:
        return pdfs[0]
    sys.exit(f"CV introuvable : mets ton CV PDF dans {DOSSIER} et indique son nom dans FICHIER_CV.")


def construire_mail(ligne, cv_bytes):
    entreprise = (ligne.get("entreprise") or "").strip() or "votre entreprise"
    contact = (ligne.get("contact") or "").strip()
    if contact:  # ex. "Madame Ben Salah"
        salutation, formule = f"{contact},", contact
    else:
        salutation, formule = "Madame, Monsieur,", "Madame, Monsieur"

    msg = EmailMessage()
    msg["From"] = f"Saba Homri <{EXPEDITEUR}>"
    msg["To"] = ligne["email"].strip()
    msg["Subject"] = OBJET
    msg.set_content(MESSAGE.format(salutation=salutation, de_entreprise=avec_de(entreprise), formule=formule))
    msg.add_attachment(cv_bytes, maintype="application", subtype="pdf", filename=trouver_cv().name)
    return msg


def journaliser(email, entreprise, statut):
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M};{email};{entreprise};{statut}\n")


def envoyer_essai(adresse):
    """Envoie UN seul mail de test à l'adresse donnée (rien n'est noté dans envois.log)."""
    cv_bytes = trouver_cv().read_bytes()
    msg = construire_mail({"entreprise": "Entreprise Test", "email": adresse, "contact": ""}, cv_bytes)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as serveur:
        serveur.login(EXPEDITEUR, MOT_DE_PASSE_APPLICATION.replace(" ", ""))
        serveur.send_message(msg)
    print(f"Mail de test envoyé à {adresse}. Vérifie ta boîte de réception (et les spams).")


def main():
    if "--essai" in sys.argv:
        i = sys.argv.index("--essai")
        adresse = sys.argv[i + 1] if len(sys.argv) > i + 1 else EXPEDITEUR
        envoyer_essai(adresse)
        return
    mode_test = "--test" in sys.argv
    cv_bytes = trouver_cv().read_bytes()
    deja = deja_envoyes()
    a_envoyer = [l for l in lire_entreprises() if l["email"].strip().lower() not in deja]
    a_envoyer = a_envoyer[:MAX_ENVOIS_PAR_JOUR]

    print(f"{len(deja)} déjà envoyés, {len(a_envoyer)} à envoyer aujourd'hui.")
    if not a_envoyer:
        return

    if mode_test:
        print("\n--- MODE TEST : aucun mail n'est envoyé ---\n")
        apercu = construire_mail(a_envoyer[0], cv_bytes)
        print("À :", apercu["To"], "\nObjet :", apercu["Subject"], "\nPièce jointe :", trouver_cv().name, "\n")
        print(apercu.get_body(("plain",)).get_content())
        for l in a_envoyer:
            print(" ->", l.get("entreprise", ""), "<" + l["email"].strip() + ">")
        return

    contexte = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexte) as serveur:
        serveur.login(EXPEDITEUR, MOT_DE_PASSE_APPLICATION.replace(" ", ""))
        for i, ligne in enumerate(a_envoyer, 1):
            email, entreprise = ligne["email"].strip(), ligne.get("entreprise", "").strip()
            try:
                serveur.send_message(construire_mail(ligne, cv_bytes))
                journaliser(email, entreprise, "OK")
                print(f"[{i}/{len(a_envoyer)}] Envoyé à {entreprise} <{email}>")
            except Exception as e:
                journaliser(email, entreprise, f"ERREUR {e}")
                print(f"[{i}/{len(a_envoyer)}] ÉCHEC {entreprise} <{email}> : {e}")
            if i < len(a_envoyer):
                pause = random.randint(PAUSE_MIN, PAUSE_MAX)
                print(f"   pause de {pause} s...")
                time.sleep(pause)

    print("\nTerminé. En cas d'erreur, relance le script : seuls les mails non envoyés partiront.")


if __name__ == "__main__":
    main()