"""
Decorator for crossdomain import
http://flask.pocoo.org/snippets/56/
"""

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    """
    Method to manage cross-domain HTTP headers
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """
        Get the allowed methods in the header
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(func_to_decorate):
        """
        Create a decorator
        """
        def wrapped_function(*args, **kwargs):
            """
            Wrap the function
            """
            options_request = request.method == 'OPTIONS'
            if automatic_options and options_request:
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(func_to_decorate(*args, **kwargs))

            if attach_to_all or options_request:
                pairs = (
                    ('Access-Control-Allow-Origin', origin),
                    ('Access-Control-Allow-Methods', get_methods()),
                    ('Access-Control-Max-Age', str(max_age)),
                    ('Access-Control-Allow-Headers', headers),
                )
                access_headers = {k: v for k, v in pairs if v is not None}
                resp.headers.extend(access_headers)
            return resp

        func_to_decorate.provide_automatic_options = False
        return update_wrapper(wrapped_function, func_to_decorate)
    return decorator
