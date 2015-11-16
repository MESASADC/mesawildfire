#!/bin/bash

MESA_ROOT="will be set by the install script"

trap "{ echo Stopping kartoza-postgis docker; docker stop supervisor_postgis; exit 0; }" EXIT

docker rm -f supervisor_postgis &> /dev/null

# Start Postgresql:
docker run --name supervisor_postgis -a stdout -a stderr --rm -v $MESA_ROOT/volumes/postgis:/var/lib/postgresql -v $MESA_ROOT/volumes/postgis/9.4/main/pg_hba.conf:/etc/postgresql/9.4/main/pg_hba.conf -p 5432:5432 kartoza/postgis
#docker run --name supervisor_postgis -a stdout -a stderr --rm -v $MESA_ROOT/volumes/postgis:/var/lib/postgresql -p 5432:5432 kartoza/postgis
RESULT=$?
echo RESULT=$RESULT

# Avoid Supervisor restarting immediately
echo Sleeping...
sleep 10
exit $RESULT
