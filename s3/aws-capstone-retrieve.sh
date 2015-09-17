#!/bin/sh -e

cd ~/workspace/hughdbrown/capstone/data

aws s3 cp s3://hughdbrown/data-capstone/data/data/system.indexes.bson dump/

aws s3 cp s3://hughdbrown/data-capstone/data/data/urls.bson dump/
aws s3 cp s3://hughdbrown/data-capstone/data/data/urls.metadata.json dump/

aws s3 cp s3://hughdbrown/data-capstone/data/data/germanwings.bson dump/
aws s3 cp s3://hughdbrown/data-capstone/data/data/germanwings.metadata.json dump/

aws s3 cp s3://hughdbrown/data-capstone/data/data/urlhist.bson dump/
aws s3 cp s3://hughdbrown/data-capstone/data/data/urlhist.metadata.json dump/
