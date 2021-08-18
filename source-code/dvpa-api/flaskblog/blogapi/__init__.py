from flask_mysqldb import MySQL
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from flaskblog import app

db = MySQL()
db.init_app(app)
jwt = JWTManager(app)
