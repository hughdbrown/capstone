#!/usr/bin/env python
"""
The second step in the project involved figuring out the most commonly hit URLs
for each data file.
"""
from __future__ import print_function, absolute_import, division

from sys import stderr

import simplejson

from utils import coalesce_jsonfiles


def main():
    dest = coalesce_jsonfiles("map-urls-json/", ".json")
    print(simplejson.dumps(dest))


if __name__ == '__main__':
    main()
