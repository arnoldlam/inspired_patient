# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0064_auto_20150824_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicationnote',
            name='medication_frequency',
        ),
        migrations.RemoveField(
            model_name='selfcarenote',
            name='frequency',
        ),
        migrations.AlterField(
            model_name='notebook',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
