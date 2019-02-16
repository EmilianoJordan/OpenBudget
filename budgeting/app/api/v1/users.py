"""
Created: 2/3/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask import jsonify, request, url_for, g
from flask_restful import Resource, reqparse, fields, marshal_with
from werkzeug.exceptions import BadRequest

from budgeting.models import User
from budgeting.app import db
from .errors import bad_request, not_found
from . import api


class UserAPI(Resource):

    @staticmethod
    def get(u_id):
        user = User.query.get_or_404(u_id)
        if g.current_user == user:
            return jsonify(user.to_dict())
        return not_found()

    def put(self, u_id):
        pass

    def delete(self, u_id):
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
            'next':
                url_for('api.user_list', page=page+1, _external=True) if users.has_next else '',
            'prev':
                url_for('api.user_list', page=page-1, _external=True) if users.has_prev else '',
            'users': users.items,
        }


class UserPost(Resource):

    def __init__(self):
        self.rparse = reqparse.RequestParser(bundle_errors=True)
        self.rparse.add_argument('email', type=str, required=True,
                                 help='No Email Provided.')
        self.rparse.add_argument('password', type=str, required=True,
                                 help='No Password Provided.')
        self.rparse.add_argument('username', type=str, required=True,
                                 help='No Username Provided.')

    @staticmethod
    def get():
        r = UserListAPI()
        return r.get(1)

    def post(self):

        try:
            data = self.rparse.parse_args()
        except BadRequest as e:
            bad_request(' '.join([v for k, v in e.data['message'].items()]))

        if User.query.filter_by(email=data['email']).first():
            return {'email': data['email']}, 201

        user = User(**data)
        db.session.add(user)
        db.session.commit()
        user.send_confirm_account_email()
        return {'email': user.email}, 201


class UserVerify(Resource):

    def get(self, code, u_id):
        user: User = User.verify_url_token(code)

        if user is None:
            bad_request("User Token Expired.")

        if user.id != u_id:
            bad_request("Invalid User Token")

        return

# api.add_resource(UserVerify, '/user/<int:u_id>/verify/<code>', endpoint='user_verify')
api.add_resource(UserAPI, '/user/<int:u_id>', endpoint='user')
api.add_resource(UserListAPI, '/users/<int:page>', endpoint='user_list')
api.add_resource(UserPost, '/user', endpoint='user_post')
