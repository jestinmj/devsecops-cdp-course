from flask import request, jsonify, render_template_string, session
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from flaskblog.auth import check_auth
from flaskblog.db_util import is_user_exists

from blogapi import db

import hashlib

from flask_restplus import Resource, Namespace, fields

api_user = Namespace('api', path="/api/v1", description='Blog related operations')

login_creds = api_user.model('Login', {
    'email': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

register_data = api_user.model('Register', {
    'email': fields.String(required=True, description='Email'),
    'full_name': fields.String(required=True, description='Full Name'),
    'password': fields.String(required=True, description='Password'),
})

forgot_password_field = api_user.model('Forgot Password', {
    'email': fields.String(required=True, description='Email')
})

@api_user.route("/auth")
class Login(Resource):

    @api_user.expect(login_creds)
    def post(self):
        print(request.json)
        email = request.json.get("email")
        password = request.json.get("password")
        if email is None:
            api_user.abort(400)
        if password is None:
            api_user.abort(400)

        user = check_auth(email, password)
        if not user:
            return {"msg": "Bad email or password"}, 401

        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=email, user_claims=user)
        print(access_token)
        session["token"] = access_token
        # return jsonify(access_token=access_token), 200
        return {"access_token" : access_token}


@api_user.route("/register")
class Register(Resource):

    @api_user.expect(register_data)
    def post(self):
        email = request.json.get("email")
        full_name = request.json.get("full_name")
        password = request.json.get("password")

        if is_user_exists(email):
            return {"msg" : "Email Is Already Registered"}, 400

        hashed_password = hashlib.md5(password.encode()).hexdigest()
        cur = db.connection.cursor()
        cur.execute(
            f"INSERT INTO users (`email`, `full_name`, `password`) VALUES ('{email}', '{full_name}', '{hashed_password}')")
        db.connection.commit()
        cur.close()

        return {"msg" : "User created succussfully"}, 200

# class Logout(MethodView):
#     decorators = [login_required]
#
#     def get(self):
#         session.pop("is_logged_in")
#         session.pop("id")
#         session.pop("email")
#         session.pop("full_name")
#
#         return redirect("/")
#
#
@api_user.route("/forgot-password")
class ForgotPassword(Resource):

    @api_user.expect(forgot_password_field)
    def post(self):
        email = request.json.get("email")

        if not is_user_exists(email):
            return {"msg" : "User not exists"}, 404

        cur = db.connection.cursor()
        cur.execute("SELECT full_name FROM users WHERE email=%s", [email])
        full_name = cur.fetchone().get("full_name")
        template = render_template_string(f'''
        <h1>Hello, {full_name}</h1>
        Here is your reset Password Link : SOME_RANDOM_LINK
        ''')

        send_password_reset_link(email, template)


        return {"msg" : "Email Reset Link Is Send To Your Email"},200
def send_password_reset_link(email, template):
    print("Send Password Reset Link")
    print(f"TO : {email}")
    print(f"Body : {template}")