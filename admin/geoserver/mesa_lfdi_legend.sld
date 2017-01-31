<?xml version="1.0" ?>
<sld:StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld">
    <sld:UserLayer>
        <sld:LayerFeatureConstraints>
            <sld:FeatureTypeConstraint/>
        </sld:LayerFeatureConstraints>
        <sld:UserStyle>
            <sld:Name>mesa_lfdi_legend</sld:Name>
            <sld:Title/>
            <sld:FeatureTypeStyle>
                <sld:Name/>
                <sld:Rule>
                    <sld:RasterSymbolizer>
                        <sld:Geometry>
                            <ogc:PropertyName>grid</ogc:PropertyName>
                        </sld:Geometry>
                        <sld:Opacity>1</sld:Opacity>
                        <sld:ColorMap type="intervals">
                            <sld:ColorMapEntry color="#0000ff" label="FDI > 0" opacity="1.0" quantity="0"/>
                            <sld:ColorMapEntry color="#00ff00" label="FDI > 20" opacity="1.0" quantity="20"/>
                            <sld:ColorMapEntry color="#ffff00" label="FDI > 40" opacity="1.0" quantity="40"/>
                            <sld:ColorMapEntry color="#ffa500" label="FDI > 60" opacity="1.0" quantity="60"/>
                            <sld:ColorMapEntry color="#ff0000" label="FDI > 75" opacity="1.0" quantity="75"/>
                        </sld:ColorMap>
                    </sld:RasterSymbolizer>
                </sld:Rule>
            </sld:FeatureTypeStyle>
        </sld:UserStyle>
    </sld:UserLayer>
</sld:StyledLayerDescriptor>
