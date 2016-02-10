<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns:sld="http://www.opengis.net/sld" xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
   <sld:NamedLayer>
      <sld:Name>point_text</sld:Name>
      <sld:UserStyle>
         <sld:Name>point_text</sld:Name>
         <sld:Title>A boring default style</sld:Title>
         <sld:Abstract>A sample style that just prints out a purple square</sld:Abstract>
         <sld:FeatureTypeStyle>
            <sld:Name>name</sld:Name>
            <sld:Rule>
               <sld:Name>Rule 1</sld:Name>
               <sld:Title>Text</sld:Title>
               <sld:Abstract>Text style</sld:Abstract>
               <sld:TextSymbolizer>
                  <sld:Label>
                     <ogc:PropertyName>NAME</ogc:PropertyName>
                  </sld:Label>
                  <sld:Font>
                     <sld:CssParameter name="font-family">Arial</sld:CssParameter>
                     <sld:CssParameter name="font-size">12.0</sld:CssParameter>
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
                           <sld:DisplacementY>-10.0</sld:DisplacementY>
                        </sld:Displacement>
                     </sld:PointPlacement>
                  </sld:LabelPlacement>
                  <sld:Halo>
                     <sld:Radius>1.5</sld:Radius>
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

