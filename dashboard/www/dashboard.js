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


var tableData = [
{
  "id": "55",
  "description": "Near Township A",
  "status": "In Progress",
  "area": 10,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township B",
  "status": "In Progress",
  "area": 20,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township C",
  "status": "Out",
  "area": 30,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township A",
  "status": "In Progress",
  "area": 10,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township B",
  "status": "In Progress",
  "area": 20,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township C",
  "status": "Out",
  "area": 30,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township A",
  "status": "In Progress",
  "area": 10,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township B",
  "status": "In Progress",
  "area": 20,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township C",
  "status": "Out",
  "area": 30,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township D",
  "status": "Responding",
  "area": 40,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township E",
  "status": "Out",
  "area": 50,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township F",
  "status": "Responding",
  "area": 60,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "55",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
},
{
  "id": "555",
  "description": "Near Township G",
  "status": "In Progress",
  "area": 70,
  "max_frp": 700,
  "first_observed": "2015/04/25",
  "last_observed": "2015/04/26",
  "fdi_first": 70,
  "fdi_last": 65,
  "fdi_current": 60
}
];



$(document).ready(function(){

  var table = $('table.fire-table').DataTable({
    "data": tableData,
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

  $('.form-control.search').on( 'keyup', function () {
      table.search( this.value ).draw();
  } );


});

// END FIRE EVENT TABLE


// BEGIN FDI CHART

      // generate data
      var chartData = [];

      function generateChartData() {
        var thisDate = new Date();
        var firstDate = new Date(thisDate.getTime() - 2 * 24 * 60 * 60 * 1000);
        firstDate.setHours(0);
        firstDate.setMinutes(0);
        firstDate.setSeconds(0);
        firstDate.setMilliseconds(0);

        for (var i = firstDate.getTime(); i < (firstDate.getTime() + 5 * 24 * 60 * 60 * 1000); i += 60 * 60 * 1000) {
          var newDate = new Date(i);
          var value1 = 0;

          if (i == firstDate.getTime()) {
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
                value1: value1
              });
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

      generateChartData();

      var chart = AmCharts.makeChart("chartdiv", {
        "type": "serial",
        "theme": "dark",
        "marginRight": 80,
        "dataProvider": chartData,
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
          "balloonText": "", // "[[title]]: [[value]]",
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
          "connect": false,
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

// END FDI CHART
