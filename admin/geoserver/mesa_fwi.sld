<?xml version="1.0" ?>
<sld:StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld">
    <sld:UserLayer>
        <sld:LayerFeatureConstraints>
            <sld:FeatureTypeConstraint/>
        </sld:LayerFeatureConstraints>
        <sld:UserStyle>
            <sld:Name>mesa_fwi</sld:Name>
            <sld:Title/>
            <sld:FeatureTypeStyle>
                <sld:Name/>
                <sld:Rule>
                    <sld:RasterSymbolizer>
                        <sld:Geometry>
                            <ogc:PropertyName>grid</ogc:PropertyName>
                        </sld:Geometry>
                        <sld:Opacity>1</sld:Opacity>
                        <sld:ColorMap >
                            <sld:ColorMapEntry color="#FFFFFF" label="" opacity="0.0" quantity="0.0"/>
                            <sld:ColorMapEntry color="#0000ff" label="0-20" opacity="1.0" quantity="0"/>
                            <sld:ColorMapEntry color="#00ff00" label="20-45" opacity="1.0" quantity="20"/>
                            <sld:ColorMapEntry color="#ffff00" label="45-59" opacity="1.0" quantity="45"/>
                            <sld:ColorMapEntry color="#ffa500" label="59-74" opacity="1.0" quantity="59"/>
                            <sld:ColorMapEntry color="#ff0000" label="74 &gt;" opacity="1.0" quantity="74"/>
                        </sld:ColorMap>
                    </sld:RasterSymbolizer>
                </sld:Rule>
            </sld:FeatureTypeStyle>
        </sld:UserStyle>
    </sld:UserLayer>
</sld:StyledLayerDescriptor>