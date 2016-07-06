#!/usr/bin/python

from geoserver.catalog import Catalog
from geoserver.support import JDBCVirtualTable, JDBCVirtualTableGeometry, JDBCVirtualTableParam
cat = Catalog("http://localhost:8080/geoserver/rest/", "admin", "geoserver")

import sys, os

namespace = 'user'
workspace = cat.get_workspace(namespace)
if workspace is None:
    workspace = cat.create_workspace(namespace, 'http://mesasadc.org/' + namespace)

namespace = 'mesa'
workspace = cat.get_workspace(namespace)
if workspace is None:
    workspace = cat.create_workspace(namespace, 'http://mesasadc.org/' + namespace)

import geoserver.util

shapefile_plus_sidecars = geoserver.util.shapefile_and_friends("mesa_shapefiles/MESASADC")

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
    ft = cat.create_coveragestore("custom_background", "mesa_rasters/HYP_50M_SR_W.tif", workspace)
except Exception, e:
    print str(e)

try:
    ds = cat.get_store('mesadb', workspace)
except:
    ds = cat.create_datastore('mesadb', workspace)
    ds.connection_parameters.update(host='postgis', port='5432', database='gis', user='docker', passwd='docker', dbtype='postgis', schema='public')
    cat.save(ds)

#ft = cat.publish_featuretype('mesa_firepixel', ds, 'EPSG:4326', srs='EPSG:4326')
#ft.native_bbox = ('10', '65', '-50', '10', 'EPSG:4326')
#ft.latlon_bbox = ('10', '65', '-50', '10', 'GEOGCS["WGS84(DD)", \n  DATUM["WGS84", \n    SPHEROID["WGS84", 6378137.0, 298.257223563]], \n  PRIMEM["Greenwich", 0.0], \n  UNIT["degree", 0.017453292519943295], \n  AXIS["Geodetic longitude", EAST], \n  AXIS["Geodetic latitude", NORTH]]')
#cat.save(ft)


#ft = cat.publish_featuretype('mesa_fire', ds, 'EPSG:4326', srs='EPSG:4326')
#ft.native_bbox = ('10', '65', '-50', '10', 'EPSG:4326')
#ft.latlon_bbox = ('10', '65', '-50', '10', 'GEOGCS["WGS84(DD)", \n  DATUM["WGS84", \n    SPHEROID["WGS84", 6378137.0, 298.257223563]], \n  PRIMEM["Greenwich", 0.0], \n  UNIT["degree", 0.017453292519943295], \n  AXIS["Geodetic longitude", EAST], \n  AXIS["Geodetic latitude", NORTH]]')
#cat.save(ft)


#ft = cat.publish_featuretype('mesa_fireevent', ds, 'EPSG:4326', srs='EPSG:4326')
#ft.native_bbox = ('10', '65', '-50', '10', 'EPSG:4326')
#ft.latlon_bbox = ('10', '65', '-50', '10', 'GEOGCS["WGS84(DD)", \n  DATUM["WGS84", \n    SPHEROID["WGS84", 6378137.0, 298.257223563]], \n  PRIMEM["Greenwich", 0.0], \n  UNIT["degree", 0.017453292519943295], \n  AXIS["Geodetic longitude", EAST], \n  AXIS["Geodetic latitude", NORTH]]')
#cat.save(ft)

#ft = cat.publish_featuretype('mesa_firefeature_active', ds, 'EPSG:4326', srs='EPSG:4326')
#ft.native_bbox = ('10', '65', '-50', '10', 'EPSG:4326')
#ft.latlon_bbox = ('10', '65', '-50', '10', 'GEOGCS["WGS84(DD)", \n  DATUM["WGS84", \n    SPHEROID["WGS84", 6378137.0, 298.257223563]], \n  PRIMEM["Greenwich", 0.0], \n  UNIT["degree", 0.017453292519943295], \n  AXIS["Geodetic longitude", EAST], \n  AXIS["Geodetic latitude", NORTH]]')
#cat.save(ft)

#ft = cat.publish_featuretype('mesa_fireevent', ds, 'EPSG:4326', srs='EPSG:4326')
#ft.native_bbox = ('10', '65', '-50', '10', 'EPSG:4326')
#ft.latlon_bbox = ('10', '65', '-50', '10', 'GEOGCS["WGS84(DD)", \n  DATUM["WGS84", \n    SPHEROID["WGS84", 6378137.0, 298.257223563]], \n  PRIMEM["Greenwich", 0.0], \n  UNIT["degree", 0.017453292519943295], \n  AXIS["Geodetic longitude", EAST], \n  AXIS["Geodetic latitude", NORTH]]')
#cat.save(ft)


os.system('curl -v -u "admin:geoserver" -XPOST -T lfdi_point_forecast_and_measured_current.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesadb/featuretypes')


#os.system('curl -v -u "admin:geoserver" -XPOST -T hotpots_today.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesadb/featuretypes')
os.system('curl -v -u "admin:geoserver" -XPOST -T mesa_fdipoint.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesadb/featuretypes')

os.system('curl -v -u "admin:geoserver" -XPOST -T fires_today.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesadb/featuretypes')
os.system('curl -v -u "admin:geoserver" -XPOST -T fires_since_yesterday.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesadb/featuretypes')
os.system('curl -v -u "admin:geoserver" -XPOST -T hotspots_today.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesadb/featuretypes')
os.system('curl -v -u "admin:geoserver" -XPOST -T hotspots_since_yesterday.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesadb/featuretypes')
os.system('curl -v -u "admin:geoserver" -XPOST -T MSG_hotspots_today.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesadb/featuretypes')
os.system('curl -v -u "admin:geoserver" -XPOST -T MSG_hotspots_since_yesterday.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesadb/featuretypes')
os.system('curl -v -u "admin:geoserver" -XPOST -T hotpots_for_fires_today.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesadb/featuretypes')


os.system('curl -v -u "admin:geoserver" -XPOST -T mesa_shapefiles.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/datastores')
os.system('curl -v -u admin:geoserver -XPUT -H "Content-type: text/plain" -d "file:///opt/geoserver/data_dir/data/mesa/mesa_shapefiles" "http://localhost:8080/geoserver/rest/workspaces/mesa/datastores/mesa_shapefiles/external.shp?configure=all"')

os.system('curl -v -u "admin:geoserver" -XPOST -T HYP_50M_SR_W.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/mesa/coveragestores')
os.system('curl -v -u "admin:geoserver" -XPUT -H "Content-type: text/plain" -d "file:///opt/geoserver/data_dir/data/mesa/mesa_rasters" "http://localhost:8080/geoserver/rest/workspaces/mesa/coveragestores/HYP_50M_SR_W/external.geotiff?configure=first')

#os.system('curl -v -u "admin:geoserver" -XPOST -T user_shapefiles.xml -H "Content-type: text/xml" http://localhost:8080/geoserver/rest/workspaces/user/datastores')
os.system('curl -v -u admin:geoserver -XPUT -H "Content-type: text/plain" -d "file:///opt/geoserver/data_dir/data/user/user_shapefiles" "http://localhost:8080/geoserver/rest/workspaces/user/datastores/user_shapefiles/external.shp?configure=all"')

os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T MSG_Hotspots.sld "http://localhost:8080/geoserver/rest/styles"')  
os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T MSG_hotspots_legend.sld "http://localhost:8080/geoserver/rest/styles"')
os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T firepixel.sld "http://localhost:8080/geoserver/rest/styles"')
os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T firepixel_legend.sld "http://localhost:8080/geoserver/rest/styles"')
os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T point_text.sld "http://localhost:8080/geoserver/rest/styles"')
os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T fdi_point.sld "http://localhost:8080/geoserver/rest/styles"')
os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T gadm2.sld "http://localhost:8080/geoserver/rest/styles"')
os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T firefeature.sld "http://localhost:8080/geoserver/rest/styles"')
os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T polygon_border.sld "http://localhost:8080/geoserver/rest/styles"')
os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T firepixel_legend_grayscale.sld "http://localhost:8080/geoserver/rest/styles"')
os.system('curl -u admin:geoserver -XPOST -H "Content-type: application/vnd.ogc.sld+xml" -T firepixel_grayscale.sld "http://localhost:8080/geoserver/rest/styles"')



os.system('curl -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>fdi_point</name><workspace>mesa</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/mesa:mesa_fdipoint')
os.system('curl -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>Default Styler</name><workspace>mesa</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/mesa:MESASADC')

os.system('curl -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>fdi_point</name><workspace>mesa</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/mesa:lfdi_point_forecast_and_measured_current')
os.system('curl -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>MSG_Hotspots</name><workspace>mesa</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/mesa:MSG_hotspots_since_yesterday')
os.system('curl -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>MSG_Hotspots</name><workspace>mesa</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/mesa:MSG_hotspots_today')

os.system('curl -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>firepixel</name><workspace>mesa</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/mesa:hotspots_today')
os.system('curl -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>firepixel</name><workspace>mesa</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/mesa:hotspots_since_yesterday')
os.system('curl -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>firefeature</name><workspace>mesa</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/mesa:fires_today')
os.system('curl -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>firefeature</name><workspace>mesa</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/mesa:fires_since_yesterday')
os.system('curl -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>firepixel_grayscale</name><workspace>mesa</workspace></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/mesa:hotpots_for_fires_today')

