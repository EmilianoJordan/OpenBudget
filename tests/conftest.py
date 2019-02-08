"""
Created: 2/6/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import pytest

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
def user(db):
    user = fake.ob_user()
    user_model = User(**user)
    user_model.confirmed = True
    db.session.add(user_model)
    db.session.commit()
    return user
