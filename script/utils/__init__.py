"""
Shared constants and code
"""
from __future__ import print_function

from sys import stdin, stderr
import os
import os.path

import simplejson


# See schema.txt for explanation of columns
COLUMNS = set(['a', 'c', 'ckw', 'cy', 'dp', 'g', 'h', 'kw', 'mc', 'nk', 'pp', 't', 'tz', 'u'])
LOCATION_COLUMNS = set(['c', 'tz', 't', 'g'])
COLUMN_REMAP = {
    'a': 'browser',
    'c': 'country',
    'ckw': 'custom',
    'cy': 'city',
    'g': 'short_url',
    'h': 'user',
    'kw': 'keyword',
    't': 'timestamp',
    'tz': 'timezone',
    'u': 'long_url',
}


def stdin_reader(f=stdin):
    """
    Read JSON objects from file, one per line.
    Yield loaded diciotnaries
    """
    loader = simplejson.loads
    for line in f:
        yield loader(line)


def filter_files_by_ext(directory, ext):
    """
    Get the names of the .csv files in the current directory
    """
    for filename in os.listdir(directory):
        if os.path.splitext(filename)[1] == ext:
            yield os.path.join(directory, filename)


def coalesce_jsonfiles(srcdir, ext):
    """
    This is really a call to `reduce`:

    dest = reduce(
        filter_files_by_ext("map-urls-json/", ".json"),
        lambda x, y: x.update(stdin_reader(y)),
        {}
    )
    """
    dest = {}
    for filename in filter_files_by_ext(srcdir, ext):
        print(filename, file=stderr)
        with open(filename) as f:
            for d in stdin_reader(f):
                print("\t{0} records read".format(len(d)), file=stderr)
                dest.update(d)
    return dest