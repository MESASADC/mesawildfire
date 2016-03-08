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
               <sld:TextSymbolizer>
                  <sld:Label>
                     <ogc:PropertyName>name</ogc:PropertyName>
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
              <Rule>
					<Name>Rule 1</Name>
					<Title>RedSquare</Title>
					<Abstract>A red fill with an 11 pixel size</Abstract>

					<!-- like a linesymbolizer but with a fill too -->
					<PointSymbolizer>
						<Graphic>
							<Mark>
								<WellKnownName>circle</WellKnownName>
								<Fill>
									<CssParameter name="fill">#FFFFFF</CssParameter>
									<CssParameter name="stroke-color">#000000</CssParameter>
								</Fill>
							</Mark>
							<Size>6</Size>
						</Graphic>
					</PointSymbolizer>
				</Rule>
         </sld:FeatureTypeStyle>
      </sld:UserStyle>
   </sld:NamedLayer>
</sld:StyledLayerDescriptor>
