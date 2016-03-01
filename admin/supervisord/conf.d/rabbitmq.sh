#!/bin/bash

MESA_ROOT="install script will set this"
source $MESA_ROOT/admin/ENV

trap "{ echo Stopping rabbitmq docker; docker stop supervisor_rabbitmq; exit 0; }" EXIT

docker rm -f supervisor_rabbitmq &> /dev/null

# Start RabbitMQ:
docker run --name supervisor_rabbitmq -a stdout -a stderr --rm -p 56720:5672 -p 56721:15672 -p 56722:61613 -p 56723:15674  -v $VOLUMES/rabbitmq:/var/lib/rabbitmq -e RABBITMQ_DEFAULT_USER=$RABBITMQ_USER -e RABBITMQ_DEFAULT_PASS=$RABBITMQ_PASS mesasadc/rabbitmq-webstomp:$BUILD_TAG

RESULT=$?
echo RESULT=$RESULT

# Avoid Supervisor restarting immediately
echo Sleeping...
sleep 1
exit $RESULT
