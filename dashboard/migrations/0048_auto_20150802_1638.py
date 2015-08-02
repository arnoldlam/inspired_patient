# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0047_contactnote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=50, verbose_name=b'Street')),
                ('unit', models.CharField(max_length=10, verbose_name=b'Unit')),
                ('city', models.CharField(max_length=30, verbose_name=b'City')),
                ('province', models.CharField(max_length=30, verbose_name=b'Province / State')),
                ('country', models.CharField(default=b'CA', max_length=30, verbose_name=b'Country', choices=[(b'CA', b'Canada'), (b'US', b'United States'), (b'UK', b'United Kingdom')])),
                ('postal_code', models.CharField(max_length=10, verbose_name=b'Postal Code')),
            ],
        ),
        migrations.RemoveField(
            model_name='contactnote',
            name='user',
        ),
        migrations.AddField(
            model_name='contactnote',
            name='email',
            field=models.EmailField(default='some@email.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactnote',
            name='first_name',
            field=models.CharField(default='some first name', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactnote',
            name='last_name',
            field=models.CharField(default='some last name', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactnote',
            name='organization_name',
            field=models.CharField(default='some organization name', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactnote',
            name='phone_number_home',
            field=models.CharField(default='123', max_length=20, verbose_name=b'Phone Number (Home)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactnote',
            name='phone_number_work',
            field=models.CharField(default='123', max_length=20, verbose_name=b'Phone Number (Work)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactnote',
            name='title',
            field=models.CharField(default='Mr', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactnote',
            name='address',
            field=models.OneToOneField(related_name='contact_notes', null=True, to='dashboard.Address'),
        ),
    ]
