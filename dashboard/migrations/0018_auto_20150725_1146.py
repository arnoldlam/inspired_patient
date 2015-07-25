# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0017_auto_20150724_1955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='users',
        ),
        migrations.AddField(
            model_name='note',
            name='editors',
            field=models.ManyToManyField(related_name='notes_read_write', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
