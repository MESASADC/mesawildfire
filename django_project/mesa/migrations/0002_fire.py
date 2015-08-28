# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import mesa.models


class Migration(migrations.Migration):

    dependencies = [
        ('mesa', '0001_initial'),
    ]
    
    fdi_fire_feature_sql = """
        CREATE MATERIALIZED VIEW mesa_fire_feature AS
        SELECT  f.id, 
                f.description, 
                f.status, 
                ST_ConvexHull(ST_Collect(ST_Buffer(p.point, GREATEST(p.hsize, p.vsize)))) AS border, 
                MIN(p.date_time) AS first_observation,
                MAX(p.date_time) AS last_observation,
                MAX(p.frp) AS max_frp,
                NULL AS current_fdi,
                NULL AS start_fdi,
                NULL AS max_fdi
        FROM mesa_fire f, mesa_firepixel p 
        WHERE p.fire_id = f.id 
        GROUP BY f.id, f.description, f.status;
        
        CREATE INDEX mesa_fire_feature_geom_id
        ON mesa_fire_feature
        USING gist (border);

    """

    operations = [

        migrations.CreateModel(
            name='Fire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=b'', max_length=50, blank=True)),
                ('status', models.CharField(default=b'', max_length=20, blank=True, choices=[(b'detected', b'Detected'), (b'confirmed', b'Confirmed'), (b'out', b'Out')])),
            ],
            bases=(models.Model, mesa.models.NotifySave),
        ),

        migrations.AddField(
            model_name='firepixel',
            name='fire',
            field=models.ForeignKey(blank=True, to='mesa.Fire', null=True),
        ),
    
        migrations.RunSQL(
            sql = fdi_fire_feature_sql,
            reverse_sql='DROP MATERIALIZED VIEW IF EXISTS mesa_fire_feature CASCADE;',
            state_operations=[migrations.CreateModel(
                name='FireFeature',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('description', models.CharField(default=b'', max_length=50, blank=True)),
                    ('status', models.CharField(default=b'', max_length=20, blank=True, choices=[(b'detected', b'Detected'), (b'confirmed', b'Confirmed'), (b'out', b'Out')])),
                    ('border', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                    ('first_seen', models.DateTimeField()),
                    ('last_seen', models.DateTimeField()),
                    ('max_frp', models.FloatField()),
                    ('current_fdi', models.FloatField()),
                    ('start_fdi', models.FloatField()),
                    ('max_fdi', models.FloatField()),
                ],
                options={
                    'abstract': False,
                    'managed': False,
                },
                bases=(models.Model, mesa.models.NotifySave),
            )]
        ),

    ]
