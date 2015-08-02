# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20150802_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genres_string',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'Genres', blank=True),
        ),
    ]
