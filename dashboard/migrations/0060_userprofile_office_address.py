# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0059_auto_20150808_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='office_address',
            field=models.OneToOneField(related_name='professional_user_profile_office', null=True, blank=True, to='dashboard.Address'),
        ),
    ]
