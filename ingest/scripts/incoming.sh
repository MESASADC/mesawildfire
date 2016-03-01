#!/bin/bash

set -x
set -e

SCRIPT_DIR=$(readlink -f `dirname $0`)
INGEST_DIR=$SCRIPT_DIR/..

INCRON_EVENT_DIR=$1
INCRON_EVENT_FILE=$2
INCRON_EVENT_FLAGS=$3
FILEPATH=$INCRON_EVENT_DIR/$INCRON_EVENT_FILE

# archive location for today's file
ARCHIVE_DIR=/data/archive
DATE=$(date +%Y/%m/%d)
mkdir -p $ARCHIVE_DIR/$DATE

# directory where files that failed to ingest will be kept
FAILED_DIR=/data/failed

function failed {
  mkdir -p $FAILED_DIR
  ln $FILEPATH $FAILED_DIR/$INCRON_EVENT_FILE
  echo Failed: $FAILED_DIR/$INCRON_EVENT_FILE
  logger MESA: Failed $FAILED_DIR/$INCRON_EVENT_FILE
  rm $FILEPATH
  exit 1
}

# create a hardlink to instantly create a "copy" in the archive
(ln $FILEPATH $ARCHIVE_DIR/$DATE/$INCRON_EVENT_FILE && logger MESA: Archived $ARCHIVE_DIR/$DATE/$INCRON_EVENT_FILE) || failed

# determine product type
case $INCRON_EVENT_FILE in
  ( MODIS?_FIRE.*.txt ) PRODUCT=af_modis ;;
  ( FireLoc_npp_*.txt ) PRODUCT=af_viirs ;;
  ( AMESD_SADC_MSG_W_ABBA*.txt ) PRODUCT=af_msg ;;
  ( MESA_SADC_FDI_SAfri_v1*.tif ) PRODUCT=mesa_fdifwi ;;
  ( AMESD_SADC_MODIS_TC* ) PRODUCT=modis_tc ;;
  ( * ) PRODUCT=
esac

# ingest the files we are interested in
if [ "$PRODUCT" != "" ]; then
  ($SCRIPT_DIR/$PRODUCT $INCRON_EVENT_DIR $INCRON_EVENT_FILE $INCRON_EVENT_FLAGS && logger MESA: Ingested $PRODUCT: $FILEPATH) || failed
fi

# remove (unlink) from incoming
rm $FILEPATH

