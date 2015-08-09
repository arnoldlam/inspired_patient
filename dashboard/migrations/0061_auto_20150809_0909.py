# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0060_auto_20150808_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='communicationnote',
            name='recipient_team_member',
            field=models.ForeignKey(related_name='communication_notes_team_member', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='communicationnote',
            name='clinic',
            field=models.ForeignKey(related_name='communication_notes', blank=True, to='dashboard.Clinic', null=True),
        ),
        migrations.AlterField(
            model_name='communicationnote',
            name='doctor',
            field=models.ForeignKey(related_name='communication_notes_doctor', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
