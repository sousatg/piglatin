from app.create_app import db
from app.models import User
from tests.functional.base import BaseTestCase


class UserRegistration(BaseTestCase):
    url = "/login"

    payload = {
        "email": "test@test.com",
        "password": "testpassword",
    }

    bad_credentials = {
        "email": "test@test.com",
        "password": "badpassword",       
    }

    def setUp(self):
        super().setUp()

        user = User(**self.payload)

        db.session.add(user)

    def test_login(self):
        """
        GIVEN that a user is already registered 
        WHEN a request is sent to login with user credentials
        THEN a 200 status code should be returned
        """
        response = self.client.post("/login", json=self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json.get("access_token"))
        self.assertIsNotNone(response.json.get("refresh_token"))


    def test_login_invalid_credentials(self):
        """
        GIVEN that a user is already registered 
        WHEN a request is sent to login with user bad credentials
        THEN a error of unauthorized should be sent
        """
        response = self.client.post("/login", json=self.bad_credentials)

        self.assertEqual(response.status_code, 401)
