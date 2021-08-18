from flask import (Blueprint, request, redirect, render_template, url_for, session)
from flask.views import MethodView

from flaskblog.config import build_api_url

import requests

posts = Blueprint('posts', __name__, template_folder='templates')


class ListView(MethodView):

    def get(self):

        return render_template('posts/list.html')

class DetailView(MethodView):

    def get(self, slug):
        return render_template('posts/detail.html')


class SearchView(MethodView):

    def get(self, page=1):
        query = request.args.get('q')

        if query == None:
            return redirect(url_for('posts.list'))

        return render_template('posts/search.html', query=query)

posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/page/<int:page>/', view_func=ListView.as_view('list_page'))
posts.add_url_rule('/post/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/search/', view_func=SearchView.as_view('search'))
posts.add_url_rule('/search/page/<int:page>/', view_func=SearchView.as_view('search_page'))