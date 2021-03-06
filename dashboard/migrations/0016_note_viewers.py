# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0015_delete_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='viewers',
            field=models.ManyToManyField(related_name='note_view_only', to=settings.AUTH_USER_MODEL),
        ),
    ]
