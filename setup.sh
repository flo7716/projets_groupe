#!/bin/bash

# Update and upgrade the system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install -y python3 python3-pip

# Install virtualenv
sudo apt-get install virtualenv

# Create a virtual environment
virtualenv /home/ubuntu/env

# Activate the virtual environment
source /home/ubuntu/env/bin/activate

# Install required Python packages
pip install boto3 flask python-dotenv requests beautifulsoup4 spacy

# Download the SpaCy model
python -m spacy download en_core_web_sm

# Deactivate the virtual environment
deactivate

# Install Git
sudo apt-get install -y git

# Clone the repository (if not already cloned)
git clone https://github.com/flo7716/projets_groupe.git /home/ubuntu/projets_groupe


echo "Setup complete. All dependencies have been installed."
