{% load misc_tags %}
function setDataLayers(theEnabledLayersList, theDisabledLayersList) 
{
  $(document).ready(function() {
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
  var time_slider = $('#slider').slider( "option", "value" );
  //var time_sliders = $('#sliders').slider( "option", "value" );

  // Convert Javascript date to Pg YYYY MM DD HH MI SS
  function pgFormatDate(date) {
    /* Via http://stackoverflow.com/questions/3605214/javascript-add-leading-zeroes-to-date */
    function zeroPad(d) {
      return ("0" + d).slice(-2)
    }
    var parsed = new Date(date)
    var date = [parsed.getUTCFullYear(), zeroPad(parsed.getMonth() + 1), zeroPad(parsed.getDate())].join("-");
    var time = [zeroPad(parsed.getHours()), zeroPad(parsed.getMinutes()), zeroPad(parsed.getSeconds())].join(":");
    return [date,time].join(" ");
  }

  /*$("#time_slider").slider({
      max: 720,
      min: 0,
      step: 60,
      slide: function (e, ui) {
          var hours = Math.floor(ui.value / 60);
          var minutes = ui.value - (hours * 60);

          if(hours.toString().length == 1) hours = '0' + hours;
          if(minutes.toString().length == 1) minutes = '0' + minutes;

        $("#time_slider_value").html( ui.value == 0 ? 'Time filter: No' : 'Time filter: Last ' + hours+':'+minutes + ' hours' );
      }
   });*/
  //(parseInt(ui.value)-1)
  $("#time_slider").slider({
      max: 72,
      min:1,
      step: 4,
      value:24,
      slide: function (e, ui) {
        $("#time_slider_value").html( (parseInt(ui.value)-1) == 0 ? 'Time filter: Last ' + (parseInt(ui.value)) + ' hours' : 'Time filter: Last ' + (parseInt(ui.value)-1) + ' hours' );
        /*if(ui.value>24){

          /*if((parseInt(ui.value)-1) == 48){
            $("#time_slider_value").html('Time filter: Yesterday');
          }else if((parseInt(ui.value)-1) == 72){
           $("#time_slider_value").html('Time filter: Day before Yesterday');
          }else if((parseInt(ui.value)-1) == 96){
           $("#time_slider_value").html('Time filter: Day After');
          }

          $(this).slider("option", "step",24);
          $(this).slider("option", "max",96);
          $(this).slider("option", "min",1);
        }
        else{
          $(this).slider("option", "step",1);
        }*/
      }
   });
   
  $("#time_slider_label").html("Time filter: Last "+$('#time_slider').slider('option','value')+" hours");

  $("#frp_slider").slider({
      max: 1000,
      step: 50,
      slide: function (e, ui) {
        $("#frp_slider_value").html( ui.value == 0 ? 'FRP filter: No' : 'FRP filter: Above ' + ui.value + ' MW/km2' );
      }
  });


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
 }); 
}
