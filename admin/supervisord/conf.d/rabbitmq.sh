#!/bin/bash

trap "{ echo Stopping rabbitmq docker; docker stop supervisor_rabbitmq; exit 0; }" EXIT

docker rm -f supervisor_rabbitmq &> /dev/null

# Start Postgresql:
docker run --name supervisor_rabbitmq -a stdout -a stderr --rm -p 56720:5672 -p 56721:15672 rabbitmq:3-management
RESULT=$?
echo RESULT=$RESULT

# Avoid Supervisor restarting immediately
echo Sleeping...
sleep 10
exit $RESULT
