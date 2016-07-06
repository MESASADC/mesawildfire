#!/bin/bash

set -x

SCRIPT_DIR=/home/mesa/mesawildfire/ingest/scripts
ARCHIVE_DIR=/data/archive
FAILED_DIR=/data/failed
UNKNOWN_DIR=${ARCHIVE_DIR}/UNKNOWN

# determine product type
datatype=${SCRIPT_DIR}/data_sort.csv

# loop through all the products and delete files older than specified age
while read -r line; do
  GROUP=$(echo "$line" | cut -d , -f 2)
  PRODUCT=$(echo "$line" | cut -d , -f 3)
  MAXDAYS=$(echo "$line" | cut -d , -f 7)
  OUTDIR="$ARCHIVE_DIR/$GROUP/$PRODUCT"
  [[ -z $MAXDAYS ]] && continue
  # if product directory exists then clean it
  if [[ -n "${GROUP}" ]] && [[  -n "${PRODUCT}" ]] && [[ -d "${OUTDIR}" ]]; then
     echo "cleaning ${OUTDIR}..."
     find "${OUTDIR}/" -ctime +${MAXDAYS} -exec rm -rf {} \;

  fi
done < ${datatype}

# clean UNKNOWN_DIR, keep only less than 10 days old
if [[ -d "${UNKNOWN_DIR}/" ]]; then
   echo "cleaning ${UNKNOWN_DIR}..."
   find "${UNKNOWN_DIR}/" -ctime +10 -exec rm -rf {} \;
fi
# clean FAILED_DIR, keep only less than 10 days old
if [[ -d "${FAILED_DIR}/" ]]; then
   echo "cleaning ${FAILED_DIR}..."
   find "${FAILED_DIR}/" -ctime +10 -exec rm -rf {} \;
fi
exit
