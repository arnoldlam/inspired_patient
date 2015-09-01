# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0068_auto_20150831_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='team_member_requests',
            field=models.ManyToManyField(related_name='requested_team_members', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
