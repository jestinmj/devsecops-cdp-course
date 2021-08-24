import os
import time

from flask import (Blueprint, request, redirect, render_template, url_for, session, flash, jsonify, Response, make_response)
from flask.views import MethodView
from werkzeug import secure_filename

import sys
import flask
from flaskblog import db, BASE_DIR
from flaskblog.auth import requires_auth
from flaskblog.decorator import login_required
from flaskblog.db_util import is_post_exists
import json
import yaml

from bson import json_util

from flaskblog.dashboard import dashboard


class List(MethodView):
    decorators = [login_required]

    def get(self, page=1):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM posts WHERE author=%s", [session.get("id")])
        posts = cur.fetchall()
        cur.close()
        return render_template('dashboard/list.html', posts=posts, pagination=posts)


class CreatPost(MethodView):
    decorators = [login_required]
    template_name = "dashboard/detail.html"

    def get(self):
        return render_template(self.template_name, create=True)

    def post(self):
        title = request.form.get("title")
        body = request.form.get("body")
        slug = "-".join(title.split())
        cur = db.connection.cursor()
        cur.execute(
            f"INSERT INTO posts (`body`, `slug`, `author`, `title`) VALUES (%s, %s, %s, %s)",
            [body, slug, session.get("id"), title])
        db.connection.commit()
        cur.close()

        return redirect(url_for("dashboard.index"))


class EditPost(MethodView):
    decorators = [login_required]

    def get_context(self, slug=None):
        if slug:
            cur = db.connection.cursor()
            cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")
            post = cur.fetchone()
            if post is None:
                return "Not Found"

            # form_class = model_form(Post, exclude=('created_date',))
            # if request.method == 'POST':
            #     form = form_class(request.form, initial=post._data)
            # else:
            #     form = form_class(obj=post)
        # else:
        #     post = Post()
        #     form_class = model_form(Post, exclude=('created_date',))
        #     form = form_class(request.form)

        context = {
            'post': post,
            # 'form': form,
            'create': slug is None
        }

        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('dashboard/detail.html', **context)

    def post(self, slug):
        title = request.form.get("title")
        body = request.form.get("body")

        cur = db.connection.cursor()
        cur.execute("UPDATE `posts` SET `body` = %s, `title` = %s WHERE `posts`.`slug` = %s", [body, title, slug])
        db.connection.commit()
        cur.close()
        #
        # context = self.get_context(slug)
        # form = context.get('form')
        # if form.validate():
        #     post = context.get('post')
        #     form.populate_obj(post)
        #     post.save()
        return redirect(url_for('dashboard.index'))
        # return render_template('dashboard/detail.html', **context)


class DeletePost(MethodView):
    decorators = [login_required]

    def get(self, slug):
        if not is_post_exists(slug):
            flash("Post Is Not Exists", "error")
            return redirect(url_for('dashboard.index'))

        # FIXME: CSRF
        # IDOR
        cur = db.connection.cursor()
        cur.execute("DELETE FROM `posts` WHERE `posts`.`slug` = %s", [slug])
        db.connection.commit()
        cur.close()

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

    def post(self):

        export_format = request.form.get("format")
        action = request.args.get("action")

        if export_format not in ["yaml", "json"]:
            flash("Invalid Format", "danger")
            return render_template(self.template_name)

        if action == "export":

            cur = db.connection.cursor()
            cur.execute("SELECT * FROM posts WHERE author=%s", [session.get("id")])
            posts = cur.fetchall()
            cur.close()

            # https://stackoverflow.com/questions/1136437/inserting-a-python-datetime-datetime-object-into-mysql
            # https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
            # import ipdb; ipdb.set_trace()

            mime_type = "application/json"

            if export_format == "json":
                # export_post_data = {"posts" : json.dumps(posts, default=json_util.default)}
                # export_post_data = {"posts" : json.dumps(posts, default=json_util.default)}
                export_post_data = json.dumps(posts, default=str)
            elif export_format == "yaml":
                export_post_data = yaml.dump(posts)
                mime_type = "application/yaml"

            export_file_name = os.path.join("export_files", f"post-{time.time()}.{export_format}")
            with open(export_file_name, "wb") as f:
                f.write(export_post_data.encode())

            cur = db.connection.cursor()
            cur.execute("INSERT INTO exports (`owner`, `filename`) VALUES (%s, %s)",
                        [session.get("id"), export_file_name])
            db.connection.commit()
            cur.close()

            return Response(export_post_data, mimetype=mime_type)
            # return jsonify(export_post_data)

        elif action == "import":
            # cur = db.connection.cursor()
            # cur.execute("SELECT * FROM posts WHERE author=%s", [session.get("id")])
            # posts = cur.fetchall()
            # cur.close()

            f = request.files['import_file']
            import_data = f.stream.read()
            # f.save(secure_filename(f.filename))

            if export_format == "json":
                import_post_data = json.loads(import_data)
                # import_post_data = json.loads(import_data, object_hook=json_util.object_hook)

            elif export_format == "yaml":
                import_post_data = yaml.load(import_data)

            cur = db.connection.cursor()
            for post in import_post_data:
                print(post)

                cur.execute("INSERT INTO posts (`body`, `slug`, `author`, `title`) VALUES (%s, %s, %s, %s)",
                            [post.get("body"), post.get("slug"), post.get("author"), post.get("title")])
            db.connection.commit()
            cur.close()

            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid Action", "danger")
            return render_template(self.template_name)


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
