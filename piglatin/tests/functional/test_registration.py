import unittest
from flask import current_app
from app.config import TestConfig
from app.create_app import create_app, db
from sqlalchemy_utils import database_exists, create_database
from app.models import User


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        if not database_exists(db.engine.url):
            create_database(db.engine.url)

        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


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
