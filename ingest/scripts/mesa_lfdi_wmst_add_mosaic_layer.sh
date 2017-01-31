#!/bin/bash

<<COMMENT1
    Script to add MESA_SADC_FDI layer
    image to existing GeoServer ImageMosaic

	Dependencies:
	-mosaic.py
	-Name of ImageMosaic
	-MESA_SADC_FDI_SAfri_v1.2016-02-01T1200Z.2016-02-01T1200Z.*
	-GeoServer Path[http://url:port]
	-Geoserver Workpace
	-Geoserver user
	-Geoserver Password

	Run:
	./mesa_lfdid_wmst_add_mosaic.sh NAMEOFIMAGEMOSAIC MESA_SADC_FDI_SAfri_v1.2016-02-01T1200Z.2016-02-01T1200Z.* GEOSERVERURL GEOSERVERWORKSPACE GEOSERVERUSERNAME GEOSERVERPASSWORD 
 
COMMENT1

MOSAIC=$1
TIFF_FILE=$2
#GeoServer
GEOSERVER_PATH=$3
GEOSERVER_WORKSPACE=$4
GEOSERVER_USER=$5
GEOSERVER_PASSWORD=$6
SCRIPT_DIR=$(readlink -f `dirname $0`)

if [ "$#" -ne 6 ]; then
    echo "Illegal number of parameters"
	echo "Parameters:
  -Name of Image mosaic
  -MESA_SADC_FDI_SAfri_v1.2016-02-01T1200Z.2016-02-01T1200Z.*
  -GeoServer Path[http://url:port]
  -Geoserver Workpace
  -Geoserver user
  -Geoserver Password"
	exit 0
fi
#/data/tellicast/eumetcast/MESA_SADC_FDI_SAfri_v1.2017-01-26T1200Z.2017-01-23T1200Z.lfdid.tif

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
	cp $TIFF_FILE $NEWFILE
else
	SECONDDATE=${PARAMS[0]}
	NEWFILE=$( echo ${TIFF_FILENAME} | sed 's/'$TIFF_FILENAME'/'$SECONDDATE'.fwi.tif/g')
	cp $TIFF_FILE $NEWFILE
fi

# create zip file with the new tiff file
zip $NEWFILE.zip $NEWFILE

# add a granule to the mosaic
python $SCRIPT_DIR/mosaic.py --user $GEOSERVER_USER --password $GEOSERVER_PASSWORD --geoserver $GEOSERVER_PATH --workspace=$GEOSERVER_WORKSPACE --store=$MOSAIC --layer=$NEWFILE.zip

# clean up
rm /$NEWFILE
rm /$NEWFILE.zip