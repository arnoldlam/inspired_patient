# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20150719_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='follow_up',
            field=models.CharField(max_length=250, blank=True),
        ),
    ]
