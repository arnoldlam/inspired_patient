# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20150719_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dischargenote',
            name='emergency_instructions',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='dischargenote',
            name='selfcare_instructions',
            field=models.TextField(),
        ),
    ]
