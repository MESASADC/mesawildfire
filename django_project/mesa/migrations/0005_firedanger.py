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
                CREATE EXTENSION tablefunc;
                CREATE OR REPLACE VIEW mesa_fdiforecast AS
  SELECT t[1]::int as fdi_point_id, t[2]::timestamp without time zone as date_time, fdi_value::int, fwi::int, rh_pct::int, (temp_k-273.15)::int as temp_c, sqrt(power(uwind_ms,2)+power(vwind_ms,2))*3.6 as windspd_kmh, (180*atan2(uwind_ms,vwind_ms)/pi())+180 as winddir_deg, uwind_ms, vwind_ms FROM crosstab(
  'SELECT ARRAY[A.id::text, forecast_utc::text] AS t, variable, ST_Value(rast, A.point) AS value FROM mesa_fdipoint A
INNER JOIN mesa_firedanger B ON ST_Intersects(A.point, rast)
WHERE forecast_utc::DATE >= DATE ''yesterday'' 
AND forecast_utc::DATE < DATE ''today'' + INTERVAL ''2 days''
AND forecast_utc::time = time ''12:00''
ORDER BY 1,2'
  ,$$SELECT unnest('{lfdid,fwi,rh_pct,temp_k,uwind_ms,vwind_ms}'::text[])$$)
AS ct ("t" text[], "fdi_value" double precision, "fwi" double precision, "rh_pct" double precision, "temp_k" double precision, "uwind_ms" double precision, "vwind_ms" double precision);
            """,
            reverse_sql="""
                DROP TABLE IF EXISTS mesa_firedanger;
                DROP INDEX IF EXISTS mesa_firedanger_dateidx;
                DROP INDEX IF EXISTS mesa_firedanger_rast_gist_idx;
                DROP VIEW mesa_fdiforecast;
                DROP EXTENSION tablefunc;
            """,
        ),
    ]
