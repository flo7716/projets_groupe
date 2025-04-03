#!/bin/bash


# Define environment and script locations
ENV_LOCATION="/home/ubuntu/env/bin"
SCRIPT_LOCATION="/home/ubuntu/projets_groupe/Projet_federateur_IA"

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
fi

python "$SCRIPT_LOCATION/scraper.py"


echo "Script termine"
