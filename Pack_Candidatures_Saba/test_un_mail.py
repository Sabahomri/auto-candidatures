"""
Test : envoie UN SEUL mail de candidature, à une seule adresse.
Rien n'est envoyé aux entreprises.

Utilisation (dans le terminal, dans le dossier du pack) :
    python test_un_mail.py
"""

import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

# ===================== À CONFIGURER =====================
EXPEDITEUR = "sabahomri96@gmail.com"
MOT_DE_PASSE_APPLICATION = "qiqo egad wowm jivu"  # mot de passe d'application Gmail (16 caractères)
DESTINATAIRE_TEST = "sabahomri96@gmail.com"       # l'adresse qui reçoit le mail de test
FICHIER_CV = "HOMRI_Saba_CV_IA_Data.pdf"
ENTREPRISE_TEST = "Entreprise Test"
# ========================================================

OBJET = "Candidature spontanée – Ingénieure IA & Data"

MESSAGE = f"""Madame, Monsieur,

Ingénieure IA & Data récemment diplômée, je vous adresse ma candidature spontanée pour un poste d'Ingénieure IA, Data ou Machine Learning au sein de {ENTREPRISE_TEST}.

Lors de mon projet de fin d'études chez VERMEG Solution, j'ai conçu et déployé une plateforme de détection de fraude bancaire. Elle s'appuie sur des modèles de Machine Learning (XGBoost, SHAP), sur un LLM avec un système RAG et sur une chaîne MLOps complète (MLflow, Docker, FastAPI, PostgreSQL). Cette expérience m'a permis de maîtriser tout le cycle d'un projet d'IA, de la préparation des données à la mise en production.

J'ai complété ce parcours par plusieurs expériences en développement full stack (Spring Boot, Angular, Node.js, React), ce qui me permet d'intégrer efficacement des solutions d'IA dans des applications réelles.

Rigoureuse, curieuse et orientée résultats, je serais ravie de mettre ces compétences au service de vos projets et de vous présenter mon parcours lors d'un entretien.

Vous trouverez mon CV en pièce jointe.

Je vous remercie de l'attention portée à ma candidature et vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

Saba Homri
Ingénieure IA & Data
+216 28 608 328
sabahomri96@gmail.com
"""


def main():
    chemin_cv = Path(__file__).resolve().parent / FICHIER_CV
    if not chemin_cv.exists():
        print(f"CV introuvable : {chemin_cv}\nMets le fichier PDF dans le même dossier que ce script.")
        return

    msg = EmailMessage()
    msg["From"] = f"Saba Homri <{EXPEDITEUR}>"
    msg["To"] = DESTINATAIRE_TEST
    msg["Subject"] = OBJET
    
    msg.set_content(MESSAGE)
    msg.add_attachment(chemin_cv.read_bytes(), maintype="application", subtype="pdf", filename=FICHIER_CV)

    print(f"Envoi du mail de test à {DESTINATAIRE_TEST}...")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as serveur:
            serveur.login(EXPEDITEUR, MOT_DE_PASSE_APPLICATION.replace(" ", ""))
            serveur.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        print("Connexion refusée : vérifie le mot de passe d'application Gmail (16 lettres).")
        return
    except Exception as e:
        print(f"Erreur : {e}")
        return

    print("Mail envoyé ! Vérifie ta boîte de réception (et les spams).")


if __name__ == "__main__":
    main()