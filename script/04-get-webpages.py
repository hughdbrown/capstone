#!/usr/bin/env python
"""
The fourth step in the project involved downloading content for each long url
and storing in a database.
"""
from __future__ import print_function, absolute_import, division

from sys import stderr
from csv import DictReader

import simplejson
from pymongo import MongoClient
import requests

from utils.collateral import is_website_collateral


# Number of hits across 72 hours by rank
# 25k rank = 937 hits
# 50k rank = 431 hits
# 100k rank = 178 hits
# 200k rank = 68 hits

CUTOFF = 150

client = MongoClient()
db = client.data
collection = db.urls

FIELDNAMES = ('short_url', 'count')


def url_counts():
    """
    Extract the number of times a particular URL was hit in 72 hours
    from precomputed data. Use this to filter out low hit counts.
    """
    print("Opening CSV file of url counts", file=stderr)
    with open("../data//hits-aggregated.csv") as f:
        print("Reading CSV", file=stderr)
        reader = DictReader(f, fieldnames=FIELDNAMES)
        return {
            row["short_url"]: int(row['count'])
            for row in reader
        }


# Read mapping of short url to number of hits into global variable
URL_COUNTS = url_counts()


def load_url(short_url, long_url, count=CUTOFF):
    """
    Load a given short_url/long_url combination into Mongodb
    """
    doc = {'short_url': short_url, 'long_url': long_url, 'count': count}
    d = collection.find_one({'short_url': short_url})
    if d:
        print("Already in database: {0}".format(short_url), file=stderr)
    elif is_website_collateral(long_url):
        # Skip urls that cannot have HTML content
        doc['exc'] = 'Website collateral'
    elif count < CUTOFF:
        doc['exc'] = "Too few hits"
    else:
        try:
            # Record text scraped
            print("> {0}".format(short_url), file=stderr)
            r = requests.get(long_url, timeout=12)
            print("< {0}".format(short_url), file=stderr)
        except Exception as exc:
            # Record exception if process was not successful
            doc['exc'] = str(exc)
            print("Exception: {0}".format(exc), file=stderr)
        else:
            headers = r.headers
            status_code = r.status_code
            if status_code >= 400:
                doc.update({'exc': "Bad status_code", 'status_code': status_code})
            else:
                content_type = headers.get('content-type')
                if not content_type or ('text/html' not in content_type):
                    doc.update({'exc': "Bad content type", 'content_type': content_type})
                else:
                    try:
                        text = r.text
                    except Exception as exc1:
                        doc['exc'] = str(exc1)
                        print("Exception: {0}".format(exc1), file=stderr)
                    else:
                        content_length = int(headers.get('content-length', len(text)))
                        if content_length > 200 * 1000:
                            doc.update({'exc': "Too long", 'content_length': content_length})
                        else:
                            doc['text'] = text
    if not d:
        print("> Inserting {0}".format(short_url), file=stderr)
        collection.insert_one(doc)
        print("< Inserting {0}".format(short_url), file=stderr)
    return short_url


def longurls():
    while True:
        r = requests.get("http://localhost:5000/")
        j = r.json()
        if j:
            yield j
        else:
            break


def main():
    """
    Main entry point
    """
    for d in longurls():
        short_url = d['short_url']
        long_url = d['long_url']
        load_url(short_url, long_url, count=URL_COUNTS[short_url])


if __name__ == '__main__':
    main()
