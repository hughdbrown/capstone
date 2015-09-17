#!/bin/sh -e

# The second step in the project involved figuring out the most commonly hit URLs for each data file.

DST_DIR="../data"
[ ! -d "${DST_DIR}" ] && mkdir "${DST_DIR}"
FILENAME="urlhist-US-DE-ES-IT.json"
DST_FILE=$DST_DIR/$FILENAME

#for file in $( ls ../data-capstone/* ); do
#    echo "Processing ${file}"
#    zcat < "${file}" | python "07-extract-urls.py" --country=US --country=DE --country=ES --country=IT >> $TMP_FILE
#done

cat ../data-capstone/*.log | \
    python "07-extract-urls.py" --country=US --country=DE --country=ES --country=IT | \
    python summarize-urls.py --field='country' | \
    python convert-objs-to-json.py > $DST_FILE
