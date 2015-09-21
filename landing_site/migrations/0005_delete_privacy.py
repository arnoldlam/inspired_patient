# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing_site', '0004_privacy'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Privacy',
        ),
    ]
