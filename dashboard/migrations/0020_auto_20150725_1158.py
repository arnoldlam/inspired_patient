# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_auto_20150725_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date_accessed',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date accessed'),
        ),
    ]
