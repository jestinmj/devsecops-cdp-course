from flask import (Blueprint, request, redirect, render_template, url_for, flash, session, render_template_string)
from flask.views import MethodView
from flaskblog import db
from flaskblog import auth
from flaskblog import db_util
from flaskblog.decorator import anonymous_required, login_required

import hashlib

user = Blueprint('user', __name__, template_folder='templates')


class Login(MethodView):
    decorators = [anonymous_required]

    def get(self):

        next_url = request.args.get("next")

        return render_template("auth/login.html", next_url=next_url)

    def post(self):
        username = request.form.get("email")
        password = request.form.get("password")

        if not auth.check_auth(username, password):
            flash("Email/Password Is Incorrect!", "error")
            return render_template("auth/login.html", forms_error="Email/Password Is Incorrect!")

        # FIXME: Open Redirect
        next_url = request.args.get("next")

        if next_url is None:
            return redirect("/")

        return redirect(next_url)


class Register(MethodView):
    decorators = [anonymous_required]

    def get(self):
        return render_template("auth/register.html")

    def post(self):
        email = request.form.get("email")
        full_name = request.form.get("full_name")
        password = request.form.get("password")

        if db_util.is_user_exists(email):
            flash("Email Is Already Registered", "error")
            return render_template("auth/register.html", form_error="Email Is Already Registered")

        hashed_password = hashlib.md5(password.encode()).hexdigest()

        cur = db.connection.cursor()
        cur.execute(
            f"INSERT INTO users (`email`, `full_name`, `password`) VALUES ('{email}', '{full_name}', '{hashed_password}')")
        db.connection.commit()
        cur.close()

        return redirect("user.login")

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

    def post(self):
        email = request.form.get("email")

        if not db_util.is_user_exists(email):
            flash("No User With This Email", "danger")
            return render_template(self.template_name)

        cur = db.connection.cursor()
        cur.execute("SELECT full_name FROM users WHERE email=%s", [email])
        full_name = cur.fetchone().get("full_name")
        template = render_template_string(f'''
        <h1>Hello, {full_name}</h1>
        Here is your reset Password Link : SOME_RANDOM_LINK
        ''')

        send_password_reset_link(email, template)

        flash("Email Reset Link Is Send To Your Email", "success")

        return render_template(self.template_name)


def send_password_reset_link(email, template):
    print("Send Password Reset Link")
    print(f"TO : {email}")
    print(f"Body : {template}")





user.add_url_rule("/login", view_func=Login.as_view('login'))
user.add_url_rule("/logout", view_func=Logout.as_view('logout'))
user.add_url_rule("/register", view_func=Register.as_view('register'))
user.add_url_rule("/forgot_password", view_func=ForgotPassword.as_view("forgot_password"))
