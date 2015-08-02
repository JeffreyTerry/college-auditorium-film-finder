# -*- coding: utf-8 -*-
from django.apps import AppConfig
from imdb import IMDb
from datetime import datetime
import threading
import requests
import json
import re
import os


class MoviesAppConfig(AppConfig):
    name = 'movies'
    verbose_name = 'Movies App'
    ia = IMDb()

    def ready(self):
        if not 'POPULATING_MOVIE_DATABASE' in os.environ:
            os.environ['POPULATING_MOVIE_DATABASE'] = 'True'
            thread = threading.Thread(target=self.populate_movie_database)
            thread.start()

    def populate_movie_database(self):
        movies = self.parse_movies_from_swank()
        self.save_movies_to_database(movies)
        print 'Done parsing data from Swank'
        os.environ['POPULATING_MOVIE_DATABASE'] = ''
        del os.environ['POPULATING_MOVIE_DATABASE']

    def parse_movies_from_swank(self):
        content = requests.get('http://colleges.swankmp.com/new-releases').text

        try:
            film_listing_controls_index = content.index('filmListingControls')

            items_keyword_index = content.index('Items', film_listing_controls_index)
            headers_keyword_index = content.index('Headers', film_listing_controls_index)

            json_start_index = content.index('[', items_keyword_index)
            json_end_index = content.rindex(']', 0, headers_keyword_index) + 1

            film_list_content = content[json_start_index:json_end_index]
            film_list = json.loads(film_list_content)

            Movie = self.get_model('Movie')
            movie_list = []
            # i = 0
            for film_data in film_list:
                # i += 1
                # if i > 200:
                #     break

                # Replace all whitespace with single spaces
                for key, attr in film_data.iteritems():
                    if isinstance(film_data[key], unicode):
                        film_data[key] = re.sub(r'\s+', ' ', film_data[key]).strip()

                film_data['Title'] = self.format_title(film_data['Title'])

                if Movie.objects.filter(title=film_data['Title']):
                    continue
                else:
                    print 'Finding movie data for "' + film_data['Title'] + '"'

                # if not "Insurgent" in film_data['Title']:
                #     continue

                # Build the movie object
                if not film_data['ReleaseDatePreRelease']:
                    film_data['ReleaseDatePreRelease'] = ''
                if not film_data['InHomeDate']:
                    film_data['InHomeDate'] = ''
                movie = Movie(
                    title=film_data['Title'],
                    college_release_date=film_data['ReleaseDatePreRelease'],
                    home_release_date=film_data['InHomeDate'])

                # Add IMDb data to the movie
                self.add_imdb_data_to_movie(movie)

                # Add the movie to the result list
                movie_list.append(movie)
        except ValueError as e:
            print 'Error: Could not find film list on Swank due to error "' + str(e) + '"'
            raise

        return movie_list

    def add_imdb_data_to_movie(self, movie):
        # Grab data from IMDb
        imdb_datas = MoviesAppConfig.ia.search_movie(movie.title, results=5)

        imdb_data = None
        for data in imdb_datas:
            if not 'episode title' in data.keys()\
                    and not '(vg)' in data['long imdb canonical title'].lower()\
                    and data['year'] > datetime.now().year - 2:
                imdb_data = data
                break

        if not imdb_data:
            print 'Error: Could not find IMDb data for movie: %s' % movie
            nothing = {}
            self.add_imdb_attr_to_movie(movie, 'genres', nothing, 'genres')
            self.add_imdb_attr_to_movie(movie, 'user_rating', nothing, 'rating')
            self.add_imdb_attr_to_movie(movie, 'critic_rating', nothing, 'metascore')
            self.add_imdb_attr_to_movie(movie, 'plot', nothing, 'plot')
            self.add_imdb_attr_to_movie(movie, 'gross', nothing, 'gross')
            self.add_imdb_attr_to_movie(movie, 'imdb_votes', nothing, 'votes')
            movie.imdb_url = '#'
            return

        MoviesAppConfig.ia.update(imdb_data, 'main')
        MoviesAppConfig.ia.update(imdb_data, 'plot')
        MoviesAppConfig.ia.update(imdb_data, 'business')
        MoviesAppConfig.ia.update(imdb_data, 'critic reviews')
        MoviesAppConfig.ia.update(imdb_data, 'vote details')

        # Add data to our movie object
        self.add_imdb_attr_to_movie(movie, 'genres', imdb_data, 'genres')
        self.add_imdb_attr_to_movie(movie, 'user_rating', imdb_data, 'rating')
        self.add_imdb_attr_to_movie(movie, 'critic_rating', imdb_data, 'metascore')
        self.add_imdb_attr_to_movie(movie, 'plot', imdb_data, 'plot')
        self.add_imdb_attr_to_movie(movie, 'gross', imdb_data['business'], 'gross')
        self.add_imdb_attr_to_movie(movie, 'imdb_votes', imdb_data, 'votes')
        movie.imdb_url = MoviesAppConfig.ia.get_imdbURL(imdb_data)

    def format_title(self, title):
        return re.sub(r'\s*\(Subtitled\)', '', title, flags=re.I).title()

    def add_imdb_attr_to_movie(self, movie, movie_attr, imdb_data, imdb_attr):
        try:
            attr = imdb_data[imdb_attr]
            if isinstance(attr, list) and imdb_attr != 'genres':
                attr = attr[0]
            if imdb_attr == 'gross':
                match = re.match(ur'[\$€][1-9][0-9,]+', attr)
                if match:
                    attr = match.group(0)
            setattr(movie, movie_attr, attr)
        except (KeyError, IndexError):
            if movie_attr == 'user_rating' or\
                    movie_attr == 'critic_rating' or\
                    movie_attr == 'imdb_votes':
                setattr(movie, movie_attr, 0)
            else:
                setattr(movie, movie_attr, '')

    def save_movies_to_database(self, movies):
        for movie in movies:
            movie.save()
