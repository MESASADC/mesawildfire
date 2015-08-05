// BEGIN LAYOUT

function unique(list) {
    var result = [];
    $.each(list, function(i, e) {
        if ($.inArray(e, result) == -1) result.push(e);
    });
    return result;
}

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

// END LAYOUT


// BEGIN FIRE EVENT TABLE



/*var drest ={    

            "station_name": "PRETORIA UNIVERSITY PROEFPLAAS",
            "distance_m": 4497.3784,
            "data": [{
                      "rain_mm": null,
                      "ws_kmh": 2.16,
                      "rh_pct": 68,
                      "LFDI": [
                         11,
                         "0000ff"
                      ],
                      "temp_c": 6,
                      "firedanger": 11,
                      "winddirection_deg": 94,
                      "localtime": "2015-07-27 02:00:00"
                      }
             };*/


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
/*
function parse_forecast(json){

    for(key in json){
        var date = new Date(key);
        date.setHours(12);
        date.setMinutes(0);
        FORECAST.push({
          date: date,
          fdi: parseFloat(json[key].LFDI[0])
        });
      
    }
    console.log(FORECAST);
};
function compare(a,b) {
  if (a.date < b.date)
    return -1;
  if (a.date > b.date)
    return 1;
  return 0;
}


function declare_graph_data(){

      for (var i = 0; i < FORECAST.length; i++){
          TABLEDATAA.push({
            date: FORECAST[i].date,
            value2: FORECAST[i].fdi
          });
      }
    for (var i =0; i < HISTORIC.length; i++){
          TABLEDATAA.push({
            date: HISTORIC[i].date,
            value1: HISTORIC[i].fdi
          });
    }

    
  TABLEDATAA.sort(compare);
  sorted =   TABLEDATAA.sort(compare);
}
*/

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
      "defaultContent": ''
    }, {
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



  var table = $('table.fire-table').DataTable({
    "data": tableData,
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
      "data": "id"
    }, {
      "data": "description"
    }, {
      "data": "status"
    }, {
      "data": "area"
    }, {
      "data": "max_frp"
    }, {
/*      "data": "first_observed"
    }, {
      "data": "last_observed"
    }, {
      "data": "fdi_first"
    }, {
      "data": "fdi_last"
    }, {
*/      "data": "fdi_current"
    }],
    "order": [
      [1, 'asc']
    ]
  });

 
  /* Formatting function for row details - modify as you need */

    var custom_names = {
        "first_observed": "First Observation",
        "last_observed": "First Observation",
        "fdi_first": "FDI at first observation",
        "fdi_last": "FDI at last observation"
    };

  /* Formatting function for row details - modify as you need */
  function format(d) {
    var visible_columns = $(".dataTable").find("th.sorting, th.sorting-asc,th.sorting-desc");

    var visible_column_names = Array();
    for (var i =0 ; i < visible_columns.length; i++){
        visible_column_names.push($(visible_columns[i]).text());
    }
    visible_columns = unique(visible_column_names);

    var displaying_keys = Array();
    for (key in d){
        for (var i = 0; i < visible_columns.length; i++){
            var my_key = visible_columns[i].trim().toLowerCase();
            my_key = my_key.replace(/[^\w\s]/gi, '').trim().replace(/ /g,'_');
            if (key == my_key){
                displaying_keys.push(key);
                break;
            }
        }
    }

    var html = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;display:inline">';
    for (key in d){
        if (displaying_keys.indexOf(key) == -1){
            var string;
            if (custom_names[key] != null)
                string = custom_names[key];
            else
                string = key.charAt(0).toUpperCase() + "" + key.substring(1).replace(/_/g,' ');

            html +='<tr>' +
            '<td>'+string+':</td>' +
            '<td>' + d[key]+ '</td>' +
            '</tr>';
        }
    }
    html += '</table>';
    return html ;
  }


  // Add event listener for opening and closing details
  $('table.fire-table tbody').on('click', 'td.details-control', function() {
    var tr = $(this).closest('tr');
    var wms_image = "<image style='width:200px; height:200px; display:inline;'/>";
    var row = table.row(tr);

    if (row.child.isShown()) {
      // This row is already open - close it
      row.child.hide();
      tr.removeClass('shown');
    } else {
      // Open this row
      row.child(format(row.data())).show();
      tr.addClass('shown');
      tr.parent().find('td[colspan=7]').parent().prepend(wms_image);
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


      // generate data
      var chartData = [];

      function generateChartData() {
        var thisDate = new Date();
        var twoDaysAgoDate = new Date(thisDate.getTime() - 2 * DAY);
        twoDaysAgoDate.setHours(0);
        twoDaysAgoDate.setMinutes(0);
        twoDaysAgoDate.setSeconds(0);
        twoDaysAgoDate.setMilliseconds(0);

        for (var i = twoDaysAgoDate.getTime(); i < (twoDaysAgoDate.getTime() + 5 * DAY); i += 1 * HOUR) {
          var newDate = new Date(i);
          var value1 = 0;

          if (i == twoDaysAgoDate.getTime()) {
            value1 = Math.round(Math.random() * 40 + 20);
          } else {
            value1 = Math.round(chartData[chartData.length - 1].value1 / 100 * (90 + Math.round(Math.random() * 20)) * 100) / 100;
          }

          value2 = value1;

          if (newDate < thisDate) {

            if (newDate.getHours() == 12) {
              // we set daily data on 12th hour only
              chartData.push({
                date: newDate,
                value1: value1,
                value2: value2
              });
            } else {
              chartData.push({
                date: newDate,
                value1: value1});
            }

          } else {
            if (newDate.getHours() == 12) {
              // we set daily data on 12th hour only
              chartData.push({
                date: newDate,
                value1: value1,
                value2: value2
              });
            }
          }
        }
      }

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


/*
  $(document).ready(function(){

  var table = $('table.fdi-table display').DataTable({
    "data": RealTime,
    deferRender:    true,
    dom:            "tS",
    scrollY:        "60%",
    scrollCollapse: true,
    stateSave:      true,
    paging:         false,
    "columns": [{
      "className": 'details-control',
      "orderable": false,
      "data": null,
      "defaultContent": ''
    }, {
      "data": "station_name"
    }, {
      "data": "LFDI"
    }, {
      "data": "ws_kmh"
    }, {
      "data": "temp_c"
    }, {
      "data": "rh_pct"
    }, {
     "data": "rain_mm"
    }],
    "order": [
      [1, 'asc']
    ]
  });*/


     //generateChartData();
     parse_historic(RealTime[1]);
     parse_forecast(ForeCast);
     declare_graph_data();
     render_chart();
     //generateChartData();


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
