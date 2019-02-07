"""
Created: 1/26/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from pathlib import Path

import pytest

from budgeting.app import create_app


class TestBaseConfig:
    def setup_class(self):
        self.app = create_app('base')

    def test_app_is_base_config(self):
        assert self.app.env == 'production'
        assert not self.app.config['DEBUG']
        assert not self.app.config['TESTING']
        assert self.app.config['SECRET_KEY']
        assert isinstance(self.app.config['SECRET_KEY'], bytes)
        assert Path(self.app.config['SQLALCHEMY_DATABASE_URI']).name == 'base_db.sqlite'


class TestDevConfig:
    def setup_class(self):
        self.app = create_app('dev')

    def test_app_is_development_config(self):
        assert self.app.env == 'development'
        assert self.app.config['DEBUG']
        assert not self.app.config['TESTING']
        assert self.app.config['SECRET_KEY']
        assert isinstance(self.app.config['SECRET_KEY'], bytes)
        assert Path(self.app.config['SQLALCHEMY_DATABASE_URI']).name == 'dev_db.sqlite'


class TestTestConfig:
    def setup_class(self):
        self.app = create_app('test')

    def test_app_is_test_config(self):
        assert self.app.env == 'development'
        assert self.app.config['DEBUG']
        assert self.app.config['TESTING']
        assert self.app.config['SECRET_KEY']
        assert isinstance(self.app.config['SECRET_KEY'], bytes)
        assert self.app.config['SQLALCHEMY_DATABASE_URI'] is None
