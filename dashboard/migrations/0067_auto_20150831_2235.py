# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0066_auto_20150831_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='requested_team_members',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='team_member_requests',
            field=models.ManyToManyField(related_name='team_member_requests_rel_+', to='dashboard.UserProfile', blank=True),
        ),
    ]
