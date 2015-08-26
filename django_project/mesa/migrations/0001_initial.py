# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mesa.models
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
            bases=(models.Model, mesa.models.NotifySave),
        ),
        migrations.CreateModel(
            name='ConfigSetting',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('type', models.CharField(default=b'str', max_length=20, choices=[(b'int', b'Integer'), (b'float', b'Float'), (b'str', b'String')])),
                ('value', models.CharField(max_length=100, null=True, blank=True)),
            ],
            bases=(models.Model, mesa.models.NotifySave),
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
            bases=(models.Model, mesa.models.NotifySave),
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
            bases=(models.Model, mesa.models.NotifySave),
        ),
        migrations.AddField(
            model_name='fdimeasurement',
            name='fdi_point',
            field=models.ForeignKey(blank=True, to='mesa.FdiPoint', null=True),
        ),
        migrations.RunSQL(
            sql="""CREATE OR REPLACE VIEW mesa_fdiforecast AS SELECT 0 id, 0 rain_mm, 0 windspd_kmh, 0 winddir_deg, 0 rh_pct, 0 fdi_value, '0'::varchar fdi_rgb, 0 fwi_value, '0'::varchar fwi_rgb, 0 temp_c, '=now()'::timestamp date_time, null::int fdi_point_id;""",
            reverse_sql='DROP VIEW IF EXISTS mesa_fdiforecast CASCADE;',
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
    
    fdi_table_select = """
        SELECT
                  mesa_fdipoint.id, 
                  mesa_fdipoint.name, 
                  mesa_fdipoint.type, 
                  mesa_fdipoint.station_name, 
                  mesa_fdimeasurement.fdi_value, 
                  mesa_fdimeasurement.fdi_rgb, 
                  mesa_fdipoint.point, 
                  mesa_fdipoint.lon, 
                  mesa_fdipoint.lat, 
                  mesa_fdimeasurement.rain_mm, 
                  mesa_fdimeasurement.windspd_kmh, 
                  mesa_fdimeasurement.winddir_deg, 
                  mesa_fdimeasurement.rh_pct, 
                  mesa_fdimeasurement.temp_c, 
                  mesa_fdimeasurement.date_time,
                  FALSE AS is_forecast
        FROM 
          public.mesa_fdipoint 
          LEFT JOIN public.mesa_fdimeasurement ON mesa_fdimeasurement.fdi_point_id = mesa_fdipoint.id

        UNION

        SELECT
                  mesa_fdipoint.id, 
                  mesa_fdipoint.name, 
                  mesa_fdipoint.type, 
                  mesa_fdipoint.station_name, 
                  mesa_fdiforecast.fdi_value, 
                  mesa_fdiforecast.fdi_rgb, 
                  mesa_fdipoint.point, 
                  mesa_fdipoint.lon, 
                  mesa_fdipoint.lat, 
                  mesa_fdiforecast.rain_mm, 
                  mesa_fdiforecast.windspd_kmh, 
                  mesa_fdiforecast.winddir_deg, 
                  mesa_fdiforecast.rh_pct, 
                  mesa_fdiforecast.temp_c, 
                  mesa_fdiforecast.date_time,
                  TRUE AS is_forecast
        FROM 
          public.mesa_fdipoint 
          LEFT JOIN public.mesa_fdiforecast ON mesa_fdiforecast.fdi_point_id = mesa_fdipoint.id
    """

 
    operations += [
        migrations.RunSQL(
            sql="CREATE OR REPLACE VIEW mesa_fditable AS %s;" % fdi_table_select,
            reverse_sql='DROP VIEW IF EXISTS mesa_fditable CASCADE;',
            state_operations=[migrations.CreateModel(
                name='FdiTable',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('name', models.CharField(unique=True, max_length=40)),
                    ('type', models.CharField(default=b'poi', max_length=20, blank=True, choices=[(b'wstation', b'Weather station'), (b'poi', b'Point of interest')])),
                    ('station_name', models.CharField(default=None, max_length=40, unique=True, null=True, blank=True)),
                    ('station_id', models.CharField(default=None, max_length=40, unique=True, null=True, blank=True)),
                    ('fdi_value', models.IntegerField()),
                    ('fdi_rgb', models.CharField(default=b'', max_length=10, blank=True)),
                    ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                    ('lon', models.FloatField()),
                    ('lat', models.FloatField()),
                    ('rain_mm', models.FloatField(null=True, blank=True)),
                    ('windspd_kmh', models.FloatField()),
                    ('winddir_deg', models.FloatField()),
                    ('rh_pct', models.FloatField()),
                    ('temp_c', models.FloatField()),
                    ('date_time', models.DateTimeField(null=True, blank=True)),
                    ('is_forecast', models.BooleanField()),
                ],
                options={
                    'abstract': False,
                    'managed': False,
                },
            )],
        )
    
    ]

