# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0041_auto_20150802_1128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='procedurenote',
            old_name='selfcare_instructions',
            new_name='self_care_instructions',
        ),
    ]
