#!/usr/bin/env python
"""
The fourth step in the project involved downloading content for each long url
and storing in a database.
"""
from __future__ import print_function, absolute_import, division

from sys import stderr
import concurrent.futures
from csv import DictReader
import random
from urlparse import urlparse

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
    with open("../data//hits-aggregated.csv") as f:
        print("Reading CSV", file=stderr)
        reader = DictReader(f, fieldnames=FIELDNAMES)
        return {
            row["short_url"]: int(row['count'])
            for row in reader
        }


# Read mapping of short url to number of hits into global variable
URL_COUNTS = url_counts()


def is_website_collateral(long_url):
    """
    Boolean method for whether a URL is a skippable web asset
    """
    p = urlparse(long_url)
    collateral = (
        '.jpg', '.jpeg', '.png', '.gif',
        '.tif', '.tiff',
        '.jif', '.jfif',
        '.jp2', '.jpx', '.j2k', '.j2c',	
        '.fpx',
        '.pcd',
        '.pdf',
        '.css', '.js',
    )
    streaming_data = (
        '.3gp', '.3g2',
        '.nsv', '.m4v',
        '.mpg', '.mpeg', '.m2v',
        '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv',
        '.asf',
        '.rm',
        '.wmv',
        '.mov', '.qt',
        '.avi',
        '.ogv', '.ogg',
        '.flv',
        '.mkv',
        '.webm',
        '.vob',
    )
    archive = (
        '.zip', '.gz', '.tar', '.apk', '.iso', '.rar',
        '.cpio', '.shar', '.bz2', '.lz', '.xz', '.7z', '.s7z',
        '.cab', '.dmg',
        '.jar', '.war',
        '.zoo',
        '.pak',
        '.tgz', '.lzma',
    )
    return (
        'stream' in long_url or
        any(p.path.endswith(x) for x in (collateral, streaming_data, archive))
    )


def load_url(args):
    """
    Load a given short_url/long_url combination into Mongodb
    """
    short_url, long_url = args
    count = URL_COUNTS[short_url]
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
    print("Opening JSON", file=stderr)
    with open("map-urls-json/map-urls-aggregated.json") as f:
        print("Reading JSON", file=stderr)
        d = simplejson.loads(f.read())
        print("Yielding {0} short_url/long_url pairs".format(len(d)), file=stderr)
        # python 2.7 code
        for key, value in d.items():
            yield key, value
        # python 3.x code
        # yield from d.items()


def main():
    #print("Creating executor", file=stderr)
    #with concurrent.futures.ProcessPoolExecutor(max_workers=None) as executor:
    #    print("Creating the futures to execute", file=stderr)
    #    for data in executor.map(load_url, longurls()):
    #        print(data['short_url'])
    for url in longurls():
        load_url(url)


if __name__ == '__main__':
    main()
