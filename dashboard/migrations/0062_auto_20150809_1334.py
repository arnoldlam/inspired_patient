# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0061_auto_20150809_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='office_address_city',
            field=models.CharField(max_length=30, verbose_name=b'Office City', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='office_address_country',
            field=models.CharField(default=b'CA', max_length=30, verbose_name=b'Office Country', blank=True, choices=[(b'CA', b'Canada'), (b'US', b'United States'), (b'UK', b'United Kingdom')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='office_address_postal_code',
            field=models.CharField(max_length=10, verbose_name=b'Office Postal Code', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='office_address_province',
            field=models.CharField(max_length=30, verbose_name=b'Office Province / State', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='office_address_street',
            field=models.CharField(max_length=50, verbose_name=b'Office Street', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='office_address_unit',
            field=models.CharField(max_length=10, verbose_name=b'Office Unit', blank=True),
        ),
    ]
