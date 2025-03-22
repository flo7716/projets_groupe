#!/bin/bash
ENV_LOCATION=/home/ubuntu/env/bin
SCRIPT_LOCATION=/home/ubuntu/projets_groupe/Projet_federateur_IA

# Activation de l'environnement Python
source $ENV_LOCATION/activate

# Exécution du script de scraping et redirection des erreurs vers un fichier log
echo "Exécution du script Python de scraping"
python $SCRIPT_LOCATION/scraper.py > /home/ubuntu/scraping.log 2>&1

# Vérification du code de sortie de Python
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'exécution du script Python de scraping. Voir le log pour plus de détails."
    exit 1
fi

echo "Script terminé"
