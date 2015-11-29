import os
from zipfile import ZipFile

from django.contrib.gis.gdal import *

from settings import *

def getFeaturesFromZipFile( zipfile, geometry, numFeatures = "all"):
  """ Takes a zip archive and extracts N features of the specified geometry type. """
  
  # inspect the zip file
  zippedShape = ZipFile(zipfile)
  # check if the contents of the archive are the usual 3 files with no subdirectories.
  if any([f.endswith('/') for f in zippedShape.namelist()]):
    raise RuntimeError('The archive contains subdirectories. Please zip only the shp, .shx, .dbf[, .prj] files.')
  extensionsList = [fullname.split(".")[-1] for fullname in zippedShape.namelist()]
  presentExtensions = set(extensionsList).intersection(set(["shp", "shx", "dbf"]))
  if len(presentExtensions) < 3:
    raise RuntimeError('At least one of .shp, .shx, .dbf is missing.')
  # extract - for Python 2.5. Python 2.6 has a nice ZipFile.extract()
  for each in zippedShape.namelist():
    destinationFile = os.path.join(MEDIA_ROOT, each)
    data = zippedShape.read(each)
    f = open(destinationFile, 'w')
    f.write(data)
    f.close()
  zippedShape.close()
  
  shpName = [elem for elem in zippedShape.namelist() if "shp" in elem].pop()
  shpFileOnDiskPath = os.path.join(MEDIA_ROOT, shpName)
  # load the shapefile in GeoDjango
  dataSource = DataSource(shpFileOnDiskPath)
  
  # extract the first polygon if any
  if dataSource[0].geom_type == geometry:
    firstLayer = dataSource[0]
  else:
    # cleanup before exiting
    for each in zippedShape.namelist():
      os.remove(os.path.join(MEDIA_ROOT, each))
    raise RuntimeError('The geometry ' + geometry + ' is not available in this shapefile.')
  
  # some info.
  print "Zip archive name: " + zippedShape.filename
  print "Shapefile name: " + shpName
  print "Full datasource name: " + dataSource.name
  print "Number of available features: " + str(dataSource[0].num_feat)
  print "Geometry type: " + firstLayer.geom_type.name
  print "Number of extracted features: " + str(numFeatures)
  
  # extract the N geometries, otherwise all of them
  if numFeatures != "all":
    geometriesList = [pt.wkt for pt in firstLayer.get_geoms()][0:numFeatures]
  else:
    geometriesList = [pt.wkt for pt in firstLayer.get_geoms()]
  
  # cleanup of dezipped files
  for each in zippedShape.namelist():
    os.remove(os.path.join(MEDIA_ROOT, each))

  # return the data
  return geometriesList