#!/bin/bash
sudo docker exec -t supervisor_postgis psql -U docker -d gis -c " WITH old_fires_ids AS(  
                                                                  SELECT fe.id FROM mesa_fireevent fe 
                                                                  WHERE ((fe.last_seen - fe.first_seen) > INTERVAL '30 days')
                                                                ),too_large_clusters AS (
                                                                  SELECT fc.id
                                                                  FROM mesa_firecluster fc
                                                                  WHERE  fc.id IN(SELECT id FROM old_fires_ids) 
                                                                  OR (st_area(st_transform(border,54008))/10000 > 8000) 
                                                                ),no_result AS (
                                                                  SELECT reset_firepixel_fireid(fp.id) 
                                                                  FROM mesa_firepixel fp 
                                                                  WHERE fp.fire_id IN (SELECT id FROM too_large_clusters) OR fp.fire_id IN (SELECT id FROM old_fires_ids)
                                                                ),cleanup AS (
                                                                  DELETE FROM mesa_firecluster fc WHERE fc.id IN (SELECT id FROM too_large_clusters) OR fc.id IN (SELECT id FROM old_fires_ids)
                                                                )
                                                                SELECT * FROM no_result;
                                                               "


