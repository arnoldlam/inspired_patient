# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0045_auto_20150802_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentnote',
            name='clinic',
        ),
        migrations.AddField(
            model_name='appointmentnote',
            name='clinic',
            field=models.ForeignKey(related_name='appointments', to='dashboard.Clinic', null=True),
        ),
        migrations.RemoveField(
            model_name='appointmentnote',
            name='doctor',
        ),
        migrations.AddField(
            model_name='appointmentnote',
            name='doctor',
            field=models.ForeignKey(related_name='appointments', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
