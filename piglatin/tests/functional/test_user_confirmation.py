from tests.functional.base import BaseTestCase
from app.models import User
from app.extensions import db

class TestUserConfirmation(BaseTestCase):
    url = "/verification"

    def test_confirm_user(self):
        """
        GIVEN a user with email test@email.com is unconfirmed
        WHEN he sends a request to confirm is account
        THEN check if the user account was confirmed
        """
        user = User(email="test@email.com", password="password")

        db.session.add(user)
        db.session.commit()

        response = self.client.post(self.url, json={"token": user.confirmation_token})

        self.assertEqual(response.status_code, 204)

        user = User.query.filter_by(email="test@email.com").first()

        self.assertTrue(user.confirmed)

    def test_confirm_user_invalid_token(self):
        """
        GIVEN a user with email test@email.com is unconfirmed
        WHEN he sends a request to confirm is account with a invalid token
        THEN check if a error is returned and the account keeps in a inactive state
        """
        user = User(email="test@email.com", password="password")

        db.session.add(user)
        db.session.commit()

        response = self.client.post(self.url, json={"token": "random_token"})

        self.assertEqual(response.status_code, 400)

        user = User.query.filter_by(email="test@email.com").first()

        self.assertFalse(user.confirmed)

    def test_reuse_confirmation_token(self):
        """
        GIVEN a user is already confirmed is account
        WHEN a request is sent again with the same confirmation token
        THEN check if a error is returned
        """
        user = User(email="test@email.com", password="password")

        db.session.add(user)
        db.session.commit()

        response = self.client.post(self.url, json={"token": user.confirmation_token})

        self.assertEqual(response.status_code, 204)

        response = self.client.post(self.url, json={"token": user.confirmation_token})

        self.assertEqual(response.status_code, 400)
