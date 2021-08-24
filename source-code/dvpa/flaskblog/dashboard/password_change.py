from flask import (request, redirect, render_template, url_for, session, flash)
from flask.views import MethodView

from flaskblog import db
from flaskblog.decorator import login_required

from flaskblog.dashboard import dashboard
from flaskblog.decorator import login_required

import hashlib

class PasswordChange(MethodView):
    decorator = [login_required]
    template_name = "dashboard/user/change-password.html"

    def get(self):
        return render_template(self.template_name)

    def post(self):
        # FIXME: CSRF
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 != password2:
            flash("Password Not Match", "danger")
            return render_template(self.template_name)

        hashed_password = hashlib.md5(password1.encode()).hexdigest()

        cur = db.connection.cursor()
        cur.execute("UPDATE `users` SET `password` = %s WHERE `users`.`id` = %s", [hashed_password, session.get("id")])
        db.connection.commit()
        cur.close()

        flash("Password Changed Successfully", "success")

        return redirect(url_for("dashboard.index"))