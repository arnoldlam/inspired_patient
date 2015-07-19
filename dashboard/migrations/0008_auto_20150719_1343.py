# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20150718_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communicationnote',
            name='instructions',
        ),
        migrations.AlterField(
            model_name='communicationnote',
            name='importance',
            field=models.CharField(default=b'read', max_length=20, choices=[(b'read', b'Read'), (b'respond', b'Respond'), (b'urgent', b'Urgent')]),
        ),
    ]
