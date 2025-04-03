#!/bin/bash

HOME_DIR=/home/$(whoami)


# Update and upgrade the system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install -y python3 python3-pip

# Install virtualenv
sudo apt-get install virtualenv

# Create a virtual environment
virtualenv $HOME_DIR/env

# Activate the virtual environment
source $HOME_DIR/env/bin/activate

# Install required Python packages
pip install boto3 flask python-dotenv requests beautifulsoup4 spacy

# Download the SpaCy model
python -m spacy download en_core_web_sm

# Deactivate the virtual environment
deactivate

# Install Git
sudo apt-get install -y git

# Clone the repository (if not already cloned)
cd $HOME_DIR/Documents
if [ ! -d "$HOME_DIR/Documents/projets_groupe" ]; then
    git clone https://github.com/flo7716/projets_groupe 
fi



echo "Setup complete. All dependencies have been installed."
