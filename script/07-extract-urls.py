#!/usr/bin/env python
from __future__ import print_function, absolute_import, division

from sys import stderr
import simplejson
from datetime import datetime
import pickle

from utils import LOCATION_COLUMNS, COLUMN_REMAP, stdin_reader


def filter_dicts(series, germanwings):
    """
    Filter dictionaries by short_url
    """
    for d in series:
        short_url = d["g"]
        if short_url in germanwings:
            yield d


def sanitize_dicts(series):
    """
    Write out only columns that appear in LOCATION_COLUMNS;
    remap the column names using COLUMN_REMAP
    """
    converter = datetime.utcfromtimestamp
    for d in series:
        d['t'] = converter(d['t']).isoformat()
        yield {
            COLUMN_REMAP[k]: v
            for k, v in d.items()
            if k in LOCATION_COLUMNS
        }


def load_germanwings():
    filename = "../data/germanwings.pkl"
    print("Loading {0}".format(filename), file=stderr)
    with open(filename, "rb") as f:
        germanwings = pickle.load(f)
        assert type(germanwings) == set
        return germanwings


def main():
    try:
        germanwings = load_germanwings()
        dumper = simplejson.dumps
        print("Extracting urls", file=stderr)
        records = 0
        for i, item in enumerate(sanitize_dicts(filter_dicts(stdin_reader(), germanwings))):
            print(dumper(item))
            records = i
        print("{0} records written".format(records), file=stderr)
    except Exception as exc:
        print(exc)


if __name__ == '__main__':
    main()
