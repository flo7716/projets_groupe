#!/bin/bash
set -x  # Enable debugging

# Define environment and script locations
ENV_LOCATION="/home/ubuntu/env/bin"
SCRIPT_LOCATION="/home/ubuntu/projets_groupe/Projet_federateur_IA"

# Activate the Python virtual environment
if [ ! -f "$ENV_LOCATION/activate" ]; then
    echo "Erreur: Le fichier d'activation de l'environnement Python est introuvable."
    exit 1
fi
source "$ENV_LOCATION/activate"

# Execute the Python scraping script and redirect errors to a log file
echo "Execution du script Python de scraping"
if [ ! -f "$SCRIPT_LOCATION/scraper.py" ]; then
    echo "Erreur: Le script Python de scraping est introuvable."
    exit 1
fi

python "$SCRIPT_LOCATION/scraper.py" > /home/ubuntu/scraping.log 2>&1

# Check the exit code of the Python script
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'execution du script Python de scraping. Voir le log pour plus de details."
    exit 1
fi

echo "Script termine"
