# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0023_notereply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('view_status', models.CharField(default=b'unread', max_length=15, choices=[(b'unread', b'Unread'), (b'read', b'Read')])),
                ('message', models.CharField(max_length=400)),
                ('action_url', models.URLField(blank=True)),
                ('recipient', models.ForeignKey(related_name='notifications_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='notifications_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
