# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import mesa.models


class Migration(migrations.Migration):

    dependencies = [
        ('mesa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('first_seen', models.DateTimeField(null=True, blank=True)),
                ('last_seen', models.DateTimeField(null=True, blank=True)),
                ('description', models.CharField(default=b'', max_length=50, blank=True)),
                ('status', models.CharField(default=b'', max_length=20, blank=True, choices=[(b'detected', b'Detected'), (b'confirmed', b'Confirmed'), (b'active', b'Active'), (b'out', b'Out')])),
                ('max_frp', models.FloatField()),
                ('current_fdi', models.FloatField()),
                ('start_fdi', models.FloatField()),
                ('max_fdi', models.FloatField()),
            ],
            bases=(models.Model, mesa.models.NotifySave),
        ),
    ]
