# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_auto_20150725_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='viewers',
            field=models.ManyToManyField(related_name='notes_read_only', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
