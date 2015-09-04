#!/bin/sh

# Copy data from bit.ly S3 bucket to my won
aws s3 sync s3://bitly-challenges/hdb_sanitized s3://hughdbrown/data-capstone
