# # -*- coding: utf-8 -*-
# from django.apps import AppConfig
# from imdb import IMDb
# from datetime import datetime
# import threading
# import requests
# import json
# import re
# import os


# class MoviesAppConfig(AppConfig):
#     name = 'movies'
#     verbose_name = 'Movies App'
#     ia = IMDb()

#     def ready(self):
#         if not 'POPULATING_MOVIE_DATABASE' in os.environ:
#             self.Movie = self.get_model('Movie')
#             os.environ['POPULATING_MOVIE_DATABASE'] = 'True'
#             thread = threading.Thread(target=self.populate_movie_database)
#             thread.start()

#     def populate_movie_database(self):
#         movies = self.parse_movies_from_swank()
#         print 'Done parsing data from Swank'
#         os.environ['POPULATING_MOVIE_DATABASE'] = ''
#         del os.environ['POPULATING_MOVIE_DATABASE']

#     def parse_movies_from_swank(self):
#         content = requests.get('http://colleges.swankmp.com/new-releases').text

#         try:
#             first_film_listing_controls_index = content.index('filmListingControls')
#             new_releases_list = self.get_film_list_from_script(content, first_film_listing_controls_index)

#             second_film_listing_controls_index = content.index('filmListingControls', first_film_listing_controls_index + 1)
#             recent_releases_list = self.get_film_list_from_script(content, second_film_listing_controls_index)

#             all_releases_list = new_releases_list + recent_releases_list
#             movie_list = []
#             for film_data in all_releases_list:
#                 # Replace all whitespace in all data with single spaces
#                 for key, attr in film_data.iteritems():
#                     if isinstance(film_data[key], unicode):
#                         film_data[key] = re.sub(r'\s+', ' ', film_data[key]).strip()

#                 film_data['Title'] = self.format_title(film_data['Title'])

#                 if self.Movie.objects.filter(title=film_data['Title']):
#                     continue
#                 else:
#                     print 'Finding movie data for "' + film_data['Title'] + '"'

#                 # Build the movie object
#                 if not 'ReleaseDatePreRelease' in film_data or\
#                         not film_data['ReleaseDatePreRelease']:
#                     film_data['ReleaseDatePreRelease'] = ''
#                 if not 'InHomeDate' in film_data or\
#                         not film_data['InHomeDate']:
#                     film_data['InHomeDate'] = ''
#                 movie = self.Movie(
#                     title=film_data['Title'],
#                     college_release_date=film_data['ReleaseDatePreRelease'],
#                     home_release_date=film_data['InHomeDate'])

#                 # Add IMDb data to the movie
#                 if self.add_imdb_data_to_movie(movie):
#                     self.save_movie_to_database(movie)

#                 # Add the movie to the result list
#                 movie_list.append(movie)
#         except ValueError as e:
#             print 'Error: Could not find film list on Swank due to error "' + str(e) + '"'
#             raise

#         return movie_list

#     def get_film_list_from_script(self, content, film_listing_controls_index):
#         sliced_content = content[film_listing_controls_index:]

#         items_keyword_index = sliced_content.index('Items')
#         headers_keyword_index = sliced_content.index('Headers')

#         json_start_index = sliced_content.index('[', items_keyword_index)
#         json_end_index = sliced_content.rindex(']', 0, headers_keyword_index) + 1

#         film_list_content = sliced_content[json_start_index:json_end_index]
#         return json.loads(film_list_content)

#     def add_imdb_data_to_movie(self, movie):
#         # Grab data from IMDb
#         imdb_datas = MoviesAppConfig.ia.search_movie(movie.title, results=5)

#         imdb_data = None
#         for data in imdb_datas:
#             try:
#                 if not 'episode title' in data.keys()\
#                         and not '(vg)' in data['long imdb canonical title'].lower()\
#                         and data['year'] > datetime.now().year - 2:
#                     imdb_data = data
#                     break
#             except KeyError:
#                 imdb_data = data

#         if not imdb_data:
#             print 'Error: Could not find IMDb data for movie: %s' % movie
#             nothing = {}
#             self.add_imdb_attr_to_movie(movie, 'genres', nothing, 'genres')
#             self.add_imdb_attr_to_movie(movie, 'user_rating', nothing, 'rating')
#             self.add_imdb_attr_to_movie(movie, 'critic_rating', nothing, 'metascore')
#             self.add_imdb_attr_to_movie(movie, 'plot', nothing, 'plot')
#             self.add_imdb_attr_to_movie(movie, 'gross', nothing, 'gross')
#             self.add_imdb_attr_to_movie(movie, 'imdb_votes', nothing, 'votes')
#             movie.imdb_url = '#'
#             return False

#         MoviesAppConfig.ia.update(imdb_data, 'main')
#         MoviesAppConfig.ia.update(imdb_data, 'plot')
#         MoviesAppConfig.ia.update(imdb_data, 'business')
#         MoviesAppConfig.ia.update(imdb_data, 'critic reviews')
#         MoviesAppConfig.ia.update(imdb_data, 'vote details')

#         # Add data to our movie object
#         self.add_imdb_attr_to_movie(movie, 'genres', imdb_data, 'genres')
#         self.add_imdb_attr_to_movie(movie, 'user_rating', imdb_data, 'rating')
#         self.add_imdb_attr_to_movie(movie, 'critic_rating', imdb_data, 'metascore')
#         self.add_imdb_attr_to_movie(movie, 'plot', imdb_data, 'plot')
#         self.add_imdb_attr_to_movie(movie, 'gross', imdb_data['business'], 'gross')
#         self.add_imdb_attr_to_movie(movie, 'imdb_votes', imdb_data, 'votes')
#         movie.imdb_url = MoviesAppConfig.ia.get_imdbURL(imdb_data)

#         return True

#     def format_title(self, title):
#         result = re.sub(r'\s*\(Subtitled\)', '', title, flags=re.I)
#         result = re.sub(r'\s*\(Domestic\)', '', result, flags=re.I)
#         return result.title()

#     def add_imdb_attr_to_movie(self, movie, movie_attr, imdb_data, imdb_attr):
#         try:
#             attr = imdb_data[imdb_attr]
#             if isinstance(attr, list) and imdb_attr != 'genres':
#                 attr = attr[0]
#             if imdb_attr == 'gross':
#                 match = re.match(ur'[\$€][1-9][0-9,]+', attr)
#                 if match:
#                     attr = match.group(0)
#             setattr(movie, movie_attr, attr)
#         except (KeyError, IndexError):
#             if movie_attr == 'user_rating' or\
#                     movie_attr == 'critic_rating' or\
#                     movie_attr == 'imdb_votes':
#                 setattr(movie, movie_attr, 0)
#             else:
#                 setattr(movie, movie_attr, '')

#     def save_movie_to_database(self, movie):
#         if not self.Movie.objects.filter(title=movie.title):
#             movie.save()
