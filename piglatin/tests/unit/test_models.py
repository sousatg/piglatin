from app.models import User
import unittest

class TestUserModel(unittest.TestCase):
    def test_create_user(self):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the email and password fields are defined correctly
        """
        user = User(email="test@email.com", password="testpassword")

        self.assertEqual(user.email, "test@email.com")
        self.assertNotEqual(user.password, "testpassword")
        self.assertFalse(user.confirmed)
        self.assertIsNone(user.confirmed_at)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.confirmation_token)

    def test_confirm_user(self):
        """
        GIVEN a User model
        WHEN a new user is confirmed
        THEN check if it was confirmed with success, confirmed_at was set and confirmation token as removed 
        """
        user = User(email="test@email.com", password="testpassword")

        self.assertFalse(user.confirmed)
        self.assertIsNone(user.confirmed_at)
        self.assertIsNotNone(user.confirmation_token)

        user.confirm()

        self.assertTrue(user.confirmed)
        self.assertIsNotNone(user.confirmed_at)
        self.assertIsNone(user.confirmation_token)

    def test_valid_password(self):
        """
        GIVEN a User 
        WHEN a valid password is verified
        THEN true should be returned if the password is valid
        """
        user = User(email="test@email.com", password="testpassword")

        self.assertTrue(user.is_valid_password("testpassword"))

    def test_invalid_password(self):
        """
        GIVEN a User 
        WHEN a invalid password is verified
        THEN false should be returned
        """
        user = User(email="test@email.com", password="testpassword")

        self.assertFalse(user.is_valid_password("invalid_password"))
