# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0053_auto_20150803_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selfcarenote',
            name='frequency',
            field=models.CharField(default=b'not_repeating', max_length=150, choices=[(b'not_repeating', b'Not repeating'), (b'every_day', b'Every Day'), (b'every_week', b'Every Week'), (b'every_month', b'Every Month')]),
        ),
    ]
