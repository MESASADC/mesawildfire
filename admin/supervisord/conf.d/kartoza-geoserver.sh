#!/bin/bash

docker rm -f supervisor_geoserver

# Make sure Postgresql is up and accepting connections:
docker run --link supervisor_db --rm=true martin/wait

# Start Geoserver:
docker run --name supervisor_geoserver --link supervisor_db -a stdout -a stderr --rm -p 58081:8080 kartoza/geoserver
RESULT=$?

# Avoid Supervisor restarting immediately
sleep 10
exit($RESULT)

