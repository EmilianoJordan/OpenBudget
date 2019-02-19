"""
Created: 2/6/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from base64 import b64encode
import json
from os import environ
import pytest
import sys

from budgeting.app import create_app, db as database
from budgeting.models import User
from budgeting.models.permissions import BasicUserRoles

from tests.helpers import fake


@pytest.fixture(scope='session')
def app():
    # Clean up module space incase someone else didn't clean up after themselves.
    if 'budgeting.app' in sys.modules:
        del sys.modules['budgeting.app']

    environ['FLASK_CONFIG'] = 'test'

    from budgeting.ob import app

    with app.app_context():
        yield app

    # On a session level fixture this isn't needed but if this is ever changed to have less scope
    # I want to future proof it a bit.
    del sys.modules['budgeting.ob']  # Clean up module import for any further testing.


@pytest.fixture(scope='session')
def db(app, tmpdir_factory):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
            'sqlite:///'
            + str(tmpdir_factory.getbasetemp().join('test_db.sqlite'))
    )
    database.create_all()
    yield database
    database.session.close()
    database.drop_all()

# @pytest.fixture(scope='session')


@pytest.fixture(scope='session')
def client(app, db):
    return app.test_client()


@pytest.fixture
def user(user_generator, confirmed=True):
    return user_generator(1, confirmed=confirmed)[0]


@pytest.fixture
def employee(user_generator):
    return user_generator(1, permissions=BasicUserRoles.EMPLOYEE)[0]


@pytest.fixture
def employee_admin(user_generator):
    return user_generator(1, permissions=BasicUserRoles.EMPLOYEE_SUPER_ADMIN)[0]


@pytest.fixture
def user_generator(db):
    _user_dict = {}

    def _create_users(num, confirmed=True, permissions=BasicUserRoles.USER):

        key = json.dumps(permissions)

        # This resets the DB with all the faked user information.
        limit = (num if num < len(_user_dict.setdefault(key, [])) else len(_user_dict[key]))
        for user in _user_dict[key][:limit]:
            user_model: User = User.query.filter_by(email=user['email'])
            [setattr(user_model, k, v) for k, v in user.items()]
            user_model.confirmed = confirmed
            user_model.permissions = permissions

        # Create new users if needed.
        while len(_user_dict[key]) < num:
            user = fake.ob_user()
            user['permissions'] = permissions
            user_model = User(**user)
            user_model.confirmed = confirmed
            db.session.add(user_model)
            _user_dict.setdefault(key, []).append(user)



        db.session.commit()

        return _user_dict[key][:num]

    yield _create_users

    for k in _user_dict:
        db.session.query(User).filter(User.email.in_([x['email'] for x in _user_dict[k]]))


@pytest.fixture(scope='session')
def json_headers():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


@pytest.fixture(scope='session')
def get_auth_headers():
    def _gen_auth_headers(user):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': ('Basic ' + b64encode(
                (user['email'] + ':' + user['password']).encode('utf-8')).decode('utf-8'))
        }

    return _gen_auth_headers
