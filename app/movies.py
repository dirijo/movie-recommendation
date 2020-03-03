from flask import Blueprint, current_app, jsonify, redirect, request, url_for
from .models import Movie
from .serializer import MovieSchema

bp_movies = Blueprint("movies", __name__)


@bp_movies.route("/list", methods=["GET"])
def list():
    result = Movie.query.all()
    return MovieSchema(many=True).jsonify(result), 200


@bp_movies.route("/details/<int:movie_id>", methods=["GET"])
def detail(movie_id):
    ms = MovieSchema()
    result = Movie.query.filter(Movie.id == movie_id).first()
    if result:
        return ms.jsonify(result), 200
    response = {"message": f"404 - ID {movie_id} not found"}
    return jsonify(response), 404


@bp_movies.route("/create", methods=["POST"])
def create():
    ms = MovieSchema()
    movie = ms.load(request.json)
    current_app.db.session.add(movie)
    current_app.db.session.commit()
    return ms.jsonify(movie), 201


@bp_movies.route("/delete/<int:movie_id>", methods=["DELETE"])
def delete(movie_id):
    remove_movie = Movie.query.filter(Movie.id == movie_id).delete()
    current_app.db.session.commit()
    if remove_movie:
        response = {"message": f"ID {movie_id} has been deleted"}
        return jsonify(response), 200
    response = {"message": f"404 - ID {movie_id}  not found"}
    return jsonify(response), 404


@bp_movies.route("/update/<int:movie_id>", methods=["PUT"])
def update(movie_id):
    query = Movie.query.filter(Movie.id == movie_id).update(request.json)
    current_app.db.session.commit()
    if query:
        response = {"message": f"200 - ID {movie_id} updated"}
        return jsonify(response), 200
    response = {"message": f"404 - ID {movie_id} not found"}
    return jsonify(response), 404
