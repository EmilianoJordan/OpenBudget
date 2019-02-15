"""
Created: 1/21/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from functools import lru_cache

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# local import
from budgeting.config import config
from .decorators import cache_app

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@cache_app
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    db.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .api.v1 import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    from .api.v1.auth import auth

    return app
