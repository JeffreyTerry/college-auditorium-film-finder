# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='box_office_tickets',
            field=models.CharField(default=0, max_length=200, verbose_name=b'Box Office Numbers'),
        ),
    ]
