# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0058_auto_20150808_1336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='office_address',
            new_name='address',
        ),
    ]
