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

