from flask import (Blueprint, request, redirect, render_template, url_for, jsonify)

from flask_restplus import Api, Resource, Namespace

api_home = Namespace('api', path="/api/v1", description='Blog related operations')

from blogapi import db

@api_home.route("/index")
class IndexApi(Resource):

    def get(self):
        cur = db.connection.cursor()
        cur.execute("SELECT * from posts")
        posts = cur.fetchall()
        cur.close()

        return jsonify(posts)


@api_home.route("/detail/<string:slug>")
class DetailView(Resource):

    def get_context(self, slug):
        cur = db.connection.cursor()
        cur.execute(f"SELECT * FROM posts WHERE slug='{slug}'")
        post = cur.fetchone()
        cur.close()
        context = {
            'post': post,
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return jsonify(context)

@api_home.route("/search")
@api_home.param("q", "Search query", required=True)
class SearchView(Resource):

    def get(self):
        query = request.args.get('q')

        if query == None:
            api_home.abort(400)

        cur = db.connection.cursor()
        cur.execute(f"SELECT * FROM posts WHERE title LIKE '%{query}%'")
        search_posts = cur.fetchall() #Post.objects(title__icontains=query)

        return jsonify(search_posts)