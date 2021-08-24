from flask import redirect, request, url_for, session

import functools


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("user.login", next=request.url))
        return func(*args, **kwargs)

    return secure_function

def anonymous_required(func):
    @functools.wraps(func)
    def not_pretect_function(*args, **kwargs):
        print(session)
        if "email" in session:
            return redirect("/")
        return func(*args, **kwargs)

    return not_pretect_function