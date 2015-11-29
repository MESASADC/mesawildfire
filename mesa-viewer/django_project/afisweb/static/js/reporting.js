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
var gDefaultLat = -28;
var gDefaultLon = 24;
var gZoomLevel = 5;
var gPlaceZoomLevel = 8;
var gLayers = null;
var gLayersDict = {};
var userLocation = 'africa';

if (location.hostname.indexOf('europe.') == 0) {
	userLocation = 'europe';
	gDefaultLat = 48;
	gDefaultLon = 10.8;
} else if (location.hostname.indexOf('southamerica.') == 0) {
	userLocation = 'southamerica';
	gDefaultLat = -18;
	gDefaultLon = -60;
	gZoomLevel = 4;
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


    // the control is outside the map
    gMap.addControl(new OpenLayers.Control.ScaleBar({
      div: document.getElementById("scalebar"),
      align: "right",
      minWidth: 200,
      maxWidth: 300
    }));

    gMap.addControl(new OpenLayers.Control.MouseDefaults());

    var myLoadingPanel = new OpenLayers.Control.LoadingPanel();
    gMap.addControl(myLoadingPanel);


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
      gMap.addControl( myControl );
    }

    /* End measure distance snippet */

    // display the progress bar
    myLoadingPanel.maximizeControl();

    addBackdropLayers();

    // remove it as the above function returns
    myLoadingPanel.minimizeControl()
    var myLonLat = new OpenLayers.LonLat(gDefaultLon,
        gDefaultLat).transform(new OpenLayers.Projection("EPSG:4326"),
          gMap.getProjectionObject());
    gMap.setCenter(myLonLat, gZoomLevel);

    // getFeatureInfo, not done by openlayers as it requires proxy
    // for cross site calls, but instead by Django via a view
    gMap.events.register('click', gMap, setAOI );

  }
  catch (err) {
    alert('Could not initialize:\n' + err);
  }
}

function setAOI(event)
{
  var myMousePos = gMap.getLonLatFromPixel(event.xy);
  var EPSG4326 = new OpenLayers.Projection("EPSG:4326");
  var EPSG900913 = new OpenLayers.Projection("EPSG:900913");
  var myLonLatGCS = myMousePos.transform( EPSG900913,EPSG4326 );
  var myBounds = gMap.getExtent().clone();
  var myBoundingBox = myBounds.toBBOX();
  markPositionOnMap( myMousePos.lon, myMousePos.lat, "star");
  Event.stop(event);
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
// Zoom to named place
//-------------------------------------------

function setupPlaceZoom()
{
  var myPlacesDialog = $('<div></div>').load(AFIS_PREFIX + "/places/").dialog({
    modal: true,
    show: 'slide',
    hide: 'slide',
    autoOpen: false,
    title: 'Zoom to South African place:',
    buttons: { "Close": cancelDialog, "Go!": zoomToPlace, "Reset": resetZoomExtents },
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
}

function zoomToPlace()
{
  // get the values from the boxes
  var myZoomLon = $("#longitude").val();
  var myZoomLat = $("#latitude").val();
  // the zoomlevel must be casted to int. lat lon don't. The LonLat
  // constructor accepts floats.
  var myZoomLevel = parseInt($("#zoom-level").val());
  var myZoomLonLat = new OpenLayers.LonLat(myZoomLon,
    myZoomLat).transform(new OpenLayers.Projection("EPSG:4326"),
      gMap.getProjectionObject());
  gMap.setCenter(myZoomLonLat, myZoomLevel);
};

function resetZoomExtents()
{
  // return to full south africa extent
  var myLonLat = new OpenLayers.LonLat(gDefaultLon,
    gDefaultLat).transform(new OpenLayers.Projection("EPSG:4326"),
      gMap.getProjectionObject());
  gMap.setCenter(myLonLat, gZoomLevel);
};

function cancelDialog()
{
  $(this).dialog('close');
}

function init()
{
  $("#map-controls").buttonset();
  $("#map-buttons").buttonset();
  $("#menu").buttonset();
  // This next thing is a hack for bug in jquery ui 1.8rc3 for IE. Remove when fixed.
  $("#map-controls label").click(function(event) { var id = $(this).attr('for'); $('#'+id).click(); });
  /* Also requiring 1.8 - layout the header using the new positioning system */
  $('#logo').position({ my: 'left top', at: 'left top', offset: '0 1', of: '#header' });
  /* end of jquery-ui 1.8 dependency */


  //------------------------------------------
  // Run through various components setting things up
  //------------------------------------------
  setupOpenLayers();
  setupFancyBox();
  setupPlaceZoom();
  // end of document ready function.
}

