# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20150802_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='college_release_date',
            field=models.CharField(default=b'N/A', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres_string',
            field=models.CharField(default=b'N/A', max_length=200, verbose_name=b'Genres', blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='home_release_date',
            field=models.CharField(default=b'N/A', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imdb_url',
            field=models.CharField(default=b'N/A', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='plot',
            field=models.CharField(default=b'N/A', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='user_rating',
            field=models.CharField(default=b'N/A', max_length=200, verbose_name=b'IMDb User Rating'),
        ),
    ]
