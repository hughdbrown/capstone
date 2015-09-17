from __future__ import absolute_import, print_function

import os
import os.path
from csv import DictReader

FIELDNAMES1 = ('timezone', 'count')
FIELDNAMES2 = ('timezone', 'offset1', 'offset2')


def main():
    rootdir = "timezones"
    d = set()
    for filename in os.listdir(rootdir):
        fullpath = os.path.join(rootdir, filename)
        with open(fullpath, "rb") as f:
            for row in DictReader(f, fieldnames=FIELDNAMES1):
                d.add(row['timezone'])
    return d


def load_timezones():
    e = set()
    with open("../js/timezone-map.csv", "rb") as f:
        for row in DictReader(f, fieldnames=FIELDNAMES2):
            e.add(row['timezone'])
    return e


if __name__ == '__main__':
    d = main()
    e = load_timezones()
    print(sorted(d - e))
    # ['Africa/Bissau', 'Africa/Porto-Novo', 'America/Port-au-Prince', 'America/Rio_Branco', 'US/Samoa']
