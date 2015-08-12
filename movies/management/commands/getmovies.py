# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime
# from lxml import etree
# from io import StringIO
# from HTMLTableParser import HTMLTableParser
from bs4 import BeautifulSoup, Tag
from imdb import IMDb
from movies.models import Movie
from arrow.parser import ParserError
import arrow
import requests
import json
import re


class Command(BaseCommand):
    help = 'Grabs movies from swank, adds IMDb data to them, then saves them to the local database'
    ia = IMDb()

    def handle(self, *args, **options):
        self.populate_movie_database()

    def populate_movie_database(self):
        movies = self.parse_movies_from_criterion()
        self.stdout.write('Done parsing data from Criterion')
        movies = self.parse_movies_from_swank()
        self.stdout.write('Done parsing data from Swank')

    def parse_movies_from_criterion(self):
        content = requests.get('http://www.criterionpicusa.com/release-schedule').text

        try:
            # Isolate the <table> html that we are going to parse
            table_header_row_index = content.index('tableJX7headerRow')
            table_element_start_index = content.rindex('<table', 0, table_header_row_index)
            table_element_end_index = content.index('</table', table_header_row_index)
            table_element_end_index = content.index('>', table_element_end_index) + 1
            table_content = content[table_element_start_index:table_element_end_index]
            # print table_content

            # Pull the table into BeautifulSoup
            soup = BeautifulSoup(table_content, 'html.parser')
            data_rows = soup.find_all('tr')

            # Parse the headers from the soup
            headers = [self.get_content_from_tag(col) for col in data_rows[0] if isinstance(col, Tag)]

            # Parse the data from the soup
            movie_list = []
            for row in data_rows[1:]:
                # Parse data from the current row
                values = [self.get_content_from_tag(col) for col in row if isinstance(col, Tag)]

                # Reformat Criterion's date data
                for i, header in enumerate(headers):
                    if 'Date' in header:
                        try:
                            date = arrow.get(values[i], 'YYYY-MM-DD')
                            values[i] = date.format('M/D/YYYY')
                        except ParserError:
                            values[i] = ''

                # Build the movie object
                dirty_movie = dict(zip(headers, values))
                movie = Movie(
                    title=dirty_movie['Title'],
                    college_release_date=dirty_movie['Criterion Date'],
                    home_release_date=dirty_movie['Home Video Release Date'])

                if Movie.objects.filter(title=dirty_movie['Title']):
                    continue
                else:
                    self.stdout.write('Finding movie data for "' + dirty_movie['Title'] + '"')

                # Add IMDb data to the movie
                if self.add_imdb_data_to_movie(movie):
                    self.save_movie_to_database(movie)

                # Add the movie to the result list
                movie_list.append(movie)
        except ValueError as e:
            self.stdout.write('Error: Could not find film list on Criterion due to error "' + str(e) + '"')
            raise

        return movie_list

    def parse_movies_from_swank(self):
        content = requests.get('http://colleges.swankmp.com/new-releases').text

        try:
            first_film_listing_controls_index = content.index('filmListingControls')
            new_releases_list = self.get_film_list_from_script(content, first_film_listing_controls_index)

            # Uncomment this and iterate over the "all_releases_list" in order to parse recent releases from Swank.
            # second_film_listing_controls_index = content.index('filmListingControls', first_film_listing_controls_index + 1)
            # recent_releases_list = self.get_film_list_from_script(content, second_film_listing_controls_index)
            # all_releases_list = new_releases_list + recent_releases_list

            movie_list = []
            for film_data in new_releases_list:
                # Replace all whitespace in all data with single spaces
                for key, attr in film_data.iteritems():
                    if isinstance(film_data[key], unicode):
                        film_data[key] = re.sub(r'\s+', ' ', film_data[key]).strip()

                film_data['Title'] = self.format_title(film_data['Title'])

                if Movie.objects.filter(title=film_data['Title']):
                    continue
                else:
                    self.stdout.write('Finding movie data for "' + film_data['Title'] + '"')

                # Build the movie object
                if not 'ReleaseDatePreRelease' in film_data or\
                        not film_data['ReleaseDatePreRelease']:
                    film_data['ReleaseDatePreRelease'] = ''
                if not 'InHomeDate' in film_data or\
                        not film_data['InHomeDate']:
                    film_data['InHomeDate'] = ''
                movie = Movie(
                    title=film_data['Title'],
                    college_release_date=film_data['ReleaseDatePreRelease'],
                    home_release_date=film_data['InHomeDate'])

                # Add IMDb data to the movie
                if self.add_imdb_data_to_movie(movie):
                    self.save_movie_to_database(movie)

                # Add the movie to the result list
                movie_list.append(movie)
        except ValueError as e:
            self.stdout.write('Error: Could not find film list on Swank due to error "' + str(e) + '"')
            raise

        return movie_list

    def get_content_from_tag(self, tag):
        while tag.find(True, class_='field'):
            tag = tag.find(True, class_='field')
        while tag.find('a'):
            tag = tag.find('a')
        return tag.contents[0]

    def get_film_list_from_script(self, content, film_listing_controls_index):
        sliced_content = content[film_listing_controls_index:]

        items_keyword_index = sliced_content.index('Items')
        headers_keyword_index = sliced_content.index('Headers')

        json_start_index = sliced_content.index('[', items_keyword_index)
        json_end_index = sliced_content.rindex(']', 0, headers_keyword_index) + 1

        film_list_content = sliced_content[json_start_index:json_end_index]
        return json.loads(film_list_content)

    def add_imdb_data_to_movie(self, movie):
        # Grab data from IMDb
        imdb_datas = Command.ia.search_movie(movie.title, results=5)

        imdb_data = None
        for data in imdb_datas:
            try:
                if not 'episode title' in data.keys()\
                        and not '(vg)' in data['long imdb canonical title'].lower()\
                        and data['year'] > datetime.now().year - 2:
                    imdb_data = data
                    break
            except KeyError:
                imdb_data = data

        if not imdb_data:
            self.stdout.write('Error: Could not find IMDb data for movie: %s' % movie)
            nothing = {}
            self.add_imdb_attr_to_movie(movie, 'genres', nothing, 'genres')
            self.add_imdb_attr_to_movie(movie, 'user_rating', nothing, 'rating')
            self.add_imdb_attr_to_movie(movie, 'critic_rating', nothing, 'metascore')
            self.add_imdb_attr_to_movie(movie, 'plot', nothing, 'plot')
            self.add_imdb_attr_to_movie(movie, 'gross', nothing, 'gross')
            self.add_imdb_attr_to_movie(movie, 'imdb_votes', nothing, 'votes')
            movie.imdb_url = '#'
            return False

        Command.ia.update(imdb_data, 'main')
        Command.ia.update(imdb_data, 'plot')
        Command.ia.update(imdb_data, 'business')
        Command.ia.update(imdb_data, 'critic reviews')
        Command.ia.update(imdb_data, 'vote details')

        # Add data to our movie object
        self.add_imdb_attr_to_movie(movie, 'genres', imdb_data, 'genres')
        self.add_imdb_attr_to_movie(movie, 'user_rating', imdb_data, 'rating')
        self.add_imdb_attr_to_movie(movie, 'critic_rating', imdb_data, 'metascore')
        self.add_imdb_attr_to_movie(movie, 'plot', imdb_data, 'plot')
        self.add_imdb_attr_to_movie(movie, 'gross', imdb_data['business'], 'gross')
        self.add_imdb_attr_to_movie(movie, 'imdb_votes', imdb_data, 'votes')
        movie.imdb_url = Command.ia.get_imdbURL(imdb_data)

        return True

    def format_title(self, title):
        result = re.sub(r'\s*\(Subtitled\)', '', title, flags=re.I)
        result = re.sub(r'\s*\(Domestic\)', '', result, flags=re.I)
        return result.title()

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

    def save_movie_to_database(self, movie):
        if not Movie.objects.filter(title=movie.title):
            movie.save()
