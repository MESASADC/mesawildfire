#!/bin/bash

SCRIPT_DIR=$(readlink -f `dirname $0`)
FILENAMEFDI='/home/mesa/mesawildfire/admin/geoserver/mesa_rasters/MESA_SADC_FDI_SAfri_v1.2016-05-06T1200Z.2016-05-07T1200Z.lfdid.tif'
FILENAMEFWI='/home/mesa/mesawildfire/admin/geoserver/mesa_rasters/MESA_SADC_FDI_SAfri_v1.2016-05-10T1200Z.2016-05-07T1200Z.fwi.tif'

source $SCRIPT_DIR/ENV

$SCRIPT_DIR/mesa_lfdi_wmst_init_mosaic.sh $NAMEOFIMAGEMOSAIC $FILENAMEFDI $GEOSERVERURL $GEOSERVERWORKSPACE $GEOSERVERUSERNAME $GEOSERVERPASSWORD $DATABASEHOST $DATABASEPORT $DATABASENAME $DATABASESCHEMA $DATABASEUSER $DATABASEPASSWORD
$SCRIPT_DIR/mesa_lfdi_wmst_init_mosaic.sh $NAMEOFIMAGEMOSAICFWI $FILENAMEFWI $GEOSERVERURL $GEOSERVERWORKSPACE $GEOSERVERUSERNAME $GEOSERVERPASSWORD $DATABASEHOST $DATABASEPORT $DATABASENAME $DATABASESCHEMA $DATABASEUSER $DATABASEPASSWORD







