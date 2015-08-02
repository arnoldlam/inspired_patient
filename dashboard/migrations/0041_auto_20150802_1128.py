# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0040_auto_20150801_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='users',
        ),
        migrations.AlterField(
            model_name='procedurenote',
            name='procedure',
            field=models.TextField(),
        ),
    ]
