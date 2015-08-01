# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0034_auto_20150801_1319'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MedicalInformationNote',
            new_name='ResourceNote',
        ),
    ]
