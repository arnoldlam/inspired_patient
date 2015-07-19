# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20150718_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notebook',
            name='date_accessed',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date accessed'),
        ),
        migrations.AlterField(
            model_name='notebook',
            name='date_modified',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date modified'),
        ),
    ]
