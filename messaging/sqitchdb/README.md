Using PostgREST
-----------------

1. Make sure that a file ENV exists which is similar to ENV.example

2. Has the postgrest docker been built? See: ../../docker-postgrest

3. $ postgrest

3. Switch to different terminal tab

4. $ curl -X OPTIONS http://localhost:3000/active_fire_modis | jsonlint -f

5. $ curl http://localhost:3000/active_fire_modis | jsonlint -f

6. $ curl -d '{"type":"AF","geom":null,"lat":0,"lon":0,"date_time":null,"src":"CSIR","btemp":350,"sat":"T","frp":140}' http://localhost:3000/active_fire_modis

7. $ curl http://localhost:3000/active_fire_modis | jsonlint -f
