# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0057_auto_20150807_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notebook',
            name='notes',
            field=models.ManyToManyField(related_name='notebooks', to='dashboard.Note', blank=True),
        ),
    ]
