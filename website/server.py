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
import simplejson

from crossdomain import crossdomain

app = Flask(__name__, static_url_path='')


@app.route('/data/<filename>', methods=['GET'])
@crossdomain(origin='*')
def retrieve_data(filename):
    """
    Respond to Flask request for /data
    """
    try:
        print("Getting {0}".format(filename))
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
