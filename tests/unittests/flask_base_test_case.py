from unittest import TestCase
from app import create_app


class TestFlaskBase(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()


class TestFlaskSystem(TestFlaskBase):
    def setUp(self):
        super().setUp()
        self.app.db.create_all()

    def tearDown(self):
        self.app.db.drop_all()
