# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_auto_20150802_0458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='critic_rating',
            field=models.IntegerField(verbose_name=b'Metascore', blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imdb_votes',
            field=models.IntegerField(verbose_name=b'Number of Votes on IMDb', blank=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='user_rating',
            field=models.FloatField(verbose_name=b'IMDb User Rating', blank=True),
        ),
    ]
