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

#check for updates (and install if any) for Debian based systems
sudo $PKG_MANAGER update

#install updates if they are found (only for Debian based systems)
if [ "$PKG_MANAGER" == "apt-get" ]; then
    sudo $PKG_MANAGER upgrade -y
fi



#check for updates into Git repository on this folder
cd $HOME_DIR/projets_groupe
git pull
cd ..
