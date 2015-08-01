# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0032_auto_20150729_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='users',
            field=models.ManyToManyField(related_name='notes', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
