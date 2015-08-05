// BEGIN LAYOUT


  function applyMargins() {
    /* var leftToggler = $(".mini-submenu-left");
    var rightToggler = $(".mini-submenu-right");
    if (leftToggler.is(":visible")) {
      $("#map .ol-zoom")
        .css("margin-left", 0)
        .removeClass("zoom-top-opened-sidebar")
        .addClass("zoom-top-collapsed");
    } else {
      $("#map .ol-zoom")
        .css("margin-left", $(".sidebar-left").width())
        .removeClass("zoom-top-opened-sidebar")
        .removeClass("zoom-top-collapsed");
    }
    if (rightToggler.is(":visible")) {
      $("#map .ol-rotate")
        .css("margin-right", 0)
        .removeClass("zoom-top-opened-sidebar")
        .addClass("zoom-top-collapsed");
    } else {
      $("#map .ol-rotate")
        .css("margin-right", $(".sidebar-right").width())
        .removeClass("zoom-top-opened-sidebar")
        .removeClass("zoom-top-collapsed");
    }
    */
  }


  function isConstrained() {
    return $("div.mid").width() == $(window).width();
  }

  function applyInitialUIState() {
    if (isConstrained()) {
      $(".sidebar-left .sidebar-body").fadeOut('slide');
      $(".sidebar-right .sidebar-body").fadeOut('slide');
      $('.mini-submenu-left').fadeIn();
      $('.mini-submenu-right').fadeIn();
    }
  }

  $(function() {
    $('.sidebar-left .slide-submenu').on('click', function() {
      var thisEl = $(this);
      thisEl.closest('.sidebar-body').fadeOut('slide', function() {
        $('.mini-submenu-left').fadeIn();
        applyMargins();
      });
    });

    $('.mini-submenu-left').on('click', function() {
      var thisEl = $(this);
      $('.sidebar-left .sidebar-body').toggle('slide');
      thisEl.hide();
      applyMargins();
    });

    $('.sidebar-right .slide-submenu').on('click', function() {
      var thisEl = $(this);
      thisEl.closest('.sidebar-body').fadeOut('slide', function() {
        $('.mini-submenu-right').fadeIn();
        applyMargins();
      });
    });

    $('.mini-submenu-right').on('click', function() {
      var thisEl = $(this);
      $('.sidebar-right .sidebar-body').toggle('slide');
      thisEl.hide();
      applyMargins();
    });

    $(window).on("resize", applyMargins);

// BEGIN OPEN LAYERS

    var map = new ol.Map({
      target: "map",
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM()
        })
      ],
      view: new ol.View({
        center: [0, 0],
        zoom: 2
      })
    });
    applyInitialUIState();
    applyMargins();

// END OPEN LAYERS

  });

   var HISTORIC = [];
   var FORECAST = [];
   var TABLEDATAA = Array();

   Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
   };


function fdi_table_data(json){
  for (var j =0; j < json.length; j++){
      var data = json[j];
      HISTORIC.push({
          type:"WS",
          station: data.station_name,
          fdi: parseFloat(data.data[0].LFDI[0]),
          wind : data.data[0].ws_kmh,
          temp : data.data[0].temp_c,
          relativeH : data.data[0].rh_pct,
          rain : data.data[0].rain_mm
        });
  }
    console.log(HISTORIC);
};


$(document).ready(function(){

  fdi_table_data(RealTime);
  var tableFdi = $('table.fdi-table').DataTable({
   
    "data": HISTORIC,
    deferRender:    true,
    dom:            "tS",
    scrollY:        "60%",
    scrollCollapse: true,
    scrollX:        "60%",
    stateSave:      true,
    paging:         false,
    "columns": [{
      "className": 'weather-station-select',
      "orderable": false,
      "data": null,
      "defaultContent": ' '
    },
    {
      "data":"type"
    } 
    ,
    {
      "data":"station"
    }, {
      "data":"fdi"
    }, {
      "data": "wind"
    }, {
      "data": "temp"
    }, {
      "data": "relativeH"
    }, {
      "data": "rain"
    }],
    "order": [
      [1, 'asc']
    ]
  });
  $("td.weather-station-select").html('<i class="fa fa-line-chart"></i>');
  // Add event listener for updating the FDI graph
  $('table.fdi-table tbody').on('click','tr',function() {    
      update_graph(tableFdi.row(this).index());
  });


//Get fire-table data.
$.get("http://146.64.28.95:3000/fire", function(table_data,status){ 
       
       console.log(status);
      var table = $('table.fire-table').DataTable({
          "data": table_data,
          deferRender:    true,
          dom:            "tS",
          scrollY:        "40%",
          scrollCollapse: true,
          stateSave:      true,
          paging:         false,
          "columns": [{
            "className": 'details-control',
            "orderable": false,
            "data": null,
            "defaultContent": ''
          }, {
            "data": "pk"
          }, {
            "data": "type"
          }, {
            "data": "geom"
          }, {
            "data": "lat"
          }, {
            "data": "lon"
          }, {
           "data": "date_time"
          }, {
            "data": "src"
          }, {
            "data": "btemp"
          },{
            "data": "sat"
          },{
            "data": "frp"
          }],
          "order": [
            [1, 'asc']
          ]
        });

});


/* Formatting function for row details - modify as you need */

  function format(d) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
      '<tr>' +
        '<td>First Observation:</td>' +
        '<td>' + d.first_observed + '</td>' +
      '</tr>' +
      '<tr>' +
        '<td>Last Observation:</td>' +
        '<td>' + d.last_observed + '</td>' +
      '</tr>' +
      '<tr>' +
        '<td>FDI at first observation:</td>' +
        '<td>' + d.fdi_first + '</td>' +
      '</tr>' +
      '<tr>' +
        '<td>FDI at last observation:</td>' +
        '<td>' + d.fdi_last + '</td>' +
      '</tr>' +
    '</table>';
  }


  // Add event listener for opening and closing details
  $('table.fire-table tbody').on('click', 'td.details-control', function() {
    var tr = $(this).closest('tr');
    var row = table.row(tr);

    if (row.child.isShown()) {
      // This row is already open - close it
      row.child.hide();
      tr.removeClass('shown');
    } else {
      // Open this row
      row.child(format(row.data())).show();
      tr.addClass('shown');
    }
  });


  $('#fire-table-search').on( 'keyup', function () {
      table.search( this.value ).draw();
  } );

   $('#fdi-table-search').on( 'keyup', function () {
      tableFdi.search( this.value ).draw();
  } );

});

// END FIRE EVENT TABLE


// BEGIN FDI CHART

var SECOND = 1000;
var MINUTE = 60* SECOND;
var HOUR = 60 * MINUTE;
var DAY = 24 * HOUR;



   var LFDILOCAL = [];
   var LFDIFORECAST = [];
   var graph_data = Array();
   Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
   };


function parse_historic(json){
  LFDILOCAL = [];
    for(var i = 0;i < json.data.length;i++){
      LFDILOCAL.push({
          date: new Date(json.data[i].localtime),
          fdi: parseFloat(json.data[i].LFDI[0])
        });
      
    }
    console.log(LFDILOCAL);
};

function parse_forecast(json){

    for(key in json){
        var date = new Date(key);
        date.setHours(12);
        date.setMinutes(0);
        LFDIFORECAST.push({
          date: date,
          fdi: parseFloat(json[key].LFDI[0])
        });
      
    }
    console.log(LFDIFORECAST);
};
function compare(a,b) {
  if (a.date < b.date)
    return -1;
  if (a.date > b.date)
    return 1;
  return 0;
}


function declare_graph_data(){
    graph_data = [];
      for (var i = 0; i < LFDIFORECAST.length; i++){
          graph_data.push({
            date: LFDIFORECAST[i].date,
            value2: LFDIFORECAST[i].fdi
          });
      }
    for (var i =0; i < LFDILOCAL.length; i++){
          graph_data.push({
            date: LFDILOCAL[i].date,
            value1: LFDILOCAL[i].fdi
          });
    }

    
  graph_data.sort(compare);
  sorted =   graph_data.sort(compare);
}

function update_graph(weather_station_index){
     parse_historic(RealTime[weather_station_index]);
     declare_graph_data();
     render_chart();
}


     parse_historic(RealTime[1]);
     parse_forecast(ForeCast);
     declare_graph_data();
     render_chart();



function render_chart(){
      var chart = AmCharts.makeChart("chartdiv", {
        "type": "serial",
        "theme": "dark",
        "marginRight": 80,
        "dataProvider": graph_data,
        "valueAxes": [{
          "maximum": 100,
          "minimum": 0,
          "axisAlpha": 0.4,
          "guides": [{}, {
            "lineColor": "#4e0000",
            "lineThickness": 3,
            "lineAlpha": 0,
            "value": 0,
            "toValue": 20
          }, {
            "lineColor": "#0000FF",
            "lineThickness": 3,
            "lineAlpha": 1,
            "value": 20,
            "toValue": 45
          }, {
            "lineColor": "#FFFF00",
            "lineThickness": 3,
            "lineAlpha": 1,
            "value": 45,
            "toValue": 60
          }, {
            "lineColor": "#FFA500",
            "lineThickness": 3,
            "lineAlpha": 1,
            "value": 60,
            "toValue": 75
          }, {
            "lineColor": "#FF0000",
            "lineAlpha": 1,
            "lineThickness": 3,
            "value": 75
          }]
        }],

        "graphs": [{
          "balloonText": "",
          "columnWidth": 15,
          "fillColors": "#000000",
          "fillAlphas": 0.4,
          "lineAlpha": 0,
          "title": "12H00 Forecast",
          "type": "column",
          "valueField": "value2"
        }, {
          "balloonText": "[[title]]: [[value]]",
          "lineThickness": 3,
          "connect": true,
          "title": "FDI",
          "lineColor": "#FFFFFF",
          "type": "smoothedLine",

          "valueField": "value1"
        }],
        "zoomOutButtonRollOverAlpha": 0.15,
        "chartCursor": {
          "categoryBalloonDateFormat": "MMM DD JJ:NN",
          "cursorPosition": "mouse",
          "showNextAvailable": true
        },
        "autoMarginOffset": 5,
        "columnWidth": 1,
        "categoryField": "date",
        "categoryAxis": {
          "minPeriod": "hh",
          "parseDates": true
        },
        "export": {
          "enabled": true
        }
      });
     }

      

// END FDI CHART
