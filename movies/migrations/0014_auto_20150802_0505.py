# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_auto_20150802_0500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='college_release_date',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='home_release_date',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
