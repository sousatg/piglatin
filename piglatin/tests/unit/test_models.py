from app.models import User
import unittest

class TestUserModel(unittest.TestCase):
    def create_user(self):
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
