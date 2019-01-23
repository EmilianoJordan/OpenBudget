import itsdangerous
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'GsZrIyJMqZFZ5FR1hrQSiUJqspSKe7nt5eiCa7LbGXpQ46m9u9nbh70eZPz0'
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev.sqlite')


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://' + os.path.join(basedir, 'test.sqlite')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)


class Config:
    DEV = DevelopmentConfig
    TEST = TestingConfig
    PROD = ProductionConfig
    DEFAULT = DevelopmentConfig

    CONFIG_KEYS = [
        'SECRET_KEY',
        'DEBUG',
        'TESTING',
        'SSL_REDIRECT',
        'SQLALCHEMY_TRACK_MODIFICATIONS',
        'SQLALCHEMY_RECORD_QUERIES',
        'SQLALCHEMY_DATABASE_URI'
    ]

    CONFIG_FILE = os.path.join(basedir, 'config.cfg')

    def __getitem__(self, item: str):

        item = item.upper()

        if hasattr(self, item):
            config_cls = getattr(self, item)
            self._init_config(item, config_cls)

        # @TODO run config prompt for new config values

    @staticmethod
    def _init_config(config_name, config_class):

