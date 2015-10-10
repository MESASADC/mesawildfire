#!/bin/bash

trap "{ echo Stopping geoserver docker; docker stop supervisor_geoserver; exit 0; }" EXIT

docker rm -f supervisor_geoserver &> /dev/null

# Make sure Postgresql is up and accepting connections:
docker run --link supervisor_postgis --rm=true martin/wait

# Start Geoserver:
docker run --name supervisor_geoserver --link supervisor_postgis:postgis -a stdout -a stderr --rm -p 58081:8080 kartoza/geoserver
RESULT=$?

# Avoid Supervisor restarting immediately
sleep 10
exit($RESULT)

