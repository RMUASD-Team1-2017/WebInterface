# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmergencyCommon', '0002_auto_20170918_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='droneposition',
            name='altitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]