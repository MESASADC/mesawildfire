#!/bin/bash

SCRIPT_DIR=$(readlink -f `dirname $0`)

# There is no way to set env variables from the incrontab, so needed this wrapper script

POSTGIS_DOCKER_EXEC=1 $SCRIPT_DIR/mesa_fdifwi.sh $*
