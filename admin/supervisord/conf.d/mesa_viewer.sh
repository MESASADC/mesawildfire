#!/bin/bash

MESA_ROOT="install script will set the directory"
VOLUMES="install script will set the directory"

trap "{ echo Stopping mesa_viewer docker; docker stop supervisor_mesa_viewer; exit 0; }" EXIT

docker rm -f supervisor_mesa_viewer &> /dev/null

echo "Make sure Postgresql and RabbitMQ is up and accepting connections:"
docker run --link supervisor_postgis --rm martin/wait
#docker run --link supervisor_rabbitmq --rm martin/wait
docker run --link supervisor_geoserver --rm martin/wait

echo "Give PostGIS docker time to start up"
sleep 10

# Create viewer DB if not exists
docker exec supervisor_postgis su - postgres -c "createdb -T template_postgis viewer"
docker exec supervisor_postgis su - postgres -c "psql -c '\l'"

echo "Start viewer:"
source $MESA_ROOT/mesa-viewer/ENV
docker run --name supervisor_mesa_viewer -t \
--link supervisor_postgis:postgis \
--link supervisor_geoserver:geoserver \
-v $MESA_ROOT/mesa-viewer/docker_runtime:/tmp/runtime \
-v $MESA_ROOT/mesa-viewer/django_project:/tmp/django_project \
-v $MESA_ROOT/mesa-viewer/public:/tmp/public \
-v $MESA_ROOT/mesa-viewer/logs:/tmp/logs \
-e AFIS_VIEWER_DATABASE_NAME=$AFIS_VIEWER_DATABASE_NAME \
-e AFIS_VIEWER_DATABASE_USER=$AFIS_VIEWER_DATABASE_USER \
-e AFIS_VIEWER_DATABASE_PASS=$AFIS_VIEWER_DATABASE_PASS \
-e AFIS_VIEWER_DATABASE_HOST=$AFIS_VIEWER_DATABASE_HOST \
-e AFIS_VIEWER_DATABASE_PORT=$AFIS_VIEWER_DATABASE_PORT \
-e AFIS_VIEWER_STATIC_ROOT=/tmp/django_project/afisweb/static/ \
-e DJANGO_SETTINGS_MODULE=settings.afis_web_basic \
mesa_viewer \
python /tmp/django_project/manage.py runserver 0.0.0.0:8000

RESULT=$?

echo "Avoid Supervisor restarting immediately"
sleep 1
exit $RESULT

