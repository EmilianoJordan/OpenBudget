"""
Created: 2/3/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask import url_for, g
from flask_restful import Resource, reqparse, fields, marshal_with
from sqlalchemy.orm.session import sessionmaker
from werkzeug.exceptions import BadRequest

from budgeting.models import User, Email
from budgeting.app import db
from .errors import bad_request, not_found
from . import api


email_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'confirmed': fields.Boolean
}
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'default_email': fields.String,
    'emails': fields.List(fields.Nested(email_fields)),
    'confirmed': fields.Boolean
}


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
    @marshal_with(user_fields)
    def get(uid):
        """
        Return the queried user.

        :param uid:
        :type uid:
        :return:
        :rtype:
        """
        if g.current_user.id == uid:
            return g.current_user.to_dict()
        return not_found('User not found')

    def put(self, uid):

        # Validate the user to be edited is the same as the authenticated user.
        if (uid != g.current_user.id
                and not g.current_user.employee
                and not g.current_user.employee_admin):
            bad_request("Unable to modify a user other than the currently logged in user.")

        if uid == g.current_user.id:
            u = g.current_user
        else:
            u: User = User.query.filter_by(id=uid).first()

        try:
            data = self.rparse.parse_args()
        except BadRequest as e:
            bad_request(' '.join([v for k, v in e.data['message'].items()]))

        if data['email'] is not None and u.email != data['email']:
            u.send_confirm_account()
            u.confirmed = False
            u.email = data['email']

        [setattr(u, k, v) for k, v in data.items() if k != 'email' and v is not None]

        db.session.commit()

        return '', 204

    def delete(self, uid):

        if (uid != g.current_user.id
                and not g.current_user.employee
                and not g.current_user.employee_admin):
            bad_request("Unable to DELETE a user other than the currently logged in user.")

        if uid == g.current_user.id:
            u = g.current_user

        else:
            u: User = User.query.filter_by(id=uid).first()

            if u is None:
                not_found('User not Found.')

        # Need to make sure that the object is not bound to any other sessions or else the
        # db.session.delete() call will fail.
        session = sessionmaker().object_session(u)
        if session is not None:
            session.expunge(u)

        del g.current_user
        db.session.delete(u)
        db.session.commit()

        return '', 204


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
            'users': [u.to_dict() for u in users.items],
        }


class UserPost(Resource):
    """
    This class is for posting new users.

    @TODO need to add the return path to the user settings and put methods
    """
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
        # user.emails.append(Email(user.email))
        db.session.add(user)
        db.session.commit()
        assert len(user.emails) == 1
        user.send_confirm_account()
        return {'email': user.email}, 201


class UserVerify(Resource):
    """
    Verifies codes that are sent to the user's email.
    """
    def get(self, uid, code):

        u, data = User.verify_url_token(code)

        if u is None or u.id != uid:
            bad_request('Could Not verify the user.')

        u.confirmed = True
        [setattr(e, 'confirmed', True) for e in u.emails if e.email == u.email]
        db.session.commit()
        return


api.add_resource(UserAPI, '/user/<int:uid>', endpoint='user')
api.add_resource(UserVerify, '/user/<int:uid>/verify/<code>', endpoint='user_verify')
api.add_resource(UserListAPI, '/users/<int:page>', endpoint='user_list')
api.add_resource(UserPost, '/user', endpoint='user_post')