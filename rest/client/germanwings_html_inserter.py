#!/usr/bin/env python
from __future__ import print_function, absolute_import

import time

import simplejson
import requests
from selenium import webdriver
import pymongo

PHANTOM_PATH = '/usr/local/bin/phantomjs'

client = pymongo.MongoClient()
conn = client.data
coll = conn.germanwings_html
# db.germanwings_html.createIndex({'short_url': 1}, {'unique': 1})

def client(url, key):
    try:
        driver = webdriver.PhantomJS(executable_path=PHANTOM_PATH)
        driver.set_page_load_timeout(3)
        driver.get(url)
        text = driver.page_source
    except Exception as exc:
        print(str(exc))
    else:
        try:
            record = {
                'short_url': key,
                'long_url': url,
                'text': text,
            }
            coll.insert(record)
        except pymongo.errors.DuplicateKeyError:
            pass
    finally:
        driver.close()


def main():
    while True:
        d = requests.get("http://localhost:5000/").json()
        if not d:
            break
        else:
            client(d["short_url"], d["long_url"])


if __name__ == '__main__':
    main()
