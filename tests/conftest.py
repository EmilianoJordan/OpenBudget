"""
Created: 2/6/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import pytest

from budgeting.app import create_app, db as database


@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    app.app_context().push()
    return app


@pytest.fixture(scope='session')
def db(app):
    database.create_all()
    yield database
    database.drop_all()



