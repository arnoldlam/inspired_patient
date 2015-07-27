# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0025_auto_20150726_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(related_name='notifications_sent', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
