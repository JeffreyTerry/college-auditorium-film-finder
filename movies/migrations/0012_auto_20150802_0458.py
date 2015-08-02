# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_movie_bootstrap_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='college_release_date',
            field=models.DateField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='critic_rating',
            field=models.IntegerField(default=b'', max_length=200, verbose_name=b'Metascore'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='home_release_date',
            field=models.DateField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imdb_votes',
            field=models.IntegerField(default=b'', max_length=200, verbose_name=b'Number of Votes on IMDb'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='user_rating',
            field=models.FloatField(default=b'', max_length=200, verbose_name=b'IMDb User Rating'),
        ),
    ]
