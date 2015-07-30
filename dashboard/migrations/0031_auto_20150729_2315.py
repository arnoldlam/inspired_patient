# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0030_auto_20150728_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='job_title',
            field=models.CharField(default='None', max_length=100, verbose_name=b'Job Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='office_address',
            field=models.CharField(default='None', max_length=250, verbose_name=b'Office Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='office_email',
            field=models.EmailField(default='some@email.com', max_length=254, verbose_name=b'Office Email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='office_tel',
            field=models.CharField(default='None', max_length=50, verbose_name=b'Office Telephone'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='qualification',
            field=models.CharField(default='None', max_length=250),
            preserve_default=False,
        ),
    ]
