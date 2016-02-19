#!/bin/bash

MESA_ROOT="will be set by the install script"

trap "{ echo Stopping kartoza-postgis docker; docker stop supervisor_postgis; exit 0; }" EXIT

docker rm -f supervisor_postgis &> /dev/null

# Start Postgresql:
docker run --name supervisor_postgis -a stdout -a stderr --rm -e POSTGIS_ENABLE_OUTDB_RASTERS=1 -e POSTGIS_GDAL_ENABLED_DRIVERS=ENABLE_ALL -v $MESA_ROOT/admin/postgresql/pg_hba.conf:/etc/postgresql/9.4/main/pg_hba.conf -v $MESA_ROOT/volumes/postgis:/var/lib/postgresql -v $MESA_ROOT/ingest:/mnt/ingest -v $MESA_ROOT/admin/postgresql/start-postgis.sh:/start-postgis.sh -p 5432:5432 kartoza/postgis /start-postgis.sh
RESULT=$?
echo RESULT=$RESULT

# Avoid Supervisor restarting immediately
echo Sleeping...
sleep 1
exit $RESULT
