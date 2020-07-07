import os
import datetime
from flask import Flask, request, jsonify, abort, render_template, url_for, redirect
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST, PUT, GET, PATCH, OPTIONS, DELETE")
        return response

    ## ROUTES

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/callback")
    def callback():
        token = request.args.get("access_token")
        print(request.url)
        if token:
            return f"<h1>{token}</h1>"
        else:
            return redirect(url_for("dashboard"))
    
    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")
    
    #Movies Start Here 
    
    @app.route("/movies", methods=["GET"])
    @requires_auth(permission="get:movies")
    def get_movies(jwt):
        movies = Movie.query.all() 
        movies = [m.movie_formatted() for m in movies]
        return jsonify({
            "success": True, 
            "movies": movies
        }), 200
    
    
    @app.route("/movie-detail/<int:id>")
    @requires_auth(permission="get:movie-detail")
    def get_movie(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none() 
        if not movie:
            abort(404)
        return jsonify({
            "success": True, 
            "movie": movie.movie_formatted()
        }), 200
    
    
    @app.route("/movies", methods=["POST"])
    @requires_auth(permission="post:movie")
    def create_movie(jwt):
        body = request.get_json() 
        if "title" not in body or "release_date" not in body:
            abort(400)
        title = body.get("title", None)
        release_date = body.get("release_date", None) 
        release_date = datetime.datetime.strptime(release_date, '%Y-%m-%d')
        print(release_date)
    
        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
        except:
            abort(422) 
        return jsonify({"success": True, "movie": movie.movie_formatted()}), 201
    
    
    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth(permission="patch:movie")
    def update_movie(jwt,id):
        if not id:
            abort(404) 
        body = request.get_json() 
        try:
            release_date = body.get("release_date", None) 
            title = body.get("title", None)
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                abort(404)
            if release_date is not None:
                release_date = datetime.datetime.strptime(release_date, '%Y-%m-%d')
                movie.release_date = release_date
            if title is not None:
                movie.title = title
            movie.update()
        except:
            abort(422)
        return jsonify({"success": True,  "movie": movie.movie_formatted()})
    
    
    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth(permission="delete:movie")
    def delete_movie(jwt, id):
        if not id:
            abort(404)
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            movies = Movie.query.all()
            movies = [m.movie_formatted() for m in movies]
        except:
            abort(422) 
        return jsonify({"success": True, "deleted": movie.id, "movies": movies})
    
    ## Movie Endpoints End Here
    
    
    ## Actor Endpoints Start Here 
    
    @app.route("/actors", methods=["GET"])
    @requires_auth(permission="get:actors")
    def get_actors(jwt):
        actors = Actor.query.all() 
        actors = [a.actor_formatted() for a in actors]
        return jsonify({
            "success": True, 
            "actors": actors
        }), 200
    
    
    @app.route("/actor-detail/<int:id>")
    @requires_auth(permission="get:actor-detail")
    def get_actor(jwt, id):
        actor = Actor.query.filter(Movie.id == id).one_or_none() 
        if not actor:
            abort(404)
        return jsonify({
            "success": True, 
            "movie": actor.actor_formatted()
        }), 200
    
    
    @app.route("/actors", methods=["POST"])
    @requires_auth(permission="post:actor")
    def create_actor(jwt):
        body = request.get_json() 
        if "name" not in body or "gender" not in body:
            abort(400)
        name = body.get("name", None)
        gender = body.get("gender", None) 
        try:
            actor = Actor(name=name, gender=gender)
            actor.insert()
        except:
            abort(422) 
        return jsonify({"success": True, "actor": actor.actor_formatted()}), 201
    
    
    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth(permission="patch:actor")
    def update_actor(jwt,id):
        if not id:
            abort(404) 
        body = request.get_json() 
        try:
            gender = body.get("gender", None) 
            name = body.get("name", None)
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                abort(404)
            if gender is not None:
                actor.gender = gender
            if name is not None:
                actor.name = name
            actor.update()
        except:
            abort(422)
        return jsonify({"success": True,  "actor": actor.actor_formatted()})
    
    
    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth(permission="delete:actor")
    def delete_actor(jwt, id):
        if not id:
            abort(404)
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                abort(404)
            actor.delete()
            actors = Actor.query.all()
            actors = [a.actor_formatted() for a in actors]
        except:
            abort(422) 
        return jsonify({"success": True, "deleted": actor.id, "actors": actors})
    
    
    ## Actor Endpoints End Here
    
    
    ## Error Handling
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": "unprocessable"
                        }), 422
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "not found"
                        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        "success": False, 
                        "error": 400,
                        "message": "bad request"
                        }), 400
                    
    @app.errorhandler(401)
    def not_authorized(error):
        return jsonify({
                        "success": False, 
                        "error": 401,
                        "message": "Not Authorized"
                        }), 401
    
    
    @app.errorhandler(AuthError)
    def authorization_failed(error):
        return jsonify({
                        "success": False, 
                        "error": error.status_code,
                        "message": error.error
                        }), error.status_code
    return app