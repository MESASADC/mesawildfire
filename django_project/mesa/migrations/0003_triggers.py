# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import mesa.models


class Migration(migrations.Migration):

    dependencies = [
        ('mesa', '0002_fire'),
    ]

    operations = [

  
        migrations.RunSQL(
            sql = """
                CREATE OR REPLACE FUNCTION update_fire_merge(fireid integer)
                  RETURNS integer AS
                $BODY$
                DECLARE
                    spatial_m  int = 3000;
                    temporal_h int = 12;
                    new_fireid int;
                BEGIN

                    -- find the nearest neighbour in range to merge with
                    RAISE NOTICE 'looking for nearest neighbour within range of: %', fireid;
                    new_fireid := (
                        WITH neighbours AS (
                            SELECT b.id, ST_Distance(a.border, b.border) AS distance_m FROM mesa_fire a, mesa_fire b WHERE a.id = fireid AND a.id < b.id ORDER BY a.border <#> b.border LIMIT 20
                        )
                        SELECT id FROM neighbours WHERE distance_m < 0.03 ORDER BY distance_m ASC LIMIT 1
                    );

                    IF new_fireid IS NULL THEN
                        -- stop recursion
                        RAISE NOTICE 'stop: %', fireid;
                        RETURN fireid;
                    ELSE
                        -- merge firepixels into selected fire
                        RAISE NOTICE 'merge firepixels';
                        UPDATE mesa_firepixel SET fire_id = new_fireid WHERE fire_id = fireid;
                        -- determine the new fire border
                        RAISE NOTICE 'update border';
                        PERFORM update_fire_border(new_fireid);
                        -- merge recursively   
                        RAISE NOTICE 'in: %', new_fireid;
                        new_fireid := update_fire_merge(new_fireid);
                        RAISE NOTICE 'out: %', new_fireid;
                        RETURN new_fireid;
                    END IF;
                    
                END
                $BODY$
                  LANGUAGE plpgsql VOLATILE
                  COST 1000;
            """,
            reverse_sql = """
                DROP FUNCTION IF EXISTS update_fire_merge(integer)
            """,
        ),

        migrations.RunSQL(
            sql = """
                CREATE OR REPLACE FUNCTION update_fire_border(fireid integer)
                    RETURNS double precision AS
                $BODY$
                DECLARE
                    spatial_m  int = 1000;
                    temporal_h int = 12;
                BEGIN  

                    UPDATE mesa_fire SET border = 
                    (
                        SELECT 
                            ST_Union(ST_Buffer(ST_ConCavehull(ST_Collect(p.point), 0.8), p.size), ST_Union(p.buffer)) AS border
                        FROM mesa_fire f,
                            ( SELECT id,
                                point,
                                st_buffer(mesa_firepixel.point, 1::double precision * GREATEST(mesa_firepixel.hsize, mesa_firepixel.vsize)) AS buffer,
                                GREATEST(mesa_firepixel.hsize, mesa_firepixel.vsize) AS size,
                                fire_id
                              FROM mesa_firepixel
                            ) p
                        WHERE p.fire_id = f.id AND f.id = fireid
                        GROUP BY f.id, p.size
                    )
                    WHERE id = fireid;
                    RETURN (SELECT ST_Area(border::geography) FROM mesa_fire f WHERE id = fireid);
                END
                $BODY$
                  LANGUAGE plpgsql VOLATILE
                  COST 1000;
            """,
            reverse_sql = """
                DROP  FUNCTION IF EXISTS update_fire_border(integer)
            """,
        ),

        migrations.RunSQL(
            sql = """
                CREATE OR REPLACE FUNCTION tf_firepixel_nearest_fire()
                RETURNS trigger AS
                $BODY$
                BEGIN
                    -- find the closest fire within range
                    NEW.fire_id := (
                        WITH neighbours AS ( 
                            SELECT id, ST_Distance_Sphere(border, NEW.point) AS distance_m FROM mesa_fire ORDER BY border::geometry <-> NEW.point::geometry LIMIT 10
                        )
                        SELECT id FROM neighbours WHERE distance_m < 3000 ORDER BY distance_m ASC LIMIT 1   
                    ); 
                    IF NEW.fire_id IS NULL THEN
                        INSERT INTO mesa_fire (description, status, border) SELECT 'hotspot #' || NEW.id, 'hotspot', st_buffer(NEW.point, 2::double precision * GREATEST(NEW.hsize, NEW.vsize)) RETURNING id INTO NEW.fire_id;
                    END IF;
                    RETURN NEW;
                END
                $BODY$
                    LANGUAGE plpgsql VOLATILE
                    COST 100;
            """,
            reverse_sql = """
                DROP FUNCTION IF EXISTS tf_firepixel_nearest_fire();
            """,
        ),


        migrations.RunSQL(
            sql = """
            CREATE OR REPLACE FUNCTION tf_firepixel_fire_update()
            RETURNS trigger AS
            $BODY$
            BEGIN

                PERFORM update_fire_border(NEW.fire_id);
                PERFORM update_fire_merge(NEW.fire_id);
                RETURN NEW;
                
            END
            $BODY$
                LANGUAGE plpgsql VOLATILE
                COST 100;
            """,
            reverse_sql = """
                DROP FUNCTION IF EXISTS tf_firepixel_fire_update();
            """,
        ),


        migrations.RunSQL(
            sql = """
                CREATE TRIGGER mesa_firepixel_before_insert
                BEFORE INSERT
                ON mesa_firepixel
                FOR EACH ROW
                WHEN ((new.fire_id IS NULL))
                EXECUTE PROCEDURE tf_firepixel_nearest_fire();
            """,
            reverse_sql = """
                DROP TRIGGER IF EXISTS mesa_firepixel_before_insert ON mesa_firepixel;
            """,
        ),

        migrations.RunSQL(
            sql = """
                CREATE TRIGGER mesa_firepixel_after_insert
                AFTER INSERT
                ON mesa_firepixel
                FOR EACH ROW
                WHEN ((new.fire_id IS NOT NULL))
                EXECUTE PROCEDURE tf_firepixel_fire_update();
            """,
            reverse_sql = """
                DROP TRIGGER IF EXISTS mesa_firepixel_after_insert ON mesa_firepixel;
            """,
        ),



    ]
