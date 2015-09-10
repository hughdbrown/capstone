#!/bin/sh

cd ~
mkdir -p scripts
mkdir -d data

sudo yum install -y awscli tmux vim wget

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
