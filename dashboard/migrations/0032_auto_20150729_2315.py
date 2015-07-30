# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_auto_20150729_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='job_title',
            field=models.CharField(max_length=100, verbose_name=b'Job Title', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='office_address',
            field=models.CharField(max_length=250, verbose_name=b'Office Address', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='office_email',
            field=models.EmailField(max_length=254, verbose_name=b'Office Email', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='office_tel',
            field=models.CharField(max_length=50, verbose_name=b'Office Telephone', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='qualification',
            field=models.CharField(max_length=250, blank=True),
        ),
    ]
