#!/bin/bash
cd "$(dirname "$0")"
echo "=== TEST : aucun mail ne sera envoye ==="
python3 envoyer_candidatures.py --test
read -p "Appuie sur Entree pour fermer"
