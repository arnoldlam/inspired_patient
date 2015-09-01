# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0069_auto_20150901_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(default=b'patient', max_length=15, choices=[(b'professional', b'Professional'), (b'individual', b'Individual')]),
        ),
    ]
