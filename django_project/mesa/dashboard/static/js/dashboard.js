
// CONSTANTS

var FDI_URL = "/rest/FdiPointData/?format=json";
var FIRE_URL = "/rest/FireEvent/?format=json";
var NUM_INITIAL_FIRES = 8;
var FIRE_THUMBNAIL_URL = "http://localhost/geoserver/mesa/wms?service=WMS&version=1.1.0&request=GetMap&layers=mesa:day-natural.c,mesa:mesa_firefeature,mesa:mesa_firepixel_area&styles=&width=200&height=200&srs=EPSG:4326&format=image/png&bbox="

// GLOBALS

var fdiTable;
var fireTable;
var map;
var defaultView;


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
    /*window.onload = function () {
    // Use SockJS
    Stomp.WebSocketClass = SockJS;
     
    // Connection parameters
    var mq_username = "guest",
        mq_password = "guest",
        mq_vhost    = "/",
        mq_url      = 'http://127.0.0.1:32775/stomp',
     
        // The queue we will read. The /topic/ queues are temporary
        // queues that will be created when the client connects, and
        // removed when the client disconnects. They will receive
        // all messages published in the "amq.topic" exchange, with the
        // given routing key, in this case "mymessages"
    mq_queue    = "/testing/tests";
     

    // This will be called upon successful connection
    function on_connect() {
      console.log('Connected to RabbitMQ-Web-Stomp');
      console.log(client);
      client.subscribe(mq_queue, on_message);
    }
     
    // This will be called upon a connection error
    function on_connect_error() {
     console.log('Connection failed!');
    }
     
    // This will be called upon arrival of a message
    function on_message(m) {
      console.log('message received'); 
      console.log(m);
      console.log(m.body);
    }
     
      // Create a client
      var client = Stomp.client(mq_url);
      // Connect
      client.connect(mq_username,mq_password,on_connect,on_connect_error,mq_vhost);
    }*/


    window.onload = function () {

        var ws = new SockJS('http://localhost:32775/stomp/');
        var client = Stomp.over(ws);

        client.heartbeat.outgoing = 0;
        client.heartbeat.incoming = 0;

        var onConnect = function() {
          client.subscribe('/queue/testing', function(d) {
            console.log(JSON.parse(d.body));
          });
        };

        var on_connect = function(x) {
           console.log(x);
          client.subscribe("/exchange/amq.topic", function(d) {
              //client.send('/queue/testing', {"content-type":"text/plain"}, "data datad");
              
              console.log(d.body);
          });

      };

        // This will be called upon arrival of a message
        var onMessage = function(m) {
          console.log('message received'); 
          console.log(m);
          console.log(m.body);
        }

        var onError = function(e) {
          console.log('ERROR', e);
        };
        
        var onDebug = function(m) {
          console.log('DEBUG', m);
        };
        client.onmessage = onMessage;
        //client.debug = onDebug;
        client.connect('guest', 'guest', on_connect, onError, '/');
        };
    
});

$(function() {
    // BEGIN OPEN LAYERS

    var backdrop_osm = new ol.layer.Tile({
        source: new ol.source.OSM(),
        preload: 10
    });

    
    var backdrop = new ol.layer.Tile({
        source: new ol.source.TileWMS({
          url: '/geoserver/wms',
          params: {'LAYERS': 'mesa:custom_background'},
          serverType: 'geoserver'
        }),
        preload: 10
    });

    var gadm2 = new ol.layer.Image({
        source: new ol.source.ImageWMS({
          url: '/geoserver/wms',
          params: {'LAYERS': 'mesa:gadm2'},
          serverType: 'geoserver'
        })
    });

    var fireStyle = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'black',
            width: 3
        }),
        fill: new ol.style.Fill({
            color: 'rgba(100, 100, 100, 0.1)'
        })
    });

    var firesVector = new ol.layer.Vector({
        source: new ol.source.Vector({
            projection: 'EPSG:4326',
            url: '/rest/FireFeature/?format=json',
            format: new ol.format.GeoJSON()
        }),
        style: fireStyle
    });
    
    var firesWMS = new ol.layer.Image({
        source: new ol.source.ImageWMS({
          url: '/geoserver/wms',
          params: {'LAYERS': 'mesa:fires_today'},
          serverType: 'geoserver'
        })
    });

    var firePixelWMS = new ol.layer.Image({
        source: new ol.source.ImageWMS({
          url: '/geoserver/wms',
          params: {'LAYERS': 'mesa:firepixel_polygons_today'},
          serverType: 'geoserver'
        })
    });

    var msgWMS = new ol.layer.Image({
        source: new ol.source.ImageWMS({
          url: '/geoserver/wms',
          params: {'LAYERS': 'mesa:day-natural.c'},
          serverType: 'geoserver'
        }),
        minResolution: 2000
    });


    /**
     * Elements that make up the info popup.
     */
    var container = document.getElementById('popup');
    var content = document.getElementById('popup-content');
    var closer = document.getElementById('popup-closer');


    /**
     * Add a click handler to hide the popup.
     * @return {boolean} Don't follow the href.
     */
    closer.onclick = function() {
      overlay.setPosition(undefined);
      closer.blur();
      return false;
    };


    /**
     * Create an overlay to anchor the popup to the map.
     */
    var overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
      element: container,
      autoPan: true,
      autoPanAnimation: {
        duration: 250
      }
    }));
    
    defaultView = new ol.View({
        center: ol.proj.transform([25.85, -17.53], 'EPSG:4326', 'EPSG:3857'),
        zoom: 6,
        minZoom: 4,
        maxZoom: 12
    });

    map = new ol.Map({
        //projection: 'EPSG:4326',
        layers: [ backdrop, gadm2, msgWMS, firesWMS, firePixelWMS ],
        target: "map",
        view: defaultView,
        overlays: [overlay],
        controls: ol.control.defaults().extend([
            //new ol.control.FullScreen() not working properly
        ]),

    });

    var layersToRefresh = [ msgWMS, firesWMS, firePixelWMS ];

    function refreshLayers() {
        layersToRefresh.forEach(function(layer) {
            layer.getSource().changed();
        }); 
    }; 

    setInterval(refreshLayers, 10000);
    
    
    // select interaction working on "singleclick"
    var selectSingleClick = new ol.interaction.Select();
    map.addInteraction(selectSingleClick);
    selectSingleClick.on('select', function () {
        this.getFeatures().forEach( function (feat) {
            console.log(feat);
            var fireId = feat.getId();
            //tr = $('#fire-table tbody tr[fire-id="' + fireId + '"]');
            //var row = fireTable.row(tr);
            //console.log(row);
            //var i = fireTable.rows().indexOf(row);
            //console.log(i);
            //row.scrollTo(true);
            console.log(
                fireTable.$('#fire-table tbody tr[fire-id="' + fireId + '"]')
            );
        })
    });
    
    /**
     * Add a click handler to the map to render the popup.
     */
    /*map.on('singleclick', function(evt) {
    var coordinate = evt.coordinate;
    var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
        coordinate, 'EPSG:3857', 'EPSG:4326'));
        content.innerHTML = '<p>You clicked here:</p><code>' + hdms + '</code>';
      overlay.setPosition(coordinate);
    }); popup size issue
    */  

    
    var exportPNGElement = document.getElementById('export-png');
    if ('download' in exportPNGElement) {
        exportPNGElement.addEventListener('click', function(e) {
        map.once('postcompose', function(event) {
          var canvas = event.context.canvas;
          exportPNGElement.href = canvas.toDataURL('image/png');
        });
        map.renderSync();
      }, false);
    } else {
      var info = document.getElementById('no-download');
      /**
       * display error message
       */
      info.style.display = '';
    };
    

});



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


var simpleDate = (function() {
    // Turns Javascript Date Objects into human readable form
     
    var measures = {
        second: 1,
        minute: 60,
        hour: 3600,
        day: 86400,
        week: 604800,
        month: 2592000,
        year: 31536000
    };
 
    var chkMultiple = function(amount, type) {
        return (amount > 1) ? amount + " " + type + "s": "one " + type;
    };

    function only_HH_MM(date) {
       var localeSpecificTime = date.toLocaleTimeString();
       return localeSpecificTime.replace(/:\d+$/, '');
    };
    
    return function(thedate, before) {

        if (!measures.hasOwnProperty(before)) 
            before = 'hour';

        before = (typeof before === 'undefined') ? 'hour' : before;
        
        thedate = new Date(thedate);
        var dateStr, amount, denomination,
            current = new Date().getTime(),
            diff = (current - thedate.getTime()) / 1000; // work with seconds

        var future = diff < 0;
        diff = Math.abs(diff);  // use absolute diff together with future boolean from now on
 
        // if the interval is larger than the specified denomination
        if (diff >= measures[before]) {
            var isToday = (thedate.toDateString() == (new Date()).toDateString());
            if (isToday) {
                return only_HH_MM(thedate) + ' today';
            } else {
                return thedate.toLocaleString();
            };
        };

        if(diff > measures.year) {
            denomination = "year";
        } else if(diff > measures.month) {
            denomination = "month";
        } else if(diff > measures.week) {
            denomination = "week";
        } else if(diff > measures.day) {
            denomination = "day";
        } else if(diff > measures.hour) {
            denomination = "hour";
        } else if(diff > measures.minute) {
            denomination = "minute";
        } else {
            if (future) {
                dateStr = "in a few seconds";
            } else {
                dateStr = "a few seconds ago";
            };
            return dateStr;
        };
        amount = Math.round(diff/measures[denomination]);
        if (future) {
            dateStr = "in about " + chkMultiple(amount, denomination);
        } else {
            dateStr = "about " + chkMultiple(amount, denomination) + " ago";
        };
        return dateStr;
    };
    
})();


$(document).ready(function() {

    var fdiData = {};
    var fdiColors = {};

    // get fdi data
    $.get(FDI_URL, function(result, status) {

        var selected = null;
                       
        result.features.forEach(function (feature) {

            var properties = feature.properties;
            
            if (properties.fdi_value === null) {
                return;
            }

            var point_id = feature.id;
            
            var weather = {
                point_id: point_id,
                point_name: properties.name,
                type: properties.type,
                fdi: properties.fdi_value,
                fdiColor: properties.fdi_rgb,
                wind: properties.windspd_kmh,
                temp: properties.temp_c,
                relativeH: properties.rh_pct,
                rain: properties.rain_mm,
                date: new Date(properties.date_time),
                temperature: properties.temp_c,
                windSpeed: properties.windspd_kmh,
                windDirection: properties.winddir_deg,
                is_forecast: properties.is_forecast,
                forecast_actual: properties.is_forecast ? "Forecast" : "Actual"
            };
            
            if (properties.is_forecast) {
                weather.forecast_fdi = properties.fdi_value;
            } else {
                weather.actual_fdi = properties.fdi_value;
            };

            if (fdiData[point_id] === undefined) {
                fdiData[point_id] = [];
            };
            
            fdiData[point_id].push(weather);
            fdiColors[weather.fdi] = weather.fdiColor; // perhaps rather have a js function to compute rgb?
            
            if (selected === null) {
                selected = point_id;
            };
            
        });


        var fdiTableData = [];
        var last;
        
        for (key in fdiData) {
            if (fdiData.hasOwnProperty(key)) {
                fdiData[key].sort(compare_date);
                if (fdiData[key].length > 0) { 
                    // after sorting, get the last value for the table
                    last = fdiData[key].pop();
                    // and put it back again
                    fdiData[key].push(last);
                    // show current fdi for fdi point
                    fdiTableData.push(last);
                } else {
                    last = null;
                }
            }

        };
        
        render_chart(selected);
    
        fdiTable = $('#fdi-table').DataTable({

            data: fdiTableData,
            deferRender: true,
            dom: "tS",
            scrollY: "90%",
            scrollCollapse: true,
            scrollX: "90%",
            stateSave: true,
            scroller: true,
            paging: true,
            columns: [{
                    "className": 'hidden point_id',
                    "orderable": false,
                    "data": "point_id",
                    "defaultContent": ' '
                },
                {
                    "className": "point-type icon-column",
                    "data": "type"
                }, {
                    "data": "point_name"
                }, {
                    "className": "fdi",
                    "data": "fdi"
                }, {
                    "className": "fdi-date",
                    "data": "date",
                    "render": function ( data, type, row, meta ) {
                        return (type == 'display' | type == 'filter') ? simpleDate(data) : data;
                    }
                }, {
                    "data": "forecast_actual"
                }
            ],
            "order": [
                [1, 'asc']
            ]
        });

        for (tr in $("#fdi-table, #fire-table").find("tr")) {
            var td_fdi = $(tr).find("td.fdi").toArray();
            td_fdi.forEach(function(td) {
                var fdiValue = $(td).text();
                var fdiColor = fdiColors[fdiValue];
                $(td).css("background-color", fdiColor);
                var rgb = extract_rgb($(td).css("background-color"));
                var o = Math.round(((parseInt(rgb[0]) * 299) + (parseInt(rgb[1]) * 587) + (parseInt(rgb[2]) * 114)) / 1000);
                (o > 125) ? $(td).css('color', 'black'): $(td).css('color', 'white');
            });
            var td_type = $(tr).find("td.point-type").toArray();
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

        $('#fdi-table-search').on('keyup', function() {
            fdiTable.search(this.value).draw();
        });

    }); // get fdi data 


    // get fire data.
    $.get(FIRE_URL + '&limit=' + NUM_INITIAL_FIRES + '&offset=0', function(data, status) {
        
        var tableData = [];
        var fires;
        var remaining;
        
        if (data.hasOwnProperty('results')) {
            fires = data.results;
            remaining = data.count - fires.length; 
        }
        else {
            fires = data;
            remaining = 0;
        };

        fires.forEach(function (fire) {
            tableData.push(fire);
        });

        fireTable = $('#fire-table').DataTable({
            data: tableData,
            deferRender: true,
            dom: "tS",
            scrollY: "35%",
            scrollCollapse: false,
            paging: true,
            scroller: true,
            stateSave: true,
            "initComplete": function( settings, json ) {
                // the idea is to load a small subset of fires first to speed up rendering the table on page load
                if (remaining > 0) {
                    $.get(FIRE_URL + '&limit=' + remaining + '&offset=' + NUM_INITIAL_FIRES, function(data, status) {
                        fireTable.rows.add(data.results).draw();
                    });
                    //flyToPoint(row(1).select();
                };
            },
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
                "data": "area",
                "render": function ( data, type, row, meta ) {
                    if (type == 'display') {
                        sqkm = data / Math.pow(10,6);
                        ha = data / Math.pow(10, 4);
                        return ha.toFixed(2) + " ha";
                    } else {
                        return data;
                    }
                }
            }, {
                "className": "fdi",
                "data": "current_fdi"
            }, {
                "data": "current_fdi_date",
                "render": function ( data, type, row, meta ) {
                    return (type == 'display' | type == 'filter') ? simpleDate(data) : data;
                }
            }, {
                "data": "max_frp"
            }, {
                "data": "max_frp_date",
                "render": function ( data, type, row, meta ) {
                    return (type == 'display' | type == 'filter') ? simpleDate(data) : data;
                }
            }],
            "order": [
                [1, 'asc']
            ]
        });
        
        debugvar = tableData;

        $('#fire-table-search').on('keyup', function() {
            fireTable.search(this.value).draw();
        });

        /* Formatting function for row details - modify as you need */

        var custom_names = {
            "first_seen": "First observation",
            "last_seen": "Last observation",
            "start_fdi": "FDI at the first observation",
            "max_fdi": "Maximum FDI during the fire"
        };


        /* Formatting function for row details - modify as you need */
        function row_detail(d) {
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
            html += 
                '<tr>' +
                    '<th rowspan="' + displaying_keys.length + '"><image class="fire-detail-thumbnail" fire-id="' + d.id + '" style="width:200px; height:200px;" src="' + FIRE_THUMBNAIL_URL + d.vbox_west + ',' + d.vbox_south + ',' + d.vbox_east + ',' + d.vbox_north + '"/></th>' +
                    '<td colspan="2" class="fire-detail-title">Additional info:</td>'+
                '</tr>';
            
            for (key in d) {
                if (displaying_keys.indexOf(key) == -1) {
                    var string;
                    if (custom_names[key] !== undefined) {
                        string = (d[key] instanceof Date) ? simpleDate(d[key]) : d[key];
                        html += '<tr>' +
                            '<td>' + custom_names[key] + ':</td>' +
                            '<td>' + string + '</td>' +
                        '</tr>';
                    } else {
                        //string = key.charAt(0).toUpperCase() + "" + key.substring(1).replace(/_/g, ' ');
                    }
                }
            }
            html += '</table>';
            return html;
        }





        function flyToPoint(lon, lat) {
            var start = +new Date();
            var from = defaultView.getCenter();
            var to = ol.proj.fromLonLat([lon, lat]);

            // Determine zoom level needed to see from and to points at the same time             
            var distanceX = Math.abs(to[0] - from[0]);
            var distanceY = Math.abs(to[1] - from[1]);
            var startPixel = map.getPixelFromCoordinate(from);
            var endPixel = map.getPixelFromCoordinate(to);
            var distancePixelX = Math.abs(endPixel[0] - startPixel[0]);
            var distancePixelY = Math.abs(endPixel[1] - startPixel[1]);
            var mapSizeX = map.getSize()[0];
            var mapSizeY = map.getSize()[1];
            
            var ratioX = distancePixelX / mapSizeX; 
            var ratioY = distancePixelY / mapSizeY; 
            var ratio = Math.max(ratioX, ratioY);

            var wgs84 = new ol.Sphere(6378137);
            var geodesicDistance = wgs84.haversineDistance(from, to); 

            var duration = 1000 * Math.max(0.5, Math.min(2, Math.abs(ratio)));

            var pan = ol.animation.pan({
                duration: duration,
                source: from,
                start: start
            });
            var bounce = ol.animation.bounce({
                duration: duration,
                resolution: defaultView.getResolution() * Math.max(1, Math.abs(ratio)),
                start: start
            });
            map.beforeRender(pan, bounce);
            defaultView.setCenter(to);
        };
        /*
        var ws = new SockJS('http://127.0.0.1:32775/stomp');
        var client = Stomp.over(ws);

        client.heartbeat.outgoing = 0;
        client.heartbeat.incoming = 0;

        var onDebug = function(m) {
          console.log('DEBUG', m);
        };

        var onConnect = function() {
          client.subscribe('/queue/testing', function(d) {
            console.log(JSON.parse(d.body));
          });
        };

        var onError = function(e) {
          console.log('ERROR', e);
        };

        client.debug = onDebug;
        window.onload = function () {
        client.connect('guest', 'guest', onConnect, onError, '/');
        }
        */

        

     



        // Add event listener for opening and closing details
        $('#fire-table tbody').on('click', 'td.details-control', function() {
            var tr = $(this).closest('tr');
            var row = fireTable.row(tr);

            if (row.child.isShown()) {
                // This row is already open - close it
                row.child.hide();
                tr.removeClass('shown');
            }
            else {
                // Open this row, close others
                $('#fire-table tbody tr.shown').removeClass('shown');
                var child = row.child(row_detail(row.data()));
                child.show();
                tr.addClass('shown');
                row.scrollTo();
            }
        });
        
        $('#fire-table tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            fireTable.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            var row = fireTable.row($(this));
            if (row) {
                var data = row.data();
                flyToPoint(data.centroid_x, data.centroid_y);
            };
        }
    } );

        /*$('#fire-table tbody tr').each( function () {
            var row = fireTable.row(this);
            if (row & row.data()) {
                $(this).attr('fire-id', row.data()['id']);
            }
        });*/


    }); // get fire data



    // END FIRE EVENT TABLE


    // BEGIN FDI CHART

    var SECOND = 1000;
    var MINUTE = 60 * SECOND;
    var HOUR = 60 * MINUTE;
    var DAY = 24 * HOUR;


    // Add event listener for updating the FDI graph
    $('#fdi-table').on('click', 'tr', function() {
        var point_id = $(this).find('td.point_id').text();
        render_chart(point_id);
        //$("table.fdi-table tbody tr").removeClass('fdi-table');
        //$(this).addClass('fdi-table');
    });

            
    function render_chart(point_id) {
        
        $("#point-name").html("FDI: " + fdiData[point_id][0].point_name);
        
        fdiData[point_id] 

        var chart = AmCharts.makeChart("chartdiv", {
            "type": "serial",
            "theme": "dark",
            "marginRight": 80,
            "dataProvider": fdiData[point_id],
            "valueAxes": [{
                "maximum": 100,
                "minimum": 0,
                "axisAlpha": 0.4,
                "guides": [{}, {
                    "lineColor": "#0000FF",
                    "lineThickness": 3,
                    "lineAlpha": 0,
                    "value": 0,
                    "toValue": 20
                }, {
                    "lineColor": "#00FF00",
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
                "balloonText": "Actual FDI:[[forecast_fdi]]",
                "columnWidth": 15,
                "fillColors": "black",
                "fillAlphas": 0.4,
                "lineAlpha": 0,
                "title": "12H00 Forecast",
                "type": "column",
                "valueField": "forecast_fdi"
            }, {
                "balloonText": "Actual FDI:[[actual_fdi]]",
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


    function refresh_tables_and_chart() {

    };

    setInterval(refresh_tables_and_chart, 60000);


});
