from flask import Blueprint, abort

from flask_restful import (Resource, Api, reqparse, fields,
                           url_for, marshal)

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
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No task provided!',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            required=True,
            help='Task status not provided!',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        todos = [marshal(todo, todo_fields)
                 for todo in models.Todo.select()]
        return (todos, 200)

    def post(self):
        args = self.reqparse.parse_args()
        if args.completed == 'False':
            args.completed = False
        todo = models.Todo.create(**args)
        context = marshal(todo, todo_fields)
        headers = {'Location': url_for('resources.todos.todo', id=todo.id)}
        return (context, 201, headers)


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No task provided!',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            required=True,
            help='Task status not provided!',
            location=['form', 'json']
        )
        super().__init__()

    def put(self, id):
        args = self.reqparse.parse_args()
        if args.completed == 'False':
            args.completed = False
        query = models.Todo.update(**args).where(models.Todo.id == id)
        query.execute()
        context = marshal(todo_or_404(id), todo_fields)
        headers = {'Location': url_for('resources.todos.todo', id=id)}
        return (context, 200, headers)

    def delete(self, id):
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
