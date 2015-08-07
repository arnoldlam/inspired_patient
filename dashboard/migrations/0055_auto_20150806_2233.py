# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0054_auto_20150806_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentnote',
            name='frequency',
            field=models.CharField(default=b'not_repeating', max_length=150, choices=[(b'not_repeating', b'Not repeating'), (b'every_day', b'Every Day'), (b'every_week', b'Every Week'), (b'every_month', b'Every Month')]),
        ),
        migrations.AlterField(
            model_name='medicationnote',
            name='medication_frequency',
            field=models.CharField(default=b'not_repeating', max_length=150, choices=[(b'not_repeating', b'Not repeating'), (b'every_day', b'Every Day'), (b'every_week', b'Every Week'), (b'every_month', b'Every Month')]),
        ),
    ]
