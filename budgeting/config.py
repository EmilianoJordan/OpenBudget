import configparser
import os

basedir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(basedir, 'ob.cfg')

cfg = configparser.ConfigParser()
cfg.read(config_file)


class BaseConfig:
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    DEBUG = False
    TESTING = False
    OB_PASS_REQUIRED = True
    SQLALCHEMY_DATABASE_URI = (
            os.environ.get('DEV_DATABASE_URL')
            or 'sqlite:///' + os.path.join(basedir, 'base_db.sqlite'))
    OB_PASS_EXPIRES = 600

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    @classmethod
    def init_app(cls, app):
        """
        Loads values from the ob.cfg file into app.config.
        By default any values in the BaseConfig are loaded first
        and then the values from the particular class name are loaded.

        This is a replacement for something like the dotenv library.
        I chose this way to allow multiple config options in the .cfg
        file and to stick with a standard library package.

        :param app:
        :type app:
        :return:
        :rtype:
        """

        cls_name = cls.__name__
        d = {}

        config = {**cfg['BaseConfig'], **cfg.setdefault(cls_name, {})}

        for key, val in config.items():
            if key == 'secret_key':
                d[key.upper()] = val.encode()
            elif val == 'True':
                d[key.upper()] = True
            elif val == 'False':
                d[key.upper()] = None
            elif val == 'None':
                d[key.upper()] = None
            else:
                d[key.upper()] = val

        app.config.update(**d)


class DevConfig(BaseConfig):
    ENV = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    DEBUG = True
    TESTING = False
    OB_PASS_REQUIRED = False
    OB_ROOT_URL = 'http://127.0.0.1:5000/'
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'dev_db.sqlite'))


class TestConfig(BaseConfig):
    ENV = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    DEBUG = True
    TESTING = True  # This will supress emails from flask-mail as well.
    SQLALCHEMY_DATABASE_URI = None
    SERVER_NAME = '127.0.0.1:5000'


config = {
    'base': BaseConfig,
    'dev': DevConfig,
    'test': TestConfig
}
