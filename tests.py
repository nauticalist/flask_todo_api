import unittest
import json

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


class TestTodoResource(unittest.TestCase):
    def setUp(self):
        """
        Create test db and data
        """
        app.testing = True,
        self.app = app.test_client()

        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        self.completed_task = {
            'name': 'completed task 1',
            'completed': True
        }
        self.task1 = models.Todo.create(
            name=self.completed_task['name'],
            completed=self.completed_task['completed']
        )
        self.incomplete_task = {
            'name': 'incomplete task 1',
            'completed': False
        }
        self.task2 = models.Todo.create(
            name=self.incomplete_task['name'],
            completed=self.incomplete_task['completed']
        )

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_todo_list(self):
        resp = self.app.get('/api/v1/todos')
        data = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.completed_task['name'], data)

    def test_get_single_todo(self):
        resp = self.app.get('/api/v1/todos/1')
        resp_notfound = self.app.get('/api/v1/todos/99999')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_notfound.status_code, 404)

    def test_post_data(self):
        data = {
            'name': 'valid task name',
            'completed': False
        }
        resp = self.app.post(
            '/api/v1/todos',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 201)
        self.assertIn(data['name'], resp.get_data(as_text=True))

    def test_put_data(self):
        data = {
            'name': 'modifid valid task name',
            'completed': False
        }
        resp = self.app.put(
            '/api/v1/todos/1',
            data=json.dumps(data),
            content_type='application/json'
        )
        invalid_resp = self.app.put(
            '/api/v1/todos/9999',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(invalid_resp.status_code, 404)
        self.assertIn(data['name'], resp.get_data(as_text=True))
        self.assertNotIn(self.completed_task['name'],
                         resp.get_data(as_text=True))

    def test_delete_data(self):
        resp = self.app.delete('/api/v1/todos/2')
        self.assertEqual(resp.status_code, 204)
        self.assertNotIn(self.incomplete_task['name'],
                         resp.get_data(as_text=True))
