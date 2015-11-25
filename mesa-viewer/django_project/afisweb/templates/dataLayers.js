{% load misc_tags %}
function setDataLayers(theEnabledLayersList, theDisabledLayersList) 
{
  {# This function refreshes the map layers, both at initial page load and when the #}
  {# user saves new layer stack from Layer Manager.#}

  {% if myObjects.length == 0 %}
  return;
  {% endif %}
  
  {# ---------------------------------------------- #}
  {# First we create Javascript defs for each layer #}
  {# ---------------------------------------------- #}
  //var now = new Date();
  //var tzo = encodeURIComponent(now.getTimezoneOffset().toString());
  // requires jquery.cookie.js, cookie value set in afis.js using getTimezoneOffset()
  var tzo = encodeURIComponent(decodeURIComponent($.cookie('timezoneoffset')));
  var tz = encodeURIComponent(decodeURIComponent($.cookie('timezone')));
  {# myObjects are UserWMSLayers #}
  {% for myObject in myObjects %}
      {% if myObject.has_access %}
        {# as_open_layer will return executable javascript code #}
        {# { myObject.wmslayer.as_open_layer|safe} #}
        try {
          var xxx = "{{ myObject.wmslayer.as_open_layer|remove_newlines|reduce_spaces }}";
          eval(xxx.replace(/_TZOFFSET_/g,tzo).replace(/_TIMEZONE_/g,tz));
        }
        catch(err) {
          alert('Error loading wmslayer\n' + err);
        }
    {% endif %}
  {% endfor %}


  {# ---------------------------------------------- #}
  {# Next we order the layers in the legend         #}
  {# ---------------------------------------------- #}
  {# if the parameters for this function are empty, read the order from database... #}
  if ( arguments.length < 2 ) 
  {
    {# myObjects are UserWMSLayers #}
    {% for myObject in myObjects reversed %}
      {% if myObject.has_access %}
          try
          {
            var myVisibility = false;
            {% if myObject.is_visible %}
              myVisibility = true;
            {% endif %}
            {{ myObject.wmslayer.layerName }}.setVisibility( myVisibility );
            gMap.addLayer( {{ myObject.wmslayer.layerName}} );
          }
          catch(err)
          {
            alert('Error loading {{ myObject.wmslayer.name }}\n' + err);
          }
      {% endif %}
    {% endfor %}
  
  } 
  else 
  {
    {# read the two lists, drop layers theDisabledLayersList... #}
    if ( theDisabledLayersList.length > 0 ) {
      for (var myLayerIndex=0; myLayerIndex<theDisabledLayersList.length; myLayerIndex++) {
        var myLayerId = theDisabledLayersList[myLayerIndex];
        var myLayerName = $("#available-layers li[id=" + myLayerId + "]").attr("name");
        {# pick up the OpenLayer layer variable name, the name of the layer is not suitable for map. #}
        var myLayer = gMap.getLayersByName( myLayerName );// it's an array, not a OL layer.
        if (myLayer.length > 0) {
          myLayer[0].setVisibility( false );
        }
      }
    }
    var myBaseLayerCount = 4;
    {# @NOTE By Tim. Above logic assumes 4 base layers which is bad! #}
    var myLayerZIndex = 0;
    {# ... cycle among the layers that must be in the map #}
    for ( var myLayerIndex=0; myLayerIndex < theEnabledLayersList.length; myLayerIndex++ ) 
    {
      {# z-index for openlayers is zero-indexed, and starts from bottom counting base layers. #}
      {# therefore the new index for the layer is the first above the present stack (4 base #}
      {# layers + each layer in this cycle) #}
      myLayerZIndex = myBaseLayerCount + (theEnabledLayersList.length - 1 - myLayerIndex);
      var myLayerId = theEnabledLayersList[myLayerIndex];
      var myLayerName = $("#selected-layers li[id=" + myLayerId + "]").attr("name");
      {# if it is already in the map, reset its index #}
      var myLayers = gMap.getLayersByName( myLayerName ); {# returns an array, not a OL layer. #}
      if (myLayers.length == 0) 
      {
        {# add it to map #}
        gMap.addLayer( myLayers[0] );
      }
      {# at the right place and set it visible #}
      gMap.setLayerIndex( myLayers[0], myLayerZIndex);
      myLayers[0].setVisibility( true );
    }
  }
}
