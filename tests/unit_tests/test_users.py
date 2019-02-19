"""
Created: 2/6/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer as Serializer
import json
import pytest
from sqlalchemy.exc import IntegrityError

from budgeting.models import User
from budgeting.models.permissions import BasicUserRoles, UserPermissions

from tests.helpers import fake


@pytest.mark.user
class TestUserModel:

    def test_user_initialization(self):
        u = fake.ob_user()
        u1 = User(**u)

        assert u1.email == u['email']
        assert u1.username == u['username']
        assert u1.password_hash != u['password']

        with pytest.raises(AttributeError):
            u1.password

        assert u1.verify_password(u['password'])

    def test_user_db_insert(self, db):
        """
        Verify that the user is being properly inserted into the db.
        :param db:
        :type db:
        :return:
        :rtype:
        """
        u = fake.ob_user()
        u1 = User(**u)
        assert u1.id is None
        db.session.add(u1)
        db.session.commit()
        assert isinstance(u1.id, int)

    def test_user_db_uniqueness(self, db):
        u = fake.ob_user()
        u1 = User(**u)
        db.session.add(u1)
        db.session.commit()

        u2 = User(**u)
        db.session.add(u2)

        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()
        db.session.commit()

    def test_user_is_user(self, user):
        assert user['permissions'] == BasicUserRoles.USER
        u: User = User.query.filter_by(email=user['email']).one()
        assert json.loads(u._permissions) == BasicUserRoles.USER

        for p in BasicUserRoles.USER:
            assert u.has_permission(p)

        assert not u.has_permission(UserPermissions.EMPLOYEE)
        assert not u.has_permission(UserPermissions.EMPLOYEE_ADMIN)

        assert not u.employee
        assert not u.employee_admin

    def test_employee_is_employee(self, employee):
        assert employee['permissions'] == BasicUserRoles.EMPLOYEE
        u = User.query.filter_by(email=employee['email']).one()
        assert json.loads(u._permissions) == BasicUserRoles.EMPLOYEE

        for p in BasicUserRoles.EMPLOYEE:
            assert u.has_permission(p)

        assert not u.has_permission(UserPermissions.EMPLOYEE_ADMIN)

        assert u.employee
        assert not u.employee_admin

    def test_employee_admin_is_employee_admin(self, employee_admin):
        assert employee_admin['permissions'] == BasicUserRoles.EMPLOYEE_SUPER_ADMIN
        u = User.query.filter_by(email=employee_admin['email']).one()
        assert json.loads(u._permissions) == BasicUserRoles.EMPLOYEE_SUPER_ADMIN

        for p in BasicUserRoles.EMPLOYEE_SUPER_ADMIN:
            assert u.has_permission(p)

        assert u.employee
        assert u.employee_admin

    def test_user_auth_token(self, user):
        u: User = User.query.filter_by(email=user['email']).one()
        token = u.generate_auth_token()

        u_verification = User.verify_auth_token(token)

        assert u_verification.id == u.id
        assert u_verification.email == u.email

    def test_user_url_token(self, user):
        u: User = User.query.filter_by(email=user['email']).one()

        token = u.generate_url_token('verify_email')

        u_verification, action = User.verify_url_token(token)

        assert u_verification.id == u.id
        assert u_verification.email == u.email
        assert action == 'verify_email'

    def test_user_bad_auth_token(self, app, user):

        u: User = User.query.filter_by(email=user['email']).one()
        s = Serializer(app.config['SECRET_KEY'])
        token = s.dumps({'spmedatya': 1})
        u_verification = User.verify_auth_token(token)

        assert u_verification is None

        u_verification = User.verify_auth_token('asdkgjhl')

        assert u_verification is None

    def test_user_bad_url_token(self, app, user):

        u: User = User.query.filter_by(email=user['email']).one()
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = s.dumps({'spmedatya': 1})
        u_verification, action = User.verify_url_token(token)

        assert u_verification is None

        u_verification, action = User.verify_url_token('asdkgjhl')

        assert u_verification is None
