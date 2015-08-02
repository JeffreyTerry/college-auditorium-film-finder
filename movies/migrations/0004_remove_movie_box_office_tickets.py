# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20150802_0252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='box_office_tickets',
        ),
    ]
