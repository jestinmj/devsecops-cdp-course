import os
import time

from flask import (Blueprint, request, redirect, render_template, url_for, session, flash, jsonify, Response, make_response)
from flask.views import MethodView
from werkzeug import secure_filename

import sys
from flaskblog import BASE_DIR
from flaskblog.decorator import login_required
from flaskblog.config import build_api_url
from flaskblog.db_util import is_post_exists, db
import json
import yaml
import requests

from bson import json_util

from flaskblog.dashboard import dashboard


class List(MethodView):
    decorators = [login_required]

    def get_context(self):
        r = requests.get(build_api_url("/api/v1/dashboard/mypost"), headers={"Authorization": f"Bearer {session.get('token')}"})

        return {"posts" : json.loads(r.content)}
    def get(self, page=1):

        context = self.get_context()
        print(context)

        return render_template('dashboard/list.html', **context)


class CreatPost(MethodView):
    decorators = [login_required]
    template_name = "dashboard/detail.html"

    def get(self):
        return render_template(self.template_name, create=True)

class EditPost(MethodView):
    decorators = [login_required]

    def get_context(self, slug=None):
        if slug:
            r = requests.get(build_api_url(f"/api/v1/detail/{slug}"), headers={"Authorization": f"Bearer {session.get('token')}"})

        post = json.loads(r.content)
        print("Edit post", post)
        context = {
            'post': post.get("post"),
            # 'form': form,
            'create': slug is None
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('dashboard/detail.html', **context)


class DeletePost(MethodView):
    decorators = [login_required]

    def get(self, slug):
        print("POST SLUG ", slug)
        if not is_post_exists(slug):
            flash("Post Is Not Exists", "error")
            return redirect(url_for('dashboard.index'))

        # FIXME: CSRF
        # IDOR
        # cur = db.connection.cursor()
        # cur.execute("DELETE FROM `posts` WHERE `posts`.`slug` = %s", [slug])
        # db.connection.commit()
        # cur.close()

        flash("Post Deleted", "success")
        return redirect(url_for('dashboard.index'))


class ExportPost(MethodView):
    decorators = [login_required]
    template_name = "dashboard/export-post.html"

    def get_context(self):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM exports WHERE owner=%s", [session.get("id")])
        exported_post = cur.fetchall()
        cur.close()

        context = dict()
        context["exports"] = exported_post

        return context

    def get(self):
        contenxt = self.get_context()
        return render_template(self.template_name, **contenxt)

class ExportFileDownload(MethodView):
    def get(self):
        filename = request.args.get("filename")

        if filename is None:
            return redirect(url_for("dashboard.index"))

        file_path = os.path.join(BASE_DIR, filename)
        with open(file_path, "rb") as f:
            export_data = f.read()

        response = make_response(export_data)
        response.headers['Content-Type'] = 'text/json'
        response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'

        # return Response(export_data, mimetype="application/data")
        return response
