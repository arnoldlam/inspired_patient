# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0046_auto_20150802_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactNote',
            fields=[
                ('note_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dashboard.Note')),
                ('user', models.OneToOneField(related_name='contact_note', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('dashboard.note',),
        ),
    ]
