"""
The first task of the project was to make it easier for bit.ly to extract so much data for me.
This meant that:
1. the data files had to be sanitized of columns that were internal to bit.ly
2. the data had to be filtered by time (i.e. I was taking only the top ten Minutes of each hour)

The code is written to use generators to minimize the memory profile and to make them
effective as parts of a unix pipeline. The code was executed in the scope of an internal bit.ly
pipeline so there are no examples of running it locally.
"""
from __future__ import print_function, absolute_import, division

from sys import stdin, stderr
from simplejson import loads as loader, dumps as dumper
from datetime import datetime

# See schema.txt for explanation of columns
COLUMNS = set(['a', 'c', 'ckw', 'cy', 'dp', 'g', 'h', 'kw', 'mc', 'nk', 'pp', 't', 'tz', 'u'])


def stdin_reader():
    """
    A generator that translate a line of JSON read from stdin to a python dict
    """
    for line in stdin:
        yield loader(line)


def filter_dicts(series):
    """
    Filter dictionaries by timestamp
    """
    converter = datetime.fromtimestamp
    for d in series:
        t = converter(d['t'])
        if 0 <= t.minute < 10:
            yield d


def sanitize_dicts(series):
    """
    Write out only columns that appear in COLUMNS
    """
    for d in series:
        yield {k: v for k, v in d.items() if k in COLUMNS}


def main():
    for i, item in enumerate(sanitize_dicts(filter_dicts(stdin_reader()))):
        # 131 seconds for 10 minutes of data (system json)
        # print(dumper(item, sort_keys=True))
        # 66 second for 10 minutes of data (system json)
        # 58 second for 10 minutes of data (simplejson)
        print(dumper(item))
    print("{0} records written".format(i), file=stderr)


if __name__ == '__main__':
    main()
