#!/bin/bash

# Update package list and install system dependencies
sudo apt-get update
sudo apt-get install -y mysql-server
sudo apt-get install -y git
sudo apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt-get install -y libmysqlclient-dev

# Install Python dependencies
pip3 install -r requirements.txt

# Download NLTK data
python3 -m nltk.downloader punkt



