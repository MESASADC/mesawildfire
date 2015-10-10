#!/bin/bash

MESA_ROOT="install script will set the directory"

trap "{ echo Stopping mesa_web docker; docker stop supervisor_mesa_web; exit 0; }" EXIT

docker rm -f supervisor_mesa_web &> /dev/null

# Make sure Postgresql and RabbitMQ is up and accepting connections:
docker run --link supervisor_postgis --rm=true martin/wait
docker run --link supervisor_rabbitmq --rm=true martin/wait
docker run --link supervisor_geoserver --rm=true martin/wait

# Start django:
echo run
docker run --rm -a stdout -a stderr --name supervisor_mesa_web --link supervisor_geoserver:geoserver --link supervisor_postgis:postgis --link supervisor_rabbitmq:rabbitmq -v $MESA_ROOT/django_project/ENV:/ENV -v $MESA_ROOT/django_project/start.sh:/start.sh -v $MESA_ROOT/django_project:/django_project  mesa_django 
echo result
RESULT=$?

# Avoid Supervisor restarting immediately
sleep 10
exit($RESULT)

