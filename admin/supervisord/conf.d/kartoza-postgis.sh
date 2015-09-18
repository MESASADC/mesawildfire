#!/bin/bash

docker rm -f supervisor_db

# Start Postgresql:
docker run --name supervisor_db -a stdout -a stderr --rm -p 65432:5432 kartoza/postgis
RESULT=$?
echo RESULT=$RESULT

# Avoid Supervisor restarting immediately
echo Sleeping...
sleep 10
exit $RESULT
