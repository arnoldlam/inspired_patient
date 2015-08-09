# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0058_auto_20150808_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='office_address_city',
            field=models.CharField(max_length=30, verbose_name=b'City', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='office_address_country',
            field=models.CharField(default=b'CA', max_length=30, verbose_name=b'Country', blank=True, choices=[(b'CA', b'Canada'), (b'US', b'United States'), (b'UK', b'United Kingdom')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='office_address_postal_code',
            field=models.CharField(max_length=10, verbose_name=b'Postal Code', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='office_address_province',
            field=models.CharField(max_length=30, verbose_name=b'Province / State', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='office_address_street',
            field=models.CharField(max_length=50, verbose_name=b'Street', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='office_address_unit',
            field=models.CharField(max_length=10, verbose_name=b'Unit', blank=True),
        ),
    ]
