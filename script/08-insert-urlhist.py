from __future__ import print_function, absolute_import, division

from sys import stderr
from datetime import datetime

from pymongo import MongoClient

from utils import stdin_reader


def main():
    date_fmt = "%Y-%m-%dT%H:%M:%S"
    client = MongoClient()
    db = client.data
    collection = db["urlhist"]
    converter = datetime.strptime
    for i, doc in enumerate(stdin_reader()):
        doc["timestamp"] = converter(doc["timestamp"], date_fmt)
        collection.insert(doc)
        records = i
    print("{0} records read".format(records), file=stderr)


if __name__ == '__main__':
    main()
