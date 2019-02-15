"""
Created: 2/6/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import pytest
from base64 import b64encode
from budgeting.app import create_app, db as database
from budgeting.models import User
from budgeting.models.permissions import BasicUserRoles
import json

from tests.helpers import fake


@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    app.app_context().push()
    return app


@pytest.fixture(scope='session')
def db(app, tmpdir_factory):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
            'sqlite:///'
            + str(tmpdir_factory.getbasetemp().join('test_db.sqlite'))
    )
    database.create_all()
    yield database
    database.drop_all()

@pytest.fixture(scope='session')


@pytest.fixture(scope='session')
def client(app, db):
    return app.test_client()


@pytest.fixture(scope='class')
def user(user_generator, confirmed=True):
    return user_generator(1, confirmed=confirmed)[0]


@pytest.fixture(scope='class')
def employee(user_generator):
    return user_generator(1, permissions=BasicUserRoles.EMPLOYEE)[0]


@pytest.fixture(scope='class')
def employee_admin(user_generator):
    return user_generator(1, permissions=BasicUserRoles.EMPLOYEE_SUPER_ADMIN)[0]


@pytest.fixture(scope='class')
def user_generator(db):

    _user_dict = {}

    def _create_users(num, confirmed=True, permissions=BasicUserRoles.USER):

        key = json.dumps(permissions)

        while len(_user_dict.setdefault(key, [])) < num:
            user = fake.ob_user()
            user['permissions'] = permissions
            user_model = User(**user)
            user_model.confirmed = confirmed
            db.session.add(user_model)
            db.session.commit()
            _user_dict.setdefault(key, []).append(user)

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
