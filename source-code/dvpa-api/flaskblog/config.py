# Host & Databases
HOSTNAME = '127.0.0.1'
MONGODB_SETTINGS = 'flaskblog_db'
SECRET_KEY = 'flaskblog_secret_key'

# Debugging & Reloader
debugger = True
reloader = True

# Admin authentication
# url for: /admin/
username = 'admin'
password = 'secret'

# Disqus Configuration
disqus_shortname = 'blogpythonlearning'  # please change this.

# Post pagination per-page
per_page = 5


BASE_URL = "http://127.0.0.1:5000"

import urllib.parse
def build_api_url(path):
    return urllib.parse.urljoin(BASE_URL, path)