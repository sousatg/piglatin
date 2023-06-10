from app.create_app import db
from app.models import User
from tests.functional.base import BaseTestCase


class UserRegistration(BaseTestCase):
    url = "/register"

    payload = {
        "email": "test@test.com",
        "password": "testpassword",
    }

    bad_payload = {}

    def test_registering_user(self):
        """
        GIVEN the user doesnt already exist
        WHEN the '/register' endpoint receives payload (POST)
        THEN check if the user was created with success
        """

        response = self.client.post(self.url, json=self.payload)

        self.assertEqual(response.status_code, 201)

        user = User.query.filter_by(email="test@test.com").count()

        self.assertEqual(user, 1)

    def test_duplicated_email(self):
        """
        GIVEN the user already exists
        WHEN the '/register' endpoint receives payload (POST)
        THEN check if the proper error message is returned
        """
        user = User(email="test@test.com", password="testpassword")

        db.session.add(user)

        response = self.client.post(self.url, json=self.payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get("error"), "Email address already in registered")

    def test_invalid_schema(self):
        """
        GIVEN the payload we are sending is missing fields
        WHEN the '/register' endpoint receives payload (POST)
        THEN check if the a bad request is returned
        """
        response = self.client.post(self.url, json=self.bad_payload)

        self.assertEqual(response.status_code, 400)
