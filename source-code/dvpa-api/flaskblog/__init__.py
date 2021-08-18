from flask import Flask, render_template, session
from flask_mongoengine import MongoEngine
from flaskblog import config

import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {'yaml', 'json', 'yml'}
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST", config.HOSTNAME)
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER",'root')
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD",'passw0rd')
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB", 'medaum-pdso')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False


# db = MongoEngine(app)
# db = MySQL(app)


from flask_restplus import Api


from blogapi.home import api_home
from blogapi.user import api_user
from blogapi.dashboard import api_dashboard



api = Api(
    doc="/docs",
    title='PDSO Blog',
    version='1.0',
    description='A description',
)

def register_api_namespace(app):
    api.add_namespace(api_home)
    api.add_namespace(api_user)
    api.add_namespace(api_dashboard)
    api.init_app(app)

    # print(api.__schema__)

def register_blueprints(app):
    from flaskblog.views import posts
    from flaskblog.user import user
    from flaskblog.dashboard.routes import dashboard
    # from flaskblog.admin import admin

    app.register_blueprint(posts)
    app.register_blueprint(user)
    app.register_blueprint(dashboard)

@app.route("/")
def index():
    print(session)
    return render_template('posts/list.html')

register_api_namespace(app)
register_blueprints(app)

if __name__ == '__main__':
    app.run(threaded=True)
