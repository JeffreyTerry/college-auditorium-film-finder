# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('college_release_date', models.DateField()),
                ('home_release_date', models.DateField()),
                ('user_rating', models.FloatField(verbose_name=b'IMDB User Rating')),
                ('critic_rating', models.IntegerField(verbose_name=b'Metacritic Score')),
            ],
        ),
    ]
