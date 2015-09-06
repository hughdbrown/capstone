"""
The second step in the project involved figuring out the most commonly hit URLs
for each data file.
"""
from __future__ import print_function, absolute_import, division

from sys import stdin, stderr
from collections import Counter
from operator import itemgetter

from . import stdin_reader


def main():
    key_fn = itemgetter(1)
    c = Counter(d['g'] for d in stdin_reader(stdin))
    for k, v in sorted(c.items(), key=key_fn, reverse=True):
        print("{0}, {1}".format(k, v))


if __name__ == '__main__':
    main()
