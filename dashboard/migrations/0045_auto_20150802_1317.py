# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0044_appointmentnote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_type',
            field=models.CharField(default=b'general_note', max_length=20, choices=[(b'general_note', b'General note'), (b'instruction_note', b'Instruction note'), (b'communication_note', b'Communication note'), (b'procedure_note', b'Procedure note'), (b'self_care_note', b'Self care note'), (b'resource_note', b'Resource note'), (b'appointment_note', b'Appointment note')]),
        ),
    ]
