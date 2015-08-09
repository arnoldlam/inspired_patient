# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0059_auto_20150808_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='office_address',
        ),
    ]
