# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20150802_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='gross',
            field=models.CharField(default=b'N/A', max_length=200, verbose_name=b'Gross'),
        ),
    ]
