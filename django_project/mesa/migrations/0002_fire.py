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
                ('description', models.CharField(default=b'', max_length=100, blank=True)),
                ('status', models.CharField(default=b'', max_length=20, blank=True, choices=[(b'confirmed', b'Confirmed'), (b'merged', b'Merged'), (b'hotspot', b'Hotspot'), (b'out', b'Out')])),
                ('border', django.contrib.gis.db.models.fields.PolygonField(default=None, srid=4326)),
            ],
            bases=(models.Model, mesa.models.NotifySave),
        ),

        migrations.AddField(
            model_name='firepixel',
            name='fire',
            field=models.ForeignKey(blank=True, to='mesa.Fire', null=True),
        ),

        migrations.RunSQL(
            sql = """
                CREATE INDEX index_mesa_fire_border
                ON mesa_fire
                USING gist
                (border);

                CREATE INDEX index_mesa_fire_status
                ON mesa_fire
                USING btree
                (status);

                CREATE INDEX index_mesa_fire_id
                ON mesa_fire
                USING btree
                (id);
            """,
            reverse_sql = """
                DROP INDEX IF EXISTS index_mesa_fire_border;
                DROP INDEX IF EXISTS index_mesa_fire_status;
                DROP INDEX IF EXISTS index_mesa_fire_id;
            """,
        ),

        migrations.RunSQL(
            sql = """
                CREATE INDEX index_mesa_firepixel_fire_id
                ON mesa_firepixel
                USING btree
                (fire_id);

                CREATE INDEX index_mesa_firepixel_date_time
                ON mesa_firepixel
                USING btree
                (date_time);

                CREATE INDEX index_mesa_firepixel_point
                ON mesa_firepixel
                USING gist
                (point);
            """,
            reverse_sql = """
                DROP INDEX IF EXISTS index_mesa_firepixel_fire_id;
                DROP INDEX IF EXISTS index_mesa_firepixel_date_time;
                DROP INDEX IF EXISTS index_mesa_firepixel_point;
            """,
        ),


        migrations.RunSQL(
            sql = """
                CREATE OR REPLACE VIEW mesa_firefeature AS
                SELECT  f.id,
                        f.description,
                        f.status,
                        f.border,
                        ST_Area(f.border::geography) as area,
                        min(p.date_time) AS first_seen,
                        max(p.date_time) AS last_seen,
                        max(p.frp) AS max_frp,
                        min(p.date_time) AS max_frp_date,
                        0 AS current_fdi,
                        min(p.date_time) AS current_fdi_date,
                        0 AS start_fdi,
                        0 AS max_fdi,
                        max(p.date_time) AS max_fdi_date,
                        (max(p.date_time) + '5 days'::interval) > now() AS is_active
                FROM mesa_fire f JOIN mesa_firepixel p ON p.fire_id = f.id
                GROUP BY f.id, f.description, f.status;
            """,
            reverse_sql="""
                DROP VIEW IF EXISTS mesa_firefeature CASCADE;
            """,
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
        
        
        migrations.RunSQL(
            sql = """
                CREATE OR REPLACE VIEW mesa_firefeature_active AS
                SELECT mesa_firefeature.id,
                    mesa_firefeature.description,
                    mesa_firefeature.status,
                    mesa_firefeature.border,
                    mesa_firefeature.area,
                    mesa_firefeature.first_seen::timestamp without time zone AS first_seen,
                    mesa_firefeature.last_seen::timestamp without time zone AS last_seen,
                    mesa_firefeature.max_frp,
                    mesa_firefeature.max_frp_date,
                    mesa_firefeature.current_fdi,
                    mesa_firefeature.current_fdi_date,
                    mesa_firefeature.start_fdi,
                    mesa_firefeature.max_fdi,
                    mesa_firefeature.max_fdi_date,
                    mesa_firefeature.is_active
                FROM mesa_firefeature
                WHERE mesa_firefeature.is_active = true;
            """,
            reverse_sql="""
                DROP VIEW IF EXISTS mesa_firefeature_active CASCADE;
            """,
            state_operations=[migrations.CreateModel(
                name='FireFeatureActive',
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
