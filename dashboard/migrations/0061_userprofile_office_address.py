# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0060_remove_userprofile_office_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='office_address',
            field=models.CharField(max_length=250, verbose_name=b'Office Address', blank=True),
        ),
    ]
