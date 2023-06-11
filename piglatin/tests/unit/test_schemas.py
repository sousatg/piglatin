import unittest
from app.schemas import RegistrationSchema
from app.schemas import LoginSchema
from app.models import User

class TestRegistrationSchema(unittest.TestCase):
    def test_valid_schema(self):
        """
        GIVEN a Registration schema
        WHEN a payload is evaluated
        THEN check if there are no errors
        """
        errors = RegistrationSchema().validate({
            "email": "test@test.com",
            "password": "password",
        })

        self.assertEqual(len(errors), 0)

    def test_invalid_email(self):
        """
        GIVEN a Registration schema
        WHEN a payload with invalid email is evaluated
        THEN check if a error is returned
        """
        errors = RegistrationSchema().validate({
            "email": "test",
            "password": "passwrod",
        })

        self.assertEqual(len(errors), 1)
        self.assertTrue("Not a valid email address." in errors.get("email"))

    def test_missing_email(self):
        """
        GIVEN a Registration schema
        WHEN a payload with missing email is evaluated
        THEN check if a error is returned
        """
        errors = RegistrationSchema().validate({
            "password": "passwrod",
        })

        self.assertEqual(len(errors), 1)
        self.assertTrue("Missing data for required field." in errors.get("email"))

    def test_missing_password(self):
        """
        GIVEN a Registration schema
        WHEN a payload with missing password is evaluated
        THEN check if a error is returned
        """
        errors = RegistrationSchema().validate({
            "email": "test@email.com",
        })

        self.assertEqual(len(errors), 1)
        self.assertTrue("Missing data for required field." in errors.get("password"))

    def test_dump(self):
        """
        GIVEN a Registration schema
        WHEN a payload is loaded
        THEN check if a User instance is returned
        """
        user = RegistrationSchema().load({
            "email": "test@test.com",
            "password": "password",
        })

        self.assertIsInstance(user, User)

class TestLoginSchema(unittest.TestCase):
    def test_valid_schema(self):
        errors = LoginSchema().validate({
            "email": "test@email.com",
            "password": "password"
        })

        self.assertEqual(len(errors), 0)

    def test_invalid_email(self):
        """
        GIVEN a Login schema
        WHEN a payload with invalid email is evaluated
        THEN check if a error is returned
        """
        errors = LoginSchema().validate({
            "email": "test",
            "password": "passwrod",
        })

        self.assertEqual(len(errors), 1)
        self.assertTrue("Not a valid email address." in errors.get("email"))

    def test_missing_email(self):
        """
        GIVEN a Login schema
        WHEN a payload with missing email is evaluated
        THEN check if a error is returned
        """
        errors = LoginSchema().validate({
            "password": "passwrod",
        })

        self.assertEqual(len(errors), 1)
        self.assertTrue("Missing data for required field." in errors.get("email"))

    def test_missing_password(self):
        """
        GIVEN a Login schema
        WHEN a payload with missing password is evaluated
        THEN check if a error is returned
        """
        errors = LoginSchema().validate({
            "email": "test@email.com",
        })

        self.assertEqual(len(errors), 1)
        self.assertTrue("Missing data for required field." in errors.get("password"))

    def test_dump(self):
        """
        GIVEN a Login schema
        WHEN a payload is loaded
        THEN check if the data is properly loaded
        """
        data = LoginSchema().load({
            "email": "test@test.com",
            "password": "password",
        })

        self.assertEqual(data, {
            "email": "test@test.com",
            "password": "password",
        })
