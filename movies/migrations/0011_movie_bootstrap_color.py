# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_auto_20150802_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='bootstrap_color',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
