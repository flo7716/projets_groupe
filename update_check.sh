#!/bin/bash

#check for updates
sudo apt-get update

#install updates if they are found
sudo apt-get upgrade -y


#check for updates into Git repository
cd projets_groupe
git pull
cd ..
