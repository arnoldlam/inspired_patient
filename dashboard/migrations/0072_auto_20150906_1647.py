# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0071_auto_20150903_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='has_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='latest_payment',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='payment_rate',
            field=models.CharField(blank=True, max_length=10, choices=[(b'basic', b'Basic'), (b'premium', b'Premium')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='payment_term',
            field=models.CharField(blank=True, max_length=10, choices=[(b'monthly', b'Monthly'), (b'annually', b'Annually')]),
        ),
    ]
