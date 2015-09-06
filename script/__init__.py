"""
Shared constants and code
"""
import simplejson
from sys import stdin
import os
import os.path


# See schema.txt for explanation of columns
COLUMNS = set(['a', 'c', 'ckw', 'cy', 'dp', 'g', 'h', 'kw', 'mc', 'nk', 'pp', 't', 'tz', 'u'])


def stdin_reader(f=stdin):
    """
    Read JSON objects from file, one per line.
    Yield loaded diciotnaries
    """
    loader = simplejson.loads
    for line in f:
        yield loader(line)


def filter_files_by_ext(directory, ext):
    """
    Get the names of the .csv files in the current directory
    """
    for filename in os.listdir(directory):
        if os.path.splitext(filename)[1] == ext:
            yield filename

