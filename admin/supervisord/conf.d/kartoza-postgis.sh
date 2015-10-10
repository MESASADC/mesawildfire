#!/bin/bash

trap "{ echo Stopping kartoza-postgis docker; docker stop supervisor_postgis; exit 0; }" EXIT

docker rm -f supervisor_postgis &> /dev/null

# Start Postgresql:
docker run --name supervisor_postgis -a stdout -a stderr --rm -p 65432:5432 kartoza/postgis
RESULT=$?
echo RESULT=$RESULT

# Avoid Supervisor restarting immediately
echo Sleeping...
sleep 10
exit $RESULT
