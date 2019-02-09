"""
Created: 2/3/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask import jsonify, request, url_for, g
from flask_restful import Resource, reqparse

from budgeting.models import User
from budgeting.app.api.v1 import api_bp
from budgeting.app import db
from .errors import bad_request, not_found
from . import api


class UserAPI(Resource):

    def get(self, id):
        user = User.query.get_or_404(id)
        if g.current_user == user:
            return jsonify(user.to_dict())
        return not_found()

    def put(self, id):
        pass

    def delete(self, id):
        pass


class UserListAPI(Resource):

    def __init__(self):

        self.rparse = reqparse.RequestParser()
        self.rparse.add_argument('email', type=str, location='json', required=True,
                                 help='No Email Provided')
        self.rparse.add_argument('password', type=str, location='json', required=True,
                                 help='No Password Provided')
        self.rparse.add_argument('username', type=str, location='json', required=True,
                                 help='No Username Provided')

    def post(self):
        data = request.get_json() or {}

        if 'username' not in data or 'email' not in data or 'password' not in data:
            return bad_request('Must include username, email and password.')

        if User.query.filter_by(email=data['email']).first():
            return bad_request('Bad email. If this is your email address check your inbox.')

        user = User()
        user.from_dict(data, new_user=True)
        db.session.add(user)
        db.session.commit()
        response = jsonify(user.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.get_user', id=user.id)
        return response


api.add_resource(UserAPI, '/user/<int:id>', endpoint='user')
api.add_resource(UserListAPI, '/user', endpoint='user_list')