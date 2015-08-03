# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0050_medicationnote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentnote',
            name='date',
        ),
        migrations.RemoveField(
            model_name='appointmentnote',
            name='time',
        ),
        migrations.AddField(
            model_name='appointmentnote',
            name='date_and_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 3, 22, 56, 8, 732852, tzinfo=utc), verbose_name=b'Date and Time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='note',
            name='note_type',
            field=models.CharField(default=b'general_note', max_length=20, choices=[(b'general_note', b'General note'), (b'instruction_note', b'Instruction note'), (b'communication_note', b'Communication note'), (b'procedure_note', b'Procedure note'), (b'self_care_note', b'Self care note'), (b'resource_note', b'Resource note'), (b'appointment_note', b'Appointment note'), (b'contact_note', b'Contact note'), (b'medication_note', b'Medication note')]),
        ),
    ]
