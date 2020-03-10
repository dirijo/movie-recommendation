from json import dumps
from unittest import mock
from flask import url_for
from .flask_base_test_case import TestFlaskBase
from app.models import Movie
import app.movies


class TestMovies(TestFlaskBase):
    def test_api_should_register_a_movie(self):
        import ipdb; ipdb.set_trace()
        
        self.movie_create_called = False
        def fake_create(title):
            self.movie_create_called = True
            self.status_code = 201
            self.movie = {
                'id': 1,
                'title': title.get('title')
            }
        app.movies.create = fake_create

        movie = {'title': 'Scary Movie'}
        result = self.client.post('/create', json=movie)
        self.assertTrue(self.movie_create_called)
