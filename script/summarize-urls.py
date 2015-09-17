#!/usr/bin/env python
"""
Scan a bit.ly data file and filter by the short_urls found in the germanwings.pkl file,
i.e.: create the data for a germanwings-hist JSON file using CSV files.

Usage: summarize-urls --field=<FIELDNAME>...

Arguments:
    FIELDNAME           Field name to summarize data on

Options:
    -h --help           Show this screen.
    --field=<FIELDNAME> Optional repeating name of field to summarize on

"""
from __future__ import print_function, absolute_import, division

from sys import stderr
from datetime import datetime
import itertools
from operator import itemgetter

import dateutil.parser
import simplejson
from docopt import docopt

from utils import stdin_reader


def main(fields):
    data = []
    for item in stdin_reader():
        dt = dateutil.parser.parse(item["timestamp"])
        data.append(dict(
            [(k, v) for k, v in item.items() if k in fields] +
            [("day", dt.day), ("hour", dt.hour), ("minute", dt.minute)]
        ))

    keys = fields + ["day", "hour", "minute"]
    keyfn = itemgetter(*keys)
    data = sorted(data, key=keyfn)
    for k, g in itertools.groupby(data, key=keyfn):
        d = {
            "key": k[0],
            "timestamp": datetime(2015, 3, k[1], k[2], k[3]),
            "count": len(list(g)),
        }
        print(simplejson.dumps(d))


if __name__ == '__main__':
    options = docopt(__doc__)
    fields = list(options.get("--field"))
    main(fields)
