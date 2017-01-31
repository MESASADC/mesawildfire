//----------------------------------------------------------------
//
// AFIS Javascript Functions. These functions make heavy use of
// openlayers api and JQuery API.
//                                            Tim Sutton 2010
//----------------------------------------------------------------

var AFIS_PREFIX = "";


//-------------------------------------------
// OpenLayers Related stuff follows
//-------------------------------------------

var gMap = null;
var gMapControls = null;
var gDefaultLat = -28.5;
var gDefaultLon = 24;
var gZoomLevel = 5;
var gPlaceZoomLevel = 8;
var gLayers = null;
var gLayersDict = {};
var userLocation = 'africa';
var myLoadingPanel;
var myDateQueryDialog;
OpenLayers.ProxyHost = "/cgi-bin/proxy.cgi?url=";

var lookupWasSuccessful = false;   
var lookupAoi = null;




function toHDD_MM_MMM(deg, h, H) {
    var str = "";
	var val;

	str += (deg > 0) ? H : h;
	val = Math.abs(deg);
	str += parseInt (val) + '.'; // degrees
	val = (val - parseInt(val)) * 60;
	str += parseInt (val) + ","; // minutes
	val = (val - parseInt(val)) * 1000;
	str += parseInt (val); // decimal minutes

    return str;
}

function formatFloat(value, precision) {
	var power = Math.pow(10, precision || 0);
    return String(Math.round(value * power) / power);
}

function formatMouseCoordinates(lonLat) {

    var str = "";

	// HDD_MM_MMM format:
	try {
		str += toHDD_MM_MMM(lonLat.lon, 'W', 'E');
		str += "  ";
		str += toHDD_MM_MMM(lonLat.lat, 'S', 'N');
	} catch ( e ) {
		// just keep swimming...
	};
	
	return str;
}


/*
if (!(typeof urlQuerystringLat === 'undefined') && !(typeof urlQuerystringLon === 'undefined')) {    
    gDefaultLat = urlQuerystringLat;
    gDefaultLon = urlQuerystringLon;
    gZoomLevel = 10;
} else if (location.hostname.indexOf('global.') == 0) {
    userLocation = 'global';
    gDefaultLat = 0;
    gDefaultLon = 0;
    gZoomLevel = 2;
} else if (location.hostname.indexOf('easteurope.') == 0) {
    userLocation = 'easteurope';
    gDefaultLat = 48;
    gDefaultLon = 25;
} else if (location.hostname.indexOf('europe.') == 0) {
    userLocation = 'europe';
    gDefaultLat = 48;
    gDefaultLon = 10.8;
} else if (location.hostname.indexOf('eastafrica.') == 0) {
    userLocation = 'eastafrica';
    gDefaultLat = 3;
    gDefaultLon = 31;
} else if (location.hostname.indexOf('southamerica.') == 0) {
    userLocation = 'southamerica';
    gDefaultLat = -18;
    gDefaultLon = -60;
    gZoomLevel = 4;
} else if (location.hostname.indexOf('northamerica.') == 0) {
    userLocation = 'northamerica';
    gDefaultLat = 39.5;
    gDefaultLon = -99.2;
    gZoomLevel = 4;
} else if ((location.hostname.indexOf('zim.') == 0) || (location.hostname.indexOf('.zw.') >= 0)) {
    userLocation = 'zimbabwe';
    gDefaultLat = -19;
    gDefaultLon = 30;
    gZoomLevel = 7;
} else if ((location.hostname.indexOf('argentina.') == 0) || (location.hostname.indexOf('.ar.') >= 0)) {
    userLocation = 'argentina';
    gDefaultLat = -35;
    gDefaultLon = -65;
    gZoomLevel = 4;
} else if ((location.hostname.indexOf('portugal.') == 0) || (location.hostname.indexOf('.pt.') >= 0)) {
    userLocation = 'portugal';
    gDefaultLat = 40;
    gDefaultLon = -8;
    gZoomLevel = 7;
} else if ((location.hostname.indexOf('southernafrica.') == 0) || (location.hostname.indexOf('.za.') >= 0)) {
    userLocation = 'southernafrica';
    gDefaultLat = -28.5;
    gDefaultLon = 24;
    gZoomLevel = 5;
} else if (location.hostname.indexOf('westafrica.') == 0) {
    userLocation = 'westafrica';
    gDefaultLat = 9;
    gDefaultLon = 4;
    gZoomLevel = 5;
} else if (location.hostname.indexOf('ca.us.') == 0) {
    userLocation = 'california';
    gDefaultLat = 36.4;
    gDefaultLon = -117.36;
    gZoomLevel = 6;
} else {
    userLocation = 'sadc';
    gDefaultLat = 0;
    gDefaultLon = 0;
    gZoomLevel = 3;
}
*/

userLocation = 'sadc';
gDefaultLat = -18.25;
gDefaultLon = 25;
gZoomLevel = 4;


if (!(typeof urlQuerystringZoom === 'undefined') && urlQuerystringZoom >= 1 && urlQuerystringZoom <= 18) {
    gZoomLevel = urlQuerystringZoom;
}

function setupOpenLayers() {
  try {
    var myOptions = {
      projection: new OpenLayers.Projection("EPSG:900913"),
      displayProjection: new OpenLayers.Projection("EPSG:4326"),
      units: "m",
      numZoomLevels: 18,
      maxResolution: 156543.0339,
      maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34, 20037508.34, 20037508.34),
      controls: [] //no controls by default we add them explicitly lower down
    };
    gMap = new OpenLayers.Map('map', myOptions);

    gMap.addControl(new OpenLayers.Control.MousePosition({
      element: OpenLayers.Util.getElement('coordinates')
    }));

    gMap.addControl(new OpenLayers.Control.MousePosition({
      element: OpenLayers.Util.getElement('coordinates2'),
      formatOutput: formatMouseCoordinates
    }));

    // the control is outside the map
    gMap.addControl(new OpenLayers.Control.ScaleBar({
      div: document.getElementById("scalebar"),
      align: "right",
      minWidth: 200,
      maxWidth: 300
    }));

    //20130114 OL-2.12 gMap.addControl(new OpenLayers.Control.MouseDefaults());
    gMap.addControl(new OpenLayers.Control.Navigation());

    // myLoadingPanel = new OpenLayers.Control.LoadingPanel();
    // gMap.addControl(myLoadingPanel);


    /* Measure distance and area controls. From
     * http://dev.openlayers.org/releases/OpenLayers-2.8/examples/measure.html
     * */

    gMapControls = {
      line: new OpenLayers.Control.Measure(
      OpenLayers.Handler.Path, {
        persist: true
      }),
      polygon: new OpenLayers.Control.Measure(
      OpenLayers.Handler.Polygon, {
        persist: true
      }),
      zoomin: new OpenLayers.Control.ZoomBox({
        title: "Zoom in box",
        out: false
      }),
      zoomout: new OpenLayers.Control.ZoomBox({
        title: "Zoom out box",
        out: true
      })
    };

    var myControl;
    for (var myKey in gMapControls)
    {
      myControl = gMapControls[myKey];
      myControl.events.on({
        "measure": handleMeasurements,
        "measurepartial": handleMeasurements
      });
      gMap.addControl( myControl );
    }

    /* End measure distance snippet */

    // display the progress bar
    // myLoadingPanel.maximizeControl();

    // This timezone detection code has to be placed before the setDataLayers call!
    // Requires jquery.cookie.js
    if(($.cookie('timezoneoffset')==null) || ($.cookie('timezone')==null)) {
      var now = new Date();
      var tzoval = parseInt(-(new Date()).getTimezoneOffset(), 10);
      var tzo = encodeURIComponent(tzoval.toString());
      $.cookie('timezoneoffset', tzo, { expires: 1, path: '/' });
      var tz = encodeURIComponent((tzoval/60).toString());
      $.cookie('timezone', tz, { expires: 1, path: '/' });
    }

    addBackdropLayers();
    setDataLayers();

    // for wildcard subdomains, ex. wc.za.afis.co.za, we get the lat,lon and extent values from the gadm2 database
    try {
      if (userLocation == 'lookup') {
        $.get(AFIS_PREFIX + "/getWildcardSubDomainInfo/", 
          function( theData ) {
            try {
                var response = $.parseJSON( theData );
                if (response.success) {
                  lookupAoi = new OpenLayers.Bounds(response.info.west, response.info.south, response.info.east, response.info.north);
                  var mapAoi = lookupAoi.clone().transform(new OpenLayers.Projection("EPSG:4326"), gMap.getProjectionObject());
                  gMap.zoomToExtent(mapAoi);
                  lookupWasSuccessful = true;
                }
                else {
                  lookupWasSuccessful = false;
                  resetZoomExtents();
                }
            }
            catch (err) {
                lookupWasSuccessful = false;
                resetZoomExtents();
            }     
          }
        );
      }
      else {
        lookupWasSuccessful = false;
        resetZoomExtents();
      }
    }
    catch (err) {
      lookupWasSuccessful = false;
      resetZoomExtents();
    }     
 
    // remove it as the above function returns
    // myLoadingPanel.minimizeControl();
    
    // getFeatureInfo, not done by openlayers as it requires proxy
    // for cross site calls, but instead by Django via a view
    gMap.events.register('click', gMap, showFeatureInfo );
    gMap.events.register('click', gMap, getFireReport);

  }
  catch (err) {
    alert('Could not initialize:\n' + err);
  }
}

function handleMeasurements(event) {
  var myGeometry = event.geometry;
  var myUnits = event.units;
  var myOrder = event.order;
  var myMeasure = event.measure;
  var myResult = "";
  if ( myOrder == 1 )
  {
    myResult += "Measure: " + myMeasure.toFixed(3) + " " + myUnits;
  }
  else
  {
    // square kms
    //myResult += "Measure: " + measure.toFixed(3) + " " + myUnits + "<sup>2</" + "sup>"; // leftover for square kms
    // hectares
    myResult += "Measure: " + myMeasure.toFixed(3) * 100 + " " + "ha";
  }
  $("#output").html( myResult );
}

function toggleControl(theElement)
{
  for (myKey in gMapControls)
  {
    var myControl = gMapControls[myKey];
    if( $(theElement).attr("value") == myKey )
    {
      myControl.activate();
    }
    else
    {
      myControl.deactivate();
    }
  }
}

function scaleChanged()
{
  $("#output").html("Scale changed to: " + gMap.scale() );
  alert("Scale changed! " + gMap.scale());
}

function recenterToDefaultPosition()
{
  if (lookupWasSuccessful) {
    // Fit map to lookup AOI bounds   
    var mapAoi = lookupAoi.clone().transform(new OpenLayers.Projection("EPSG:4326"), gMap.getProjectionObject());
    gMap.zoomToExtent(mapAoi);
  }
  else {
    // no lookupAoi defined, so use default lon,lat and zoom
    var myLonLat = new OpenLayers.LonLat(
      gDefaultLon, gDefaultLat).transform(
        new OpenLayers.Projection("EPSG:4326"), gMap.getProjectionObject());
    gMap.setCenter(myLonLat, gZoomLevel);
  }
}

function getFireReport(event)
{
  if(!$("#fire-report-button").is(':checked')) {
   return;
  }
  $("#messages").html('Querying, please wait...<img src=' + AFIS_PREFIX + '"/static/images/query-progress.gif" style="vertical-align:middle">');
  $("#messages").slideDown('slow'); 
  var myMousePos = gMap.getLonLatFromPixel(event.xy);
  var EPSG4326 = new OpenLayers.Projection("EPSG:4326");
  var EPSG900913 = new OpenLayers.Projection("EPSG:900913");
  var myLonLatGCS = myMousePos.transform( EPSG900913,EPSG4326 );
  var lon = myMousePos.lon;
  var lat = myMousePos.lat;
  $.get(AFIS_PREFIX + "/getFireReport?theLon=" + lon + "&theLat=" +lat ,function(theData){
    $("#messages").html('Query complete');
    $("#query-results").html( theData );
    var myQueryResultsDialog = $('#query-results').dialog({     
      autoOpen: true,      
      title: 'Fire Information Report',
      buttons: { "Ok": function() { $(this).dialog("close"); } },
      closeOnEscape: false,
      dialogClass: 'scrollable',
      height: $(window).height() / 1.5,
      width: $(window).width() / 1.5,
      cache:false,
      zIndex: 1003,
      modal: true, 
      open: function(event, ui) { $('#top_firereport').focus(); }
    });
  });
  return false;
}

// Get feature info implementation for openlayer
// see http://trac.openlayers.org/wiki/GetFeatureInfo
function showFeatureInfo(event)
{
  //only do it if the identify tool is enabled
  if (!$("#identify-button").is(':checked'))
  {
    return;
  }
  $("#messages").html('Querying, please wait...<img src=' + AFIS_PREFIX + '"/static/images/query-progress.gif" style="vertical-align:middle">');
 
 

  $("#messages").slideDown('slow');  
  var myMousePos = gMap.getLonLatFromPixel(event.xy);
  var EPSG4326 = new OpenLayers.Projection("EPSG:4326");
  var EPSG900913 = new OpenLayers.Projection("EPSG:900913");
  var myLonLatGCS = myMousePos.transform( EPSG900913,EPSG4326 );
  var myBounds = gMap.getExtent().clone();
  //var myBounds = myBounds.transform(EPSG900913, EPSG4326);
  var myBoundingBox = myBounds.toBBOX();
  //20130114 OL-2.12
  //var myPixelX = event.xy.x;
  //var myPixelY = event.xy.y;
  var myPixelX = Math.round(event.xy.x);
  var myPixelY = Math.round(event.xy.y);  
  var myMapWidth = gMap.size.w;
  var myMapHeight = gMap.size.h;
  var myScale = gMap.getScale();
  markPositionOnMap( myMousePos.lon, myMousePos.lat, "star");
  //gMap.setCenter( new OpenLayers.Geometry.Point( myMousePos.lon, myMousePos.lat ), 5);
  // store the map layers in a list to pass it to the view. As anonymous user
  // can edit layer visibility but not the db, the view can't use the db for
  // him / her.
  var myMapLayersList = [];
  var myLayers = gMap.layers;

  for (var myCounter = 0; myCounter < myLayers.length; myCounter++)
  {
    var myLayer = myLayers[myCounter];
    if (myLayer.getVisibility() &&
	 !myLayer.isBaseLayer &&
	 myLayer.name != "User Custom Layer")
    {
      myMapLayersList.push(gLayersDict[myLayer.id]);
    }
  }

  $.get(AFIS_PREFIX + "/getFeatureInfo/" + myLonLatGCS.lon + "/" + myLonLatGCS.lat + "/" +
      myBoundingBox + "/" + myPixelX +"/" + myPixelY + "/" + myMapWidth + "/" +
      myMapHeight +"/" + myScale + "/", {gLayers: myMapLayersList}, function( theData ) {

    $("#messages").html('Query complete');
    $("#query-results").html( theData );
    $("table tr:even").addClass("odd");
    $("table tr:odd").addClass("even");
    $("#legend-color-cell").removeClass("odd");
    $("#legend-color-cell").removeClass("even");
    var myQueryResultsDialog = $('#query-results').dialog({
      autoOpen: true,
      title: 'Query Results',
      buttons: { "Ok": function() { $(this).dialog("close"); } },
      closeOnEscape: false,
      dialogClass: 'scrollable',
      height: $(window).height() / 1.5,
      width: $(window).width() / 1.5,
      modal: true
    });
  });
  return false;
}

function markPositionOnMap( theLon, theLat, theStyle )
{
    /*
    * Mark the identified position on the map
    */
    // we want opaque external graphics and non-opaque internal graphics
    var myLayerStyle = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
    myLayerStyle.fillOpacity = 0.2;
    myLayerStyle.graphicOpacity = 1;
    /*
    * Blue style
    */
    var myBlueMarkerStyle = OpenLayers.Util.extend({}, myLayerStyle);
    myBlueMarkerStyle.strokeColor = "blue";
    myBlueMarkerStyle.fillColor = "blue";
    myBlueMarkerStyle.graphicName = "star";
    myBlueMarkerStyle.pointRadius = 5;
    myBlueMarkerStyle.strokeWidth = 1;
    myBlueMarkerStyle.rotation = 45;
    myBlueMarkerStyle.strokeLinecap = "butt";
    if ( removeLayerByName("Query Position") )
    {
      //alert("Deleting Query Position layer");
    }
    var myLayer = new OpenLayers.Layer.Vector("Query Position", {style: myLayerStyle});
    // create a point feature
    var myPoint = new OpenLayers.Geometry.Point( theLon, theLat );
    var myPointFeature = new OpenLayers.Feature.Vector( myPoint,null,myBlueMarkerStyle);
    myLayer.addFeatures([myPointFeature]);

    gMap.addLayer(myLayer);
}


//-------------------------------------------
// Legend related
//-------------------------------------------
function setupLegend()
{

  // toggle Legend images with a graceful animation
  $('.legend-toggle').live('click', function (event) {
    var myId = this.id.replace("legend-toggle-", "");
    $("#legend-image-" + myId).toggle(200);
  });
  $('#manage-button').live('click', function (event) {
    $('#manage-button').toggleClass("down");
    if ($('#manage-button').hasClass('down'))
    {
        $(".legend-manage-icon").show();
        $(".layer-deleted").show();
        $(".sortableLegend").sortable({disabled : false});
        correctIcons();


        $(".accordion").sortable({disabled : false});
    }
    else
    {
        $(".legend-manage-icon").hide();
        $(".layer-deleted").hide();
        saveLegendOrder();
        $(".sortableLegend").sortable({disabled : true});
        $("#messages").html( "Legend saved, deleted layers will disappear after two days!" );

        $(".accordion").sortable({disabled : true});
    }
  });
  
  function saveLegendOrder() {
    $('.sortableLegend li').each(function(index) {
      var myId = this.id.replace("legend-", "");
      myUrl = AFIS_PREFIX + "/saveLegend/" + myId + '/';
      if ($(this).hasClass("layer-deleted")) 
      {
        myUrl += index + "/t/";
      }
      else
      {
        myUrl += index + "/f/";
      } 
      $.get(myUrl, "", function ( theResponseData ) {
        //$("#messages").html( theResponseData );
      }, "html");
    });
  };

  function updateLayerVisibility(myName, myId){
    //var myId = this.id.replace("layer-", "");
    //myId = myId.replace("-checkbox", "");
    myLayers = gMap.layers;
    try
    {
      myLayer = getLayerByName( myName );
      if (!myLayer) return;
      myUrl = AFIS_PREFIX + "/setLayerVisibility/" + myId;
      if (myLayer.getVisibility())
      {
        myLayer.setVisibility(false);
        myUrl += "/f/";
      }
      else
      {
        myLayer.setVisibility(true);
        myUrl += "/t/";
      }
      //also tell the backend that we want this layer to
      //have different default visibility now
      $.get(
      myUrl, "", function ( theResponseData ) {
        $("#messages").html( theResponseData );
      }, "html");
    }
    catch (err)
    {
      alert(err + '\n');
    }
  }

  function correctIcons() {  
    $("li.layer-deleted a.legend-restore-icon").show();        
    $("li.layer-not-deleted a.legend-delete-icon").show();        
    $("li.layer-deleted a.legend-delete-icon").hide();        
    $("li.layer-not-deleted a.legend-restore-icon").hide();        
  };
  /* Bind the click event of any checkboxes of class layerCheckBox
   * to a custom event. We do this because if the checkbox was loaded
   * into the page via ajax, it wont be able to directly call a fn on
   * the parent page. Binding (via live fn below) requires jquery. */
  $('.layer-checkbox').live('click', function (event) {
    var myName = this.name;
    var myId = this.id.replace(/^layer-(\d+)-checkbox.*/, "$1");
    updateLayerVisibility(myName, myId);
  });

  // This function seems erroneous. George.
  // Event handler to sync checkbox state whose id is similar to the changed checkbox

//  $('.layer-checkbox').live('change', function () {
//    try {
//      var checked = this.checked;
//      var selector = 'input[id^=' + this.id.replace(/^(layer-\d+-checkbox).*/, "$1") + ']';
//      if ($(selector).length > 1) {
//        if (checked) {
//          $(selector).attr("checked", "checked");
//        } else {
//          $(selector).removeAttr("checked");
//        }
//      }
//    } catch (err) {
//      alert("Sync chkbox error:" + err + '\n');
//    }
//  });


  $('a.legend-restore-icon').live('click', function (event) {
    var myId = this.id.replace("legend-restore-", "");
    try
    {
      myUrl = AFIS_PREFIX + "/setLayerDeletedState/" + myId;
      myUrl += "/f/f/";
      $.get(
      myUrl, "", function ( theResponseData ) {
        $("#messages").html( theResponseData );
      }, "html");
      $("#legend-" + myId).addClass("layer-not-deleted");
      $("#legend-" + myId).removeClass("layer-deleted");
      correctIcons();
      $(".layer-deleted").show();
    }
    catch (err)
    {
      alert(err + '\n');
    }
  });
  // Added `a` below in order to distinguish between links and img with the class
  // legend-delete-icon
  $('a.legend-delete-icon').live('click', function (event) {
    var myId = this.id.replace("legend-delete-", "");
    // To address #257. When clicking the legend-delete-icon, uncheck the layer
    // select checkbox and hide the layer on the map. A bit hacky....!
    var theCheckbox = $(this).siblings(':checkbox')[0];
    var myName = theCheckbox.name;
    $(theCheckbox).removeAttr('checked');
    removeLayerByName(myName);
    updateLayerVisibility(myName, myId);
    try
    {
      myUrl = AFIS_PREFIX + "/setLayerDeletedState/" + myId;
      myUrl += "/t/t/";
      $.get(
      myUrl, "", function ( theResponseData ) {
        $("#messages").html( theResponseData );
      }, "html");
      $("#legend-" + myId).addClass("layer-deleted");
      $("#legend-" + myId).removeClass("layer-not-deleted");
      correctIcons();
      $(".layer-deleted").show();
    }
    catch (err)
    {
      alert(err + '\n');
    }
  });

}

function removeLayerByName( theName ) {
  myLayers = gMap.layers;
  try
  {
    for (var i = 0; i < myLayers.length; i++)
    {
      myLayer = myLayers[i];
      //alert (myLayer.name);
      if (myLayer.name == theName)
      {
        // remove layer from map
        gMap.removeLayer(myLayer);
        return true;
      }
    }
    return false;
  }
  catch (err)
  {
    alert(err + '\n');
    return false;
  }
}

function getLayerByName( theName )
{
  myLayers = gMap.layers;
  try
  {
    for (var i = 0; i < myLayers.length; i++)
    {
      myLayer = myLayers[i];
      if (myLayer.name == theName)
      {
        return myLayer;
      }
    }
    return false;
  }
  catch (err)
  {
    alert(err + '\n');
    return false;
  }
}

//-------------------------------------------
// Fancybox
//-------------------------------------------
function setupFancyBox()
{
  /* Prepare help etc popup windowing */
  $("a.fancybox").fancybox({
    "overlayShow": true,
    "imageScale": true,
    "zoomSpeedIn": 600,
    "zoomSpeedOut": 500,
    "easingIn": "easeOutBack",
    "easingOut": "easeInBack",
    "frameWidth": 500,
    "frameHeight": 500,
    "hideOnContentClick": false
  });
}

//-------------------------------------------
// JQuery dialog for layer manager
//-------------------------------------------
function setupLayerManager()
{
  var myLayerManagerDialog = $('<div></div>').load(AFIS_PREFIX + "/showLayerManager/").dialog({
    autoOpen: false,
    title: 'Layer Manager',
    modal: true,
    show: 'slide',
    hide: 'slide',
    height: $(window).height() / 2,
    width: $(window).width() / 2,
    buttons: { "Close" : function() { myLayerManagerDialog.dialog("close"); }, 
               "Save"  :   function saveLegend()
  {
    // This code sucks - redo as a single call!
    // Using a separate post for each layer update is really inefficient
    // TS

    // 1. set the selected layers as non-deleted...
    // obtain the ordered new list of layers. It is the id.
    var mySelectedLayers = $('#selected-layers').sortable('toArray');
    // build the url for the view, zB /saveLegend/12/1/
    for (var i = 0; i < mySelectedLayers.length; i++) {
      var myLayerId = mySelectedLayers[i];
      var myUrl = AFIS_PREFIX + "/saveLegend/" + myLayerId + "/" + i + "/f/";
      // post it to save status in the database. One post for each layer.
      jQuery.ajax({
        url: myUrl,
        async: false
      });
    }
    // 2. ...and set the available as deleted
    var myAvailableLayers = $('#available-layers').sortable('toArray');
    // build the url for the view, zB /saveLegend/12/1/
    for (var i = 0; i < myAvailableLayers.length; i++) {
      var myLayerId = myAvailableLayers[i];
      var myUrl = AFIS_PREFIX + "/saveLegend/" + myLayerId + "/" + i + "/t/";
      // post it to save status in the database. One post for each layer.
      jQuery.ajax({
        url: myUrl,
        async: false,
        success: function( theResponse ) {
          //pass
        }
      });
    }
    // it works after the ajax calls
    $("#layers").load(AFIS_PREFIX + "/showLegend/");
    // reload the map - only the diff is processed.
    setDataLayers( mySelectedLayers, myAvailableLayers );
    myLayerManagerDialog.dialog('close');
  }
  }
  });

  $('#layer-manager-button').click(function () {
    myLayerManagerDialog.dialog('open');
  });
  //http://jqueryui.com/demos/sortable/#connect-lists
  //the code for enabling drag-droppability is embedded in layermanager.html

}

//-------------------------------------------
// JQuery dialog for layer request
//-------------------------------------------
function setupLayerRequest()
{
  var myLayerRequestDialog = $('<div></div>').load(AFIS_PREFIX + "/show-contact-form/").dialog({
    autoOpen: false,
    title: 'Contact Us',
    modal: true,
    show: 'slide',
    hide: 'slide',
    height: $(window).height() / 2,
    width: $(window).width() / 2,
    buttons: { "Close" : function() { myLayerRequestDialog.dialog("close"); }, 
               "Send"  :   function sendLayerRequest()
      {
          myUrl = AFIS_PREFIX + "/send-user-message/";
          var data = {
            name: $("#layer-request-name").val(),
            email: $("#layer-request-email").val(),
            phone: $("#layer-request-phone").val(),
            message: $("#user-message").val(),
            csrfmiddlewaretoken: $('#csrf_token').val()
          };
          $.post(myUrl, data, function ( theResponseData ) {
            $("#messages").html( theResponseData );
          }, "html");          
          myLayerRequestDialog.dialog("close");
      }
    }
  });


  $('#user-message').click(function () {
    myLayerRequestDialog.dialog('open');
  });

}


//-------------------------------------------
// Base Layer management
//-------------------------------------------
function setupBaseLayerSwitcher()
{
  // JQuery popup dialog for base layer choice
  var myBaseLayerDialog = $('<div></div>').load(AFIS_PREFIX + "/baseLayerDialog/").dialog({
    modal: true,
    show: 'slide',
    hide: 'slide',
    autoOpen: false,
    resize: 'auto',
    title: 'Choose Base Layer:',
    buttons: { Ok: function() { myBaseLayerDialog.dialog("close"); } }

  });

  $('#base-layer-button').click(function () {
    myBaseLayerDialog.dialog('open');
  });

  // swap baselayers according to the choice in combobox
  $('.baselayer').live('click', function (event) {
    myLayers = gMap.layers;
    try
    {
          getLayerByName( this.id);
          gMap.setBaseLayer(myLayer);
    }
    catch (err)
    {
      alert(err + '\n');
    }
  });
}

//-------------------------------------------
//  Date Query
//-------------------------------------------
function setupDateQueryDialog()
{
  // JQuery popup dialog for datequery
  myDateQueryDialog = $('<div id="date-query-dialog"></div>').load(AFIS_PREFIX + "/dateQuery/").dialog({
    modal: true,
    show: 'slide',
    hide: 'slide',
    autoOpen: false,
    width: '520px',
    title: 'Date Query:',
    buttons: {
      "Close": function(){
        myDateQueryDialog.dialog("close");
      },
      "Query": function(){
        submitDateQuery();
      }
    }
  });

  $('#date-query-button').click(function () {
    myDateQueryDialog.dialog('open');
  });
}

var MESA_PREFIX = "http://127.0.0.1";
function submitDateQuery() {
   //myLoadingPanel.maximizeControl();
  $("#date-query-validation").hide();
  //validate the form using jquery
  //@todo- disable Submit until all is filled?
  myMessage = "";
  if ( $("#date-query-layer-name").val()=='' )
  {
    myMessage += "<div>Please enter a name for the new query layer.</div>";
  }
  if ( $("#start-date").val()=='')
  {
    myMessage += "<div>Please select a start date for the new query layer.</div>";
  }
  if ( $("#end-date").val()=='')
  {
    myMessage += "<div>Please select an end date for the new query layer.</div>";
  }
  if ( $("#end-date").val() < $("#start-date").val())
  {
    myMessage += "<div>Please select an end date after given start date.</div>";
  }
  if ( myMessage != "" )
  {
    $("#errorMessage").html( myMessage );
    $("#date-query-validation").show();
    return;
  }
  myDateQueryDialog.dialog("close");
  // construct a post request from form details
  myDataString="sensor=" + $("#sensor").val();
  myDataString+="&start-date=" + $("#start-date").val();
  myDataString+="&end-date=" + $("#end-date").val();
  myDataString+="&name=" + $("#date-query-layer-name").val();
  console.log( MESA_PREFIX + "/dateQuery/");
  $.ajax({
    url: MESA_PREFIX + "/dateQuery/",
    type: "GET",
    processData: false,
    dataType: "script",
    data: myDataString,
    success: function(theResponseData){
       //myLoadingPanel.minimizeControl();
      }
  });
  return false;
}


//-------------------------------------------
// Login form
//-------------------------------------------

var myLoginDialog;
function setupLoginForm()
{
    var myPasswordResetDialog = $('<div></div>').load(AFIS_PREFIX + "/password/reset").dialog({
        modal: true,
        show: {effect: 'fade', duration: 300},
        hide: 'puff',
        width: 300,
        maxWidth: 300,
        resizable: false,
        autoOpen: false,
        title: 'Reset password:',
        dialogClass: 'no-close',
        closeOnEscape: true
    });

    myLoginDialog = $('<div></div>').load(AFIS_PREFIX + "/login", function() {
            $('#register-link').click(function () {
                myLoginDialog.dialog('close');
                myRegisterDialog.dialog('open');
            });
            $('#password-reset-link').click(function () {
                myPasswordResetDialog.dialog('open');
            });
            $('#login-registration-links').show();
      // login-form-wrapper id required for AJAX form submission
        }).attr('id', 'login-form-wrapper').dialog({
            modal: true,
            hide: 'puff',
            width: 400,
            maxWidth: 400,
            position: { my: "center top", at: "center bottom", of: "div#header" },
            resizable: false,
            autoOpen: false,
            title: 'AFIS login:',
            dialogClass: 'no-close',
            closeOnEscape: false
        });

    $('#login-button').click(function () {
        myLoginDialog.dialog("option", "buttons", { "Cancel": function() { myLoginDialog.dialog("close"); } });
        myLoginDialog.dialog('open');
    });


};

//-------------------------------------------
// Register form
//-------------------------------------------
var myRegisterDialog;
function setupRegisterForm()
{
  // JQuery popup dialog for user registration
  //$("#messages").load(AFIS_PREFIX + "/register");
  myRegisterDialog = $('<div></div>').load(AFIS_PREFIX + "/register").dialog({
    modal: true,
    show: {effect: 'fade', duration: 300},
    hide: 'puff',
    width: 400,
    maxWidth: 400,
    resizable: false,
    autoOpen: false,
    title: 'User registration:',
    dialogClass: 'no-close',
    closeOnEscape: false
  });

  $('#register-button').click(function () {
    myRegisterDialog.dialog("option", "buttons", { "Cancel": function() { myRegisterDialog.dialog("close"); } });
    myRegisterDialog.dialog('open');
  });

}


//-------------------------------------------
// Zoom to named place
//-------------------------------------------

function setupPlaceZoom()
{
  var myPlacesDialog = $('<div></div>').load(AFIS_PREFIX + "/places/").dialog({
    modal: true,
    show: 'slide',
    hide: 'slide',
    autoOpen: false,
    title: 'Zoom to country, city or place:',
    buttons: { Close: function() { myPlacesDialog.dialog("close");  }, "Go!": zoomToPlace, "Reset": resetZoomExtents },
    open:  setupPlacesAutoComplete
  });
  $('#places-button').click(function ()
  {
    myPlacesDialog.dialog('open');
  });
}

function setupPlacesAutoComplete(event, ui)
{
  $("#place-name").autocomplete({
    source: AFIS_PREFIX + "/getPlaceNames",
    minLength: 2,
    select: function(event, ui)
    {
      if ( ui.item )
      {
        $("#longitude").val( ui.item.lon );
        $("#latitude").val( ui.item.lat );
        $("#zoom-level").val( gPlaceZoomLevel );
      }
      else
      {
        //do nothing
        $("#longitude").val( "" );
        $("#latitude").val( "" );
        $("#zoom-level").val( "" );
      }
    }
  });
  setTimeout('focusPlaceName()',2000);
}

function focusPlaceName()
{
  $("#place-name").focus();
}

function zoomToPlace()
{
  // get the values from the boxes
  var myZoomLon = $("#longitude").val();
  var myZoomLat = $("#latitude").val();
  // the zoomlevel must be casted to int. lat lon don't. The LonLat
  // constructor accepts floats.
  var myZoomLevel = parseInt($("#zoom-level").val(), 10);
  var myZoomLonLat = new OpenLayers.LonLat(myZoomLon,
    myZoomLat).transform(new OpenLayers.Projection("EPSG:4326"),
      gMap.getProjectionObject());
  gMap.setCenter(myZoomLonLat, myZoomLevel);
}

function resetZoomExtents()
{
  if (lookupWasSuccessful) {
    // Fit map to lookup AOI bounds   
    var mapAoi = lookupAoi.clone().transform(new OpenLayers.Projection("EPSG:4326"), gMap.getProjectionObject());
    gMap.zoomToExtent(mapAoi);
  }
  else {
	if (userLocation == 'lookup') {
		// if a wildcard subdomain lookup failed, redirect to global.afis.co.za, so that impression is not given that site exists
		//window.location = "http://global.afis.co.za";
	}
    // no lookupAoi defined, so use default lon,lat and zoom
    var myLonLat = new OpenLayers.LonLat(gDefaultLon,
      gDefaultLat).transform(new OpenLayers.Projection("EPSG:4326"), 
      gMap.getProjectionObject());
    gMap.setCenter(myLonLat, gZoomLevel);
  }
}

function cancelDialog()
{
  $(this).dialog("close");
}

function overpass_callback(data){
  var msg = "";
  if(data.length >= 1){
    var d = new Date(data[0].los_utc);
    d.setSeconds(d.getSeconds()+1800);
    msg = "Next southern Africa overpass: " + data[0].satellite + " " + d.toLocaleString();
  }
  $("#overpass_info").html(msg);
}

function display_overpass_info(){
  if ($("#overpass_info").length > 0){
    $.ajax({
      url: "http://qi.afis.co.za/next_overpass/?next=1",
      type: "GET",
      jsonp: "callback",
      dataType: "jsonp",
      crossDomain: true,
      success: overpass_callback
    });
  }
}

var timeId = 0;
var refresher = function(button, event){
  for(layer in gMap.layers){
    l = gMap.layers[layer];
    if(l.isBaseLayer===false && l.getVisibility()){
      l.redraw(true);
    }
  }
  display_overpass_info();
};

var setTimer = function(interval){
  if(interval <= 60){
    interval = 60;
  }
  timeId = setInterval("refresher()", interval*1000);
};

var clearTimer = function(){
  clearInterval(timeId);
};

function init() {
  // init() is called by both init_for_user and init_not_authenticated
  // refactored to prevent unnecessary AJAX calls for authenticated users

  $("#tabs").tabs();
  /* Main page layout defined using jquery layout extension */
  $('body').layout({
    east__size:             350, //width
    north__size:            110, //height
    east__resizable:        true,
    west__resizable:        false,
    west__closed:           true,
    south__resizable:       false,
    initClosed:             false
    });
  //$('#center').layout({ south__resizable: false, initClosed: false });
  $('#footer').css( 'z-index', 10000);
  $('#login-form').hide();
  /* requires jquery-ui 1.8 - setup buttons using jquery*/
  $("#map-controls").buttonset();
  $("#map-buttons").buttonset();
  $("#toolbar-buttons").buttonset();
  $("#menu").buttonset();
  $("#map-controls input:radio").click( function() { toggleControl($(this)) });
  // This next thing is a hack for bug in jquery ui 1.8rc3 for IE. Remove when fixed.
  $("#map-controls label").click(function(event) { var id = $(this).attr('for'); $('#'+id).click(); });
  /* Also requiring 1.8 - layout the header using the new positioning system */
  $('#logo').position({ my: 'left top', at: 'left top', offset: '0 1', of: '#header' });
  /* end of jquery-ui 1.8 dependency */

  // Crude fix for display bug. RVDD 2013-01-29
  $("div#map-controls input").hide();
  $("#header").css("height", "100px");

  setTimer(600);
};

function init_for_user() {

  init();

  //------------------------------------------
  // Run through various components setting things up
  //------------------------------------------
  setupOpenLayers();
  setupLegend();
  setupFancyBox();
  setupDateQueryDialog();
  setupPlaceZoom();
  setupBaseLayerSwitcher();
  setupLayerManager();
  //setupLayerRequest();

  //------------------------------------------
  // Load in panels by ajax
  //------------------------------------------
  $("#messages").load(AFIS_PREFIX + "/showFireStats/");
  $("#layers").load(AFIS_PREFIX + "/showLegend/", function() {
    // Hack to sync next-swath checkbox state with userwmslayer.is_visible
    var cbid = "layer-2879-checkbox";
    var selector = 'input[id^=' + cbid + '-]';
    if ( $("#"+cbid) && $(selector) ) {
      if ( $("#"+cbid).attr("checked") ) {
        $(selector).attr("checked", "checked");
      } else {
        $(selector).removeAttr("checked");
      }
    }
  });
  display_overpass_info();
}

// Extra login for when the user is not logged in
function init_not_authenticated() {
  //init();
  //setupLoginForm();
  //setupRegisterForm();
  // Users must log in.
  //myLoginDialog.dialog('open');
  init_for_user();
}

// Redraw map canvas on window resize
window.onresize = function() {
  setTimeout( function() { if(gMap) gMap.updateSize();}, 200);
}
