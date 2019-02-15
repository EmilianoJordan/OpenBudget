"""
Created: 1/21/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import json
from typing import List

from flask import current_app, url_for, render_template
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature,
                          URLSafeTimedSerializer as URLSerializer, SignatureExpired)
from sqlalchemy import event
from werkzeug.security import generate_password_hash, check_password_hash

from ..app import db
from ..app.email import send_email
from .permissions import BasicUserRoles, UserPermissions


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(264))
    confirmed = db.Column(db.Boolean, default=False)
    _permissions = db.Column(db.String, nullable=False)

    def __init__(self,
                 username=None,
                 email=None,
                 password=None,
                 confirmed=False,
                 permissions=BasicUserRoles.USER):

        self.username = username
        self.email = email
        if password:
            self.password = password
        self.confirmed = confirmed
        self._permissions = json.dumps(permissions)

    @property
    def employee(self):
        return UserPermissions.EMPLOYEE in json.loads(self._permissions)

    @property
    def employee_admin(self):
        return UserPermissions.EMPLOYEE_ADMIN in json.loads(self._permissions)

    @property
    def permissions(self):
        raise AttributeError(f"{type(self).__name__}.permissions is not readable")

    @permissions.setter
    def permissions(self, v):
        if not all((isinstance(x, int) for x in v)):
            raise ValueError(f"{type(self).__name__}.permissions is a list of integer permissions")
        self._permissions = json.dumps(v)

    @permissions.deleter
    def permissions(self):
        raise AttributeError('Cannot delete Permissions, try setting new permissions.')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def generate_url_token(self):
        s = URLSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_url_token(token, expiration=86400):
        s = URLSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(data['id'])

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(data['id'])

    def has_permission(self, p: int):
        """

        :param p: A Permission value from .permissions.UserPermissions
        :type p: int
        :rtype: bool
        """
        return p in json.loads(self._permissions)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
        }
        if include_email:
            data['email'] = self.email

        return data

    def send_confirm_account_email(self):
        send_email(
            f'{self.username} Verify You Email Address',
            [self.email],
            render_template('confirm_email.txt', user=self),
            render_template('confirm_email.html', user=self),
        )

    def send_account_exists_email(self):
        pass