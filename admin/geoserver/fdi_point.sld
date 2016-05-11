<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns:sld="http://www.opengis.net/sld" xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
    <sld:NamedLayer>
        <sld:Name>fdi_point</sld:Name>
        <sld:UserStyle>
            <sld:Name>fdi_point</sld:Name>
            <sld:Title>FDI Points</sld:Title>
            <sld:Abstract>FDI points can be weather stations</sld:Abstract>
            <sld:FeatureTypeStyle>
                <sld:Name>point_name</sld:Name>
                <sld:Rule>
                    <sld:Name>Is Weatherstation</sld:Name>
                    <sld:Title>Weather station</sld:Title>
                    <sld:Abstract>FDI point is a weather station</sld:Abstract>
                    <sld:MaxScaleDenominator>10000000</sld:MaxScaleDenominator>
                    <sld:PointSymbolizer>
                        <sld:Graphic>
                            <sld:Mark>
                                <sld:WellKnownName>circle</sld:WellKnownName>
                                <sld:Fill>
                                    <sld:CssParameter name="fill">#FFFFFF</sld:CssParameter>
                                </sld:Fill>
                                <sld:Stroke>
                                    <sld:CssParameter name="stroke">#000000</sld:CssParameter>
                                </sld:Stroke>
                            </sld:Mark>
                            <sld:Size>
                              <ogc:Function name="Categorize">
                                  <!-- Value to transform -->
                                  <ogc:Function name="env">
                                    <ogc:Literal>wms_scale_denominator</ogc:Literal>
                                  </ogc:Function>
                                  <ogc:Literal>18</ogc:Literal>
                                  <ogc:Literal>2000000</ogc:Literal>
                                  <ogc:Literal>10</ogc:Literal>
                                </ogc:Function>
                     </sld:Size>
                        </sld:Graphic>
                    </sld:PointSymbolizer>
                    <sld:TextSymbolizer>
                        <sld:Label>
                            <ogc:PropertyName>point_name</ogc:PropertyName>
                        </sld:Label>
                        <sld:Font>
                            <sld:CssParameter name="font-family">Arial</sld:CssParameter>
                            <CssParameter name="font-size">
                                <ogc:Function name="Categorize">
                                  <!-- Value to transform -->
                                  <ogc:Function name="env">
                                    <ogc:Literal>wms_scale_denominator</ogc:Literal>
                                  </ogc:Function>
                                  <ogc:Literal>20</ogc:Literal>
                                  <ogc:Literal>2000000</ogc:Literal>
                                  <ogc:Literal>12</ogc:Literal>
                                </ogc:Function>
                            </CssParameter>
                            <sld:CssParameter name="font-style">normal</sld:CssParameter>
                            <sld:CssParameter name="font-weight">normal</sld:CssParameter>
                        </sld:Font>
                        <sld:LabelPlacement>
                            <sld:PointPlacement>
                                <sld:AnchorPoint>
                                    <sld:AnchorPointX>0.5</sld:AnchorPointX>
                                    <sld:AnchorPointY>1.0</sld:AnchorPointY>
                                </sld:AnchorPoint>
                                <sld:Displacement>
                                    <sld:DisplacementX>0.0</sld:DisplacementX>
                                    <sld:DisplacementY>-12.0</sld:DisplacementY>
                                </sld:Displacement>
                            </sld:PointPlacement>
                        </sld:LabelPlacement>
                        <sld:Halo>
                            <sld:Radius>0.8</sld:Radius>
                            <sld:Fill>
                                <sld:CssParameter name="fill">#FFFFFF</sld:CssParameter>
                            </sld:Fill>
                        </sld:Halo>
                        <sld:Fill>
                            <sld:CssParameter name="fill">#000033</sld:CssParameter>
                        </sld:Fill>
                        <sld:Priority>200000</sld:Priority>
                        <sld:VendorOption name="autoWrap">100</sld:VendorOption>
                    </sld:TextSymbolizer>
                </sld:Rule>
            </sld:FeatureTypeStyle>
        </sld:UserStyle>
    </sld:NamedLayer>
</sld:StyledLayerDescriptor>
