# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_auto_20150725_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='viewers',
            field=models.ManyToManyField(related_name='notes_view_only', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
