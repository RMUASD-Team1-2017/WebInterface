# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmergencyCommon', '0003_droneposition_altitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='drone',
            name='altitude',
            field=models.FloatField(null=True),
        ),
    ]
