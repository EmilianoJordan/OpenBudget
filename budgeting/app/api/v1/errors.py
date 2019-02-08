"""
Created: 2/3/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def _error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return _error_response(400, message)


def unauthorized(message):
    return _error_response(401, message)


def forbidden(message):
    return _error_response(403, message)


def not_found(message=None):
    if message is None:
        message = 'Page Not Found'
    return _error_response(404, message)