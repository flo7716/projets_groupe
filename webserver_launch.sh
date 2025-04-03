#!/bin/bash

ENV_LOCATION=$HOME_DIR/env/bin
SCRIPT_LOCATION=$HOME_DIR/Documents/projets_groupe/Projet_federateur_IA

#activation environnement virtuel
source $ENV_LOCATION/activate

# lancement serveur web
cd $SCRIPT_LOCATION
python3 app.py

