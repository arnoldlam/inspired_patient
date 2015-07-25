# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20150725_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='author',
            field=models.ForeignKey(related_name='authored_notes', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='note_type',
            field=models.CharField(default=b'general_note', max_length=20, choices=[(b'general_note', b'General note'), (b'instruction_note', b'Instruction note'), (b'communication_note', b'Communication note'), (b'discharge_note', b'Discharge note')]),
        ),
    ]
