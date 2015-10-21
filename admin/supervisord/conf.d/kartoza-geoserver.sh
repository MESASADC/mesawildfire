#!/bin/bash

MESA_ROOT="will be set by install script"

trap "{ echo Stopping geoserver docker; docker stop supervisor_geoserver; exit 0; }" EXIT

docker rm -f supervisor_geoserver &> /dev/null

# Make sure Postgresql is up and accepting connections:
docker run --link supervisor_postgis --rm martin/wait

# Start Geoserver:
docker run --name supervisor_geoserver --link supervisor_postgis:postgis -a stdout -a stderr --rm -v $MESA_ROOT/volumes/geoserver_data:/opt/geoserver/data_dir -v $MESA_ROOT/volumes/geoserver_extensions:/usr/local/tomcat/webapps/ROOT/WEB-INF/ -p 58080:8080 kartoza/geoserver
RESULT=$?

# Avoid Supervisor restarting immediately
sleep 10
exit($RESULT)

