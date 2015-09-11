#!/bin/sh

cd ~
mkdir -p scripts
mkdir -d data

# Need epel-release to get htop
sudo yum install -y wget
wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
sudo rpm -ivh epel-release-7-5.noarch.rpm

sudo yum install -y awscli tmux vim tree htop

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install -r requirements.txt

REGION="us-west-2"

cd ~/data
aws s3 cp --recursive --region $REGION s3://hughdbrown/data-capstone/data .
aws s3 cp --recursive --region $REGION s3://hughdbrown/data-capstone/urls.bson .

cd ~/script
python 04-create-database.py
mongorestore --db=data --collection=urls ../data/urls.bson
