from __future__ import absolute_import, print_function

import pickle
import sys

from pymongo import MongoClient


def main():
    print("Connecting to mongodb", file=sys.stderr)
    client = MongoClient()
    db = client.data
    collection = db.germanwings
    print("Generating set of short_urls", file=sys.stderr)
    germanwings = set([doc["short_url"] for doc in collection.find({}, {'short_url': 1, "_id": 0})])
    filename = "germanwings.pkl"
    print("Pickling result to {0}".format(filename), file=sys.stderr)
    with open(filename, "wb") as f:
        pickle.dump(germanwings, f)
    print("Done", file=sys.stderr)


if __name__ == '__main__':
    main()
