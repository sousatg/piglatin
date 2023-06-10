import unittest
from flask import current_app
from app.config import TestConfig
from app.create_app import create_app, db
from sqlalchemy_utils import database_exists, create_database


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