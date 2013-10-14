#!/usr/bin/env sh

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python -y
sudo apt-get install python-pip -y
sudo apt-get install python-dev -y
sudo apt-get install build-essential -y
sudo apt-get install git -y
sudo apt-get install libevent-dev -y
sudo pip install --upgrade pip
sudo pip install -r /tmp/locust/bootstrap-master/requirements.txt
