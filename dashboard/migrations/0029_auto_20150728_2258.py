# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_remove_notification_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='associates',
            field=models.ManyToManyField(related_name='associates_rel_+', null=True, to='dashboard.UserProfile', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='medical_history',
            field=models.CharField(max_length=4000, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(upload_to=b'profile_pictures', blank=True),
        ),
    ]
