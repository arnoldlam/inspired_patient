# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20150719_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dischargenote',
            name='weight',
            field=models.IntegerField(),
        ),
    ]
