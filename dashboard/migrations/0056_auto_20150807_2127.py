# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0055_auto_20150806_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicationnote',
            name='pharmacy_address',
            field=models.ForeignKey(related_name='medication_notes', to='dashboard.Address'),
        ),
    ]
