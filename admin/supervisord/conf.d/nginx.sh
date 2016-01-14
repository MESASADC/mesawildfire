#!/bin/bash

set -x

MESA_ROOT="install script will set the directory"

trap "{ echo Stopping nginx docker; docker stop supervisor_nginx; exit 0; }" EXIT

docker rm -f supervisor_nginx &> /dev/null

# Make sure Geoserver, Django and RabbitMQ is up and accepting connections:
docker run --link supervisor_rabbitmq --rm martin/wait
docker run --link supervisor_geoserver --rm martin/wait
docker run --link supervisor_mesa_web --rm martin/wait
docker run --link supervisor_mesa_viewer --rm martin/wait

# Start django:
docker run -t --rm -a stdout -a stderr --name supervisor_nginx --link supervisor_mesa_viewer:mesa_viewer --link supervisor_geoserver:geoserver --link supervisor_mesa_web:mesa_web --link supervisor_rabbitmq:rabbitmq -p 80:80 -p 8000:8000 -v $MESA_ROOT/nginx/sites:/etc/nginx/sites-enabled -v $MESA_ROOT/nginx/www:/var/www/ mesa/nginx

RESULT=$?

# Avoid Supervisor restarting immediately
sleep 10
exit $RESULT

