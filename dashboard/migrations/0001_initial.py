# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_attachment', models.FileField(upload_to=b'attachments')),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('users', models.ManyToManyField(related_name='clinics', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('date_accessed', models.DateTimeField(verbose_name=b'date accessed')),
                ('subject', models.CharField(max_length=150)),
                ('follow_up', models.CharField(max_length=250)),
                ('note_content', models.CharField(max_length=250)),
                ('note_type', models.CharField(max_length=20)),
                ('url', models.CharField(max_length=500, blank=True)),
                ('testing', models.CharField(max_length=10, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=4000, blank=True)),
                ('editors', models.ManyToManyField(related_name='notebooks_read_write', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_street', models.CharField(max_length=50, verbose_name=b'Street')),
                ('address_unit', models.CharField(max_length=10, verbose_name=b'Unit')),
                ('address_city', models.CharField(max_length=30, verbose_name=b'City')),
                ('address_province', models.CharField(max_length=30, verbose_name=b'Province')),
                ('address_country', models.CharField(max_length=30, verbose_name=b'Country')),
                ('address_postal_code', models.CharField(max_length=10, verbose_name=b'Postal Code')),
                ('phone_number', models.CharField(max_length=20)),
                ('medical_history', models.CharField(max_length=4000)),
                ('role', models.CharField(max_length=15)),
                ('title', models.CharField(max_length=15)),
                ('profile_picture', models.ImageField(upload_to=b'profile_pictures')),
                ('associates', models.ManyToManyField(related_name='associates_rel_+', to='dashboard.UserProfile', blank=True)),
                ('user', models.OneToOneField(related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunicationNote',
            fields=[
                ('note_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dashboard.Note')),
                ('attention', models.CharField(max_length=250)),
                ('importance', models.CharField(max_length=250)),
                ('instructions', models.CharField(max_length=4000)),
            ],
            bases=('dashboard.note',),
        ),
        migrations.CreateModel(
            name='DischargeNote',
            fields=[
                ('note_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dashboard.Note')),
                ('procedure', models.CharField(max_length=250)),
                ('doctor', models.CharField(max_length=250)),
                ('weight', models.IntegerField(default=0)),
                ('medication_name', models.CharField(max_length=100)),
                ('medication_dose', models.CharField(max_length=100)),
                ('next_dose', models.CharField(max_length=100)),
                ('selfcare_instructions', models.CharField(max_length=4000)),
                ('emergency_instructions', models.CharField(max_length=4000)),
            ],
            bases=('dashboard.note',),
        ),
        migrations.CreateModel(
            name='InstructionNote',
            fields=[
                ('note_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dashboard.Note')),
                ('instructions', models.CharField(max_length=4000)),
            ],
            bases=('dashboard.note',),
        ),
        migrations.CreateModel(
            name='MedicalInformationNote',
            fields=[
                ('note_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dashboard.Note')),
                ('medication_name', models.CharField(max_length=100)),
                ('medication_dose', models.CharField(max_length=100)),
                ('medication_duration', models.IntegerField()),
            ],
            bases=('dashboard.note',),
        ),
        migrations.CreateModel(
            name='SelfCareNote',
            fields=[
                ('note_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dashboard.Note')),
                ('selfcare_desc', models.CharField(max_length=1000)),
                ('frequency', models.CharField(max_length=150)),
                ('adverse_event_procedure', models.CharField(max_length=250)),
                ('procedure', models.CharField(max_length=4000)),
                ('time', models.CharField(max_length=250)),
                ('outcome', models.CharField(max_length=250)),
            ],
            bases=('dashboard.note',),
        ),
        migrations.AddField(
            model_name='notebook',
            name='notes',
            field=models.ManyToManyField(related_name='notes', to='dashboard.Note', blank=True),
        ),
        migrations.AddField(
            model_name='notebook',
            name='viewers',
            field=models.ManyToManyField(related_name='notebooks_read_only', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='note',
            name='author',
            field=models.ForeignKey(related_name='authored_notes', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='users',
            field=models.ManyToManyField(related_name='notes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attachment',
            name='note',
            field=models.ForeignKey(related_name='attachments', to='dashboard.Note'),
        ),
    ]
