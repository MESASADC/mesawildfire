// CONSTANTS

var FDI_CURRENT_URL = "/geoserver/mesa/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=mesa:lfdi_point_forecast_and_measured_current&outputFormat=application/json"
var FDI_GRAPH_URL = "/rest/FdiGraphData/?format=json";
var FIRE_THUMBNAIL_URL = "/geoserver/mesa/wms?service=WMS&version=1.1.0&request=GetMap&layers=mesa:custom_background,mesa:fires_since_yesterday,mesa:hotspots_since_yesterday&styles=&width=200&height=200&srs=EPSG:4326&format=image/png&bbox="
var FIRE_URL = "/geoserver/mesa/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=mesa:fires_since_yesterday&outputFormat=application/json"
var NUM_INITIAL_FIRES = 8;

// GLOBALS
var fdiTable;
var fireTable;
var map;
var defaultView;
var webStompSocket;
var webStompClient;
var fire_active_data;
var fireStyle;
var firesVector;


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

    var borders = new ol.layer.Image({
        source: new ol.source.ImageWMS({
          url: '/geoserver/wms',
          params: {'LAYERS': 'mesa:MESASADC'},
          serverType: 'geoserver'
        })
    });

    fireStyle = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'black',
            width: 1,
            lineDash: [5, 2]
        }),
        fill: new ol.style.Fill({
            color: 'rgba(100, 100, 100, 0.1)'
        })
    });

    var firesWMS = new ol.layer.Image({
        source: new ol.source.ImageWMS({
          url: '/geoserver/wms',
          params: {'LAYERS': 'mesa:fires_since_yesterday', 'viewparams': 'prev_days:6'},
          serverType: 'geoserver'
        })
    });

    var firePixelWMS = new ol.layer.Image({
        source: new ol.source.ImageWMS({
          url: '/geoserver/wms',
          params: {'LAYERS': 'mesa:hotspots_since_yesterday'},
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
    
    var firesVector = new ol.layer.Vector({
        source: new ol.source.Vector({
          projection: 'EPSG:4326',
          url: FIRE_URL,
          format: new ol.format.GeoJSON({defaultDataProjection :'EPSG:4326', projection: 'EPSG:3857'})
	}),
        style: fireStyle
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

    /**ws
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
        center: ol.proj.transform([35, -16], 'EPSG:4326', 'EPSG:3857'),
        zoom: 3,
        minZoom: 3,
        maxZoom: 12
    });

    map = new ol.Map({
        layers: [ backdrop, borders, msgWMS, firePixelWMS, firesVector],
        target: "map",
        view: defaultView,
        overlays: [overlay],
        controls: ol.control.defaults().extend([
            new ol.control.ScaleLine()
            //new ol.control.FullScreen() not working properly
        ]),

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

function fdiColor(fdiValue) {
    if (fdiValue > 75)
        return "#FF0000";
    else if (fdiValue > 60)
        return "#FFA500";
    else if (fdiValue > 45)
        return "#FFFF00";
    else if (fdiValue > 20)
        return "#00FF00";
    else if (fdiValue > 0)
        return "#0000FF";
    else 
        return "#FFFFFF";
};

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

    return function(thedate, before) {

        // get a Date object if thedate is a string or null
        thedate = new Date(thedate);

        // display empty string for null date
        if (!thedate.valueOf())
            return ""; 

        // before is a string that indicates where the relative representation should stop
        // if 'before' is not a valid 'measures' key, then default to hour
        var before_default = 'second';
        if (!measures.hasOwnProperty(before))
            before = before_default;
        before = (typeof before === 'undefined') ? before_default : before;

        var dateStr, amount, denomination,
            //current = new Date().getTime(),
            //diff = (current - thedate.getTime()) / 1000; // work with seconds
            current = new Date(),
            diff = (current - thedate) / 1000; // work with seconds

        var future = diff < 0;
        diff = Math.abs(diff);  // use absolute diff together with future boolean from now on

        // if the interval is larger than the specified denomination
        if (diff >= measures[before]) {
            var isToday = (thedate.toDateString() == (new Date()).toDateString());
            if (isToday) {
                return thedate.toLocaleString("en",  { hour: "numeric", hour12: true, minute: "numeric" }) + ' today';
            } else {
                return thedate.toLocaleString("en",  { weekday: "long", month: "short", day: "numeric", hour: "numeric", hour12: true, minute: "numeric"  } );
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
        } else {            
            denomination = "minute";
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


var fdiGraph = {};
var fdiRows = [];

$(document).ready(function() {
    

    // get fdi table data
    $.get(FDI_CURRENT_URL, function(result, status) {
    
        console.log('got fdi table data');

        result.features.forEach(function (feature) {

            var properties = feature.properties;

            var row = {
                feature_id: feature.id,
                point_id: properties.point_id,
                point_name: properties.point_name,
                point_type: properties.point_type,
                lfdi_value: properties.value,
                lfdi_color: fdiColor(properties.value),
                target_date_time: new Date(properties.target_date_time),
                value_class: properties.value_class
            };
            
            fdiRows.push(row);

        });



        var start = new Date().getTime();

        fdiTable = $('#fdi-table').DataTable({

            data: fdiRows,
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
                    "data": "point_type"
                }, {
                    "className": "point-name",
                    "data": "point_name"
                }, {
                    "className": "lfdi",
                    "data": "lfdi_value"
                }, {
                    "className": "fdi-date",
                    "data": "target_date_time",
                    "render": function ( data, type, row, meta ) {
                        return (type == 'display' | type == 'filter') ? simpleDate(data) : data;
                    }
                }, {
                    "data": "value_class"
                }
            ],
            "order": [
                [2, 'asc']
            ]
        });

        var end = new Date().getTime();
        var time = end - start;
        console.log('FDI Table:Start time -:- ' + start);
        console.log('FDI Table:End time -:- ' + end);
        console.log('FDI Table:Execution time -:- ' + time);
        

        for (tr in $("#fdi-table, #fire-table").find("tr")) {
            var td_fdi = $(tr).find("td.lfdi").toArray();
            td_fdi.forEach(function(td) {
                var fdiValue = $(td).text();
                $(td).css("background-color", fdiColor(fdiValue));
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

    }); // get fdi table data


    var star = new Date().getTime();
    // get fdi graph data
    $.get(FDI_GRAPH_URL, function(result, status) {
    
        console.log('got fdi graph data');

        var graphPointName;

        result.forEach(function (item) {

            var value = {
                point_id: item.point_id,
                point_name: item.point_name,
                target_date_time: item.target_date_time,
                value: item.value,
                value_class: item.value_class,
                color: fdiColor(item.value)
            };

            if ( ! (value.point_name in fdiGraph) )
                fdiGraph[value.point_name] = [];

            fdiGraph[value.point_name].push(value);

            if (!graphPointName)
                graphPointName = value.point_name;

        });

        render_chart(graphPointName);
    });

    var en = new Date().getTime();
    var tim = en - star;
    console.log('FDI graph:Execution time -:- ' + tim);


    // get fire data
    $.get(FIRE_URL + '&sortBy=id&maxFeatures=' + NUM_INITIAL_FIRES, function(data, status) {

        console.log('got initial fire data');

        var tableData = [];
        var fires;

        console.log(data);

        data.features.forEach(function (fire) {
            tableData.push(fire.properties);
        });

        fireTable = $('#fire-table').DataTable({
            data: tableData ,
            deferRender: true,
            dom: "tS",
            scrollY: "35%",
            scrollCollapse: false,
            paging: true,
            scroller: true,
            stateSave: true,
            "initComplete": function( settings, json ) {
                // the idea is to load a small subset of fires first to speed up rendering the table on page load
                $.get(FIRE_URL + '&sortBy=id&startIndex=' + NUM_INITIAL_FIRES, function(data, status) {
                    console.log('got more fire data: ' + data.features.length);
                    data.features.forEach( function (feature) {
                        fireTable.rows.add(feature.properties);
                    });
                    fireTable.draw();
                });
            },
            "columns": [{
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            }, {
                "className" : 'hidden fireid',
                "data": "id"
            }, {
                "data": "description"
            }, {
                "className" : 'hidden',
                "data": "status"
            },{
                "data": "area",
                "render": function ( data, type, row, meta ) {
					
                    if (type == 'display') 
                    {
                        sqkm = data / Math.pow(10,6);
                        ha = data / Math.pow(10, 4);
                        return ha.toFixed(1) + " ha"; 
                    } 
                    else {
                       return data;
                    }
                }
            },{
                "className": "lfdi",
                "data": "current_fdi"
            }, {
                "data": "max_frp"
            }, {
                "data": "first_seen",
                "render": function ( data, type, row, meta ) {
                    return (type == 'display' | type == 'filter') ? simpleDate(data) : data;
                }
            }, {
                "data": "last_seen",
                "render": function ( data, type, row, meta ) {
                    return (type == 'display' | type == 'filter') ? simpleDate(data) : data;
                }
            }],
            "order": [
                [8, "desc"],
                [7, "asc"]
            ]
        });
        
        // Order by last_seen (column 8)
        fireTable.order([8, "desc"], [7, "asc"]).draw();

        // Redraw table to update relative time ( "10 minutes ago")
        setInterval(function() { fireTable.draw(); }, 10 * 60 * 1000);
        
       
        $('#fire-table-search').on('keyup', function() {
            fireTable.search(this.value).draw();
        });

        /* Formatting function for row details - modify as you need */
        var key_names = {
            "first_seen": "First observation",
            "last_seen": "Last observation",
            "start_fdi": "FDI at the first observation",
            "max_fdi": "Maximum FDI during the fire"
        };

        var date_keys = [ "first_seen", "last_seen", "current_fdi_date", "max_fdi_date", "max_frp_date" ];

        var number_keys = [ "area" ]; 

        var hide_keys = [ "id", "bbox" ]; //, "vbox_west", "vbox_east", "vbox_north", "vbox_south", "centroid_x", "centroid_y" ];

        /* Formatting function for row details - modify as you need */
        function row_detail(d) {
            var visible_columns = $(".dataTable").find("th.sorting, th.sorting-asc,th.sorting-desc");

            var visible_column_names = Array();
            for (var i = 0; i < visible_columns.length; i++) {
                visible_column_names.push($(visible_columns[i]).text());
            }
            visible_columns = unique(visible_column_names);

            var visible_keys = Array();
            for (key in d) {
                for (var i = 0; i < visible_columns.length; i++) {
                    var my_key = visible_columns[i].trim().toLowerCase();
                    my_key = my_key.replace(/[^\w\s]/gi, '').trim().replace(/ /g, '_');
                    if (key == my_key) {
                        visible_keys.push(key);
                        break;
                    }
                }
            }

            var html = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;display:inline">';
            html +=
                '<tr>' +
                    '<td><div class = "img-rounded"><image class="fire-detail-thumbnail img-rounded" fire-id="' + d.id + '" style="width:100px; height:100px;" src="' + FIRE_THUMBNAIL_URL + d.west + ',' + d.south + ',' + d.east + ',' + d.north + '"/></div></th>' +
                    '<td class="fire-detail-list"><ul class="fire-detail-list">';
                
            for (key in d) {
                if ( /*(visible_keys.indexOf(key) == -1) & */ (hide_keys.indexOf(key) == -1)) {
                    var name;
                    var value;
                    if (key_names[key] !== undefined) {
                        name = key_names[key];
                    } else {
                        name = key.charAt(0).toUpperCase() + "" + key.substring(1).replace(/_/g, ' ');
                    };
                    if (date_keys.indexOf(key) > -1)
                       value = simpleDate(d[key]);
                    else if (key == "area")
                       value = (parseFloat(d[key]) / Math.pow(10, 4)).toFixed(1) + " ha";
                    else if (number_keys.indexOf(key) > -1)
                       value = Math.round(parseFloat(d[key]) * 100 / 100).toFixed(2);
                    else
                       value = d[key];
                    html += '<li><b>' + name + '</b> :  ' + value + '</li>';
                };
            };
            html += '</ul></td></tr></table>';
            return html;
        };
        



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

            var duration = 1000 * Math.max(0.5, Math.min(3, Math.abs(ratio)));

            var pan = ol.animation.pan({
                duration: duration,
                source: from
            });
            var bounce = ol.animation.bounce({
                duration: duration,
                resolution: defaultView.getResolution() * Math.max(1, Math.abs(ratio))
            });
            var dipFrom = defaultView.getResolution();
            var zoom;
            var bounceThenDip = function(map, frameState) {
                var bouncing = bounce(map, frameState);
                var zooming = false;
                if (!bouncing) {
                    if (!zoom) {
                        zoom = ol.animation.zoom({
                            duration: duration,
                            resolution: dipFrom
                        });
                        map.beforeRender(zoom);
                        defaultView.setZoom(Math.max(defaultView.getZoom(), 9));
                    };
                    zooming = zoom(map, frameState);
                }
                return bouncing || zooming;
            };
            map.beforeRender(pan, bounceThenDip);
            defaultView.setCenter(to);
        };

            //RabbitMQ WebStomp
        
            webStompSocket = new WebSocket('ws://'+document.location.hostname+':56723/ws');
            webStompClient = Stomp.over(webStompSocket);
            
            webStompClient.heartbeat.outgoing = 0;
            webStompClient.heartbeat.incoming = 0;
            
            var onDebug = function(m) {
              console.log('WebStomp DEBUG', m.body);
            }
            
            var onConnect = function() {
				
              webStompClient.subscribe('/exchange/mesa_terminal/notify.db.FireEvent.#', function(d) {
                //Received Message
                fire_active_data = JSON.parse(d.body);
                pk_id = fire_active_data.pk;
                            

               //Add fire feature.                
               var firesVector = new ol.layer.Vector({
					source: new ol.source.Vector({
					projection: 'EPSG:4326',
					url: '/rest/FireEvent/'+pk_id+'/?format=json',
					format: new ol.format.GeoJSON({defaultDataProjection :'EPSG:4326', projection: 'EPSG:3857'})
					
					}),
					style: fireStyle
				});
                map.addLayer(firesVector);
                
                

                //Add fire event data in the fire table
                $.get("http://"+document.location.hostname+"/rest/FireEvent/"+pk_id+"/?format=json",function(fire_event_data){
                        
                     var fire_event_obj = fire_event_data.properties;
                     var fire_event_id = fire_event_data.id;
                     fire_event_obj.id = fire_event_id;
                     //fire_event_obj["current_fdi"] = Math.floor(Math.random()*101);
                     fireTable.row.add(fire_event_obj).draw();
                     console.log("Added fire: "+fire_event_obj.description+" ,in the table"); 
                     
                     //Adding FDI colour after receiving new fire data.
					 var rows_fire = $("#fire-table").dataTable().fnGetNodes();
					 for(var x = 0;x < rows_fire.length;x++)
					 {
						var fdi_val = $(rows_fire[x]).find("td.lfdi");
						var fire_d = $(rows_fire[x]).find("td.fireid");
						$(fdi_val).css("background-color", fdiColor($(fdi_val).text()));
						
					 }                     

			    }).fail(function() {
                     console.log("ERROR occured:Trying to connect to: "+document.location.hostname);
                });                
              });
              
            };
            
            var onError = function(e) {
              console.log('WebStomp ERROR', e);
            };
            
            webStompClient.connect('user', 'password', onConnect, onError, '/');

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
        if ( $(this).hasClass('selected') && $(this).hasClass('row_selected') ) {
            $(this).removeClass('selected');
            $(this).removeClass('row_selected');
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
    
    //select interaction working on "singleclick"
    var selectSingleClick = new ol.interaction.Select();
    map.addInteraction(selectSingleClick);
    /*selectSingleClick.on('select', function () {
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
    });*/
    
    selectSingleClick.on('select', function(evt){
		
		if(evt.selected.length > 0){
			
			fireTable.$("#fire-table tbody tr").removeClass('selected');
                     
			var selected_fire_id_fire = evt.selected[0].getId();
			var selected_fire_id = evt.selected[0].q.id;
			var rows = $("#fire-table").dataTable().fnGetNodes();
			var fire_available = false;
			var final_selected;

			 if(selected_fire_id_fire){
				final_selected = selected_fire_id_fire;
			 }

			 if(selected_fire_id){
				final_selected = selected_fire_id;
			 }

			if(rows.length)
			{
						
				for(var i=0; i < rows.length; i++)
				{
					
					var table_fire_id = $(rows[i]).find("td.fireid").html();

					if(final_selected == table_fire_id)
					 {
						fire_available = true;
						//console.log("ROW:"+String(i));
						//console.log("Row Index:"+String(rows[i].rowIndex));
                        console.log("----------------------FOUND---------------------------------");
						console.log("Table ID:"+String(table_fire_id));
						console.log("Selected Fire ID:"+String(final_selected));
                        console.log("-------------------------------------------------------------");
						console.log(evt.selected[0].q.description+" is available in the table.");
						fireTable.$('tr:eq(' +  String(i) + ')').addClass('selected');
						fireTable.row('.selected').scrollTo();
                        //console.log(evt.selected[0]);
				     }
				
					if(fire_available == false)
					{
					   //console.log(selected_fire_id_fire);
					   console.log("Table ID:"+String(table_fire_id));
					   console.log("Selected Fire ID:"+String(final_selected));
					   console.log(evt.selected[0].q.description+" is not available in the table.");	
					}
			    }
			 }
	     }
		
    });
    
	/*var select = new ol.interaction.Select();
	map.addInteraction(select);

	var selected_collection = select.getFeatures();
	selected_collection.push(featurePoint);*/
    
    
 
       /* $('#fire-table tbody tr').each( function () {
            //var row = fireTable.row(this);
            console.log(this);
            $(this).attr('abcd', 1234);
            if (row & row.data()) {
                $(row).attr('fire-id', row.data()['id']);
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
        var point_name = $(this).find('td.point-name').text();
        render_chart(point_name);
    });


    function render_chart(point_name) {
        
        $("#point-name").html("FDI at: " + point_name);
        
        var chart = AmCharts.makeChart("chartdiv", {
            "type": "serial",
            "startDuration": 1,
            "theme": "dark",
            "marginRight": 80,
            "dataProvider": fdiGraph[point_name],
            "valueAxes": [{
                "maximum": 100,
                "minimum": 0,
                "axisAlpha": 0.4,
                "guides": [{},/* {
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
                }*/]
            }],

            "graphs": [{
                "balloonText": "Forecast FDI:[[value]]",
                "columnWidth": 15,
                "fillColors": "black",
                "fillAlphas": 0.4,
                "lineAlpha": 0,
                "title": "12H00 Forecast",
                "type": "column",
                "valueField": "value",
                "fillColorsField":"color"
            }, {/*
                "balloonText":  "Actual FDI:[[actual_fdi]]",
                "lineThickness": 3,
                "connect": true,
                "title": "FDI",
                "lineColor": "#FFFFFF",
                "type": "smoothedLine",
                "valueField": "value"*/
            /*}, {
                "balloonText": "",
                "lineThickness": 3,
                "connect": true,
                "title": "date",
                "lineColor": "#FFFFFF",
                "type": "smoothedLine",
                "valueField": "date"*/
            }],
            "depth3D": 10,
            "angle": 30,
            "zoomOutButtonRollOverAlpha": 0.15,
            "chartCursor": {
                "categoryBalloonDateFormat": "MMM DD JJ:NN",
                "cursorPosition": "pointer",
                "showNextAvailable": true
            },
            "autoMarginOffset": 5,
            "columnWidth": 1,
            "categoryField": "target_date_time",
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

});

