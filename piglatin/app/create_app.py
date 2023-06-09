from flask import Flask
from app.extensions import db, migrate, ma, CORS
from app.config import ProductionConfig

import os

ENGINE = os.environ.get('DATABASE_ENGINE')
NAME = os.environ.get('DATABASE_NAME')
USER = os.environ.get('DATABASE_USER')
PASSWORD = os.environ.get('DATABASE_PASSWORD')
HOST = os.environ.get('DATABASE_HOST')
PORT = os.environ.get('DATABASE_PORT')


def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        ma.init_app(app)
        CORS(app)

        register_blueprints(app)

    return app

def register_blueprints(app):
    from app.routes import bp

    app.register_blueprint(bp)
