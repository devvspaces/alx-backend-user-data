#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

AUTH_TYPE = getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def bef_req():
    """
    Filter each request before it's handled by the proper route
    If the request requires authentication, the method will check for
    the presence of an Authorization header and the validity of the
    credentials.
    """
    if auth is None:
        pass
    else:
        excluded = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/'
        ]
        if auth.require_auth(request.path, excluded):
            if auth.authorization_header(request) is None:
                abort(401, description="Unauthorized")
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """ 404 error handler
    This function should return a JSON-formatted 404 status code response.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Request unauthorized handler
    This function should return a JSON-formatted 401 status code response.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Request forbidden handler
    This function should return a JSON-formatted 403 status code response.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    port = getenv("API_PORT", "5000")
    host = getenv("API_HOST", "0.0.0.0")
    app.run(host=host, port=port)
