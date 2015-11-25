from django import template
from django.conf import settings
import json

register = template.Library()
@register.simple_tag
def GoogleMapsApiKey( ):
  return settings.GOOGLE_MAPS_API_KEY

@register.simple_tag
def GoogleHybridLayer():
  return '''ghyb = new OpenLayers.Layer.Google(
           "Google Hybrid",
           {type: google.maps.MapTypeId.HYBRID}
           );
        '''


@register.simple_tag
def GooglePhysicalLayer():
  return '''gphy = new OpenLayers.Layer.Google(
           "Google Physical",
           {type: google.maps.MapTypeId.TERRAIN}
           );
         '''

@register.simple_tag
def GoogleStreetsLayer():
  return '''gmap = new OpenLayers.Layer.Google(
           "Google Streets", // the default
           {type: google.maps.MapTypeId.ROADMAP}
           );
        '''

@register.simple_tag
def GoogleSatelliteLayer():
 return '''gsat = new OpenLayers.Layer.Google(
           "Google Satellite",
           {type: google.maps.MapTypeId.SATELLITE}
           );
        '''


@register.simple_tag
def CustomLayer():
 layer = settings.CUSTOM_LAYER
 return '''custom = new OpenLayers.Layer.WMS("User Custom Layer",
                                   "{host}",{{
                                    srs: 'EPSG:4326',
                                    layers: "{namespace}:{layer_name}",
                                    transparent:"true",
                                    format: "image/gif"
                                    }});
        '''.format(**layer)
