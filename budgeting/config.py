import itsdangerous
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or False
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
            os.environ.get('DEV_DATABASE_URL')
            or 'sqlite:///' + os.path.join(basedir, 'base_db.sqlite'))

    @staticmethod
    def init_app(app):
        pass

class DevConfig(BaseConfig):


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)

config = {
    'base': BaseConfig,

}