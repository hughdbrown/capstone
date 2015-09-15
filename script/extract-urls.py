"""
Usage:
  02-extract-urls --key=<KEY>

Options:
  -h --help              Show this screen.
  --key=<KEY>            Key to select on in JSON file.
"""
from __future__ import print_function, absolute_import, division

from sys import stdin, stderr
from collections import Counter
from operator import itemgetter

from docopt import docopt

from utils import stdin_reader


def main(key):
    key_fn = itemgetter(1)
    c = Counter(d[key] for d in stdin_reader(stdin) if key in d)
    for k, v in sorted(c.items(), key=key_fn, reverse=True):
        print("{0}, {1}".format(k, v))


if __name__ == '__main__':
    arguments = docopt(__doc__, help=True, version=None, options_first=True)
    key = arguments['--key']
    main(key)
