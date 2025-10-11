#!/bin/bash

HOME_DIR=/home/$(whoami)


## Check if current system is Debian or RedHat based
if [ -f /etc/debian_version ]; then
    echo "Debian-based system detected."
    PKG_MANAGER="apt-get"
elif [ -f /etc/redhat-release ]; then
    echo "RedHat-based system detected."
    PKG_MANAGER="dnf"
else
    echo "Unsupported OS. Exiting."
    exit 1

fi

# Update and upgrade the system by using respective package manager update commands
if $PKG_MANAGER == "apt-get"; then
    sudo $PKG_MANAGER update -y
    sudo $PKG_MANAGER upgrade -y
elif $PKG_MANAGER == "dnf"; then
    sudo $PKG_MANAGER check-update -y
    sudo $PKG_MANAGER upgrade -y
fi

# Install Python and pip
sudo $PKG_MANAGER install -y python3 python3-pip cron

# Install virtualenv
sudo $PKG_MANAGER install -y virtualenv

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
sudo $PKG_MANAGER install -y git

# Clone the repository (if not already cloned)
cd $HOME_DIR
if [ ! -d "$HOME_DIR/projets_groupe" ]; then
    git clone https://github.com/flo7716/projets_groupe 
fi


echo "Setup complete. All dependencies have been installed."
