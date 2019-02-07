"""
Created: 1/22/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('apiv1', __name__)
api = Api(api_bp)

from .auth import auth
from . import users, errors


@api_bp.route('/')
def home_page():
    return {'hello':'world'}