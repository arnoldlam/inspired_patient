# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0037_auto_20150801_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selfcarenote',
            name='adverse_event_procedure',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='selfcarenote',
            name='procedure',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='selfcarenote',
            name='self_care_description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='selfcarenote',
            name='time',
            field=models.DateTimeField(verbose_name=b'Time'),
        ),
    ]
