#!/usr/bin/env python
"""
Scan a bit.ly data file and filter by the short_urls found in the germanwings.pkl file,
i.e.: create the data for a germanwings-hist JSON file using CSV files.

Usage: 07-extract-urls --country=<COUNTRY>...

Arguments:
    COUNTRY         Country code to use

Options:
    -h --help           Show this screen.
    --country=<COUNTRY> Optional repeating country code

"""
from __future__ import print_function, absolute_import, division

from sys import stderr
from datetime import datetime
import pickle
from csv import DictReader, register_dialect
import itertools

import simplejson
from docopt import docopt

from utils import LOCATION_COLUMNS, COLUMN_REMAP, stdin_reader


def load_remapped_timezones():
    print("Loading timezones", file=stderr)
    with open("../data/timezone-map.csv") as f:
        reader = DictReader(f, fieldnames=["timezone", "offset1", "offset2"])
        return {row["timezone"]: row["offset1"] for row in reader}


def load_remapped_country_codes():
    print("Loading country codes", file=stderr)
    dialect = register_dialect('tabs', delimiter='\t')
    with open("../data/country-code-lookup.csv") as f:
        reader = DictReader(f, dialect='tabs')
        return {row["Code"]: row["Country name"] for row in reader}


remapped_timezone = load_remapped_timezones()
remapped_country_code = load_remapped_country_codes()


def filter_dicts(series, germanwings, country=None):
    """
    Filter dictionaries by short_url
    """
    for d in series:
        short_url = d["g"]
        if short_url in germanwings:
            if (not country) or (d.get("c") in country):
                yield d


def timestamp_remapper(timestamp):
    """
    Function that converts a timestamp to a DateTime in ISO format
    """
    return datetime.utcfromtimestamp(timestamp).isoformat()


def timezone_remapper(timezone):
    """
    Function that converts a timezone to an offset from UTC
    """
    return remapped_timezone.get(timezone, "")


def country_code_remapper(country_code):
    """
    Function that converts a country code to a longer text name
    """
    return remapped_country_code.get(country_code, "")


def noop(arg):
    """
    A no-op conversion function
    """
    return arg


def sanitize_dicts(series):
    """
    Write out only columns that appear in LOCATION_COLUMNS;
    remap the column names using `COLUMN_REMAP`
    remap the values using functions in `remapper`
    """
    remapper = {
        't': timestamp_remapper,
        'tz': timezone_remapper,
        'c': country_code_remapper,
        'g': noop,
    }

    for d in series:
        yield {
            COLUMN_REMAP[k]: remapper[k](v)
            for k, v in d.items()
            if k in LOCATION_COLUMNS
        }


def load_germanwings():
    filename = "../data/germanwings.pkl"
    print("Loading {0}".format(filename), file=stderr)
    with open(filename, "rb") as f:
        germanwings = pickle.load(f)
        return germanwings


def main(countries=None):
    try:
        germanwings = load_germanwings()
        dumper = simplejson.dumps
        print("Extracting urls", file=stderr)
        records = 0
        stream = sanitize_dicts(filter_dicts(stdin_reader(), germanwings, countries))
        for i, item in enumerate(stream):
            print(dumper(item))
            records = i
        print("{0} records written".format(records), file=stderr)
    except Exception as exc:
        print(exc)


if __name__ == '__main__':
    options = docopt(__doc__)
    countries = set(options.get("--country"))
    main(countries)
