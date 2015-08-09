# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0060_userprofile_office_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='office_address',
            new_name='address_office',
        ),
    ]
