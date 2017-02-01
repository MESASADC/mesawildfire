#!/bin/bash
sudo docker exec -t supervisor_postgis psql -U docker -d gis -c "WITH too_large_clusters AS (
                                                                   SELECT *
                                                                   FROM mesa_firecluster fc 
                                                                   WHERE st_area(border::geography)/10000 > 8000
                                                                ),
                                                                  no_result AS (
                                                                   SELECT reset_firepixel_fireid(fp.id) 
                                                                   FROM mesa_firepixel fp 
                                                                   WHERE fp.fire_id IN (SELECT id FROM too_large_clusters)
                                                                ),
                                                                  cleanup AS (
                                                                   DELETE FROM mesa_firecluster fc WHERE fc.id IN (SELECT id FROM too_large_clusters)
                                                                )
                                                                SELECT * FROM no_result;"
