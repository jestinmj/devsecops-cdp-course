from flask import (request, redirect, render_template, url_for, session, flash)
from flask.views import MethodView

from flaskblog.decorator import login_required

import hashlib

class PasswordChange(MethodView):
    decorator = [login_required]
    template_name = "dashboard/user/change-password.html"

    def get(self):
        return render_template(self.template_name)