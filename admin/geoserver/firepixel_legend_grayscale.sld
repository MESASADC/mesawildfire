<?xml version="1.0" encoding="UTF-8"?><sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.0.0"><sld:NamedLayer><sld:Name>firepixel_legend_grayscale</sld:Name><sld:UserStyle><sld:Name>firepixel_legend_grayscale</sld:Name><sld:Title>Default polygon style</sld:Title><sld:Abstract>Style point (the_geom) when zoomed out, polygon when zoomed in.</sld:Abstract><sld:FeatureTypeStyle><sld:Name>name</sld:Name><sld:Rule><sld:Title>FRP 0-150 MW/km^2</sld:Title><sld:Abstract>Abstract</sld:Abstract><ogc:Filter><ogc:PropertyIsLessThanOrEqualTo><ogc:PropertyName>frp</ogc:PropertyName><ogc:Literal>150</ogc:Literal></ogc:PropertyIsLessThanOrEqualTo></ogc:Filter><sld:MaxScaleDenominator>200000.0</sld:MaxScaleDenominator><sld:PolygonSymbolizer><sld:Geometry><ogc:PropertyName>polygon</ogc:PropertyName></sld:Geometry><sld:Fill><sld:CssParameter name="fill">#d0d0d0</sld:CssParameter></sld:Fill></sld:PolygonSymbolizer></sld:Rule><sld:Rule><sld:Title>FRP 150-300 MW/km^2</sld:Title><sld:Abstract>Abstract</sld:Abstract><ogc:Filter><ogc:And><ogc:PropertyIsGreaterThan><ogc:PropertyName>frp</ogc:PropertyName><ogc:Literal>150</ogc:Literal></ogc:PropertyIsGreaterThan><ogc:PropertyIsLessThanOrEqualTo><ogc:PropertyName>frp</ogc:PropertyName><ogc:Literal>300</ogc:Literal></ogc:PropertyIsLessThanOrEqualTo></ogc:And></ogc:Filter><sld:MaxScaleDenominator>200000.0</sld:MaxScaleDenominator><sld:PolygonSymbolizer><sld:Geometry><ogc:PropertyName>polygon</ogc:PropertyName></sld:Geometry><sld:Fill><sld:CssParameter name="fill">#b9b8b8</sld:CssParameter></sld:Fill></sld:PolygonSymbolizer></sld:Rule><sld:Rule><sld:Title>FRP 300-600 MW/km^2</sld:Title><sld:Abstract>Abstract</sld:Abstract><ogc:Filter><ogc:And><ogc:PropertyIsGreaterThan><ogc:PropertyName>frp</ogc:PropertyName><ogc:Literal>300</ogc:Literal></ogc:PropertyIsGreaterThan><ogc:PropertyIsLessThanOrEqualTo><ogc:PropertyName>frp</ogc:PropertyName><ogc:Literal>600</ogc:Literal></ogc:PropertyIsLessThanOrEqualTo></ogc:And></ogc:Filter><sld:MaxScaleDenominator>200000.0</sld:MaxScaleDenominator><sld:PolygonSymbolizer><sld:Geometry><ogc:PropertyName>polygon</ogc:PropertyName></sld:Geometry><sld:Fill><sld:CssParameter name="fill">#a2a1a1</sld:CssParameter></sld:Fill></sld:PolygonSymbolizer></sld:Rule><sld:Rule><sld:Title>FRP &gt; 600 MW/km^2</sld:Title><sld:Abstract>Abstract</sld:Abstract><ogc:Filter><ogc:PropertyIsGreaterThan><ogc:PropertyName>frp</ogc:PropertyName><ogc:Literal>600</ogc:Literal></ogc:PropertyIsGreaterThan></ogc:Filter><sld:MaxScaleDenominator>200000.0</sld:MaxScaleDenominator><sld:PolygonSymbolizer><sld:Geometry><ogc:PropertyName>polygon</ogc:PropertyName></sld:Geometry><sld:Fill><sld:CssParameter name="fill">#8b8a8a</sld:CssParameter></sld:Fill></sld:PolygonSymbolizer></sld:Rule></sld:FeatureTypeStyle></sld:UserStyle></sld:NamedLayer></sld:StyledLayerDescriptor>