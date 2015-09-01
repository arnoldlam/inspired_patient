# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0065_auto_20150830_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notereply',
            name='title',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='requested_team_members',
            field=models.ManyToManyField(related_name='requested_team_members_rel_+', to='dashboard.UserProfile', blank=True),
        ),
    ]
