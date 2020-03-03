from flask import url_for
from .flask_base_test_case import TestFlaskSystem
from app.models import Movie


class TestMovieBP(TestFlaskSystem):
    def test_api_should_register_a_movie(self):
        movie = {"title": "a very bad movie"}
        expected = {"id": 1, "title": "a very bad movie"}
        response = self.client.post(url_for("movies.create"), json=movie)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["title"], expected["title"])

    def test_api_should_update_a_movie(self):
        new_movie = {"title": "o violão triste"}
        movie = {"title": "a gaita"}
        self.client.post(url_for("movies.create"), json=movie)
        mv_object = Movie.query.first()
        response = self.client.put(
            url_for("movies.update", movie_id=mv_object.id), json=new_movie
        )
        expected = {"message": f"200 - ID {mv_object.id} updated"}
        self.assertEqual(expected, response.json)
        self.assertEqual(200, response.status_code)

    def test_api_should_not_update_a_movie_with_wrong_id(self):
        wrong_id = 23
        new_movie = {"title": "o violão triste"}
        response = self.client.put(
            url_for("movies.update", movie_id=wrong_id), json=new_movie
        )
        expected = {"message": f"404 - ID {wrong_id} not found"}
        self.assertEqual(expected, response.json)
        self.assertEqual(404, response.status_code)

    def test_api_should_get_movie_detail(self):
        movie = {"title": "power rangers"}
        self.client.post(url_for("movies.create"), json=movie)
        mv_object = Movie.query.first()
        response = self.client.get(url_for("movies.detail", movie_id=mv_object.id))
        expected = {"id": 1, "title": "power rangers"}
        self.assertEqual(expected, response.json)
        self.assertEqual(200, response.status_code)

    def test_api_should_return_404_message_when_movie_does_not_exists(self):
        wrong_id = 2
        response = self.client.get(url_for("movies.detail", movie_id=wrong_id))
        expected = {"message": f"404 - ID {wrong_id} not found"}
        self.assertEqual(expected, response.json)
        self.assertEqual(404, response.status_code)

    def test_api_should_get_movie_list(self):
        first_movie = {"title": "power rangers"}
        second_movie = {"title": "scary movie"}
        self.client.post(url_for("movies.create"), json=first_movie)
        self.client.post(url_for("movies.create"), json=second_movie)
        response = self.client.get(url_for("movies.list"))
        expected = [
            {"id": 1, "title": "power rangers"},
            {"id": 2, "title": "scary movie"},
        ]
        self.assertEqual(expected, response.json)
        self.assertEqual(200, response.status_code)

    def test_api_should_delete_a_movie(self):
        movie = {"title": "scary movie"}
        self.client.post(url_for("movies.create"), json=movie)
        mv_object = Movie.query.first()
        response = self.client.delete(url_for("movies.delete", movie_id=mv_object.id))

        expected = {"message": f"ID {mv_object.id} has been deleted"}
        self.assertEqual(expected, response.json)
        self.assertEqual(200, response.status_code)

    def test_api_should_return_404_when_id_does_not_exists(self):
        wrong_id = 999999
        response = self.client.delete(url_for("movies.delete", movie_id=wrong_id))
        expected = {"message": f"404 - ID {wrong_id}  not found"}
        self.assertEqual(expected, response.json)
        self.assertEqual(404, response.status_code)
