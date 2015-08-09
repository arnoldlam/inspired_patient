# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0058_auto_20150808_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='office_address',
            field=models.ForeignKey(blank=True, to='dashboard.Address', null=True),
        ),
    ]
