#!/bin/bash
set -x  # Enable debugging
ENV_LOCATION=/home/ubuntu/env/bin
SCRIPT_LOCATION=/home/ubuntu/projets_groupe/Projet_federateur_IA

# Activation de l'environnement Python
if [ ! -f "$ENV_LOCATION/activate" ]; then
    echo "Erreur: Le fichier d'activation de l'environnement Python est introuvable."
    exit 1
fi
source $ENV_LOCATION/activate

# Exécution du script de scraping et redirection des erreurs vers un fichier log
echo "Exécution du script Python de scraping"
if [ ! -f "$SCRIPT_LOCATION/scraper.py" ]; then
    echo "Erreur: Le script Python de scraping est introuvable."
    exit 1
fi
python $SCRIPT_LOCATION/scraper.py > /home/ubuntu/scraping.log 2>&1

# Vérification du code de sortie de Python
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'exécution du script Python de scraping. Voir le log pour plus de détails."
    exit 1
fi

echo "Script terminé"