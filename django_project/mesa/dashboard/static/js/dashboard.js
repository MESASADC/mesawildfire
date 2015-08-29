
// CONSTANTS

var FDI_URL = "/rest/FdiPointData/?format=json";
var FIRE_URL = "/rest/FireFeature/?format=json";


// BEGIN LAYOUT

function unique(list) {
    var result = [];
    $.each(list, function(i, e) {
        if ($.inArray(e, result) == -1) {
            result.push(e);
        }
    });
    return result;
}




$(function() {
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

    // END OPEN LAYERS
});

/*
var HISTORIC = [];
var FORECAST = [];
var TABLEDATAA = Array();

Object.size = function(obj) {
    var size = 0,
        key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) {
            size++;
        }
    }
    return size;
};

/*
function fdi_table_data(json){
  for (var j =0; j < json.length; j++){
    var data = json[j];
    HISTORIC.push({
      type:"WS",
      station: data.station_name,
      fdi: parseFloat(data.data[0].fdi_value),
      fdiColour: data.data[0].fdi_rgb,
      wind : data.data[0].windspd_kmh,
      temp : data.data[0].temp_c,
      relativeH : data.data[0].rh_pct,
      rain : data.data[0].rain_mm
    });
  }

};*/

/*
var DATAA = [];

function read_server_data(server_data) {

    for (var x = 0; x < server_data.features.length; x++) {

        var data = server_data.features[x];
        var today = new Date();
        if (data.properties.date_time !== null) {
            var date = new Date(data.properties.date_time);
            //if (date.getDate() == today.getDate()){
            DATAA.push({

                type: data.properties.type,
                station: data.properties.name,
                fdi: data.properties.fdi_value,
                fdiColour: data.properties.fdi_rgb,
                wind: data.properties.windspd_kmh,
                temp: data.properties.temp_c,
                relativeH: data.properties.rh_pct,
                rain: data.properties.rain_mm,
                date: data.properties.date_time

            });

            //}   
        }


    }
    console.log(DATAA);
}

*/

function extract_rgb(rgb_string) {

    var brack_index = rgb_string.indexOf("(");
    var values = rgb_string.substring(brack_index + 1, rgb_string.length - 1).split(",");
    for (var i = 0; i < values.length; i++) {
        values[i] = parseInt(values[i]);
    }
    return values;
}

var debugvar;

function compare_date(a, b) {
    if (a.date < b.date)
        return -1;
    if (a.date > b.date)
        return 1;
    return 0;
}


$(document).ready(function() {

    var fdiData = {};
    var fdiColors = {};

    // get fdi data
    $.get(FDI_URL, function(result, status) {

        var selected = null;
                       
        result.features.forEach(function (feature) {

            var properties = feature.properties;
            var station_id = feature.id;
            
            var weather = {
                station_id: station_id,
                station_name: properties.name,
                type: properties.type,
                fdi: properties.fdi_value,
                fdiColour: properties.fdi_rgb,
                wind: properties.windspd_kmh,
                temp: properties.temp_c,
                relativeH: properties.rh_pct,
                rain: properties.rain_mm,
                date: new Date(properties.date_time),
                temperature: properties.temp_c,
                windSpeed: properties.windspd_kmh,
                windDirection: properties.winddir_deg,
                is_forecast: properties.is_forecast
            };
            
            if (properties.is_forecast) {
                weather.forecast_fdi = properties.fdi_value;
            } else {
                weather.actual_fdi = properties.fdi_value;
            };

            if (fdiData[station_id] === undefined) {
                fdiData[station_id] = [];
            };
            
            fdiData[station_id].push(weather);
            fdiColors[weather.fdi] = weather.fdiColor; // perhaps rather have a js function to compute rgb?
            
            if (selected === null) {
                selected = station_id;
            };
            
        });

        render_chart(selected);


        var fdiTableData = [];
        var last;
        
        for (key in fdiData) {
            if (fdiData.hasOwnProperty(key)) {
                fdiData[key].sort(compare_date);
                // after sorting, get the last value for the table
                last = fdiData[key].pop();
                fdiData[key].push(last);
                fdiTableData.push(last);
            }
        };
        

        var fdiTable = $('table.fdi-table').DataTable({

            data: fdiTableData,
            deferRender: true,
            dom: "tS",
            scrollY: "90%",
            scrollCollapse: true,
            scrollX: "90%",
            stateSave: true,
            paging: false,
            columns: [{
                    "className": 'hidden station_id',
                    "orderable": false,
                    "data": "station_id",
                    "defaultContent": ' '
                },
                {
                    "className": "type",
                    "data": "type"
                }, {
                    "data": "name"
                }, {
                    "className": "fdi",
                    "data": "fdi_value"
                }
            ],
            "order": [
                [1, 'asc']
            ]
        });

        for (tr in $("#fdi_table").find("tr")) {
            var td_fdi = $(tr).find("td.fdi").toArray();
            td_fdi.forEach(function(td) {
                var fdiValue = $(td).text();
                var fdiColor = fdiColors[fdiValue];
                $(td).css("background-color", fdiColor);
                var rgb = extract_rgb($(td).css("background-color"));
                var o = Math.round(((parseInt(rgb[0]) * 299) + (parseInt(rgb[1]) * 587) + (parseInt(rgb[2]) * 114)) / 1000);
                (o > 125) ? $(td).css('color', 'black'): $(td).css('color', 'white');
            });
            var td_type = $(tr).find("td.type").toArray();
            td_type.forEach(function(td) {
                var type = $(td).text();
                if (type == 'wstation') {
                    $(td).addClass("fa fa-tint");
                    $(td).html('');
                } else if (type == 'poi') {
                    $(td).addClass("fa fa-map-marker");
                    $(td).html('');
                }
            });

        }

        $("table.fdi-table tbody tr").addClass('cursor');

    }); // get fdi data 

    $('#fdi-table-search').on('keyup', function() {
        fdiTable.search(this.value).draw();
    });

    // get fire data.
    $.get(FIRE_URL, function(result, status) {

        var tableData = [];
        
        result.features.forEach(function (feature) {
            var row = feature.properties;
            row.id = feature.id;
            tableData.push(row);
        });

        var fireTable = $('table.fire-table').DataTable({
            data: tableData,
            deferRender: true,
            dom: "tS",
            scrollY: "40%",
            scrollCollapse: true,
            stateSave: true,
            paging: false,
            "columns": [{
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            }, {
                "data": "description"
            }, {
                "data": "status"
            }, {
                "data": "status"
            }, {
                "data": "current_fdi"
            }, {
                "data": "max_frp"
            }],
            "order": [
                [1, 'asc']
            ]
        });

    }); // get fire data

    $('#fire-table-search').on('keyup', function() {
        fireTable.search(this.value).draw();
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
        for (var i = 0; i < visible_columns.length; i++) {
            visible_column_names.push($(visible_columns[i]).text());
        }
        visible_columns = unique(visible_column_names);

        var displaying_keys = Array();
        for (key in d) {
            for (var i = 0; i < visible_columns.length; i++) {
                var my_key = visible_columns[i].trim().toLowerCase();
                my_key = my_key.replace(/[^\w\s]/gi, '').trim().replace(/ /g, '_');
                if (key == my_key) {
                    displaying_keys.push(key);
                    break;
                }
            }
        }

        var html = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;display:inline">';
        for (key in d) {
            if (displaying_keys.indexOf(key) == -1) {
                var string;
                if (custom_names[key] !== null)
                    string = custom_names[key];
                else
                    string = key.charAt(0).toUpperCase() + "" + key.substring(1).replace(/_/g, ' ');

                html += '<tr>' +
                    '<td>' + string + ':</td>' +
                    '<td>' + d[key] + '</td>' +
                    '</tr>';
            }
        }
        html += '</table>';
        return html;
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
        }
        else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
            tr.parent().find('td[colspan=7]').parent().prepend(wms_image);
        }
    });

    // END FIRE EVENT TABLE


    // BEGIN FDI CHART

    var SECOND = 1000;
    var MINUTE = 60 * SECOND;
    var HOUR = 60 * MINUTE;
    var DAY = 24 * HOUR;


    // Add event listener for updating the FDI graph
    $('table.fdi-table').on('click', 'tr', function() {
        var station_id = $(this).find('td.station_id').text();
        render_chart(station_id);
        //$("table.fdi-table tbody tr").removeClass('fdi-table');
        //$(this).addClass('fdi-table');
    });

            
    function render_chart(station_id) {

        var chart = AmCharts.makeChart("chartdiv", {
            "type": "serial",
            "theme": "dark",
            "marginRight": 80,
            "dataProvider": graph_data[station_id],
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
                /*"balloonText": "[[is_forecast]]",
                "columnWidth": 15,
                "fillColors": "black",
                "fillAlphas": 0.4,
                "lineAlpha": 0,
                "title": "12H00 Forecast",
                "type": "column",
                "valueField": "forecast_fdi"
            }, {*/
                "balloonText": "[[actual_fdi]]",
                "lineThickness": 3,
                "connect": true,
                "title": "FDI",
                "lineColor": "#FFFFFF",
                "type": "smoothedLine",
                "valueField": "actual_fdi"
            /*}, {
                "balloonText": "",
                "lineThickness": 3,
                "connect": true,
                "title": "date",
                "lineColor": "#FFFFFF",
                "type": "smoothedLine",
                "valueField": "date"*/
            }],
            "zoomOutButtonRollOverAlpha": 0.15,
            "chartCursor": {
                "categoryBalloonDateFormat": "MMM DD JJ:NN",
                "cursorPosition": "pointer",
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



        /*
        chart.addListener("clickGraphItem", handleClick)
        function handleClick(event){
          console.log(event);
          event.graph.balloonText = '<h6>Forecast:</h6> Temperature : [[temperature]] <br> Wind Speed : [[windSpeed]] <br> Relative Humidity : [[relativeHumidity]] <br> Rain : [[rain]] <br> FDI : [[value2]]';
         
          vex.dialog.alert("Temperature:"+event.item.dataContext.temperature+"<br>"+
                           "Relative Humidity:"+event.item.dataContext.relativeHumidity+"<br>"+
                           "Wind Speed:"+event.item.dataContext.windSpeed+"<br>"+
                           "FDI:"+event.item.dataContext.value2);

        // "balloonText": "<h6>Measured:</h6>Temperature : [[temperature]] <br> Wind Speed : [[windSpeed]] <br> Relative Humidity : [[relativeHumidity]] <br> Wind Direction : [[windDirection]] <br> Rain : [[rain]] <br> FDI : [[value1]]",

        }

        */


    }
    // END FDI CHART



});
