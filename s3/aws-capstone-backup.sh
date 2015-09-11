#!/bin/sh -e

aws s3 cp system.indexes.bson s3://hughdbrown/data-capstone/data/data/

aws s3 cp urls.bson s3://hughdbrown/data-capstone/data/data/
aws s3 cp urls.metadata.json s3://hughdbrown/data-capstone/data/data/

aws s3 cp germanwings.bson s3://hughdbrown/data-capstone/data/data/
aws s3 cp germanwings.metadata.json s3://hughdbrown/data-capstone/data/data/

aws s3 cp urlhist.bson s3://hughdbrown/data-capstone/data/data/
aws s3 cp urlhist.metadata.json s3://hughdbrown/data-capstone/data/data/
