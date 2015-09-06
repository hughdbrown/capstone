#!/usr/bin/env python
"""
The second step in the project involved figuring out the most commonly hit URLs
for each data file.
"""
from __future__ import print_function, absolute_import, division

import simplejson

from utils import stdin_reader


def main():
    """
    Create a dict to store the mapping.
    *g : bitly global hash identifier
    *u : Long URL

    Need to write this out as JSON because there are no punctuation marks I can find that
    do not also appear in the long urls -- meaning that there is nothing obvious to use as
    a split character in a CSV.
    """
    c = {d["g"]: d["u"] for d in stdin_reader()}
    print(simplejson.dumps(c))


if __name__ == '__main__':
    main()
