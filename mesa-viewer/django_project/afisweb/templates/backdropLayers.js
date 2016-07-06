{% load mapboxtag %} {# Custom tag defined in templatetags/ #}

function addBackdropLayers()
{
  /*var parser = new OpenLayers.Format.WMSCapabilities();
  fetch('/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities').then(function(response) {
      return response.text();
  }).then(function(text) { */

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

        /*var result = parser.read(text);
        var timestamp;
        var layer_s = result.capability.layers;
        for(var x = 0; x < Object.keys(layer_s).length; x++)
        {
          if(layer_s[x].dimensions.hasOwnProperty('time'))
          {
            timestamp = layer_s[x].dimensions.time.values;
          }
        }
        console.log(timestamp);

        lyr10 = new OpenLayers.Layer.WMS(
        'MSG weather animination','/geoserver/wms?viewparams=tzoffset:_TZOFFSET_;tz:_TIMEZONE_',
            {
                layers: 'mesa:mesaframes',
                time: timestamp[0],
                transparent: 'true',
                format: 'image/png'
            },
            {
                minScale: 35000000,
                maxScale: 1,
                singleTile: true,
                opacity: 1.0
            }
        );*/
        gMap.addLayers([custom, mbOutdoors, mbStreetsSatellite,mbStreets,mbLight,mbDark,mbSatellite]);
        //});
    {% endif %}
  }




