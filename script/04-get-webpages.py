#!/usr/bin/env python
"""
The fourth step in the project involved downloading content for each long url
and storing in a database.
"""
from __future__ import print_function, absolute_import, division

from sys import stderr
import concurrent.futures
from csv import DictReader

import simplejson
from pymongo import MongoClient
import requests


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
    with open("hits-csv/aggregated.csv") as f:
        print("Reading CSV", file=stderr)
        reader = DictReader(f, fieldnames=FIELDNAMES)
        return {
            row["short_url"]: int(row['count'])
            for row in reader
        }


# Read mapping of short url to number of hits into global variable
URL_COUNTS = url_counts()


def is_website_collateral(long_url):
    return long_url.endswith(('.jpg', '.jpeg', '.png', '.css', '.js'))


def load_url(args):
    short_url, long_url = args
    count = URL_COUNTS[short_url]
    doc = {'short_url': short_url, 'long_url': long_url, 'count': count}
    try:
        if is_website_collateral(long_url):
            # Skip urls that cannot have HTML content
            doc['exc'] = 'Website collateral'
        elif count < CUTOFF:
            doc['exc'] = "Too few hits"
        else:
            # Record text scraped
            r = requests.get(long_url, timeout=12)
            doc['text'] = r.text
    except Exception as exc:
        # Record exception if process was not successful
        doc['exc'] = str(exc)

    collection.insert(doc)
    return short_url


def longurls():
    print("Opening JSON", file=stderr)
    with open("map-urls-json/aggregated.json") as f:
        print("Reading JSON", file=stderr)
        d = simplejson.loads(f.read())
        print("Yielding {0} short_url/long_url pairs".format(len(d)), file=stderr)
        # python 2.7 code
        for key, value in d.items():
            yield key, value
        # python 3.x code
        # yield from d.items()


def main():
    print("Creating executor", file=stderr)
    with concurrent.futures.ProcessPoolExecutor(max_workers=None) as executor:
        print("Creating the futures to execute", file=stderr)
        for data in executor.map(load_url, longurls()):
            print(data['short_url'])


if __name__ == '__main__':
    main()
