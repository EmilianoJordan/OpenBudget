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
def client(app):
    return app.test_client()


@pytest.fixture(scope='class')
def user(user_generator):
    return user_generator(1)[0]


@pytest.fixture(scope='class')
def user_generator(db):

    _user_list = []

    def _create_users(num, confirmed=True):

        while len(_user_list) < num:
            user = fake.ob_user()
            user_model = User(**user)
            user_model.confirmed = confirmed
            db.session.add(user_model)
            db.session.commit()
            _user_list.append(user)

        return _user_list[:num]

    yield _create_users

    for user in _user_list:
        db.session.query(User).filter(User.email.in_([x['email'] for x in _user_list]))


@pytest.fixture(scope='session')
def get_auth_headers():

    def _gen_auth_headers(user):
        headers = {
            'Authorization': 'Basic ' + b64encode(
                (user['email'] + ':' + user['password']).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        return headers

    return _gen_auth_headers