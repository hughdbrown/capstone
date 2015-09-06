#!/usr/bin/env python
"""
The second step in the project involved figuring out the most commonly hit URLs
for each data file.
"""
from __future__ import print_function, absolute_import, division

from . import stdin_reader


def main():
    """
    Create a dict to store the mapping.
    *g : bitly global hash identifier
    *u : Long URL
    """
    c = {d["g"]: d["u"] for d in stdin_reader()}
    assert not any(',' in value for value in c.values())
    for key, value in sorted(c.items()):
        print("{0}, {1}".format(key, value))


if __name__ == '__main__':
    main()
