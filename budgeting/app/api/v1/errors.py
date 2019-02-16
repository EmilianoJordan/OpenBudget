"""
Created: 2/3/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask_restful import abort


def bad_request(message):
    return abort(400, message=message)


def unauthorized(message):
    return abort(401, message=message)


def forbidden(message):
    return abort(403, message=message)


def not_found(message=None):
    if message is None:
        message = 'Page Not Found'
    return abort(404, message=message)
