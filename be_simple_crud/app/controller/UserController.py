from app.model.users import Users
from app.helper import response
from flask import request
from app import db
from flask_jwt_extended import *
import re
import datetime

def login():
    try:
        username = request.json['username']
        password = request.json['password']

        print("success get request")
        user = Users.query.filter_by(username=username).first()
        if not user:
            return response.badRequest('Empty....')

        if not user.checkPassword(password):
            return response.badRequest('Your credentials is invalid')
        print("success validation")

        data = singleTransform(user)
        expires = datetime.timedelta(minutes=120)
        expires_refresh = datetime.timedelta(days=1)
        access_token = create_access_token(identity=str(data['id']), fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=str(data['id']), expires_delta=expires_refresh)
        return response.ok({"data" : data, "access_token" : access_token, "refresh_token" : refresh_token}, "Welcome")
    except Exception as e:
        print(e)
        return response.badRequest('Error while login!')

@jwt_required()
def index():
    session = get_jwt()
    try:
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'id')
        order = request.args.get('order', 'asc')

        query = Users.query
        query = query.filter(Users.id != session['sub'])

        if search:
            query = query.filter(
                (Users.name.ilike(f'%{search}%')) |
                (Users.username.ilike(f'%{search}%')) |
                (Users.email.ilike(f'%{search}%'))
            )

        if hasattr(Users, sort_by):
            if order == 'desc':
                query = query.order_by(getattr(Users, sort_by).desc())
            else:
                query = query.order_by(getattr(Users, sort_by).asc())
        else:
            query = query.order_by(Users.id.asc())

        users = query.all()
        data = transform(users)
        return response.ok(data, "")
    except Exception as e:
        print(e)

@jwt_required()
def show(id):
    try:
        users = Users.query.filter_by(id=id).first()
        if not users:
            return response.badRequest("Data tidak ditemukan")
        data = singleTransform(users)
        return response.ok(data, "")
    
    except Exception as e:
        return response.ok('', 'Error finding data!')


def store():
    try:
        name = request.json['name']
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']

        users = Users(name=name, username=username, email=email)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()

        return response.ok('', 'Successfully add data!')
    except Exception as e:
        print("Get error: ", e)
        return response.badRequest('Username or email already taken!')
        
@jwt_required()
def update(id):
    try:
        name = request.json['name']
        username = request.json['username']
        email = request.json['email']

        user = Users.query.filter_by(id=id).first()
        user.email = email
        user.name = name
        user.username = username
        
        if 'password' in request.json:
          password = request.json['password']
          user.setPassword(password)

        db.session.commit()

        return response.ok('', 'Successfully update data!')

    except Exception as e:
        print("Get error: ", e)
        return response.badRequest('Server error while updating')

@jwt_required()
def delete(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], 'Empty....')

        db.session.delete(user)
        db.session.commit()

        return response.ok('', 'Successfully delete data!')
    except Exception as e:
        return response.badRequest('Empty')
  

def singleTransform(user):
    return {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'email': user.email
    }


def transform(users):
    array = []
    for i in users:
        array.append({
            'id': i.id,
            'name': i.name,
            'username': i.username,
            'email': i.email
        })
    return array

def validate_user_request(data):
    errors = {}

    # --------- NAME ----------
    if not data.get("name"):
        errors["name"] = "Name is required"
    elif len(data["name"]) < 3:
        errors["name"] = "Name must be at least 3 characters long"

    # --------- USERNAME ----------
    if not data.get("username"):
        errors["username"] = "Username is required"
    elif not re.match("^[A-Za-z0-9_]+$", data["username"]):
        errors["username"] = "Username can only contain letters, numbers, and underscores"
    elif len(data["username"]) < 3:
        errors["username"] = "Username must be at least 3 characters long"

    # --------- EMAIL ----------
    if not data.get("email"):
        errors["email"] = "Email is required"
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        errors["email"] = "Invalid email format"

    # --------- PASSWORD ----------
    if not data.get("password"):
        errors["password"] = "Password is required"
    elif len(data["password"]) < 6:
        errors["password"] = "Password must be at least 6 characters long"

    return errors