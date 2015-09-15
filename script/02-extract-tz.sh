#!/bin/sh -e

# The second step in the project involved figuring out the most commonly hit URLs for each data file.

DST_DIR="timezones"
[ ! -d "${DST_DIR}" ] && mkdir "${DST_DIR}"


for file in $( ls ../data-capstone/* ); do
    csvfile=$(basename $file ".gz")."csv"
    echo $csvfile
    zcat < "${file}" | python "extract-urls.py" --key=tz > $DST_DIR/${csvfile}
done
