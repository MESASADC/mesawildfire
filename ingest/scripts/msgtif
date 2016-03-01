#!/bin/bash

#gdal_translate -a_srs "+proj=geos +lon_0=0 +h=35785831 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs" -b 1 -b 2 -b 3  -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR --config GDAL_TIFF_INTERNAL_MASK YES $1 $1.geos.tif

set -x

cp proj_4326.jpw "${1%.jpg}.jpw"

gdal_translate -projwin 7 7 45 -35 -b 1 -b 2 -b 3  -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR --config GDAL_TIFF_INTERNAL_MASK YES $1 $1.tif

gdal_edit.py -a_srs  "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs" $1.tif

cp $1.tif "output/${1%.jpg}.tif"

rm $1.tif
