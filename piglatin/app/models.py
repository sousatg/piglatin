from app.extensions import db
from datetime import datetime
import bcrypt
import uuid

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    confirmation_token = db.Column(db.String, unique=True, nullable=True, default=uuid.uuid4().hex, index=True)

    def __init__(self, email, password):
        self.set_email(email)
        self.set_password(password)
        self.confirmed = False
        self.created_at = datetime.utcnow()
        self.confirmation_token = uuid.uuid4().hex

    def set_password(self, value):
        self.password = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())

    def set_email(self, value):
        self.email = value

    def get_email(self):
        return self.email
    
    def get_confirmation_token(self):
        return self.confirmation_token
    
    def confirm(self):
        self.confirmed = True
        self.confirmed_at = datetime.utcnow()
        self.confirmation_token = None
