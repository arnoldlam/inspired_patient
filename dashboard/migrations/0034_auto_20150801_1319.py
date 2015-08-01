# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0033_note_users'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DischargeNote',
            new_name='ProcedureNote',
        ),
    ]
