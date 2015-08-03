# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0052_auto_20150803_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentnote',
            name='date_and_time',
        ),
        migrations.RemoveField(
            model_name='medicationnote',
            name='date_and_time',
        ),
        migrations.RemoveField(
            model_name='selfcarenote',
            name='date_and_time',
        ),
        migrations.AddField(
            model_name='note',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 3, 23, 33, 13, 576373, tzinfo=utc), verbose_name=b'Date and Time', blank=True),
            preserve_default=False,
        ),
    ]
