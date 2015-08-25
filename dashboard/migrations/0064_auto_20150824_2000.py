# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0063_auto_20150818_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address_country',
            field=models.CharField(default=b'CA', max_length=30, verbose_name=b'Country', choices=[(b'CA', b'Canada'), (b'US', b'United States'), (b'UK', b'United Kingdom'), (b'AU', b'Australia')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='office_address_country',
            field=models.CharField(default=b'CA', max_length=30, verbose_name=b'Office Country', blank=True, choices=[(b'CA', b'Canada'), (b'US', b'United States'), (b'UK', b'United Kingdom'), (b'AU', b'Australia')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(default=b'patient', max_length=15, choices=[(b'patient', b'Patient'), (b'caregiver', b'Caregiver'), (b'parent', b'Parent'), (b'professional', b'Professional'), (b'individual', b'Individual')]),
        ),
    ]
