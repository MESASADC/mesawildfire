# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import mesa.models


class Migration(migrations.Migration):

    dependencies = [
        ('mesa', '0003_triggers'),
    ]

    operations = [

       
        migrations.RunSQL(
            sql = """
                CREATE OR REPLACE VIEW mesa_fireevent AS 
                    WITH dims AS (
                        SELECT mesa_firefeature.id,
                            st_xmin(mesa_firefeature.border) AS west,
                            st_xmax(mesa_firefeature.border) AS east,
                            st_ymin(mesa_firefeature.border) AS south,
                            st_ymax(mesa_firefeature.border) AS north,
                            st_xmax(mesa_firefeature.border) - st_xmin(mesa_firefeature.border) AS width,
                            st_ymax(mesa_firefeature.border) - st_ymin(mesa_firefeature.border) AS height,
                            st_x(st_centroid(mesa_firefeature.border)) as centroid_x,
                            st_y(st_centroid(mesa_firefeature.border)) as centroid_y
                        FROM mesa_firefeature
                    )
                    SELECT ff.id,
                        ff.description,
                        ff.status,
                        ff.area,
                        ff.first_seen,
                        ff.last_seen,
                        ff.max_frp,
                        ff.max_frp_date,
                        ff.current_fdi,
                        ff.current_fdi_date,
                        ff.start_fdi,
                        ff.max_fdi,
                        ff.max_fdi_date,
                        ff.is_active,
                        dims.west - dims.width * 0.05::double precision AS vbox_west,
                        dims.east + dims.width * 0.05::double precision AS vbox_east,
                        dims.south - dims.height * 0.05::double precision AS vbox_south,
                        dims.north + dims.height * 0.05::double precision AS vbox_north,
                        dims.centroid_x, 
                        dims.centroid_y 
                    FROM mesa_firefeature ff, dims
                    WHERE ff.id = dims.id;
            """,
            reverse_sql="""
                DROP VIEW IF EXISTS mesa_fireevent CASCADE;
            """,
            state_operations=[migrations.CreateModel(
                name='FireEvent',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                    ('description', models.CharField(default=b'', max_length=50, blank=True)),
                    ('status', models.CharField(default=b'', max_length=20, blank=True, choices=mesa.models.fire_status_choices.items())),
                    ('area', models.FloatField()),
                    ('first_seen', models.DateTimeField()),
                    ('last_seen', models.DateTimeField()),
                    ('max_frp', models.FloatField()),
                    ('max_frp_date', models.DateTimeField()),
                    ('current_fdi', models.FloatField()),
                    ('current_fdi_date', models.DateTimeField()),
                    ('start_fdi', models.FloatField()),
                    ('max_fdi', models.FloatField()),
                    ('max_fdi_date', models.DateTimeField()),
                    ('vbox_west', models.FloatField()),
                    ('vbox_east', models.FloatField()),
                    ('vbox_south', models.FloatField()),
                    ('vbox_north', models.FloatField()),
                    ('centroid_x', models.FloatField()),
                    ('centroid_y', models.FloatField()),
                ],
                options={
                    'abstract': False,
                    'managed': False,
                },
                bases=(models.Model, mesa.models.NotifySave),
            )]
        ),
    

    ]
