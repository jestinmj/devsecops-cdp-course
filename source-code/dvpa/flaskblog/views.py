from flask import (Blueprint, request, redirect, render_template, url_for)
from flask.views import MethodView
# from flask_mongoengine.wtf import model_form

# from flaskblog.models import (Post, Tag)
from flaskblog import config
from flaskblog import db

posts = Blueprint('posts', __name__, template_folder='templates')


class ListView(MethodView):

    def get(self, page=1):
        cur = db.connection.cursor()
        cur.execute("SELECT * from users")
        users = cur.fetchall()

        cur.execute("SELECT * from posts")
        posts = cur.fetchall()
        cur.close()
        # return str(users)
        # posts = Post.objects.paginate(page=page, per_page=config.per_page)

        return render_template('posts/list.html',
                               posts=posts)
        #                        pagination=posts,
        #                        disqus_shortname=config.disqus_shortname
        #                        )


class DetailView(MethodView):

    def get_context(self, slug):
        cur = db.connection.cursor()
        print("SLUG ", slug)
        cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")
        post = cur.fetchone()
        cur.close()
        print("POST ", post)
        # i dont no why if we use .exclude() is does not work.
        # so i handle it with this:
        # {% for rpost in related_posts %}
        #   {% if not rpost == post %}
        #       {{ rpost }}
        # related_posts = Post.objects.filter(tags__in=post.tags)[:5]

        context = {
            'post': post,
            'related_posts': "A",
            'disqus_shortname': "C"
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)


class SearchView(MethodView):

    def get(self, page=1):
        query = request.args.get('q')
        if query == None:
            return redirect(url_for('posts.list'))

        cur = db.connection.cursor()
        cur.execute(f"SELECT * FROM posts WHERE title LIKE '%{query}%'")
        search_posts = cur.fetchall() #Post.objects(title__icontains=query)
        # posts = search_posts.paginate(page=page, per_page=config.per_page)
        print("SEARCH POST", search_posts)
        return render_template('posts/search.html',
                               posts=search_posts,
                               pagination=posts,
                               query=query,
                               disqus_shortname=config.disqus_shortname
                               )


class PostTagView(MethodView):

    def get(self, slug, page=1):
        tag = Tag.objects.get_or_404(slug=slug)
        tagged_posts = Post.objects.filter(tags=tag)
        posts = tagged_posts.paginate(page=page, per_page=config.per_page)
        tag_slug = tag.slug
        return render_template('posts/tag.html',
                               tag=tag,
                               tag_slug=tag_slug,
                               posts=posts,
                               pagination=posts,
                               disqus_shortname=config.disqus_shortname
                               )


posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/page/<int:page>/', view_func=ListView.as_view('list_page'))
posts.add_url_rule('/post/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/search/', view_func=SearchView.as_view('search'))
posts.add_url_rule('/search/page/<int:page>/', view_func=SearchView.as_view('search_page'))
posts.add_url_rule('/tag/<slug>/', view_func=PostTagView.as_view('tag'))
posts.add_url_rule('/tag/<slug>/page/<int:page>/', view_func=PostTagView.as_view('tag_page'))
