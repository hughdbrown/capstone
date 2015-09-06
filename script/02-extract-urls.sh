#!/bin/sh

# The second step in the project involved figuring out the most commonly hit URLs for each data file.

DST_DIR = hits-csv
mkdir -p $DST_DIR

for file in $( ls ../data-capstone/* ); do
    csvfile=$(basename $file ".gz")."csv"
    echo $csvfile
    zcat < "${file}" | python "02-extract-urls.py" > $DST_DIR/${csvfile}
done
