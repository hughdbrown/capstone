#!/usr/bin/env python
"""
The second step in the project involved figuring out the most commonly hit URLs
for each data file.
"""
from __future__ import print_function, absolute_import, division

from sys import stderr
import os
import os.path
from csv import DictReader
from collections import Counter
from operator import itemgetter

FIELDNAMES = ["filename", "count"]

def csvfiles():
    """
    Get the names of the .csv files in the current directory
    """
    for filename in os.listdir('hits-csv/'):
        if os.path.splitext(filename)[1] == '.csv':
            yield filename

def append_to_counter(c, filename):
    """
    Add counts from the named CSV file
    """
    with open(filename) as f:
        print(filename, file=stderr)
        reader = DictReader(f, fieldnames=FIELDNAMES)
        for row in reader:
            c[row["filename"]] += int(row["count"])
    

def main():
    """
    Create a Counter that aggregates counts from multiple CSV files
    """
    c = Counter()
    for filename in csvfiles():
        append_to_counter(c, filename)
    for key, value in sorted(c.items(), reverse=True, key=itemgetter(1)):
        print("{0}, {1}".format(key, value))


if __name__ == '__main__':
    main()
