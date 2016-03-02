# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import mesa.models

class Migration(migrations.Migration):

    dependencies = [('mesa', '0004_fireevent'),]

    operations = []


    ''' ## skip for now to allow testing of install script

    operations = [

        migrations.RunSQL(
            sql = """
                CREATE OR REPLACE FUNCTION mesa_fdi_colour(fdi integer)
                  RETURNS character varying AS
                $BODY$
                BEGIN

                    IF fdi > 0 THEN
                        IF fdi <= 20 THEN
                            RETURN '#0000ff'; -- blue
                        ELSIF fdi <= 45 THEN
                            RETURN '#00ff00'; -- green
                        ELSIF fdi <= 60 THEN
                            RETURN '#ffff00'; -- yellow
                        ELSIF fdi <= 75 THEN
                            RETURN '#ffa500'; -- orange
                        ELSE
                            RETURN '#ff0000'; -- red
                        END IF;
                    END IF;
                    
                    RETURN '#808080';
                  
                END
                $BODY$
                  LANGUAGE plpgsql VOLATILE
                  COST 100;
            """,
            
            reverse_sql = """
                DROP FUNCTION IF EXISTS mesa_fdi_colour(integer);
            """
        ),

        migrations.RunSQL(
            sql = """
            CREATE OR REPLACE FUNCTION mesa_fwi_colour(fdi integer)
                RETURNS character varying AS
            $BODY$
            BEGIN
                IF fwi >= 0 THEN
                    IF fwi < 4 THEN
                        RETURN '#0000ff'; -- blue
                    ELSIF fwi < 14 THEN
                        RETURN '#00ff00'; -- green
                    ELSIF fwi < 39 THEN
                        RETURN '#ffff00'; -- yellow
                    ELSIF fwi < 91 THEN
                        RETURN '#ffa500'; -- orange
                    ELSE
                        RETURN '#ff0000'; -- red
                    END IF;
                END IF;
                
                RETURN '#808080';
              
            END
            $BODY$
                LANGUAGE plpgsql VOLATILE
                COST 100;
            """,
            
            reverse_sql = """
                DROP FUNCTION IF EXISTS mesa_fwi_colour(integer);
            """
        ),

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
                SELECT ct.t[1]::integer AS fdi_point_id,
                    ct.t[2]::timestamp without time zone AS date_time,
                    ct.fdi_value::integer AS fdi_value,
                    mesa_fdi_colour(ct.fdi_value::integer) AS fdi_rgb,
                    ct.fwi::integer AS fwi_value,
                    mesa_fwi_colour(ct.fwi_value) AS fwi_rgb,
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
                    
            reverse_sql = """
                DROP TABLE IF EXISTS mesa_firedanger;
                DROP INDEX IF EXISTS mesa_firedanger_dateidx;
                DROP INDEX IF EXISTS mesa_firedanger_rast_gist_idx;
                DROP VIEW mesa_fdiforecast;
                DROP EXTENSION tablefunc;
            """,
        ),
    ]

'''
