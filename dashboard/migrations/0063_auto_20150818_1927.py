# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0062_auto_20150809_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactnote',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='contactnote',
            name='organization_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='contactnote',
            name='phone_number_home',
            field=models.CharField(max_length=20, verbose_name=b'Phone Number (Home)', blank=True),
        ),
        migrations.AlterField(
            model_name='contactnote',
            name='phone_number_work',
            field=models.CharField(max_length=20, verbose_name=b'Phone Number (Work)', blank=True),
        ),
    ]
