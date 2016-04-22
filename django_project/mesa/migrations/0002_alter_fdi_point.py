# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-05 11:22
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mesa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fdipoint',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='fdipoint',
            name='lat',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='fdipoint',
            name='lon',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='fdipoint',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='fdipoint',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
        migrations.AlterField(
            model_name='fdipoint',
            name='station_id',
            field=models.CharField(blank=True, default=None, max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='fdipoint',
            name='station_name',
            field=models.CharField(blank=True, default=None, max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='fdipoint',
            name='type',
            field=models.CharField(blank=True, choices=[(b'wstation', b'Weather station'), (b'poi', b'Point of interest')], default=b'poi', max_length=20),
        ),
    ]
