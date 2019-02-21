"""
Created: 2/3/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask import jsonify, request, url_for, g
from flask_restful import Resource, reqparse, fields, marshal_with
from sqlalchemy import inspect, inspection
from werkzeug.exceptions import BadRequest

from budgeting.models import User, Email
from budgeting.app import db
from .errors import bad_request, not_found
from . import api


class UserAPI(Resource):

    def __init__(self):
        self.rparse = reqparse.RequestParser(bundle_errors=True)
        self.rparse.add_argument('email', type=str,
                                 help='No Email Provided.')
        self.rparse.add_argument('password', type=str,
                                 help='No Password Provided.')
        self.rparse.add_argument('username', type=str,
                                 help='No Username Provided.')

    @staticmethod
    def get(uid):
        user = User.query.get_or_404(uid)
        if g.current_user == user:
            return jsonify(user.to_dict())
        return not_found()

    def put(self, uid):

        u: User = User.query.filter_by(id=uid).first()

        # Validate the user to be edited is the same as the authenticated user.
        if (u != g.current_user
                and not g.current_user.employee
                and not g.current_user.employee_admin):
            bad_request("Unable to modify a user other than the currently logged in user.")

        try:
            data = self.rparse.parse_args()
        except BadRequest as e:
            bad_request(' '.join([v for k, v in e.data['message'].items()]))

        if data['email'] is not None and u.email != data['email']:
            u.send_confirm_account_email()
            u.confirmed = False
            u.email = data['email']

        [setattr(u, k, v) for k, v in data.items() if k != 'email' and v is not None]

        db.session.commit()

        return '', 204

    def delete(self, uid):
        u = User.query.filter_by(id=uid).first()

        if u is None:
            not_found('User not Found.')

        if (u != g.current_user
                and not g.current_user.employee
                and not g.current_user.employee_admin):
            bad_request("Unable to DELETE a user other than the currently logged in user.")

        User.query.filter_by(id=uid).delete()
        db.session.commit()

        return '', 204


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
                url_for('api.user_list', page=page + 1, _external=True) if users.has_next else '',
            'prev':
                url_for('api.user_list', page=page - 1, _external=True) if users.has_prev else '',
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

        e: Email = Email.query.filter_by(email=data['email']).first()
        if e:
            # @TODO need to send already exists email
            return {'email': data['email']}, 201

        user = User(**data)
        user.emails.append(Email(data['email']))
        db.session.add(user)
        db.session.commit()

        user.send_confirm_account_email()
        return {'email': user.email}, 201


class UserVerify(Resource):

    def get(self, uid, code):
        u, data = User.verify_url_token(code)

        if u is not None and u.id == uid:
            u.confirmed = True
            db.session.commit()
            return

        bad_request('Could Not verify the user.')


api.add_resource(UserAPI, '/user/<int:uid>', endpoint='user')
api.add_resource(UserVerify, '/user/<int:uid>/verify/<code>', endpoint='user_verify')
api.add_resource(UserListAPI, '/users/<int:page>', endpoint='user_list')
api.add_resource(UserPost, '/user', endpoint='user_post')
