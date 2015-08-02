# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0039_auto_20150801_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='selfcarenote',
            old_name='adverse_event_procedure',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='selfcarenote',
            old_name='self_care_description',
            new_name='emergency_procedure',
        ),
        migrations.RemoveField(
            model_name='communicationnote',
            name='attention',
        ),
        migrations.RemoveField(
            model_name='procedurenote',
            name='medication_dose',
        ),
        migrations.RemoveField(
            model_name='procedurenote',
            name='medication_name',
        ),
        migrations.RemoveField(
            model_name='procedurenote',
            name='next_dose',
        ),
        migrations.RemoveField(
            model_name='resourcenote',
            name='medication_dose',
        ),
        migrations.RemoveField(
            model_name='resourcenote',
            name='medication_duration',
        ),
        migrations.RemoveField(
            model_name='resourcenote',
            name='medication_name',
        ),
        migrations.RemoveField(
            model_name='selfcarenote',
            name='time',
        ),
        migrations.AddField(
            model_name='communicationnote',
            name='clinic',
            field=models.ForeignKey(related_name='communication_notes', to='dashboard.Clinic', null=True),
        ),
        migrations.AddField(
            model_name='communicationnote',
            name='doctor',
            field=models.ForeignKey(related_name='communication_notes', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='procedurenote',
            name='clinic',
            field=models.ForeignKey(related_name='procedure_notes', to='dashboard.Clinic', null=True),
        ),
        migrations.AddField(
            model_name='procedurenote',
            name='follow_up_instructions',
            field=models.TextField(default='instructions'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='procedurenote',
            name='pre_procedure_instructions',
            field=models.TextField(default='instructions'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resourcenote',
            name='clinic',
            field=models.ForeignKey(related_name='resource_notes', to='dashboard.Clinic', null=True),
        ),
        migrations.AddField(
            model_name='resourcenote',
            name='doctor',
            field=models.ForeignKey(related_name='resource_notes', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='procedurenote',
            name='doctor',
            field=models.ForeignKey(related_name='procedure_notes', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
