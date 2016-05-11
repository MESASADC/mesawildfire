{% load mapboxtag %} {# Custom tag defined in templatetags/ #}

function addBackdropLayers()
{
  {% custom_layer %}

  {% no_internet as no_internet %}

  {% if no_internet %}
      gMap.addLayers([custom]);
  {% else %}
      {% mb_outdoors_layer %}
      {% mb_streets_satellite_layer %}
      {% mb_streets_layer %}
      {% mb_light_layer %}
      {% mb_dark_layer %}
      {% mb_satellite_layer %}
      gMap.addLayers([custom, mbOutdoors, mbStreetsSatellite,mbStreets,mbLight,mbDark,mbSatellite]);
  {% endif %}
}
