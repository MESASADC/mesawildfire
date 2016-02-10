<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   
  <NamedLayer>
    <Name>polygon_border</Name>
    <UserStyle>
        <!-- they have names, titles and abstracts -->
      
      <Title>A boring default style</Title>
      <Abstract>A sample style that just prints out a transparent red interior with a red outline</Abstract>
      <!-- FeatureTypeStyles describe how to render different features -->
      <!-- a feature type for polygons -->

      <FeatureTypeStyle>
        <!--FeatureTypeName>Feature</FeatureTypeName-->
        <Rule>
          <Name>Rule 1</Name>
          <Title>Outline</Title>
          <Abstract>outline 1 pixel in width</Abstract>

          <!-- like a linesymbolizer but with a fill too -->
          <PolygonSymbolizer>
            <Stroke>
              <CssParameter name="stroke">#000000</CssParameter>
              <CssParameter name="stroke-width">1</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
          
          <sld:TextSymbolizer>
   <sld:Label>
     <ogc:PropertyName>NAME</ogc:PropertyName>
   </sld:Label>
   <sld:Font>
     <sld:CssParameter name="font-family">Arial</sld:CssParameter>
     <sld:CssParameter name="font-size">16.0</sld:CssParameter>
     <sld:CssParameter name="font-style">normal</sld:CssParameter>
     <sld:CssParameter name="font-weight">normal</sld:CssParameter>
   </sld:Font>
   <sld:LabelPlacement>
     <sld:PointPlacement>
       <sld:AnchorPoint>
         <sld:AnchorPointX>
           <ogc:Literal>0.5</ogc:Literal>
         </sld:AnchorPointX>
         <sld:AnchorPointY>
           <ogc:Literal>1.0</ogc:Literal>
         </sld:AnchorPointY>
       </sld:AnchorPoint>
       <sld:Displacement>
         <sld:DisplacementX>
           <ogc:Literal>0.0</ogc:Literal>
         </sld:DisplacementX>
         <sld:DisplacementY>
           <ogc:Literal>-10.0</ogc:Literal>
         </sld:DisplacementY>
       </sld:Displacement>
       <sld:Rotation>
         <ogc:Literal>0.0</ogc:Literal>
       </sld:Rotation>
     </sld:PointPlacement>
   </sld:LabelPlacement>
   <sld:Halo>
     <sld:Radius>
       <ogc:Literal>1.5</ogc:Literal>
     </sld:Radius>
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
        </Rule>

        </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
