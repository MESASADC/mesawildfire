#!/bin/bash

MESA_ROOT="will be set by install script"

trap "{ echo Stopping geonode docker; docker stop supervisor_geonode; exit 0; }" EXIT

docker rm -f supervisor_geonode &> /dev/null

# Make sure Postgresql is up and accepting connections:
docker run --link supervisor_postgis --rm martin/wait

# Start Geoserver:
docker run --name supervisor_geonode --link supervisor_postgis:postgis -a stdout -a stderr --rm -v $MESA_ROOT/volumes/geonode_data:/geonode/geoserver/data -v $MESA_ROOT/geonode/local_settings.py:/geonode/geonode/local_settings.py -p 8111:8000 -p 8080:8080 geonode
RESULT=$?

# Avoid Supervisor restarting immediately
sleep 10
exit($RESULT)

