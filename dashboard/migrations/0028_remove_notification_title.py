# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_auto_20150726_2324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='title',
        ),
    ]
