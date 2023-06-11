from app.extensions import ma
from app.models import User
from marshmallow import Schema, fields, post_load, validates, ValidationError


class RegistrationSchema(ma.Schema):
    email = fields.Email(required=True, allow_none=False)
    password = ma.Str(required=True, allow_none=False)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class LoginSchema(ma.Schema):
    email = fields.Email(required=True, allow_none=False)
    password = ma.Str(required=True, allow_none=False)
