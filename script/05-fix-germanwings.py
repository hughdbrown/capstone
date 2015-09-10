#!/usr/bin/env python
"""
Generate a list of urls for likely Germanwings hits
"""
from __future__ import print_function, absolute_import, division

import sys
import re
from urlparse import urlparse

from pymongo import MongoClient
import simplejson


def main():
    client = MongoClient()
    db = client.data
    collection = db.urls

    regex = re.compile(r""".*(germanwing|plane.+crash|pilot).*""", re.IGNORECASE)

    query = {
         "long_url": regex,
         "exc" : "Too few hits",
    }
    fields = {
        'short_url': 1,
        'long_url': 1,
        '_id': 0,
    }

    urliter = ((d['short_url'], d["long_url"]) for d in collection.find(query, fields))
    doc = {
        short_url: long_url
        for short_url, long_url in urliter
        if "pilot" not in urlparse(long_url).netloc
    }
    print(simplejson.dumps(doc))
    print("{0} records found".format(len(doc)), file=sys.stderr)


if __name__ == '__main__':
    main()
