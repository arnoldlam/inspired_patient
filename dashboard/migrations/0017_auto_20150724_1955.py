# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_note_viewers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='users',
            field=models.ManyToManyField(related_name='notes', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='viewers',
            field=models.ManyToManyField(related_name='note_view_only', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
