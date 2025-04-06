#!/bin/bash

HOME_DIR=/home/$(whoami)

#check for updates
sudo apt-get update

#install updates if they are found
sudo apt-get upgrade -y


#check for updates into Git repository on this folder
cd $HOME_DIR/projets_groupe
git pull
cd ..
