<sld:StyledLayerDescriptor xmlns:sld="http://www.opengis.net/sld" xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
   <sld:NamedLayer>
      <sld:Name>firefeature</sld:Name>
      <sld:UserStyle>
         <sld:Name>firefeature</sld:Name>
         <sld:Title>A boring default style</sld:Title>
         <sld:Abstract>A sample style that just prints out a transparent red interior with a red outline</sld:Abstract>
         <sld:FeatureTypeStyle>
            <sld:Name>name</sld:Name>
            <sld:Rule>
               <sld:Name>Rule 1</sld:Name>
               <sld:Title>Fire event border</sld:Title>
               <sld:Abstract>10% transparent fill with an outline 1 pixel in width</sld:Abstract>
               <sld:PolygonSymbolizer>
                  <sld:Fill>
                     <sld:CssParameter name="fill">#FFFFFF</sld:CssParameter>
                     <sld:CssParameter name="fill-opacity">0.1</sld:CssParameter>
                  </sld:Fill>
                  <sld:Stroke>
                     <sld:CssParameter name="stroke-dasharray">5.0 2.0</sld:CssParameter>
                  </sld:Stroke>
               </sld:PolygonSymbolizer>
            </sld:Rule>
         </sld:FeatureTypeStyle>
      </sld:UserStyle>
   </sld:NamedLayer>
</sld:StyledLayerDescriptor>
