#!/usr/bin/env python
"""
Convert a series of JSON objects, one per line in a file,
to a real JSON object. Reads from stdin, writes to stdout.
"""
from __future__ import print_function, absolute_import

import simplejson

from utils import stdin_reader


def main():
    all_objs = list(stdin_reader())
    print(simplejson.dumps(all_objs))


if __name__ == '__main__':
    main()
