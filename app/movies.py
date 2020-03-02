from flask import Blueprint, current_app, request, jsonify
from .models import Movie
from .serializer import MovieSchema

bp_movies = Blueprint("movies", __name__)


@bp_movies.route("/exibir", methods=["GET"])
def list():
    result = Movie.query.all()
    return MovieSchema(many=True).jsonify(result), 200


@bp_movies.route("/detalhes/<int:movie_id>", methods=["GET"])
def detail(movie_id):
    ms = MovieSchema()
    result = Movie.query.filter(Movie.id == movie_id).first()
    return ms.jsonify(result)


@bp_movies.route("/cadastrar", methods=["POST"])
def create():
    ms = MovieSchema()
    movie = ms.load(request.json)
    current_app.db.session.add(movie)
    current_app.db.session.commit()
    return ms.jsonify(movie), 201


@bp_movies.route("/deletar/<int:movie_id>", methods=["DELETE"])
def delete(movie_id):
    remove_movie = Movie.query.filter(Movie.id == movie_id).delete()
    current_app.db.session.commit()
    return f"ID {movie_id} deletado", 200


@bp_movies.route("/atualizar/<int:movie_id>", methods=["PUT"])
def update(movie_id):
    ms = MovieSchema()
    movie_data = request.json
    query = Movie.query.filter(Movie.id == movie_id)
    query.update(movie_data)
    current_app.db.session.commit()
    return ms.jsonify(query.first()), 200
