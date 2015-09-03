# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=4000)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('author_name', models.CharField(max_length=100)),
            ],
        ),
    ]
