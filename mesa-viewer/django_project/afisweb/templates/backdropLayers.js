{% load googlemapstag %} {# Custom tag defined in templatetags/ #}
function addBackdropLayers()
{
  {% CustomLayer %}
  {% GooglePhysicalLayer %}
  {% GoogleStreetsLayer %}
  {% GoogleHybridLayer %}
  {% GoogleSatelliteLayer %}
  {# full featured google dataset. But only the first layer is used as base layer. #}
  gMap.addLayers([custom,ghyb,gphy,gmap,gsat]);
}
