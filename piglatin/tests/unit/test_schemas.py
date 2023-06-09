import unittest
from app.schemas import RegistrationSchema
from app.models import User

class TestRegistrationSchema(unittest.TestCase):
    def test_valid_schema(self):
        """
        GIVEN a Registration schema
        WHEN a payload is evaluated
        THEN check if there are no errors
        """
        error = RegistrationSchema().validate({
            "email": "test@test.com",
            "password": "password",
        })

        self.assertEqual(len(error), 0)

    def test_invalid_email(self):
        """
        GIVEN a Registration schema
        WHEN a payload with invalid email is evaluated
        THEN check if a error is returned
        """
        error = RegistrationSchema().validate({
            "email": "test",
            "password": "passwrod",
        })

        self.assertEqual(len(error), 1)
        self.assertTrue("Not a valid email address." in error.get("email"))

    def test_missing_email(self):
        """
        GIVEN a Registration schema
        WHEN a payload with missing email is evaluated
        THEN check if a error is returned
        """
        error = RegistrationSchema().validate({
            "password": "passwrod",
        })

        self.assertEqual(len(error), 1)
        self.assertTrue("Missing data for required field." in error.get("email"))

    def test_missing_password(self):
        """
        GIVEN a Registration schema
        WHEN a payload with missing password is evaluated
        THEN check if a error is returned
        """
        error = RegistrationSchema().validate({
            "email": "test@email.com",
        })

        self.assertEqual(len(error), 1)
        self.assertTrue("Missing data for required field." in error.get("password"))

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
