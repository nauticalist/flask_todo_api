import unittest

from peewee import *

from app import app
import models

MODELS = [models.Todo]
test_db = SqliteDatabase(':memory:')


class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_my_todos_view(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'My TODOs!', resp.data)


class TestTodoModel(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_todo_table(self):
        self.assertTrue(models.Todo.table_exists())

    def test_todo_creation(self):
        models.Todo.create(name="testthiscode")
        todo = models.Todo.select().where(models.Todo.name == 'testthiscode')
        self.assertEqual(todo.count(), 1)

    def test_model_initialization(self):
        models.initialize()
