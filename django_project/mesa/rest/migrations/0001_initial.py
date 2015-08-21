# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mesa.rest.models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AfModis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=40, blank=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('date_time', models.DateTimeField(null=True, blank=True)),
                ('src', models.CharField(default=b'', max_length=20, blank=True)),
                ('sat', models.CharField(default=b'', max_length=20, blank=True)),
                ('frp', models.FloatField()),
                ('btemp', models.FloatField()),
            ],
            bases=(models.Model, mesa.rest.models.NotifySave),
        ),
        migrations.CreateModel(
            name='ConfigSetting',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('type', models.CharField(default=b'str', max_length=20, choices=[(b'int', b'Integer'), (b'float', b'Float'), (b'str', b'String')])),
                ('value', models.CharField(max_length=100, null=True, blank=True)),
            ],
            bases=(models.Model, mesa.rest.models.NotifySave),
        ),
        migrations.CreateModel(
            name='FdiMeasurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rain_mm', models.FloatField()),
                ('windspd_kmh', models.FloatField()),
                ('winddir_deg', models.FloatField()),
                ('rh_pct', models.FloatField()),
                ('fdi_value', models.IntegerField()),
                ('fdi_rgb', models.CharField(default=b'', max_length=10, blank=True)),
                ('temp_c', models.FloatField()),
                ('date_time', models.DateTimeField(null=True, blank=True)),
            ],
            bases=(models.Model, mesa.rest.models.NotifySave),
        ),
        migrations.CreateModel(
            name='FdiPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('type', models.CharField(default=b'poi', max_length=20, blank=True, choices=[(b'wstation', b'Weather station'), (b'poi', b'Point of interest')])),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('station_name', models.CharField(default=None, max_length=40, unique=True, null=True, blank=True)),
                ('station_id', models.CharField(default=None, max_length=40, unique=True, null=True, blank=True)),
            ],
            bases=(models.Model, mesa.rest.models.NotifySave),
        ),
        migrations.AddField(
            model_name='fdimeasurement',
            name='fdi_point',
            field=models.ForeignKey(blank=True, to='rest.FdiPoint', null=True),
        ),
        migrations.RunSQL(
            sql="""CREATE OR REPLACE VIEW rest_fdiforecast AS SELECT 0 id, 0 rain_mm, 0 windspd_kmh, 0 winddir_deg, 0 rh_pct, 0 fdi_value, '0'::varchar fdi_rgb, 0 fwi_value, '0'::varchar fwi_rgb, 0 temp_c, '=now()'::timestamp date_time, null::int fdi_point_id;""",
            reverse_sql='DROP VIEW IF EXISTS rest_fdiforecast CASCADE;',
            state_operations=[migrations.CreateModel(
                name='FdiForecast',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('rain_mm', models.FloatField(null=True, blank=True)),
                    ('windspd_kmh', models.FloatField()),
                    ('winddir_deg', models.FloatField()),
                    ('rh_pct', models.FloatField()),
                    ('fdi_value', models.IntegerField()),
                    ('fdi_rgb', models.CharField(default=b'', max_length=10, blank=True)),
                    ('fwi_value', models.IntegerField()),
                    ('fwi_rgb', models.CharField(default=b'', max_length=10, blank=True)),
                    ('temp_c', models.FloatField()),
                    ('date_time', models.DateTimeField(null=True, blank=True)),
                    ('fdi_point_id', models.IntegerField()),
                ],
                options={
                    'abstract': False,
                    'managed': False,
                },
            )],
        ),
    ]
