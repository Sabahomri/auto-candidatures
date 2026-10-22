#!/bin/bash
cd "$(dirname "$0")"
echo "=== ENVOI REEL - laisse cette fenetre ouverte (environ 2h40) ==="
python3 envoyer_candidatures.py
read -p "Appuie sur Entree pour fermer"
