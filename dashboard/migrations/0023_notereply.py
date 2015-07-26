# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0022_auto_20150725_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteReply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('author', models.ForeignKey(related_name='note_replies', to=settings.AUTH_USER_MODEL)),
                ('note', models.ForeignKey(related_name='replies', to='dashboard.Note')),
            ],
        ),
    ]
