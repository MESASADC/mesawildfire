#!/bin/bash

<<COMMENT1
    Script to initialize Geoserver ImageMosaic
    for MESA SADC FDI layer 

	Dependencies:
	-mosaic.py
	-Name of ImageMosaic
	-MESA_SADC_FDI_SAfri_v1.2016-02-01T1200Z.2016-02-01T1200Z.*
	-GeoServer Path[http://url:port]
	-Geoserver Workpace
	-Geoserver user
	-Geoserver Password
	-Database host
	-Database port
	-Database Name
	-Database schema
	-Database user
	-Database password	 

    Setup GeoServer Layer Definition:
	 -On Data tab Change 'SRS handling' to 'Force declared'
	 -On Dimensions tab change 'Default value' to 'Use the biggest domain value'
	 
	 Run:
	 ./mesa_lfdi_wmst_init_mosaic.sh NAMEOFIMAGEMOSAIC MESA_SADC_FDI_SAfri_v1.2016-02-01T1200Z.2016-02-01T1200Z.* GEOSERVERURL 
	   GEOSERVERWORKSPACE GEOSERVERUSERNAME GEOSERVERPASSWORD DATABASEHOST DATABASEPORT DATABASENAME DATABASESCHEMA 
	   DATABASEUSER DATABASEPASSWORD

COMMENT1

MOSAIC=$1
TIFF_FILE=$2

#GeoServer
GEOSERVER_PATH=$3
GEOSERVER_WORKSPACE=$4
GEOSERVER_USER=$5
GEOSERVER_PASSWORD=$6

#Database
DATABASE_HOST=$7
DATABASE_PORT=$8
DATABASE_NAME=$9
DATABASE_SCHEMA=${10}
DATABASE_USER=${11}
DATABASE_PASSWORD=${12}

if [ "$#" -ne 12 ]; then
    echo "Illegal number of parameters"
	echo "Parameters:
  -Name of ImageMosaic
  -MESA_SADC_FDI_SAfri_v1.2016-02-01T1200Z.2016-02-01T1200Z.*(tiff file)
  -GeoServer Path[http://url:port]
  -Geoserver Workpace
  -Geoserver user
  -Geoserver Password
  -Database host
  -Database port
  -Database Name
  -Database schema
  -Database user
  -Database password"
	exit 0
fi

# we will later zip this dir:
rm -rf initial
mkdir -p initial

TIFF_FILENAME=$(echo "${TIFF_FILE##/*/}")

# Use Python's regex module. Regex created using https://regex101.com/#python
PARAMS=( $(python -c \
	"import sys,re; \
	  match = re.match(r'.*(?P<seconddate>[0-9]{4}\-[0-9]{2}\-[0-9]{2}T[0-9]{4}Z).*', sys.argv[1]); \
	  print ' '.join(match.groups()) \
	" $TIFF_FILENAME ) \
)

EXTENSION=$(echo $TIFF_FILENAME | cut -d'.' -f4-)

if [[ $EXTENSION == 'lfdid.tif' ]]; then
	SECONDDATE=${PARAMS[0]}
	NEWFILE=$( echo ${TIFF_FILENAME} | sed 's/'$TIFF_FILENAME'/'$SECONDDATE'.lfdid.tif/g')
	cp $TIFF_FILE initial/$NEWFILE
else
	SECONDDATE=${PARAMS[0]}
	NEWFILE=$( echo ${TIFF_FILENAME} | sed 's/'$TIFF_FILENAME'/'$SECONDDATE'.fwi.tif/g')
	cp $TIFF_FILE initial/$NEWFILE
fi

# create timeregex and indexer files
echo regex=[0-9]{4}\-[0-9]{2}\-[0-9]{2}T[0-9]{4}Z > initial/timeregex.properties
cat > initial/indexer.properties << EOT
TimeAttribute=time
Schema=*the_geom:Polygon,location:String,time:java.util.Date
PropertyCollectors=TimestampFileNameExtractorSPI[timeregex](time)
EOT

cat > initial/datastore.properties << EOT
SPI=org.geotools.data.postgis.PostgisNGDataStoreFactory
host=$DATABASE_HOST
port=$DATABASE_PORT
database=$DATABASE_NAME
schema=$DATABASE_SCHEMA
user=$DATABASE_USER
passwd=$DATABASE_PASSWORD
Loose\ bbox=true
Estimated\ extends=false
validate\ connections=true
Connection\ timeout=10
preparedStatements=true
Max\ open\ prepared\ statements=5
EOT

# create zip file with initial files
cd initial && zip ../$MOSAIC.zip * && cd .. 

# create mosaic datastore and layer in Geoserver
python mosaic.py --user $GEOSERVER_USER --password $GEOSERVER_PASSWORD --geoserver $GEOSERVER_PATH --workspace=$GEOSERVER_WORKSPACE --store=$MOSAIC --mosaic=$MOSAIC

# clean up
rm $MOSAIC.zip
rm -r initial


