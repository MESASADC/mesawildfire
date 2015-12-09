#!/usr/bin/python

from geoserver.catalog import Catalog
cat = Catalog("http://localhost:8080/geoserver/rest/", "admin", "geoserver")


namespace = 'mesa'

workspace = cat.get_workspace(namespace)
if workspace is None:
    workspace = cat.create_workspace(namespace, 'http://mesasadc.org/' + namespace)


import geoserver.util
shapefile_plus_sidecars = geoserver.util.shapefile_and_friends("data/MESASADC")

# shapefile_and_friends should look on the filesystem to find a shapefile
# and related files based on the base path passed in
#
# shapefile_plus_sidecars == {
#    'shp': 'states.shp',
#    'shx': 'states.shx',
#    'prj': 'states.prj',
#    'dbf': 'states.dbf'
# }
# 'data' is required (there may be a 'schema' alternative later, for creating empty featuretypes)
# 'workspace' is optional (GeoServer's default workspace is used by... default)
# 'name' is required

try:
    ft = cat.create_featurestore("custom_background", shapefile_plus_sidecars, workspace)
except Exception, e:
    print str(e)


try:
    ds = cat.get_store('mesadb', workspace)
except:
    ds = cat.create_datastore('mesadb', workspace)
    ds.connection_parameters.update(host='postgis', port='5432', database='gis', user='docker', passwd='docker', dbtype='postgis', schema='public')
    cat.save(ds)


ft = cat.publish_featuretype('mesa_firepixel', ds, 'EPSG:4326', srs='EPSG:4326')
cat.save(ft)

ft = cat.publish_featuretype('mesa_fire', ds, 'EPSG:4326', srs='EPSG:4326')
cat.save(ft)

ft = cat.publish_featuretype('mesa_firefeature', ds, 'EPSG:4326', srs='EPSG:4326')
cat.save(ft)

ft = cat.publish_featuretype('mesa_firefeature_active', ds, 'EPSG:4326', srs='EPSG:4326')
cat.save(ft)

ft = cat.publish_featuretype('mesa_fireevent', ds, 'EPSG:4326', srs='EPSG:4326')
cat.save(ft)
