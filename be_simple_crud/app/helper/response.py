from flask import jsonify, make_response

def ok(values, message):
    response = {
        'status': 'success',
        'message': message,
        'data': values
    }
    return make_response(jsonify(response)), 200

def badRequest(message, values=[]):
    response = {
        'status': 'failed',
        'message': message,
        'data': values
    }
    return make_response(jsonify(response)), 400