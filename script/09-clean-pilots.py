#!/usr/bin/env python
"""
Find the short_urls that have `pilot` in the domain.
List will be used later to clean up germanwings collectioN in mongodb.
"""
from __future__ import absolute_import, print_function

from sys import stderr
import re
import pickle
from urlparse import urlparse

from pymongo import MongoClient

PICKLE_FILE = "pilots.pkl"


def open_mongo():
    client = MongoClient()
    return client.data


def write_pickle():
    """
    Create a pickle-file of short_urls that should not be part of germanwings or urlhist
    """
    db = open_mongo()
    coll = db.germanwings

    regex = re.compile(r'.*pilot.*')
    pilots = set()
    for doc in coll.find({}, {'long_url': 1, 'short_url': 1}):
        u = urlparse(doc["long_url"])
        m = regex.match(u.netloc)
        if m:
            pilots.add(doc["short_url"])

    with open(PICKLE_FILE, "wb") as f:
        pickle.dump(pilots, f)


def read_pickle():
    with open(PICKLE_FILE, "rb") as f:
        return pickle.load(f)


def main():
    db = open_mongo()
    pilots = read_pickle()

    for i, short_url in enumerate(pilots):
        print("Removing {0}: {1} / {2}".format(short_url, i, len(pilots)), file=stderr)
        db.germanwings.delete_many({'short_url': short_url})
        db.urlhist.delete_many({'short_url': short_url})


if __name__ == '__main__':
    main()
