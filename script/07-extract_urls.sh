#!/bin/sh -e

# The second step in the project involved figuring out the most commonly hit URLs for each data file.

DST_DIR="../data"
[ ! -d "${DST_DIR}" ] && mkdir "${DST_DIR}"
DST_FILE=$DST_DIR/germanwings

for file in $( ls ../data-capstone/* ); do
    echo "Processing ${file}"
    zcat < "${file}" | python "07-extract-urls.py" >> $DST_FILE
done

