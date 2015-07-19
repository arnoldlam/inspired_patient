# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20150717_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='notebook',
            name='date_accessed',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 19, 0, 23, 37, 897367, tzinfo=utc), verbose_name=b'date accessed', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notebook',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 19, 0, 23, 47, 289111, tzinfo=utc), verbose_name=b'date created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notebook',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 19, 0, 23, 50, 824975, tzinfo=utc), verbose_name=b'date modified', blank=True),
            preserve_default=False,
        ),
    ]
