from flask import Blueprint, abort

from flask_restful import (Resource, Api, reqparse, fields,
                           url_for, marshal, inputs)

import models

# Define task related fields
todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'completed': fields.Boolean,
}


def todo_or_404(todo_id):
    """
    Get task if exists
    """
    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        return todo


class TodoList(Resource):
    """
    Todo list resources
    """
    def __init__(self):
        """
        Define input arguments for parser
        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No task provided!',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            required=False,
            help='Invalid task status provided!',
            type=inputs.boolean,
            default=False,
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        """
        Get all todos
        """
        todos = [marshal(todo, todo_fields)
                 for todo in models.Todo.select()]
        return (todos, 200)

    def post(self):
        """
        Get post data to create a todo item
        """
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        context = marshal(todo, todo_fields)
        headers = {'Location': url_for('resources.todos.todo', id=todo.id)}
        return (context, 201, headers)


class Todo(Resource):
    """
    Todo object related tasks
    """
    def __init__(self):
        """
        Define input arguments for parser
        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No task provided!',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            required=False,
            help='Invalid task status provided!',
            type=inputs.boolean,
            default=False,
            location=['form', 'json']
        )
        super().__init__()

    def get(self, id):
        """
        Get single todo by id
        """
        context = marshal(todo_or_404(id), todo_fields)
        headers = {'Location': url_for('resources.todos.todo', id=id)}
        return (context, 200, headers)

    def put(self, id):
        """
        Update a todo item
        """
        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id == id)
        query.execute()
        context = marshal(todo_or_404(id), todo_fields)
        headers = {'Location': url_for('resources.todos.todo', id=id)}
        return (context, 200, headers)

    def delete(self, id):
        """
        Delete a todo item
        """
        query = models.Todo.delete().where(models.Todo.id == id)
        query.execute()
        headers = {'Location': url_for('resources.todos.todos')}
        return ('', 204, headers)


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/todos',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/todos/<int:id>',
    endpoint='todo'
)
