# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_auto_20150726_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 27, 6, 24, 37, 356588, tzinfo=utc), verbose_name=b'date created', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='date_read',
            field=models.DateTimeField(null=True, verbose_name=b'date accessed', blank=True),
        ),
    ]
