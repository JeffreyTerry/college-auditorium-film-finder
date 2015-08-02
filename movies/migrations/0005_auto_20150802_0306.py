# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_remove_movie_box_office_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genres_string',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'Genres'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='gross',
            field=models.CharField(default=b'0', max_length=200, verbose_name=b'Gross'),
        ),
    ]
