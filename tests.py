import os
import unittest
import tempfile

from peewee import *
from datetime import datetime

from app import app
from models import Todo


class AppTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_my_todos_view(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'My TODOs!', resp.data)
