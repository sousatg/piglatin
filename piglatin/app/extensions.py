from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()
jwt = JWTManager()