import os

basedir = os.path.abspath(os.path.dirname(__file__))


def generate_database_url():
    ENGINE = os.environ.get('DATABASE_ENGINE')
    NAME = os.environ.get('DATABASE_NAME')
    USER = os.environ.get('DATABASE_USER')
    PASSWORD = os.environ.get('DATABASE_PASSWORD')
    HOST = os.environ.get('DATABASE_HOST')
    PORT = os.environ.get('DATABASE_PORT')

    return f"{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

class Config:
    DEBUG = os.environ.get("DEBUG", False).lower() == "true"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI =generate_database_url() + "/test_database"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = generate_database_url()
    DEBUG = os.environ.get("DEBUG", False).lower() == "true"
    TESTING = False
