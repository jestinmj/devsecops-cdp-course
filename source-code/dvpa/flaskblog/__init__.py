from flask import Flask
from flask_mongoengine import MongoEngine
from flaskblog import config
from flask_mysqldb import MySQL

import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {'yaml', 'json', 'yml'}
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MYSQL_HOST'] = config.HOSTNAME
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'passw0rd'
app.config['MYSQL_DB'] = 'medaum-pdso'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# db = MongoEngine(app)
db = MySQL(app)


def register_blueprints(app):
    from flaskblog.views import posts
    from flaskblog.user import user
    from flaskblog.dashboard.routes import dashboard
    # from flaskblog.admin import admin

    app.register_blueprint(posts)
    app.register_blueprint(user)
    app.register_blueprint(dashboard)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
