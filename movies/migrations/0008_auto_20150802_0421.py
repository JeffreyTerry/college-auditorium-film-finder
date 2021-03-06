# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_auto_20150802_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='critic_rating',
            field=models.CharField(default=b'N/A', max_length=200, verbose_name=b'Metascore'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imdb_votes',
            field=models.CharField(default=b'N/A', max_length=200, verbose_name=b'Number of Votes on IMDb'),
        ),
    ]
