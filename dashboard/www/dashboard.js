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

var RealTime = 
    [{
        "station_id": "0513435A4",
        "station_name": "PRETORIA UNIVERSITY PROEFPLAAS",
        "distance_m": 4497.378442236,
        "data": [
            {
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
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.04,
                "rh_pct": 70,
                "LFDI": [
                    15,
                    "0000ff"
                ],
                "temp_c": 5.1,
                "firedanger": 15,
                "winddirection_deg": 122,
                "localtime": "2015-07-27 04:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 4.68,
                "rh_pct": 54,
                "LFDI": [
                    24,
                    "00ff00"
                ],
                "temp_c": 8.4,
                "firedanger": 24,
                "winddirection_deg": 110,
                "localtime": "2015-07-27 06:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 08:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 10:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 12:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 14:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 16:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 18:00:00"
            }
        ]},
        {
        "station_id": "0513435A4",
        "station_name": "JOHANNESBURG UNIVERSITY ",
        "distance_m": 4497.378442236,
        "data": [
            {
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
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.04,
                "rh_pct": 70,
                "LFDI": [
                    15,
                    "0000ff"
                ],
                "temp_c": 5.1,
                "firedanger": 15,
                "winddirection_deg": 122,
                "localtime": "2015-07-27 04:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 4.68,
                "rh_pct": 54,
                "LFDI": [
                    24,
                    "00ff00"
                ],
                "temp_c": 8.4,
                "firedanger": 24,
                "winddirection_deg": 110,
                "localtime": "2015-07-27 06:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 08:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 10:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 12:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 14:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 16:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 18:00:00"
            }
        ],
        "station_id": "0513435A4"
      }
    ];

    var RealTimeEG = [
    {
        "station_name": "PRETORIA UNIVERSITY PROEFPLAAS",
        "distance_m": 4497.378442236,
        "data": [
            {
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
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.04,
                "rh_pct": 70,
                "LFDI": [
                    15,
                    "0000ff"
                ],
                "temp_c": 5.1,
                "firedanger": 15,
                "winddirection_deg": 122,
                "localtime": "2015-07-27 04:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 4.68,
                "rh_pct": 54,
                "LFDI": [
                    24,
                    "00ff00"
                ],
                "temp_c": 8.4,
                "firedanger": 24,
                "winddirection_deg": 110,
                "localtime": "2015-07-27 06:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 08:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 10:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 12:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 14:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 16:00:00"
            },
            {
                "rain_mm": null,
                "ws_kmh": 5.4,
                "rh_pct": 38,
                "LFDI": [
                    35,
                    "00ff00"
                ],
                "temp_c": 13.4,
                "firedanger": 35,
                "winddirection_deg": 40,
                "localtime": "2015-07-27 18:00:00"
            }
        ],
        "station_id": "0513435A4"
    }

    ];


              var ForeCast = {

                 "2015-07-25": {
                    "rain_mm": 0,
                    "vwind_ms": 2,
                    "FWI": [
                       43,
                       "ffa500"
                    ],
                    "temp_k": 300,
                    "rh_pct": 88,
                    "LFDI": [
                       43,
                       "ffa500"
                    ],
                    "dc": 1598,
                    "temp_c": 27,
                    "dmc": 522,
                    "ffmc": 88,
                    "rain_days": 20,
                    "date": "2015-07-25",
                    "dewpt_k": 291,
                    "LFDIreal": [
                       49,
                       "ffff00"
                    ],
                    "uwind_ms": 1,
                    "ws_kmh": 8.05
                 },
                 "2015-07-26": {
                    "rain_mm": 0,
                    "dmc": 523,
                    "temp_k": 303,
                    "FWI": [
                       41,
                       "ffa500"
                    ],
                    "uwind_ms": 1,
                    "rh_pct": 88,
                    "LFDI": [
                       41,
                       "ffa500"
                    ],
                    "vwind_ms": 2,
                    "dc": 1604,
                    "temp_c": 30,
                    "ffmc": 90,
                    "rain_days": 20,
                    "date": "2015-08-01",
                    "dewpt_k": 292,
                    "LFDIreal": [
                       61,
                       "ffa500"
                    ],
                    "ws_kmh": 8.05
                 },
                 "2015-07-27": {
                    "rain_mm": 0,
                    "dmc": 523,
                    "temp_k": 303,
                    "FWI": [
                       41,
                       "ffa500"
                    ],
                    "uwind_ms": 1,
                    "rh_pct": 88,
                    "LFDI": [
                       41,
                       "ffa500"
                    ],
                    "vwind_ms": 2,
                    "dc": 1604,
                    "temp_c": 30,
                    "ffmc": 90,
                    "rain_days": 20,
                    "date": "2015-08-01",
                    "dewpt_k": 292,
                    "LFDIreal": [
                       99,
                       "ffa500"
                    ],
                    "ws_kmh": 8.05
                 },
                 "2015-07-28": {
                    "rain_mm": 0,
                    "dmc": 525,
                    "temp_k": 304,
                    "FWI": [
                       34,
                       "ffff00"
                    ],
                    "uwind_ms": 2,
                    "rh_pct": 90,
                    "vwind_ms": 5,
                    "LFDI": [
                       34,
                       "ffff00"
                    ],
                    "temp_c": 31,
                    "dc": 1607,
                    "ffmc": 90,
                    "rain_days": 20,
                    "date": "2015-08-02",
                    "dewpt_k": 290,
                    "LFDIreal": [
                       52,
                       "ffff00"
                    ],
                    "ws_kmh": 19.39
                 },
                 "2015-07-29": {
                    "rain_mm": 0,
                    "dmc": 518,
                    "temp_k": 300,
                    "FWI": [
                       59,
                       "ffa500"
                    ],
                    "uwind_ms": 0,
                    "rh_pct": 59,
                    "vwind_ms": -1,
                    "LFDI": [
                       59,
                       "ffa500"
                    ],
                    "temp_c": 27,
                    "dc": 1587,
                    "ffmc": 91,
                    "rain_days": 20,
                    "date": "2015-07-27",
                    "dewpt_k": 286,
                    "LFDIreal": [
                       60,
                       "ffff00"
                    ],
                    "ws_kmh": 3.6
                 },
                 "2015-07-30": {
                    "rain_mm": 0,
                    "dmc": 523,
                    "FWI": [
                       36,
                       "ffff00"
                    ],
                    "temp_k": 299,
                    "rh_pct": 93,
                    "LFDI": [
                       36,
                       "ffff00"
                    ],
                    "vwind_ms": 6,
                    "dc": 1601,
                    "temp_c": 26,
                    "ffmc": 87,
                    "rain_days": 20,
                    "date": "2015-07-31",
                    "dewpt_k": 292,
                    "LFDIreal": [
                       43,
                       "00ff00"
                    ],
                    "uwind_ms": 1,
                    "ws_kmh": 21.9
                 },
                 "2015-07-31": {
                    "rain_mm": 0,
                    "vwind_ms": 5,
                    "temp_k": 295,
                    "FWI": [
                       29,
                       "ffff00"
                    ],
                    "uwind_ms": 2,
                    "rh_pct": 90,
                    "LFDI": [
                       29,
                       "ffff00"
                    ],
                    "dc": 1594,
                    "temp_c": 22,
                    "dmc": 520,
                    "ffmc": 89,
                    "rain_days": 20,
                    "date": "2015-07-29",
                    "dewpt_k": 287,
                    "LFDIreal": [
                       46,
                       "ffff00"
                    ],
                    "ws_kmh": 19.39
                 },
                 "2015-08-01": {
                    "rain_mm": 0,
                    "dmc": 519,
                    "temp_k": 297,
                    "FWI": [
                       50,
                       "ffa500"
                    ],
                    "uwind_ms": 1,
                    "rh_pct": 70,
                    "LFDI": [
                       50,
                       "ffa500"
                    ],
                    "dc": 1591,
                    "temp_c": 24,
                    "vwind_ms": 6,
                    "ffmc": 91,
                    "rain_days": 20,
                    "date": "2015-07-28",
                    "dewpt_k": 288,
                    "LFDIreal": [
                       56,
                       "ffff00"
                    ],
                    "ws_kmh": 21.9
                 }
              };




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
  var tablefdi = $('table.fdi-table').DataTable({
 
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

  // Add event listener for updating the FDI graph
  $('table.fdi-table tbody').on('click','weather-station-select',function() {

    update_graph();

  });


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



/*
    var tablefdi = $('#fdi-table display').DataTable({
    "data1": drest,
    deferRender:    true,
    dom:            "tS",
    scrollY:        "60%",
    scrollCollapse: true,
    stateSave:      true,
    paging:         false,

    "columns": [{"className": 'details-control',"orderable": false,"data1": null,"defaultContent": ''}, 
    {
      "data1": "station_name"
    }, 
    {
      "data1": "LFDI"
    }, 
    {
      "data1": "ws_kmh"
    },
    {
      "data1":"temp_c"
    }, 
    {
      "data1": "rh_pct"
    }, 
    {
      "data1":  "rain_mm"
    }],
    "order": [
      [1, 'asc']
    ]
  });*/



 
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


  $('.form-control.search').on( 'keyup', function () {
      table.search( this.value ).draw();
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
     parse_historic(RealTime[0]);
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
          "balloonText": "[[title]]: [[value]]",
          "columnWidth": 15,
          "fillColors": "#000000",
          "fillAlphas": 0.4,
          "lineAlpha": 0,
          "title": "12H00 Forecast",
          "type": "column",
          "valueField": "value2"
        }, {
          "balloonText": "",
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
