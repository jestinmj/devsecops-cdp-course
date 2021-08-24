from flask import (request, redirect, render_template, url_for, session, flash)
from flask.views import MethodView

from flaskblog import db
from flaskblog.decorator import login_required


class ProfileInformation(MethodView):
    # decorator = [login_required]
    template_name = "dashboard/user/profile.html"

    def get(self, id):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id=%s", [id])
        user_info = cur.fetchone()
        cur.close()
        return render_template(self.template_name, user_info=user_info)

    def post(self, id):
        # FIXME: CSRF
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        dob = request.form.get("dob")
        # import ipdb; ipdb.set_trace()

        if is_empty_form(full_name) or is_empty_form(email):
            flash("Full Name or Email Can't Be Empty", "danger")
            # return render_template(self.template_name)
            return redirect(url_for("dashboard.profile", id=session.get("id")))

        cur = db.connection.cursor()
        cur.execute(
            f"UPDATE `users` SET `email` = %s, `full_name` = %s, `phone_number` = %s, `dob` = %s WHERE id=%s",
            [email, full_name, phone_number, dob, id])
        db.connection.commit()
        cur.close()

        flash("Profile Information Changed Successfully", "success")

        return redirect(url_for("dashboard.index"))


def is_empty_form(data):
    if data is None or data == "":
        return True
    return False
