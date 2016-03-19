# -*- coding: utf-8 -*-
from django.db import models
from jsonfield import JSONField
import re


class Movie(models.Model):
    title = models.CharField(max_length=200)
    college_release_date = models.CharField(default='', max_length=200)
    college_release_date_confirmed = models.BooleanField(default=False)
    home_release_date = models.CharField(default='', max_length=200)
    user_rating = models.FloatField('IMDb User Rating', blank=True)
    imdb_votes = models.IntegerField('Number of Votes on IMDb', blank=True)
    critic_rating = models.IntegerField('Metascore', blank=True)
    imdb_url = models.CharField(default='', max_length=200)
    plot = models.CharField(default='', max_length=200)
    genres = JSONField(default=[])
    genres_string = models.CharField('Genres', default='', max_length=200, blank=True)
    gross = models.CharField('Gross', default='', max_length=200)
    bootstrap_color = models.CharField(default='', max_length=200)
    jeff_quality = models.IntegerField(default=0)

    @staticmethod
    def get_movie_attribute_keys():
        return list([x for x, y in Movie.get_movie_attributes()])

    @staticmethod
    def get_movie_attribute_names():
        return list([y for x, y in Movie.get_movie_attributes()])

    @staticmethod
    def get_movie_attributes():
        return [
            ('title', 'Movie'),
            ('college_release_date', 'College Release'),
            ('home_release_date', 'Home Release'),
            ('user_rating', 'IMDb'),
            ('imdb_votes', '# Ratings'),
            ('critic_rating', 'Metascore'),
            ('gross', 'Gross'),
            ('genres_string', 'Genres'),
            ('jeff_quality', 'JQ')
        ]

    def calculate_jeff_quality(self):
        points = 0

        # Account for user ratings
        if 'Comedy' in self.genres:
            if self.user_rating > 7.0:
                points += 1
        else:
            if self.user_rating > 7.5:
                points += 1

        # Account for critic ratings
        try:
            if int(self.critic_rating) > 60:
                points += 1
        except (TypeError, ValueError):
            print 'Could not parse integer value from metascore data "' + str(self.critic_rating) + '"'
        try:
            if self.gross:
                numerical_gross = re.sub(ur'[\$€,]', '', self.gross)
                numerical_gross = int(numerical_gross)
                if numerical_gross > 100000000:
                    points += 1
        except (TypeError, ValueError):
            print 'Could not parse integer value from gross data "' + str(numerical_gross) + '"'

        return points

    def calculate_bootstrap_color(self, jeff_quality):
        colors = ['danger', 'warning', 'info', 'success']
        return colors[min(len(colors) - 1, jeff_quality)]

    def print_data(self):
        return unicode(self.title) + '\n' +\
            unicode(self.college_release_date) + '\n' +\
            unicode(self.home_release_date) + '\n' +\
            unicode(self.user_rating) + '\n' +\
            unicode(self.imdb_votes) + '\n' +\
            unicode(self.critic_rating) + '\n' +\
            unicode(self.imdb_url) + '\n' +\
            unicode(self.plot) + '\n' +\
            unicode(self.genres) + '\n' +\
            unicode(self.gross)

    def save(self, *args, **kwargs):
        self.jeff_quality = self.calculate_jeff_quality()
        self.bootstrap_color = self.calculate_bootstrap_color(self.jeff_quality)
        super(Movie, self).save(*args, **kwargs)

    def __setattr__(self, name, value):
        if name == 'genres':
            if isinstance(value, list):
                if value:
                    self.genres_string = ', '.join(value)
                else:
                    self.genres_string = ''
        super.__setattr__(self, name, value)

    def __unicode__(self):
        return self.title
