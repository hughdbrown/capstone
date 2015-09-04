"""
The second step in the project involved figuring out the most commonly hit URLs
for each data file.
"""
from __future__ import print_function, absolute_import, division

from sys import stdin, stderr
import simplejson
from collections import Counter
from operator import itemgetter

# See schema.txt for explanation of columns
COLUMNS = set(['a', 'c', 'ckw', 'cy', 'dp', 'g', 'h', 'kw', 'mc', 'nk', 'pp', 't', 'tz', 'u'])


def stdin_reader(f):
    loader = simplejson.loads
    for line in f:
        yield loader(line)


def main():
    key_fn = itemgetter(1)
    c = Counter(d['g'] for d in stdin_reader(stdin))
    for k, v in sorted(c.items(), key=key_fn, reverse=True):
        print("{0}, {1}".format(k, v))


if __name__ == '__main__':
    main()
