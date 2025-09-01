from app import app
from app.controller import UserController
from flask import request

@app.route('/', methods=['GET', 'POST'])
def index():
    return UserController.index()
    
@app.route('/login', methods=['POST'])
def login():
    return UserController.login()

@app.route('/register', methods=['POST'])
def register():
    return UserController.store()

@app.route('/users/<id>', methods=['PUT', 'GET', 'DELETE'])
def usersDetail(id):
    if request.method == 'GET':
        return UserController.show(id)
    elif request.method == 'PUT':
        return UserController.update(id)
    elif request.method == 'DELETE':
        return UserController.delete(id)
    
