# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-20 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmergencyCommon', '0006_waypoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='waypoint',
            name='altitude',
            field=models.FloatField(default=0),
        ),
    ]
