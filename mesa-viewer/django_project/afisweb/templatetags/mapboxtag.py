
from django import template
from django.conf import settings
import json


register = template.Library()

@register.simple_tag
def mb_outdoors_layer():
 return '''mbOutdoors = new OpenLayers.Layer.XYZ('Mapbox Outdoors',
                                        ['https://a.tiles.mapbox.com/v4/mapbox.outdoors/${z}/${x}/${y}.png?access_token=pk.eyJ1Ijoic3RldmVtYXNoYSIsImEiOiJjaW5zcmcwdGMwMGw5dnNrbDFhcHRiMzlpIn0.nx8V3jDtK_eGt2UzTWnjAw'], {
                                        sphericalMercator: true,
                                        wrapDateLine: true
                                       });'''

@register.simple_tag
def mb_streets_satellite_layer():
 return '''mbStreetsSatellite = new OpenLayers.Layer.XYZ('Mapbox Streets and Satellite',
                                        ['https://a.tiles.mapbox.com/v4/mapbox.streets-satellite/${z}/${x}/${y}.png?access_token=pk.eyJ1Ijoic3RldmVtYXNoYSIsImEiOiJjaW5zcmcwdGMwMGw5dnNrbDFhcHRiMzlpIn0.nx8V3jDtK_eGt2UzTWnjAw'], {
                                        sphericalMercator: true,
                                        wrapDateLine: true
                                       });'''

@register.simple_tag
def mb_streets_layer():
 return '''mbStreets = new OpenLayers.Layer.XYZ('Mapbox Streets',
                                        ['https://a.tiles.mapbox.com/v4/mapbox.streets/${z}/${x}/${y}.png?access_token=pk.eyJ1Ijoic3RldmVtYXNoYSIsImEiOiJjaW5zcmcwdGMwMGw5dnNrbDFhcHRiMzlpIn0.nx8V3jDtK_eGt2UzTWnjAw'], {
                                        sphericalMercator: true,
                                        wrapDateLine: true
                                       });'''

@register.simple_tag
def mb_light_layer():
 return '''mbLight = new OpenLayers.Layer.XYZ('Mapbox Light',
                                        ['https://a.tiles.mapbox.com/v4/mapbox.light/${z}/${x}/${y}.png?access_token=pk.eyJ1Ijoic3RldmVtYXNoYSIsImEiOiJjaW5zcmcwdGMwMGw5dnNrbDFhcHRiMzlpIn0.nx8V3jDtK_eGt2UzTWnjAw'], {
                                        sphericalMercator: true,
                                        wrapDateLine: true
                                       });'''

@register.simple_tag
def mb_dark_layer():
 return '''mbDark = new OpenLayers.Layer.XYZ('Mapbox Dark',
                                        ['https://a.tiles.mapbox.com/v4/mapbox.dark/${z}/${x}/${y}.png?access_token=pk.eyJ1Ijoic3RldmVtYXNoYSIsImEiOiJjaW5zcmcwdGMwMGw5dnNrbDFhcHRiMzlpIn0.nx8V3jDtK_eGt2UzTWnjAw'], {
                                        sphericalMercator: true,
                                        wrapDateLine: true
                                       });'''


@register.simple_tag
def mb_satellite_layer():
 return '''mbSatellite = new OpenLayers.Layer.XYZ('Mapbox Satellite',
                                        ['https://a.tiles.mapbox.com/v4/mapbox.satellite/${z}/${x}/${y}.png?access_token=pk.eyJ1Ijoic3RldmVtYXNoYSIsImEiOiJjaW5zcmcwdGMwMGw5dnNrbDFhcHRiMzlpIn0.nx8V3jDtK_eGt2UzTWnjAw'], {
                                        sphericalMercator: true,
                                        wrapDateLine: true
                                       });'''                                                                                                                     

@register.simple_tag
def custom_layer():
 layer = settings.CUSTOM_LAYER
 return '''custom = new OpenLayers.Layer.WMS("Custom",
                                   "{host}",{{
                                    srs: 'EPSG:4326',
                                    layers: "{namespace}:{layer_name}",
                                    transparent: false,
                                    format: "image/png",
                                    isBaseLayer: true
                                    }});
        '''.format(**layer)


@register.assignment_tag
def no_internet():
 return settings.NO_INTERNET
