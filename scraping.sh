#!/bin/bash
ENV_LOCATION=/home/ubuntu/env/bin
SCRIPT_LOCATION=/home/ubuntu/projets_groupe/Projet_Federateur_IA


#Activation environnement Python
source $ENV_LOCATION/activate

#Execution scraping
echo "Execution script Python scraping"
python $SCRIPT_LOCATION/scraper.py
echo "Script termine"


