#!/bin/sh

# The second step in the project involved storing the mappings between short urls and long urls.

DST_DIR = map-urls-csv
mkdir -p $DST_DIR

for file in $( ls ../data-capstone/* ); do
    csvfile=$(basename $file ".gz")."csv"
    echo $csvfile
    zcat < "${file}" | python "02-map-urls.py" > $DST_DIR/${csvfile}
done

