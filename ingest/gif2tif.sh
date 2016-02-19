gdal_translate $1 $1.tif
gdal_edit.py -a_srs "+proj=stere +lat_ts=-60.0 +lat_0=-90.0 +lon_0=28.0 +k_0=1.0" -a_ullr -4981512.5775054181 5124521.2160643581 46453487.422494582 39414521.216064358 $1.tif
