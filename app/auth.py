# -*- coding: utf-8 -*-
#
#    Copyright 2015 Madis Veskimeister <madis@pingviinitiivul.ee>
#  based on http://flask.pocoo.org/snippets/8/
#

from functools import wraps
from flask import request, Response
from app import app, db
from models import User

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    user = User.query.filter(User.name==username and User.password_hash==encrypt_password(passsword)).first()
    if user == None:
        return False
    else:
        return True

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
