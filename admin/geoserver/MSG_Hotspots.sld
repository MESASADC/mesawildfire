<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns:sld="http://www.opengis.net/sld" xmlns="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.0.0">

    <sld:UserLayer>
        <sld:UserStyle>
          <sld:Name>MSG_Hotspots</sld:Name>
          <sld:Title>MSG Hotspots Style</sld:Title>
          <sld:Abstract></sld:Abstract>
          <sld:FeatureTypeStyle>
                <sld:Name>MSG_Hotspots</sld:Name>
                <sld:Title>MSG Hotspots Style</sld:Title>
                <sld:Abstract>MSG Hotspots Style</sld:Abstract>
                <sld:Rule>
                    <sld:Name>rule01</sld:Name>
                    <sld:Title>Low Intensity Fire</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>0</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>150</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <sld:MinScaleDenominator>2000000</sld:MinScaleDenominator>
                    <sld:PointSymbolizer>
                        <sld:Graphic>
                            <sld:Mark>
                                <sld:WellKnownName>circle</sld:WellKnownName>
                                <sld:Fill>
                                    <sld:CssParameter name="fill">
                                        <ogc:Literal>#ffbf00</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="fill-opacity">
                                        <ogc:Literal>0.85</ogc:Literal>
                                    </sld:CssParameter>
                                </sld:Fill>
                                <sld:Stroke>
                                    <sld:CssParameter name="stroke">
                                        <ogc:Literal>#000000</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-linecap">
                                        <ogc:Literal>butt</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-linejoin">
                                        <ogc:Literal>miter</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-opacity">
                                        <ogc:Literal>0</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-width">
                                        <ogc:Literal>0.5</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-dashoffset">
                                        <ogc:Literal>0.0</ogc:Literal>
                                    </sld:CssParameter>
                                </sld:Stroke>
                            </sld:Mark>
                            <sld:Opacity>
                                <ogc:Literal>0.85</ogc:Literal>
                            </sld:Opacity>
                            <sld:Size>
                                <ogc:Literal>10</ogc:Literal>
                            </sld:Size>
                            <sld:Rotation>
                                <ogc:Literal>0.0</ogc:Literal>
                            </sld:Rotation>
                        </sld:Graphic>
                    </sld:PointSymbolizer>
                </sld:Rule>
                <sld:Rule>
                    <sld:Name>rule01a</sld:Name>
                    <sld:Title>Low Intensity Pixel</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>0</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>150</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <sld:MaxScaleDenominator>2000000</sld:MaxScaleDenominator>
                    <PolygonSymbolizer>
                        <Geometry>
                           <ogc:Function name="buffer">
                             <ogc:Function name="centroid">
                                <ogc:PropertyName>point</ogc:PropertyName>
                             </ogc:Function>
                             <ogc:Literal>0.015</ogc:Literal>
                           </ogc:Function>
                        </Geometry>
                        <sld:Fill>
                            <sld:CssParameter name="fill">
                                <ogc:Literal>#ffbf00</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="fill-opacity">
                                <ogc:Literal>0.85</ogc:Literal>
                            </sld:CssParameter>
                        </sld:Fill>
                        <sld:Stroke>
                            <sld:CssParameter name="stroke">
                                <ogc:Literal>#000000</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-linecap">
                                <ogc:Literal>butt</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-linejoin">
                                <ogc:Literal>miter</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-opacity">
                                <ogc:Literal>0</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-width">
                                <ogc:Literal>0.5</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-dashoffset">
                                <ogc:Literal>0.0</ogc:Literal>
                            </sld:CssParameter>
                        </sld:Stroke>
                      </PolygonSymbolizer>
                </sld:Rule>              
                <sld:Rule>
                    <sld:Name>rule01b</sld:Name>
                    <sld:Title>Label</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>0</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>150</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                  <sld:MaxScaleDenominator>00000</sld:MaxScaleDenominator>
                    <sld:TextSymbolizer>
                      <sld:Label>
                        &lt;-- MSG, Hotspot Intensity: Low
                      </sld:Label>
                      <sld:Halo>
                        <sld:Radius>2</sld:Radius>
                      </sld:Halo>
                    </sld:TextSymbolizer>
                </sld:Rule>
                <sld:Rule>
                    <sld:Name>rule02</sld:Name>
                    <sld:Title>Medium Intensity Fire</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>151</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>300</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <sld:MinScaleDenominator>2000000</sld:MinScaleDenominator>
                    <sld:PointSymbolizer>
                        <sld:Graphic>
                            <sld:Mark>
                                <sld:WellKnownName>circle</sld:WellKnownName>
                                <sld:Fill>
                                    <sld:CssParameter name="fill">
                                        <ogc:Literal>#ff7f00</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="fill-opacity">
                                        <ogc:Literal>0.85</ogc:Literal>
                                    </sld:CssParameter>
                                </sld:Fill>
                                <sld:Stroke>
                                    <sld:CssParameter name="stroke">
                                        <ogc:Literal>#000000</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-linecap">
                                        <ogc:Literal>butt</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-linejoin">
                                        <ogc:Literal>miter</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-opacity">
                                        <ogc:Literal>0</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-width">
                                        <ogc:Literal>0.5</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-dashoffset">
                                        <ogc:Literal>0.0</ogc:Literal>
                                    </sld:CssParameter>
                                </sld:Stroke>
                            </sld:Mark>
                            <sld:Opacity>
                                <ogc:Literal>0.85</ogc:Literal>
                            </sld:Opacity>
                            <sld:Size>
                                <ogc:Literal>10</ogc:Literal>
                            </sld:Size>
                            <sld:Rotation>
                                <ogc:Literal>0.0</ogc:Literal>
                            </sld:Rotation>
                        </sld:Graphic>
                    </sld:PointSymbolizer>
                </sld:Rule>
                <sld:Rule>
                    <sld:Name>rule02a</sld:Name>
                    <sld:Title>Medium Intensity Pixel</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>151</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>300</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <sld:MaxScaleDenominator>2000000</sld:MaxScaleDenominator>
                    <PolygonSymbolizer>
                        <Geometry>
                           <ogc:Function name="buffer">
                             <ogc:Function name="centroid">
                                <ogc:PropertyName>point</ogc:PropertyName>
                             </ogc:Function>
                             <ogc:Literal>0.015</ogc:Literal>
                           </ogc:Function>
                        </Geometry>
                        <sld:Fill>
                            <sld:CssParameter name="fill">
                                <ogc:Literal>#ff7f00</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="fill-opacity">
                                <ogc:Literal>0.85</ogc:Literal>
                            </sld:CssParameter>
                        </sld:Fill>
                        <sld:Stroke>
                            <sld:CssParameter name="stroke">
                                <ogc:Literal>#000000</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-linecap">
                                <ogc:Literal>butt</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-linejoin">
                                <ogc:Literal>miter</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-opacity">
                                <ogc:Literal>0</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-width">
                                <ogc:Literal>0.5</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-dashoffset">
                                <ogc:Literal>0.0</ogc:Literal>
                            </sld:CssParameter>
                        </sld:Stroke>
                      </PolygonSymbolizer>
                </sld:Rule>              
                <sld:Rule>
                    <sld:Name>rule02b</sld:Name>
                    <sld:Title>Label</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>151</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>300</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                  <sld:MaxScaleDenominator>00000</sld:MaxScaleDenominator>
                    <sld:TextSymbolizer>
                      <sld:Label>
                        &lt;-- MSG, Hotspot Intensity: Medium
                      </sld:Label>
                      <sld:Halo>
                        <sld:Radius>2</sld:Radius>
                      </sld:Halo>
                    </sld:TextSymbolizer>
                </sld:Rule>
                <sld:Rule>
                    <sld:Name>rule03</sld:Name>
                    <sld:Title>High Intensity Fire</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>301</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>600</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <sld:MinScaleDenominator>2000000</sld:MinScaleDenominator>
                    <sld:PointSymbolizer>
                        <sld:Graphic>
                            <sld:Mark>
                                <sld:WellKnownName>circle</sld:WellKnownName>
                                <sld:Fill>
                                    <sld:CssParameter name="fill">
                                        <ogc:Literal>#fe2712</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="fill-opacity">
                                        <ogc:Literal>0.85</ogc:Literal>
                                    </sld:CssParameter>
                                </sld:Fill>
                                <sld:Stroke>
                                    <sld:CssParameter name="stroke">
                                        <ogc:Literal>#000000</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-linecap">
                                        <ogc:Literal>butt</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-linejoin">
                                        <ogc:Literal>miter</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-opacity">
                                        <ogc:Literal>0</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-width">
                                        <ogc:Literal>0.5</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-dashoffset">
                                        <ogc:Literal>0.0</ogc:Literal>
                                    </sld:CssParameter>
                                </sld:Stroke>
                            </sld:Mark>
                            <sld:Opacity>
                                <ogc:Literal>0.85</ogc:Literal>
                            </sld:Opacity>
                            <sld:Size>
                                <ogc:Literal>10</ogc:Literal>
                            </sld:Size>
                            <sld:Rotation>
                                <ogc:Literal>0.0</ogc:Literal>
                            </sld:Rotation>
                        </sld:Graphic>
                    </sld:PointSymbolizer>
                </sld:Rule>                
                <sld:Rule>
                    <sld:Name>rule03a</sld:Name>
                    <sld:Title>High Intensity Pixel</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>301</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>600</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <sld:MaxScaleDenominator>2000000</sld:MaxScaleDenominator>
                    <PolygonSymbolizer>
                        <Geometry>
                           <ogc:Function name="buffer">
                             <ogc:Function name="centroid">
                                <ogc:PropertyName>point</ogc:PropertyName>
                             </ogc:Function>
                             <ogc:Literal>0.015</ogc:Literal>
                           </ogc:Function>
                        </Geometry>
                        <sld:Fill>
                            <sld:CssParameter name="fill">
                                <ogc:Literal>#fe2712</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="fill-opacity">
                                <ogc:Literal>0.85</ogc:Literal>
                            </sld:CssParameter>
                        </sld:Fill>
                        <sld:Stroke>
                            <sld:CssParameter name="stroke">
                                <ogc:Literal>#000000</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-linecap">
                                <ogc:Literal>butt</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-linejoin">
                                <ogc:Literal>miter</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-opacity">
                                <ogc:Literal>0</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-width">
                                <ogc:Literal>0.5</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-dashoffset">
                                <ogc:Literal>0.0</ogc:Literal>
                            </sld:CssParameter>
                        </sld:Stroke>
                      </PolygonSymbolizer>
                </sld:Rule> 
                 <sld:Rule>
                    <sld:Name>rule03b</sld:Name>
                    <sld:Title>Label</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>301</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>600</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                   <sld:MaxScaleDenominator>00000</sld:MaxScaleDenominator>
                    <sld:TextSymbolizer>
                      <sld:Label>
                        &lt;-- MSG, Hotspot Intensity: High
                      </sld:Label>
                      <sld:Halo>
                        <sld:Radius>2</sld:Radius>
                      </sld:Halo>
                    </sld:TextSymbolizer>
                </sld:Rule>
                <sld:Rule>
                    <sld:Name>rule04</sld:Name>
                    <sld:Title>Extreme Intensity Fire</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>601</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>50000</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <sld:MinScaleDenominator>2000000</sld:MinScaleDenominator>
                    <sld:PointSymbolizer>
                        <sld:Graphic>
                            <sld:Mark>
                                <sld:WellKnownName>circle</sld:WellKnownName>
                                <sld:Fill>
                                    <sld:CssParameter name="fill">
                                        <ogc:Literal>#ff0000</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="fill-opacity">
                                        <ogc:Literal>0.85</ogc:Literal>
                                    </sld:CssParameter>
                                </sld:Fill>
                                <sld:Stroke>
                                    <sld:CssParameter name="stroke">
                                        <ogc:Literal>#000000</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-linecap">
                                        <ogc:Literal>butt</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-linejoin">
                                        <ogc:Literal>miter</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-opacity">
                                        <ogc:Literal>0</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-width">
                                        <ogc:Literal>0.5</ogc:Literal>
                                    </sld:CssParameter>
                                    <sld:CssParameter name="stroke-dashoffset">
                                        <ogc:Literal>0.0</ogc:Literal>
                                    </sld:CssParameter>
                                </sld:Stroke>
                            </sld:Mark>
                            <sld:Opacity>
                                <ogc:Literal>0.85</ogc:Literal>
                            </sld:Opacity>
                            <sld:Size>
                                <ogc:Literal>10</ogc:Literal>
                            </sld:Size>
                            <sld:Rotation>
                                <ogc:Literal>0.0</ogc:Literal>
                            </sld:Rotation>
                        </sld:Graphic>
                    </sld:PointSymbolizer>
                </sld:Rule>                
                <sld:Rule>
                    <sld:Name>rule04a</sld:Name>
                    <sld:Title>Extreme Intensity Pixel</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>601</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>50000</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                    <sld:MaxScaleDenominator>2000000</sld:MaxScaleDenominator>
                    <PolygonSymbolizer>
                        <Geometry>
                           <ogc:Function name="buffer">
                             <ogc:Function name="centroid">
                                <ogc:PropertyName>point</ogc:PropertyName>
                             </ogc:Function>
                             <ogc:Literal>0.015</ogc:Literal>
                           </ogc:Function>
                        </Geometry>
                        <sld:Fill>
                            <sld:CssParameter name="fill">
                                <ogc:Literal>#ff0000</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="fill-opacity">
                                <ogc:Literal>0.85</ogc:Literal>
                            </sld:CssParameter>
                        </sld:Fill>
                        <sld:Stroke>
                            <sld:CssParameter name="stroke">
                                <ogc:Literal>#000000</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-linecap">
                                <ogc:Literal>butt</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-linejoin">
                                <ogc:Literal>miter</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-opacity">
                                <ogc:Literal>0</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-width">
                                <ogc:Literal>0.5</ogc:Literal>
                            </sld:CssParameter>
                            <sld:CssParameter name="stroke-dashoffset">
                                <ogc:Literal>0.0</ogc:Literal>
                            </sld:CssParameter>
                        </sld:Stroke>
                      </PolygonSymbolizer>
                </sld:Rule> 
                 <sld:Rule>
                    <sld:Name>rule04b</sld:Name>
                    <sld:Title>Label</sld:Title>
                    <sld:Abstract>Abstract</sld:Abstract>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>601</ogc:Literal>
                            </ogc:PropertyIsGreaterThanOrEqualTo>
                            <ogc:PropertyIsLessThanOrEqualTo>
                                <ogc:PropertyName>frp</ogc:PropertyName>
                                <ogc:Literal>50000</ogc:Literal>
                            </ogc:PropertyIsLessThanOrEqualTo>
                        </ogc:And>
                    </ogc:Filter>
                   <sld:MaxScaleDenominator>00000</sld:MaxScaleDenominator>
                    <sld:TextSymbolizer>
                      <sld:Label>
                        &lt;-- MSG, Hotspot Intensity: Extreme
                      </sld:Label>
                      <sld:Halo>
                        <sld:Radius>2</sld:Radius>
                      </sld:Halo>
                    </sld:TextSymbolizer>
                </sld:Rule>
            </sld:FeatureTypeStyle>
        </sld:UserStyle>
       </sld:UserLayer> 
</sld:StyledLayerDescriptor>
