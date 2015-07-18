# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20150717_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address_province',
            field=models.CharField(max_length=30, verbose_name=b'Province / State'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(default=b'patient', max_length=15, choices=[(b'patient', b'Patient'), (b'caregiver', b'Caregiver'), (b'parent', b'Parent'), (b'professional', b'Professional')]),
        ),
    ]
