"""
Created: 1/22/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask import Blueprint, jsonify
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from .auth import auth
from . import users, errors


@api_bp.route('/')
def home_page():
    return jsonify({'hello':'world'})