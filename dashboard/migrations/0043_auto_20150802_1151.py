# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0042_auto_20150802_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedurenote',
            name='weight',
            field=models.DecimalField(max_digits=5, decimal_places=2),
        ),
    ]
