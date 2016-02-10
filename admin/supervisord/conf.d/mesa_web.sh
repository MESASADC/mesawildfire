#!/bin/bash

MESA_ROOT="install script will set the directory"

trap "{ echo Stopping mesa_web docker; docker stop supervisor_mesa_web; exit 0; }" EXIT

docker rm -f supervisor_mesa_web &> /dev/null

echo "Make sure Postgresql and RabbitMQ is up and accepting connections:"
docker run --link supervisor_postgis --rm martin/wait
docker run --link supervisor_rabbitmq --rm martin/wait
docker run --link supervisor_geoserver --rm martin/wait

echo "Give PostGIS docker time to start up"
sleep 20

echo "Start django:"
docker run -t --rm -a stdout -a stderr --name supervisor_mesa_web --link supervisor_geoserver:geoserver --link supervisor_postgis:postgis --link supervisor_rabbitmq:rabbitmq -v $MESA_ROOT/django_project/ENV:/ENV -v $MESA_ROOT/django_project/start.sh:/start.sh -v $MESA_ROOT/django_project:/django_project -v $MESA_ROOT/volumes/web_static:/static_root/ -p 8112:8000 mesa_django

RESULT=$?

echo "Avoid Supervisor restarting immediately"
sleep 1
exit $RESULT

