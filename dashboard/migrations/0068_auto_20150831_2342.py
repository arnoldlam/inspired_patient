# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0067_auto_20150831_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address_city',
            field=models.CharField(max_length=30, verbose_name=b'City', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_country',
            field=models.CharField(default=b'CA', max_length=30, verbose_name=b'Country', blank=True, choices=[(b'CA', b'Canada'), (b'US', b'United States'), (b'UK', b'United Kingdom'), (b'AU', b'Australia')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_postal_code',
            field=models.CharField(max_length=10, verbose_name=b'Postal Code', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_province',
            field=models.CharField(max_length=30, verbose_name=b'Province / State', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_street',
            field=models.CharField(max_length=50, verbose_name=b'Street', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address_unit',
            field=models.CharField(max_length=10, verbose_name=b'Unit', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='title',
            field=models.CharField(max_length=15, blank=True),
        ),
    ]
