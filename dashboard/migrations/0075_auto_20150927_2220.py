# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0074_note_done_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='done_status',
            field=models.CharField(default=b'incomplete', max_length=20, blank=True, choices=[(b'incomplete', b'Incomplete'), (b'complete', b'Complete')]),
        ),
    ]
