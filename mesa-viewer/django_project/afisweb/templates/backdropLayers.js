{% load googlemapstag %} {# Custom tag defined in templatetags/ #}
function addBackdropLayers()
{
  {% GooglePhysicalLayer %}
  {% GoogleStreetsLayer %}
  {% GoogleHybridLayer %}
  {% GoogleSatelliteLayer %}
  {% CustomLayer %}
  {# full featured google dataset. But only the first layer is used as base layer. #}
  gMap.addLayers([ghyb,gphy,gmap,gsat,custom]);
}
