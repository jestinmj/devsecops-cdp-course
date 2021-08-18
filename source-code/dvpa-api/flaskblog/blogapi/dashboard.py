from flask import request, session, jsonify
from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_claims

import os
import json
import time
import yaml
import base64
import hashlib

from flaskblog.db_util import is_post_exists

from blogapi import db

api_dashboard = Namespace('api', path="/api/v1", description='Blog related operations')

password_change_fields = api_dashboard.model(
    "Password Change", {
        "password1" : fields.String(required=True, description='Password'),
        "password2" : fields.String(required=True, description='Password Confirmation'),

    }
)

post_fields = api_dashboard.model(
    "Create Post", {
        "title" : fields.String(required=True, description='Title'),
        "body" : fields.String(required=True, description='Body'),

    }
)

post_export_fields = api_dashboard.model(
    "Export Post", {
        "format": fields.String(required=True, description='Export Format'),
        "action": fields.String(required=True, description='Action'),
    }
)

profile_information_fields = api_dashboard.model(
    "Profile Information", {
        "email": fields.String(required=True, description='Email'),
        "full_name": fields.String(required=True, description='Full Name'),
        "phone_number": fields.String(required=True, description='Phone Number'),
        "dob": fields.String(required=True, description='Date Of Birth'),
    }
)



@api_dashboard.route("/dashboard/password-change")
@api_dashboard.header("Authorization", "JWT TOKEN", required=True)
class PasswordChange(Resource):
    method_decorators = [jwt_required]

    @api_dashboard.expect(password_change_fields, validate=True)
    def post(self):
        # FIXME: CSRF
        password1 = request.json.get("password1")
        password2 = request.json.get("password2")

        if password1 != password2:
            return {"msg": "Password Not Match"}, 400


        hashed_password = hashlib.md5(password1.encode()).hexdigest()

        cur = db.connection.cursor()
        cur.execute("UPDATE `users` SET `password` = %s WHERE `users`.`id` = %s", [hashed_password, session.get("id")])
        db.connection.commit()
        cur.close()

        return {"msg": "Password Changed Successfully"}


@api_dashboard.route("/dashboard/user")
@api_dashboard.param("uid", "User ID", required=True)
class ProfileInformation(Resource):

    method_decorators = [jwt_required]

    def get(self):
        cur = db.connection.cursor()
        cur.execute(f"SELECT * FROM users WHERE id={request.args.get('uid')}")
        user = cur.fetchone()
        print(user)
        cur.close()
        return jsonify(user)

    @api_dashboard.expect(profile_information_fields, validate=True)
    def post(self):
        email = request.json.get("email")
        full_name = request.json.get("full_name")
        phone_number = request.json.get("phone_number")
        dob = request.json.get("dob")
        # TODO: Update

        cur = db.connection.cursor()
        cur.execute(f"UPDATE `users` SET `email` = '{email}', `full_name` = '{full_name}', `phone_number` = '{phone_number}', `dob` = '{dob}' WHERE `users`.`id` = {request.args.get('uid')}")
        db.connection.commit()
        cur.close()
        return {"msg" : "Profile Updated"}

@api_dashboard.route("/dashboard/mypost")
class MyPost(Resource):

    method_decorators = [jwt_required]

    def get(self):
        cur = db.connection.cursor()
        claim = get_jwt_claims()
        cur.execute("SELECT * FROM posts WHERE author=%s", [claim.get("id")])
        posts = cur.fetchall()
        cur.close()
        return jsonify(posts)

    def post(self):
        pass

@api_dashboard.route("/dashboard/post/create")
class CreatePost(Resource):
    method_decorators = [jwt_required]

    @api_dashboard.expect(post_fields, validate=True)
    def post(self):
        claim = get_jwt_claims()
        title = request.json.get("title")
        body = request.json.get("body")
        slug = "-".join(title.split())
        cur = db.connection.cursor()
        cur.execute(
            f"INSERT INTO posts (`body`, `slug`, `author`, `title`) VALUES (%s, %s, %s, %s)",
            [body, slug, claim.get("id"), title])
        db.connection.commit()
        cur.close()

        return {"msg" : "Post Created"}

@api_dashboard.route("/dashboard/post/edit/<string:slug>")
class EditPost(Resource):
    method_decorators = [jwt_required]

    @api_dashboard.expect(post_fields, validate=True)
    def post(self, slug):
        title = request.json.get("title")
        body = request.json.get("body")

        if not title or not body:
            return {"msg" : "Value cannot be empty"},400


        cur = db.connection.cursor()
        cur.execute("UPDATE `posts` SET `body` = %s, `title` = %s WHERE `posts`.`slug` = %s", [body, title, slug])
        db.connection.commit()
        cur.close()

        return {"msg": "Post Updated"}


@api_dashboard.route("/dashboard/post/delete/<string:slug>")
class DeletePost(Resource):
    method_decorators = [jwt_required]

    def get(self, slug):
        print("Delete Post"*32)
        print(slug)
        if not is_post_exists(slug):
            return {"msg": "Post Is Not Exists"}, 404
        print("A"*32)

        # FIXME: CSRF
        # FIXME: IDOR
        cur = db.connection.cursor()
        cur.execute("DELETE FROM `posts` WHERE `posts`.`id` = %s", [slug])
        db.connection.commit()
        cur.close()

        return {"msg": "Post Deleted"}, 200

@api_dashboard.route("/dashboard/post/import-export")
class ExportPost(Resource):
    method_decorators = [jwt_required]

    @api_dashboard.expect(post_export_fields, validate=True)
    def post(self):

        export_format = request.json.get("format")
        action = request.json.get("action")
        # print(request.json.get("content"))

        claim = get_jwt_claims()

        if export_format not in ["yaml", "json"]:
            return {"msg": "Invalid Export Format"}, 400

        if action == "export":

            cur = db.connection.cursor()
            cur.execute("SELECT * FROM posts WHERE author=%s", [claim.get("id")])
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
                        [claim.get("id"), export_file_name])
            db.connection.commit()
            cur.close()

            return export_post_data
            # return jsonify(export_post_data)

        elif action == "import":
            print("IMPORT"*32)
            # cur = db.connection.cursor()
            # cur.execute("SELECT * FROM posts WHERE author=%s", [session.get("id")])
            # posts = cur.fetchall()
            # cur.close()

            # f = request.files['import_file']
            # import_data = f.stream.read()
            # f.save(secure_filename(f.filename))
            import_data = base64.b64decode(request.json.get("content"))

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

            return {"msg": "OK"}
        # else:
        #     flash("Invalid Action", "danger")
        #     return render_template(self.template_name)