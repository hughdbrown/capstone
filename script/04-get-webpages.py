#!/usr/bin/env python
"""
The fourth step in the project involved downloading content for each long url and
storing in a database.
"""
from __future__ import print_function, absolute_import, division

from sys import stderr
import concurrent.futures

import simplejson
from pymongo import MongoClient
import requests


client = MongoClient()
db = client.data
collection = db.urls


def is_website_collateral(long_url):
    return long_url.endswith(('.jpg', '.jpeg', '.png', '.css', '.js'))


def load_url(args):
    short_url, long_url = args
    doc = {'short_url': short_url, 'long_url': long_url}
    try:
        if is_website_collateral(long_url):
            # Skip urls that cannot have 
            doc['exc'] = 'Website collateral'
        else:
            # Record text scraped
            r = requests.get(long_url, timeout=12)
            doc['text'] = r.text
    except Exception as exc:
        # Record exception if process was not successful
        doc['exc'] =str(exc)

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
