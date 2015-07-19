# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20150719_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dischargenote',
            name='emergency_instructions',
            field=models.TextField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='dischargenote',
            name='next_dose',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='dischargenote',
            name='selfcare_instructions',
            field=models.TextField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='note',
            name='note_content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='note',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
