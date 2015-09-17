#!/bin/sh -e

# The second step in the project involved figuring out the most commonly hit URLs for each data file.

DST_DIR="../data"
[ ! -d "${DST_DIR}" ] && mkdir "${DST_DIR}"
FILENAME="urlhist-US-CA.json"
TMP_FILE=/tmp/$FILENAME
DST_FILE=$DST_DIR/$FILENAME

for file in $( ls ../data-capstone/* ); do
    echo "Processing ${file}"
    zcat < "${file}" | python "07-extract-urls.py" --country=US --country=CA >> $TMP_FILE
done

python convert-objs-to-json.py $TMP_FILE > $DST_FILE
rm $TMP_FILE

