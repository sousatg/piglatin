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
        salt = bcrypt.gensalt()
        bpassowrd = value.encode('utf-8')
        hashed_password = bcrypt.hashpw(bpassowrd, salt)
        encoded_password = hashed_password.decode('utf-8')
        self.password = encoded_password

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

    def is_valid_password(self, password):
        bpassword = password.encode('utf-8')
        bselfPassword = self.password.encode('utf-8')
        result = bcrypt.checkpw(bpassword, bselfPassword)

        return result
