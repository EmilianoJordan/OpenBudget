"""
Created: 2/3/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask import jsonify, request, url_for, g
from flask_restful import Resource, reqparse, fields, marshal_with

from budgeting.models import User
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


user_fields = {
    'id': fields.Integer,
    'username': fields.String
}
user_list = {
    'page': fields.Integer,
    'per_page': fields.Integer,
    'count': fields.Integer,
    'next': fields.String,
    'prev': fields.String,
    'users': fields.List(fields.Nested(user_fields))
}


class UserListAPI(Resource):

    @marshal_with(user_list)
    def get(self, page):
        if not g.current_user.employee and not g.current_user.employee_admin:
            return not_found()

        users = User.query.paginate(page, 20)
        return {
            'page': page,
            'per_page': 20,
            'count': users.total,
            'next': url_for('api.user_list', page=page+1) if users.has_next else False,
            'prev': url_for('api.user_list', page=page-1) if users.has_next else False,
            'users': users.items,
        }


class UserPost(Resource):

    def __init__(self):
        self.rparse = reqparse.RequestParser()
        self.rparse.add_argument('email', type=str,
                                 help='No Email Provided')
        self.rparse.add_argument('password', type=str,
                                 help='No Password Provided')
        self.rparse.add_argument('username', type=str,
                                 help='No Username Provided')

    def get(self):
        r = UserListAPI()
        return r.get(1)

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
api.add_resource(UserListAPI, '/users/<int:page>', endpoint='user_list')
api.add_resource(UserPost, '/user', endpoint='user_post')
