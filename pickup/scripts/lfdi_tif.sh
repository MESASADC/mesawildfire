#!/bin/bash

INCRON_EVENT_DIR=$1
INCRON_EVENT_FILE=$2
INCRON_EVENT_FLAGS=$3

# Example: MESA_SADC_FDI_SAfri_v1.2016-02-01T1200Z.2016-02-01T1200Z.lfdid.tif

# Use Python's regex module. Regex created using https://regex101.com/#python
PARAMS=( $(python -c \
"import sys,re; \
match = re.match(r'.*(?P<target_datetime>.{16})(?<=Z)\.(?P<datetime>.{16})(?<=Z)\.(?P<product>.*(?=\.)).*', sys.argv[1]); \
print ' '.join(match.groups()) \
" $INCRON_EVENT_FILE ) \
)

DATETIME=${PARAMS[0]}
DATETIME_TARGET=${PARAMS[1]}
PRODUCT=${PARAMS[2]}

raster2pgsql -R -e $INCRON_EVENT_DIR/$INCRON_EVENT_FILE lfdi_fwi_raster | ./pginsert-customize.py datetime "'$DATETIME'::timestamp" target_datetime "'$DATETIME_TARGET'::timestamp" product "'$PRODUCT'" rasterfile "'$INCRON_EVENT_DIR/$INCRON_EVENT_FILE'"
