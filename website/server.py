"""
Usage: server_main [--port=<PORT>]

Arguments:
    PORT        optional port number

Options:
    -h --help         Show this screen.
    --port=<PORT>     Optional port number [default: 8000].
"""
from __future__ import absolute_import, print_function

from flask import Flask, send_from_directory
from docopt import docopt


app = Flask(__name__, static_url_path='')

import simplejson

from crossdomain import crossdomain


@app.route('/timestamp', methods=['GET'])
@crossdomain(origin='*')
def timestamp_data():
    """
    Respond to Flask request for /timestamp
    """
    # filename = "urlhist-timestamp.json"
    filename = "urlhist-timestamp-country.json"
    try:
        return send_from_directory("static", filename, mimetype="application/json")
    except Exception as exc:
        print(str(exc))
        # logging.exception(exc, log_type=__name__)
        return simplejson.dumps([])


@app.route('/')
def html():
    filename = "jenkins_analytics.html"
    return send_from_directory("static", filename)


def main():
    options = docopt(__doc__)
    port = int(options["--port"])
    app.run(port=port)


if __name__ == '__main__':
    main()
