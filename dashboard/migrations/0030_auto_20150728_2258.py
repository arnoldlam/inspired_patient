# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_auto_20150728_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='associates',
            field=models.ManyToManyField(related_name='associates_rel_+', to='dashboard.UserProfile', blank=True),
        ),
    ]
