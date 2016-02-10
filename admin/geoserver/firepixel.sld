<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns:sld="http://www.opengis.net/sld" xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
   <sld:NamedLayer>
      <sld:Name>firepixel</sld:Name>
      <sld:UserStyle>
         <sld:Name>firepixel</sld:Name>
         <sld:Title>Default polygon style</sld:Title>
         <sld:Abstract>Style point (the_geom) when zoomed out, polygon when zoomed in.</sld:Abstract>
         <sld:FeatureTypeStyle>
            <sld:Name>name</sld:Name>
            <sld:Rule>
               <sld:Title>FRP 0-150 MW/km^2</sld:Title>
               <sld:Abstract>Abstract</sld:Abstract>
               <ogc:Filter>
                  <ogc:PropertyIsLessThanOrEqualTo>
                     <ogc:PropertyName>frp</ogc:PropertyName>
                     <ogc:Literal>150</ogc:Literal>
                  </ogc:PropertyIsLessThanOrEqualTo>
               </ogc:Filter>
               <sld:MaxScaleDenominator>2000000.0</sld:MaxScaleDenominator>
               <sld:PolygonSymbolizer>
                  <sld:Geometry>
                     <ogc:PropertyName>polygon</ogc:PropertyName>
                  </sld:Geometry>
                  <sld:Fill>
                     <sld:CssParameter name="fill">#ffbf00</sld:CssParameter>
                  </sld:Fill>
               </sld:PolygonSymbolizer>
            </sld:Rule>
            <sld:Rule>
               <sld:Title>FRP 150-300 MW/km^2</sld:Title>
               <sld:Abstract>Abstract</sld:Abstract>
               <ogc:Filter>
                  <ogc:And>
                     <ogc:PropertyIsGreaterThan>
                        <ogc:PropertyName>frp</ogc:PropertyName>
                        <ogc:Literal>150</ogc:Literal>
                     </ogc:PropertyIsGreaterThan>
                     <ogc:PropertyIsLessThanOrEqualTo>
                        <ogc:PropertyName>frp</ogc:PropertyName>
                        <ogc:Literal>300</ogc:Literal>
                     </ogc:PropertyIsLessThanOrEqualTo>
                  </ogc:And>
               </ogc:Filter>
               <sld:MaxScaleDenominator>2000000.0</sld:MaxScaleDenominator>
               <sld:PolygonSymbolizer>
                  <sld:Geometry>
                     <ogc:PropertyName>polygon</ogc:PropertyName>
                  </sld:Geometry>
                  <sld:Fill>
                     <sld:CssParameter name="fill">#ff7f00</sld:CssParameter>
                  </sld:Fill>
               </sld:PolygonSymbolizer>
            </sld:Rule>
            <sld:Rule>
               <sld:Title>FRP 300-600 MW/km^2</sld:Title>
               <sld:Abstract>Abstract</sld:Abstract>
               <ogc:Filter>
                  <ogc:And>
                     <ogc:PropertyIsGreaterThan>
                        <ogc:PropertyName>frp</ogc:PropertyName>
                        <ogc:Literal>300</ogc:Literal>
                     </ogc:PropertyIsGreaterThan>
                     <ogc:PropertyIsLessThanOrEqualTo>
                        <ogc:PropertyName>frp</ogc:PropertyName>
                        <ogc:Literal>600</ogc:Literal>
                     </ogc:PropertyIsLessThanOrEqualTo>
                  </ogc:And>
               </ogc:Filter>
               <sld:MaxScaleDenominator>2000000.0</sld:MaxScaleDenominator>
               <sld:PolygonSymbolizer>
                  <sld:Geometry>
                     <ogc:PropertyName>polygon</ogc:PropertyName>
                  </sld:Geometry>
                  <sld:Fill>
                     <sld:CssParameter name="fill">#fe2712</sld:CssParameter>
                  </sld:Fill>
               </sld:PolygonSymbolizer>
            </sld:Rule>
            <sld:Rule>
               <sld:Title>FRP &gt; 600 MW/km^2</sld:Title>
               <sld:Abstract>Abstract</sld:Abstract>
               <ogc:Filter>
                  <ogc:PropertyIsGreaterThan>
                     <ogc:PropertyName>frp</ogc:PropertyName>
                     <ogc:Literal>600</ogc:Literal>
                  </ogc:PropertyIsGreaterThan>
               </ogc:Filter>
               <sld:MaxScaleDenominator>2000000.0</sld:MaxScaleDenominator>
               <sld:PolygonSymbolizer>
                  <sld:Geometry>
                     <ogc:PropertyName>polygon</ogc:PropertyName>
                  </sld:Geometry>
                  <sld:Fill>
                     <sld:CssParameter name="fill">#ff0000</sld:CssParameter>
                  </sld:Fill>
               </sld:PolygonSymbolizer>
            </sld:Rule>
            <sld:Rule>
               <sld:Title>FRP 0-150 MW/km^2</sld:Title>
               <sld:Abstract>Abstract</sld:Abstract>
               <ogc:Filter>
                  <ogc:PropertyIsLessThanOrEqualTo>
                     <ogc:PropertyName>frp</ogc:PropertyName>
                     <ogc:Literal>150</ogc:Literal>
                  </ogc:PropertyIsLessThanOrEqualTo>
               </ogc:Filter>
               <sld:MinScaleDenominator>2000000.0</sld:MinScaleDenominator>
               <sld:PointSymbolizer>
                  <sld:Geometry>
                     <ogc:PropertyName>point</ogc:PropertyName>
                  </sld:Geometry>
                  <sld:Graphic>
                     <sld:Mark>
                        <sld:Fill>
                           <sld:CssParameter name="fill">#ffbf00</sld:CssParameter>
                        </sld:Fill>
                     </sld:Mark>
                     <sld:Size>6</sld:Size>
                  </sld:Graphic>
               </sld:PointSymbolizer>
            </sld:Rule>
            <sld:Rule>
               <sld:Title>FRP 150-300 MW/km^2</sld:Title>
               <sld:Abstract>Abstract</sld:Abstract>
               <ogc:Filter>
                  <ogc:And>
                     <ogc:PropertyIsGreaterThan>
                        <ogc:PropertyName>frp</ogc:PropertyName>
                        <ogc:Literal>150</ogc:Literal>
                     </ogc:PropertyIsGreaterThan>
                     <ogc:PropertyIsLessThanOrEqualTo>
                        <ogc:PropertyName>frp</ogc:PropertyName>
                        <ogc:Literal>300</ogc:Literal>
                     </ogc:PropertyIsLessThanOrEqualTo>
                  </ogc:And>
               </ogc:Filter>
               <sld:MinScaleDenominator>2000000.0</sld:MinScaleDenominator>
               <sld:PointSymbolizer>
                  <sld:Geometry>
                     <ogc:PropertyName>point</ogc:PropertyName>
                  </sld:Geometry>
                  <sld:Graphic>
                     <sld:Mark>
                        <sld:Fill>
                           <sld:CssParameter name="fill">#ff7f00</sld:CssParameter>
                        </sld:Fill>
                     </sld:Mark>
                     <sld:Size>6</sld:Size>
                  </sld:Graphic>
               </sld:PointSymbolizer>
            </sld:Rule>
            <sld:Rule>
               <sld:Title>FRP 300-600 MW/km^2</sld:Title>
               <sld:Abstract>Abstract</sld:Abstract>
               <ogc:Filter>
                  <ogc:And>
                     <ogc:PropertyIsGreaterThan>
                        <ogc:PropertyName>frp</ogc:PropertyName>
                        <ogc:Literal>300</ogc:Literal>
                     </ogc:PropertyIsGreaterThan>
                     <ogc:PropertyIsLessThanOrEqualTo>
                        <ogc:PropertyName>frp</ogc:PropertyName>
                        <ogc:Literal>600</ogc:Literal>
                     </ogc:PropertyIsLessThanOrEqualTo>
                  </ogc:And>
               </ogc:Filter>
               <sld:MinScaleDenominator>2000000.0</sld:MinScaleDenominator>
               <sld:PointSymbolizer>
                  <sld:Geometry>
                     <ogc:PropertyName>point</ogc:PropertyName>
                  </sld:Geometry>
                  <sld:Graphic>
                     <sld:Mark>
                        <sld:Fill>
                           <sld:CssParameter name="fill">#fe2712</sld:CssParameter>
                        </sld:Fill>
                     </sld:Mark>
                     <sld:Size>6</sld:Size>
                  </sld:Graphic>
               </sld:PointSymbolizer>
            </sld:Rule>
            <sld:Rule>
               <sld:Title>FRP &gt; 600 MW/km^2</sld:Title>
               <sld:Abstract>Abstract</sld:Abstract>
               <ogc:Filter>
                  <ogc:PropertyIsGreaterThan>
                     <ogc:PropertyName>frp</ogc:PropertyName>
                     <ogc:Literal>600</ogc:Literal>
                  </ogc:PropertyIsGreaterThan>
               </ogc:Filter>
               <sld:MinScaleDenominator>2000000.0</sld:MinScaleDenominator>
               <sld:PointSymbolizer>
                  <sld:Geometry>
                     <ogc:PropertyName>point</ogc:PropertyName>
                  </sld:Geometry>
                  <sld:Graphic>
                     <sld:Mark>
                        <sld:Fill>
                           <sld:CssParameter name="fill">#ff0000</sld:CssParameter>
                        </sld:Fill>
                     </sld:Mark>
                     <sld:Size>6</sld:Size>
                  </sld:Graphic>
               </sld:PointSymbolizer>
            </sld:Rule>
         </sld:FeatureTypeStyle>
      </sld:UserStyle>
   </sld:NamedLayer>
</sld:StyledLayerDescriptor>

