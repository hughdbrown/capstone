#!/usr/bin/env python
"""

Usage:
  url-server --filename=<filename>

Options:
  -h --help              Show this screen.
  --filename=<filename>  JSON file of short_url/long_url to load.

"""
from __future__ import print_function, absolute_import
from sys import stderr
import Queue

import simplejson

from docopt import docopt

from flask import Flask, jsonify
app = Flask(__name__)

DATA = Queue.Queue()


def load_data(filename):
    global DATA
    print("Opening JSON {0}".format(filename), file=stderr)
    # "../data//map-urls-aggregated.json"
    with open(filename) as f:
        print("Reading JSON", file=stderr)
        filedata = f.read()
        d = simplejson.loads(filedata)
        filedata = None
        print("Shuffling {0} short_url/long_url pairs".format(len(d)), file=stderr)
        for item in d.items():
            DATA.put(item)
        d = None


@app.route('/')
def get_url():
    try:
        short_url, long_url = DATA.get(block=False)
        print("{0} remaining".format(DATA.qsize()))
        d = {'short_url': short_url, 'long_url': long_url}
    except Queue.Empty:
        d = {}
    return jsonify(d)


if __name__ == '__main__':
    arguments = docopt(__doc__, help=True, version=None, options_first=True)
    filename = arguments["--filename"]
    load_data(filename)
    app.run()
