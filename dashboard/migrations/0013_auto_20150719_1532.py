# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20150719_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dischargenote',
            name='next_dose',
            field=models.CharField(max_length=50),
        ),
    ]
