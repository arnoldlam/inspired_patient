# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0036_auto_20150801_1352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='selfcarenote',
            old_name='selfcare_description',
            new_name='self_care_description',
        ),
    ]
