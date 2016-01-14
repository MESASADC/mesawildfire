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
            sql=""" 


CREATE OR REPLACE FUNCTION fdi_colour(fdi integer)
  RETURNS character varying AS
$BODY$
BEGIN

CASE 
    WHEN '[0,20]'::int4range @> fdi THEN
        RETURN '#0000FF';
    WHEN '[21,45]'::int4range @> fdi THEN
        RETURN '#00FF00';
    WHEN '[46,60]'::int4range @> fdi THEN
        RETURN '#FFFF00';
    WHEN '[61,75]'::int4range @> fdi THEN
        RETURN '#FFA500';
    WHEN '[76,100]'::int4range @> fdi THEN
        RETURN '#FF0000';
    ELSE
        RETURN '#000000';
END CASE;

END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE EXTENSION tablefunc;

CREATE OR REPLACE VIEW mesa_fdiforecast AS 
 SELECT ct.t[1]::integer AS fdi_point_id,
    ct.t[2]::timestamp without time zone AS date_time,
    ct.fdi_value::integer AS fdi_value,
    fdi_colour(ct.fdi_value::integer) AS fdi_rgb,
    ct.fwi::integer AS fwi_value,
    '#000000'::character varying AS fwi_rgb,
    NULL::double precision AS rain_mm,
    ct.rh_pct::integer AS rh_pct,
    (ct.temp_k - 273.15::double precision)::integer AS temp_c,
    sqrt(power(ct.uwind_ms, 2::double precision) + power(ct.vwind_ms, 2::double precision)) * 3.6::double precision AS windspd_kmh,
    180::double precision * atan2(ct.uwind_ms, ct.vwind_ms) / pi() + 180::double precision AS winddir_deg,
    ct.uwind_ms,
    ct.vwind_ms
   FROM crosstab('SELECT ARRAY[A.id::text, forecast_utc::text] AS t, variable, ST_Value(rast, A.point) AS value FROM mesa_fdipoint A
INNER JOIN mesa_firedanger B ON ST_Intersects(A.point, rast)
WHERE forecast_utc::DATE >= DATE ''yesterday'' 
AND forecast_utc::DATE < DATE ''today'' + INTERVAL ''2 days''
AND forecast_utc::time = time ''12:00''
ORDER BY 1,2'::text, 'SELECT unnest(''{lfdid,fwi,rh_pct,temp_k,uwind_ms,vwind_ms}''::text[])'::text) ct(t text[], fdi_value double precision, fwi double precision, rh_pct double precision, temp_k double precision, uwind_ms double precision, vwind_ms double precision);

""",
            reverse_sql='DROP VIEW IF EXISTS mesa_fdiforecast CASCADE;',
            state_operations=[migrations.CreateModel(
                name='FdiForecast',
                fields=[
                    #('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
    
    fdi_point_data_select = """
    SELECT mesa_fdipoint.id AS fdi_point_id,
            mesa_fdipoint.name,
            mesa_fdipoint.type,
            mesa_fdipoint.station_name,
            mesa_fdimeasurement.fdi_value,
            mesa_fdimeasurement.fdi_rgb,
            NULL::double precision AS fwi_value,
            NULL::character varying AS fwi_rgb,
            mesa_fdipoint.point,
            mesa_fdipoint.lon,
            mesa_fdipoint.lat,
            mesa_fdimeasurement.rain_mm,
            mesa_fdimeasurement.windspd_kmh,
            mesa_fdimeasurement.winddir_deg,
            mesa_fdimeasurement.rh_pct,
            mesa_fdimeasurement.temp_c,
            mesa_fdimeasurement.date_time,
            false AS is_forecast
        FROM mesa_fdipoint
        LEFT JOIN mesa_fdimeasurement ON mesa_fdimeasurement.fdi_point_id = mesa_fdipoint.id
    UNION
        SELECT mesa_fdipoint.id AS fdi_point_id,
            mesa_fdipoint.name,
            mesa_fdipoint.type,
            mesa_fdipoint.station_name,
            mesa_fdiforecast.fdi_value,
            mesa_fdiforecast.fdi_rgb,
            mesa_fdiforecast.fwi_value,
            mesa_fdiforecast.fwi_rgb,
            mesa_fdipoint.point,
            mesa_fdipoint.lon,
            mesa_fdipoint.lat,
            NULL::double precision AS rain_mm,
            mesa_fdiforecast.windspd_kmh,
            mesa_fdiforecast.winddir_deg,
            mesa_fdiforecast.rh_pct,
            mesa_fdiforecast.temp_c,
            mesa_fdiforecast.date_time,
            true AS is_forecast
        FROM mesa_fdipoint
        LEFT JOIN mesa_fdiforecast ON mesa_fdiforecast.fdi_point_id = mesa_fdipoint.id;
    """

 
    operations += [
        migrations.RunSQL(
            sql="CREATE OR REPLACE VIEW mesa_fdipointdata AS %s" % fdi_point_data_select,
            reverse_sql='DROP VIEW IF EXISTS mesa_fdipointdata CASCADE;',
            state_operations=[migrations.CreateModel(
                name='FdiPointData',
                fields=[
                        ('id', models.IntegerField(serialize=False, primary_key=True)),
                        ('name', models.CharField(unique=True, max_length=40)),
                        ('type', models.CharField(default=b'poi', max_length=20, blank=True, choices=[(b'wstation', b'Weather station'), (b'poi', b'Point of interest')])),
                        ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                        ('lon', models.FloatField()),
                        ('lat', models.FloatField()),
                        ('station_name', models.CharField(max_length=40, null=True, blank=True)),
                        ('rain_mm', models.FloatField()),
                        ('windspd_kmh', models.FloatField()),
                        ('winddir_deg', models.FloatField()),
                        ('rh_pct', models.FloatField()),
                        ('fdi_value', models.IntegerField()),
                        ('fdi_rgb', models.CharField(default=b'', max_length=10, blank=True)),
                        ('temp_c', models.FloatField()),
                        ('date_time', models.DateTimeField(null=True, blank=True)),
                        ('is_forecast', models.BooleanField()),
                    ],
                    options={
                        'abstract': False,
                        'managed': False,
                    },
                )],
        ),
        migrations.CreateModel(
            name='FirePixel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'', max_length=40, blank=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('vsize', models.FloatField(default=0)),
                ('hsize', models.FloatField(default=0)),
                ('date_time', models.DateTimeField(null=True, blank=True)),
                ('src', models.CharField(default=b'', max_length=20, blank=True)),
                ('sat', models.CharField(default=b'', max_length=20, blank=True)),
                ('frp', models.FloatField(blank=True)),
                ('btemp', models.FloatField(blank=True)),
            ],
            bases=(models.Model, mesa.models.NotifySave),
        ),
    
    ]
