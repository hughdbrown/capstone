#!/bin/sh -e

# The second step in the project involved storing the mappings between short urls and long urls.

DST_DIR="map-urls-json"
[ ! -d "${DST_DIR}" ] && mkdir "${DST_DIR}"

for file in $( ls ../data-capstone/* ); do
    jsonfile=$(basename $file ".gz")."json"
    echo ${jsonfile}
    zcat < "${file}" | python "02-map-urls.py" > ${DST_DIR}/${jsonfile}
done

