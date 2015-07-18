# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_remove_note_testing'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='testing',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
