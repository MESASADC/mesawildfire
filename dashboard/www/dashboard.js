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
          fdiColour: data.data[0].LFDI[1],
          wind : data.data[0].ws_kmh,
          temp : data.data[0].temp_c,
          relativeH : data.data[0].rh_pct,
          rain : data.data[0].rain_mm
        });
  }
 
};

function extract_rgb(rgb_string){
  var brack_index = rgb_string.indexOf("(");
    var values = rgb_string.substring(brack_index+1,rgb_string.length-1).split(",");
    for (var i = 0; i<values.length;i++){
      values[i] = parseInt(values[i]);
    }
    return values;
}

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
    },{
      "data":"type"
    },{
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





    var x = $("#fdi_table").find("tr");
    for (var row = 2; row < x.length; row++)
    {
        var td = $($(x[row]).find("td")[3]);
        var fdi = td.text();
        var data = HISTORIC[row-2];
        td.css("background-color",data.fdiColour);
        var rgb = extract_rgb(td.css("background-color"));
        var o = Math.round(((parseInt(rgb[0]) * 299) + (parseInt(rgb[1]) * 587) + (parseInt(rgb[2]) * 114)) /1000);
        (o > 125) ? td.css('color', 'black') : td.css('color', 'white'); 

    }


  $("td.weather-station-select").html('<i class="fa fa-line-chart"></i>');
  
  // Add event listener for updating the FDI graph
  $('table.fdi-table tbody').on('click','tr',function() {    
      update_graph(tableFdi.row(this).index());
      $("table.fdi-table tbody tr").removeClass('fdi-table');    
      $(this).addClass('fdi-table');
  });


 $("table.fdi-table tbody tr").addClass('cursor'); //Pointer Cursor
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
          fdi: parseFloat(json.data[i].LFDI[0]),
          fdiColor: json.data[i].LFDI[1],
          rain: parseFloat(json.data[i].rain_mm),
          windSpeed: parseFloat(json.data[i].ws_kmh),
          relativeHumidity: parseFloat(json.data[i].rh_pct),
          temperature: parseFloat(json.data[i].temp_c),
          windDirection: parseFloat(json.data[i].winddirection_deg)
        });

      $("#station-name").html('<i class="fa fa-line-chart"></i>  FDI Graph:' +json.station_name );
/*
      $('.fdi-table').on('mouseover', '.weather-station-select', function() {

          $(this).css("background-color",colorr );
      }).
      on('mouseout', '.weather-station-select', function() {

          $(this).css("background-color", "white");

      });
*/


     
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
          fdi: parseFloat(json[key].LFDI[0]),
          fdiColor: json[key].LFDI[1],
          rain: parseFloat(json[key].rain_mm),
          windSpeed: parseFloat(json[key].ws_kmh),
          relativeHumidity: parseFloat(json[key].rh_pct),
          temperature: parseFloat(json[key].temp_c)
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
            date: new Date(LFDIFORECAST[i].date),
            value2: LFDIFORECAST[i].fdi,
            rain: LFDIFORECAST[i].rain,
            fdiColor: "#"+LFDIFORECAST[i].fdiColor,
            windSpeed: LFDIFORECAST[i].windSpeed,
            relativeHumidity: LFDIFORECAST[i].relativeHumidity,
            temperature: LFDIFORECAST[i].temperature,
            windDirection: LFDIFORECAST[i].windDirection
          });
      }

    for (var i =0; i < LFDILOCAL.length; i++){
          graph_data.push({
            date: new Date(LFDILOCAL[i].date),
            value1: LFDILOCAL[i].fdi,
            fdiColor: "#"+LFDILOCAL[i].fdiColor,
            rain: LFDILOCAL[i].rain,
            windSpeed: LFDILOCAL[i].windSpeed,
            relativeHumidity: LFDILOCAL[i].relativeHumidity,
            temperature: LFDILOCAL[i].temperature,
            windDirection: LFDILOCAL[i].windDirection
          });
    }

  graph_data.sort(compare);
  sorted = graph_data.sort(compare);
  
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
          "fillColors": "blue",
          "fillAlphas": 0.4,
          "lineAlpha": 0,
          "fillColorsField": "fdiColor",
          "title": "12H00 Forecast",
          "type": "column",
          "valueField": "value2"
        },{
          "balloonText": "<h6>Measured:</h6>Temperature : [[temperature]] <br> Wind Speed : [[windSpeed]] <br> Relative Humidity : [[relativeHumidity]] <br> Wind Direction : [[windDirection]] <br> Rain : [[rain]] <br> FDI : [[value1]]",
          "lineThickness": 3,
          "connect": true,
          "title": "FDI",
          "lineColor": "#FFFFFF",
          "colorField":"fdiColor",
          "type": "smoothedLine",
          "valueField": "value1"
        },{
          "balloonText": "",
          "lineThickness": 3,
          "connect": true,
          "title": "date",
          "lineColor": "#FFFFFF",
          "type": "smoothedLine",
          "valueField": "date"
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



chart.addListener("clickGraphItem", handleClick)
function handleClick(event){
    console.log(event);
    event.graph.balloonText = '<h6>Forecast:</h6> Temperature : [[temperature]] <br> Wind Speed : [[windSpeed]] <br> Relative Humidity : [[relativeHumidity]] <br> Rain : [[rain]] <br> FDI : [[value2]]';

  }



      
}
// END FDI CHART
});

