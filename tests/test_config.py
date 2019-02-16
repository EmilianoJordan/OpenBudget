"""
Created: 1/26/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from os import environ
from pathlib import Path
import sys


class TestConfig:
    def test_app_is_base_config(self):
        environ['FLASK_CONFIG'] = 'base'

        from budgeting.ob import app

        assert app.env == 'production'
        assert not app.config['DEBUG']
        assert not app.config['TESTING']
        assert app.config['SECRET_KEY']
        assert isinstance(app.config['SECRET_KEY'], bytes)
        assert Path(app.config['SQLALCHEMY_DATABASE_URI']).name == 'base_db.sqlite'

        del sys.modules['budgeting.ob']  # Clean up module import for any further testing.

    def test_app_is_development_config(self):
        environ['FLASK_CONFIG'] = 'dev'

        from budgeting.ob import app

        assert app.env == 'development'
        assert app.config['DEBUG']
        assert not app.config['TESTING']
        assert app.config['SECRET_KEY']
        assert isinstance(app.config['SECRET_KEY'], bytes)
        assert Path(app.config['SQLALCHEMY_DATABASE_URI']).name == 'dev_db.sqlite'

        del sys.modules['budgeting.ob']  # Clean up module import for any further testing.

    def test_app_is_test_config(self):
        environ['FLASK_CONFIG'] = 'test'

        from budgeting.ob import app

        assert app.env == 'development'
        assert app.config['DEBUG']
        assert app.config['TESTING']
        assert app.config['SECRET_KEY']
        assert isinstance(app.config['SECRET_KEY'], bytes)
        assert app.config['SQLALCHEMY_DATABASE_URI'] is None

        del sys.modules['budgeting.ob']  # Clean up module import for any further testing.

