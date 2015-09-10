from __future__ import print_function, absolute_import
from sys import stderr
import random

import simplejson

from flask import Flask, jsonify
app = Flask(__name__)


print("Opening JSON", file=stderr)
with open("../data//map-urls-aggregated.json") as f:
    print("Reading JSON", file=stderr)
    filedata = f.read()
    d = simplejson.loads(filedata)
    filedata = None
    print("Shuffling {0} short_url/long_url pairs".format(len(d)), file=stderr)
    data = list(d.items())
    d = None
    random.shuffle(data)


@app.route('/')
def get_url():
    try:
        item = data.pop()
        short_url, long_url = item
        d = {'short_url': short_url, 'long_url': long_url}
    except IndexError:
        d = {}
    return jsonify(d)


if __name__ == '__main__':
    app.run()
