# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0073_privacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='done_status',
            field=models.CharField(default=b'incomplete', max_length=20, choices=[(b'incomplete', b'Incomplete'), (b'complete', b'Complete')]),
        ),
    ]
