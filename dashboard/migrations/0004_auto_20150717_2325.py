# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_remove_note_testing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address_country',
            field=models.CharField(default=b'CA', max_length=30, verbose_name=b'Country', choices=[(b'CA', b'Canada'), (b'US', b'United States'), (b'UK', b'United Kingdom')]),
        ),
    ]
