from flask import (request, redirect, render_template, url_for, session, flash)
from flask.views import MethodView

from flaskblog.decorator import login_required

class ProfileInformation(MethodView):
    decorator = [login_required]
    template_name = "dashboard/user/profile_information.html"

    def get(self, uid):

        return render_template(self.template_name, uid=uid)