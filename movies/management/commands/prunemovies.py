# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime
from movies.models import Movie
import arrow


def date_cmp(x, y):
    d1 = arrow.get(x, 'M/D/YYYY')
    d2 = arrow.get(y, 'M/D/YYYY')
    return cmp(d1, d2)

class Command(BaseCommand):
    help = 'Removes old movies from the database'

    def handle(self, *args, **options):
        self.prune_movie_database()

    def prune_movie_database(self):
        movies = Movie.objects.all()
        cutoff_date = arrow.now().replace(weeks=-8)
        old_movies = filter(lambda movie:
            arrow.get(movie.college_release_date, 'M/D/YYYY') < cutoff_date, movies)
        for movie in old_movies:
            print movie
            movie.delete()

