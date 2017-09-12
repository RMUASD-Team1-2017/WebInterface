# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-12 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DroneHealth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmergencyCommon.Drone')),
            ],
        ),
        migrations.CreateModel(
            name='DroneMission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmergencyCommon.Drone')),
            ],
        ),
        migrations.CreateModel(
            name='DroneState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longtitude', models.FloatField()),
                ('eta', models.DateTimeField()),
                ('state', models.CharField(max_length=30)),
                ('last_update', models.DateTimeField()),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmergencyCommon.Drone')),
            ],
        ),
    ]
