#!/bin/bash

HOME_DIR=/home/$(whoami)

# Define environment and script locations
ENV_LOCATION="$HOME_DIR/env/bin"
SCRIPT_LOCATION="$HOME_DIR/projets_groupe/Projet_federateur_IA"

# Activate the Python virtual environment
if [ ! -f "$ENV_LOCATION/activate" ]; then
    echo "Erreur: Le fichier d'activation de l'environnement Python est introuvable."
    exit 1
fi
source "$ENV_LOCATION/activate"

# Execute the Python scraping script
echo "Execution du script Python de scraping"
if [ ! -f "$SCRIPT_LOCATION/scraper.py" ]; then
    echo "Erreur: Le script Python de scraping est introuvable."
    exit 1
fi

python "$SCRIPT_LOCATION/scraper.py"


echo "Script termine"
