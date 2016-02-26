#!/bin/bash

MESA_ROOT="install script will set the directory"
source $MESA_ROOT/admin/ENV

trap "{ echo Stopping mesa_backend docker; docker stop supervisor_mesa_backend; exit 0; }" EXIT

docker rm -f supervisor_mesa_backend &> /dev/null

# Make sure Postgresql and RabbitMQ is up and accepting connections:
docker run --link supervisor_postgis --rm martin/wait
docker run --link supervisor_rabbitmq --rm martin/wait -p 5672,61613,80,15672,15674  # dont wait for port 443

# Start django:
docker run -t --rm -a stdout -a stderr --name supervisor_mesa_backend --link supervisor_postgis:postgis --link supervisor_rabbitmq:rabbitmq -v $MESA_ROOT/django_project/ENV:/ENV -v $MESA_ROOT/django_project/start.sh:/start.sh -v $MESA_ROOT/django_project:/django_project mesasadc/mesa_django:$BUILD_TAG /django_project/manage.py mesa_comms

RESULT=$?

# Avoid Supervisor restarting immediately
sleep 1
exit $RESULT

