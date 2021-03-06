#!/bin/bash

MESA_ROOT="will be set by install script"
source $MESA_ROOT/admin/ENV

trap "{ echo Stopping geoserver docker; docker stop supervisor_geoserver; exit 0; }" EXIT

docker rm -f supervisor_geoserver &> /dev/null

# Make sure Postgresql is up and accepting connections:
docker run --link supervisor_postgis --rm martin/wait

# Start Geoserver:
chmod a+w $VOLUMES/geoserver_data/logs
JAVA_OPTS="-Dorg.geotools.shapefile.datetime=true"
docker run --name supervisor_geoserver --link supervisor_postgis:postgis --rm  -e JAVA_OPTS=$JAVAS_OPTS -v $VOLUMES/geoserver_data:/opt/geoserver/data_dir -v $VOLUMES/geoserver_extensions:/usr/local/tomcat/webapps/ROOT/WEB-INF/ -p 8080:8080 mesasadc/geoserver:$BUILD_TAG
RESULT=$?

# Avoid Supervisor restarting immediately
sleep 1
exit $RESULT

