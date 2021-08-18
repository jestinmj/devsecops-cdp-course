from flask import (Blueprint, request, redirect, render_template, url_for, flash, session, render_template_string)
from flask.views import MethodView
from flaskblog.decorator import anonymous_required, login_required

user = Blueprint('user', __name__, template_folder='templates')

class Login(MethodView):
    decorators = [anonymous_required]

    def get(self):
        next_url = request.args.get("next")
        return render_template("auth/login.html", next_url=next_url)

class Register(MethodView):
    decorators = [anonymous_required]

    def get(self):
        return render_template("auth/register.html")

class Logout(MethodView):
    decorators = [login_required]

    def get(self):
        session.pop("is_logged_in")
        session.pop("id")
        session.pop("email")
        session.pop("full_name")

        return redirect("/")


class ForgotPassword(MethodView):
    decorators = [anonymous_required]
    template_name = "auth/forgot_password.html"

    def get(self):
        return render_template(self.template_name)


user.add_url_rule("/login", view_func=Login.as_view('login'))
user.add_url_rule("/logout", view_func=Logout.as_view('logout'))
user.add_url_rule("/register", view_func=Register.as_view('register'))
user.add_url_rule("/forgot_password", view_func=ForgotPassword.as_view("forgot_password"))
