# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0014_auto_20150802_0505'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='jeff_quality',
            field=models.IntegerField(default=0),
        ),
    ]
