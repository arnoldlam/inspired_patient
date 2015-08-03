# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0049_auto_20150802_1705'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicationNote',
            fields=[
                ('note_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dashboard.Note')),
                ('medication_name', models.CharField(max_length=100)),
                ('medication_dosage', models.CharField(max_length=100)),
                ('medication_frequency', models.CharField(max_length=100)),
                ('medication_duration', models.CharField(max_length=100)),
                ('pharmacy_name', models.CharField(max_length=50)),
                ('pharmacy_telephone', models.CharField(max_length=50)),
                ('pharmacy_address', models.OneToOneField(related_name='medication_notes', to='dashboard.Address')),
            ],
            bases=('dashboard.note',),
        ),
    ]
