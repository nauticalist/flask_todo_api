# Project 1: Flask Todo App

## Dependencies

* Python 3.6 or later

Refer to requirements.txt

## To start

### 1. Initialize virtual environment to run the project

```
git clone https://github.com/nauticalist/flask_todo_api.git
cd flask_todo_api
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

### 2. Start the server

```
python app.py
```
Browse http://127.0.0.1:8000 with your web browser.

### 3. Tests:

To run tests
```
coverage run -m unittest
coverage report
```
