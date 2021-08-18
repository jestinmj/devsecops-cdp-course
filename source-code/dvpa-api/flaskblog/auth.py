from functools import wraps
from flask import request, Response, session
from flaskblog import config
from blogapi import db

import hashlib

def check_auth(username, password):
    """ This function is called to check if a username / password
        combination is valid.
    """
    cur = db.connection.cursor()
    hashsed_password = hashlib.md5(password.encode()).hexdigest()
    cur.execute(f"SELECT * FROM users WHERE email='{username}' AND password='{hashsed_password}'")
    user = cur.fetchone()

    if user is None:
        return False

    session["is_logged_in"] = True
    session["id"] = user.get("id")
    session["email"] = user.get("email")
    session["full_name"] = user.get("full_name")

    return user

    # return username == config.username and password == config.password


def authenticate():
    """ Sends a 401 response that enables basic auth. """
    return Response('Not authorized to access this URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return func(*args, **kwargs)
    return decorated
