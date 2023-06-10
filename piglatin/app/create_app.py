from flask import Flask
from app.extensions import db, migrate, ma, CORS, mail
from app.config import ProductionConfig


def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        ma.init_app(app)
        CORS(app)
        mail.init_app(app)

        register_blueprints(app)

    return app

def register_blueprints(app):
    from app.routes import bp

    app.register_blueprint(bp)
