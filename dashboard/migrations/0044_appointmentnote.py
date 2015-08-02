# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0043_auto_20150802_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentNote',
            fields=[
                ('note_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dashboard.Note')),
                ('date', models.DateField(verbose_name=b'Appointment date')),
                ('time', models.TimeField(verbose_name=b'Appointment time')),
                ('reason_for_visit', models.CharField(max_length=200)),
                ('clinic', models.ManyToManyField(related_name='appointments', to='dashboard.Clinic')),
                ('doctor', models.ManyToManyField(related_name='appointments', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('dashboard.note',),
        ),
    ]
