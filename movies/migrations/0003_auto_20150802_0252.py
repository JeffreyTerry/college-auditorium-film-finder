# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_box_office_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=jsonfield.fields.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='movie',
            name='gross',
            field=models.CharField(default=0, max_length=200, verbose_name=b'Gross'),
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_url',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_votes',
            field=models.IntegerField(default=0, verbose_name=b'Number of Votes on IMDb'),
        ),
        migrations.AddField(
            model_name='movie',
            name='plot',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='box_office_tickets',
            field=models.CharField(default=0, max_length=200, verbose_name=b'Deprecated'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='college_release_date',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='critic_rating',
            field=models.IntegerField(verbose_name=b'Metascore'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='home_release_date',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='user_rating',
            field=models.FloatField(verbose_name=b'IMDb User Rating'),
        ),
    ]
