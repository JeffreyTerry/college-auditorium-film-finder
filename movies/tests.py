from django.test import TestCase
from .models import Movie


class MovieMethodTests(TestCase):

    def test_parse_movies_from_swank(self):
        """
        parse_movies_from_swank() should return a non-empty array
        of movie objects
        """
        movies = Movie.parse_movies_from_swank()
        self.assertTrue(movies)
        for movie in movies:
            self.assertTrue(isinstance(movie, Movie))
