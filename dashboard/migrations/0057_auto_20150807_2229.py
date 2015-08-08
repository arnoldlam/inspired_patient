# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0056_auto_20150807_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date_and_time',
            field=models.DateTimeField(null=True, verbose_name=b'Date and Time', blank=True),
        ),
    ]
