# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0059_auto_20150808_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='office_address',
        ),
        migrations.AlterField(
            model_name='clinic',
            name='address',
            field=models.OneToOneField(related_name='clinic', to='dashboard.Address'),
        ),
    ]
