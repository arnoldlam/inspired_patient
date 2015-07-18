# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_note_testing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='testing',
        ),
    ]
