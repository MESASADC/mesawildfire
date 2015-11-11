# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import mesa.models

class Migration(migrations.Migration):

    dependencies = [('mesa', '0004_fireevent'),]

    operations = [
        migrations.RunSQL(
            # If this bombs out, pip install sqlparse
            sql = """
                CREATE TABLE IF NOT EXISTS mesa_firedanger (
                  id serial NOT NULL,
                  variable character varying(16) NOT NULL,
                  forecast_utc timestamp without time zone,
                  reference_utc timestamp without time zone,
                  rast raster NOT NULL,
                  CONSTRAINT mesa_firedanger_pkey PRIMARY KEY (id),
                  CONSTRAINT mesa_firedanger_rast_check4 CHECK (st_srid(rast) = 4326)
                );
                DROP INDEX IF EXISTS mesa_firedanger_dateidx;
                CREATE INDEX mesa_firedanger_dateidx
                  ON mesa_firedanger USING btree (forecast_utc);
                DROP INDEX IF EXISTS mesa_firedanger_rast_gist_idx;
                CREATE INDEX mesa_firedanger_rast_gist_idx
                  ON mesa_firedanger USING gist (ST_CONVEXHULL(rast));
            """,
            reverse_sql="""
                DROP TABLE IF EXISTS mesa_firedanger;
                DROP INDEX IF EXISTS mesa_firedanger_dateidx;
                DROP INDEX IF EXISTS mesa_firedanger_rast_gist_idx;
            """,
        ),
    ]
