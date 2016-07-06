#!/bin/bash

set -x

SCRIPT_DIR=$(readlink -f `dirname $0`)
INGEST_DIR=$SCRIPT_DIR/..
ARCHIVE_DIR=/data/archive
FAILED_DIR=/data/failed

INCRON_EVENT_DIR=$1
INCRON_EVENT_FILE=$2
INCRON_EVENT_FLAGS=$3
FILEPATH=$INCRON_EVENT_DIR/$INCRON_EVENT_FILE
DATED=N

# determine product type
datatype=${SCRIPT_DIR}/data_sort.csv

# test which filter matches the incoming file
function fline (){
  fname="$1"
  while read -r line; do
  filter=$(echo "$line" | cut -d , -f 1)
  if [[ -n $(echo "$fname" | grep "$filter") ]]; then
     echo "$line"
     break
  fi
done < ${datatype}
}


line="$(fline $INCRON_EVENT_FILE)"
if [[ -n $line ]]; then
  GROUP=$(echo "$line" | cut -d , -f 2)
  PRODUCT=$(echo "$line" | cut -d , -f 3)
  DATED=$(echo "$line" | cut -d , -f 4)
  D_FORMAT=$(echo "$line" | cut -d , -f 5)
  D_POSITION=$(echo "$line" | cut -d , -f 6)
else
  GROUP=UNKNOWN
  PRODUCT=
  DATE=$(date +"%Y/%m/%d")
  DATED=
fi


if [[ "${DATED}" == "Y" ]]; then
   if [[ "$D_FORMAT" == "YYYYDOY" ]] && [[ -n ${D_POSITION} ]]; then
      fdate=${INCRON_EVENT_FILE:D_POSITION:7}
      year=${fdate:0:4}
      doy=${fdate:4:3}
      doy=$((doy-1))
      DATE=$(date +"%Y/%m/%d" -d "${year}0101 + $doy days")
   elif [[ "$D_FORMAT" == "YYYYMMDD" ]] && [[ -n ${D_POSITION} ]]; then
      fdate=${INCRON_EVENT_FILE:D_POSITION:8}
      DATE=$(date +"%Y/%m/%d" -d "${fdate}")
   elif [[ "$D_FORMAT" == "YYYY-MM-DD" ]] && [[ -n ${D_POSITION} ]]; then
      fdate=$(echo ${INCRON_EVENT_FILE:D_POSITION:10} | sed 's/-//g')
      DATE=$(date +"%Y/%m/%d" -d "${fdate}")
   fi
fi

# archive location for today's file
OUTDIR="$ARCHIVE_DIR/$GROUP/$PRODUCT/$DATE"
mkdir -p "$OUTDIR"

# function to send files that failed to ingest to the failed directory
function failed {
  mkdir -p $FAILED_DIR/$1
  ln $FILEPATH $FAILED_DIR/$1/$INCRON_EVENT_FILE
  echo Failed to $1: $FAILED_DIR/$1/$INCRON_EVENT_FILE
  logger MESA: Failed to $1: $FAILED_DIR/$1/$INCRON_EVENT_FILE
  rm $FILEPATH
  exit 1
}

# create a hardlink to instantly create a "copy" in the archive
if [ ! -e "$OUTDIR/$INCRON_EVENT_FILE" ]; then
  (ln $FILEPATH "$OUTDIR/$INCRON_EVENT_FILE" && logger MESA: Archived "$OUTDIR/$INCRON_EVENT_FILE") || failed "archive"
fi

# ingest the files we are interested in
if [[ -n $PRODUCT ]] && [[ -n $( ls "${SCRIPT_DIR}" | grep "$PRODUCT") ]]; then
  # create a hardlink to instantly create a "copy" in the ingest directory. Note: PostGIS uses this link for out of DB raster access!
  if [ ! -e $INGEST_DIR/$PRODUCT/$INCRON_EVENT_FILE ]; then
    ln $FILEPATH $INGEST_DIR/$PRODUCT/$INCRON_EVENT_FILE || cp $FILEPATH $INGEST_DIR/$PRODUCT/$INCRON_EVENT_FILE || failed "link"
  fi
  # run the script for the product
  ($SCRIPT_DIR/$PRODUCT $INCRON_EVENT_DIR $INCRON_EVENT_FILE $INCRON_EVENT_FLAGS && logger MESA: Ingested $PRODUCT: $INGEST_DIR/$PRODUCT/$INCRON_EVENT_FILE) || failed "ingest"
fi

# remove (unlink) from incoming
rm $FILEPATH

