import os
from django.conf import settings

#from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# for reflection
from django.contrib.contenttypes.models import ContentType

#rvddool 20121116 single signon common models (you will need to run ../update_common_models.sh for any change in the relevant database tables)
from common.models import *
from django.contrib.gis.db import models


# for caching fire stats and legend images
import urllib
# for datetime handling
import datetime
import logging
import re

class ImageFormat( models.Model ):
  name = models.CharField( max_length=30 )
  mime_type = models.CharField( max_length=30 )

  class Meta:
    db_table=("imageformat")
    verbose_name=_("Image Format")
    verbose_name_plural=_("Image Formats")

  def __unicode__( self ):
    return self.name

class Sensor( models.Model ):
  name = models.CharField( max_length=30 )
  description = models.TextField( )
  # layer e.g. 'openafis:MSG Active Fires Pixels Archive';
  layer = models.CharField('WMS Sublayer name for this sensor', max_length=255 )
  style = models.CharField('WMS Style name for this sensor', default='point', max_length=255 )

  class Meta:
    db_table=("sensor")
    verbose_name=_("Sensor")
    verbose_name_plural=_("Sensors")

  def __unicode__( self ):
    return self.name


class Layer( models.Model ):
  """This is an ABC (Abstract Base Class) for all models that are layers.
  It provides common api so that all layers can be treated in a similar way."""
  name = models.CharField( max_length=256,
      help_text="A short, descriptive name for this layer. Required." )
  description = models.TextField( null=True, blank=True,
      help_text="A free text description for this layer. Not required.")
  owner = models.ForeignKey( User, related_name = 'owner', default=User.objects.get(username="anonymous"),
      help_text="Owner for this layer. Set to anonymous for non logged in users to see it.")
  min_scale = models.IntegerField( null=True, blank=True, default=80000000,
      help_text="Minimum scale at which is layer is visible.  Defaults to 1:80million"  )
  max_scale = models.IntegerField( null=True, blank=True, default=1,
      help_text="Maximum scale at which is layer is visible.  Defaults to 1:1"  )
  # overridden by UserWmsLayer.is_visible - can be dropped
  is_visible = models.NullBooleanField( null=True, blank=True, default=False )
  #for reflection when we want to know what subclass created this instance
  content_type = models.ForeignKey(ContentType,editable=False,null=True)
  # store the javascript as *field*, instead of generating it on-the-fly
  as_open_layer = models.TextField( )



  def save(self):
    """Save the class type whenever saving so that we can use reflection
       to get back to it later given just a layer object.
       see:
       http://stackoverflow.com/questions/349206/how-do-i-find-the-concrete-class-of-a-django-model-baseclass """
    if(not self.content_type):
      self.content_type = ContentType.objects.get_for_model( self.__class__ )
    self.save_base()

  def asConcreteClass(self):
    """Use reflection to get back an instance of the concrete (sub)class that
       created this layer instance
       see:
       http://stackoverflow.com/questions/349206/how-do-i-find-the-concrete-class-of-a-django-model-baseclass """
    content_type = self.content_type
    model = content_type.model_class()
    if( model == Layer ):
      return self
    return model.objects.get(id=self.id)

  def asOpenLayer( self ):
    """This is a work around for the fact that in templates one cannot do:
    myLayer.asConcreteClass.asOpenLayer
    since it seems to be that you cant call methods on objects returned from methods...."""
    return self.asConcreteClass().asOpenLayer()

  def asLegend( self ):
    """This is a work around for the fact that in templates one cannot do:
    myLayer.asConcreteClass.asLegend
    since it seems to be that you cant call methods on objects returned from methods...."""
    return self.asConcreteClass().asLegend()

  def visibilityAsString( self ):
    myVisibility = None
    if self.is_visible:
      myVisibility = "true"
    else:
      myVisibility = "false"
    return myVisibility

  def layerName( self ):
    """Return the name of the layer as given to open layers. Also ensure that the name
    is a valid javascript variable name e.g. doesnt start with [0-9] numeric"""
    myName = "lyr" + str( self.id )
    return myName

  def layerShortName( self ):
    """Return an elided (shortened and terminated with ellipsis) name of the layer for use in legend"""
    myName = self.name #[0:20]+"..." #disabled for now on request from Graeme
    return myName


  def asLegend( self ):
    """Return a legend graphic image for this model
       Abstract method to be reimplemented by child class"""
    return ""

  def asOpenLayer( self ):
    """Return an openlayer layer definition for this model
       Abstract method to be reimplemented by child class"""
    return ""

  class Meta:
    abstract = True

  def __unicode__( self ):
    return self.name

class RasterLegend( models.Model ):
  name = models.CharField( max_length = 100 )  
  description = models.CharField( max_length = 500 )
  class Meta:
    db_table=("raster_legend")
    verbose_name=_("RasterLegend")
    verbose_name_plural=_("RasterLegends")

class RasterLegendItem( models.Model ):
  description = models.CharField( max_length = 500 )
  rgb = models.CharField( max_length = 6 )
  legend = models.ForeignKey( RasterLegend ) 
  value = models.IntegerField()

  class Meta:
    db_table=("raster_legend_item")
    verbose_name=_("RasterLegendItem")
    verbose_name_plural=_("RasterLegendsItems")

class LegendGroup( models.Model ):
  title = models.CharField( max_length = 100 )
  description = models.CharField( max_length = 500, null = True )
  order = models.IntegerField( default = 1)
  class Meta:
    db_table=("legend_group")
    verbose_name=_("LegendGroup")
    verbose_name_plural=_("LegendGroups")


class WmsLayer( Layer ):
  url = models.URLField( max_length=1024, verify_exists=True ) #change to true on prod site
  layers = models.CharField( max_length=256 )
  image_format = models.ForeignKey( ImageFormat )
  is_base_layer = models.NullBooleanField( null=True, blank=True, default=False )
  is_transparent = models.NullBooleanField( null=True, blank=True, default=False )
  # link to user-layer model to keep status of legend
  users = models.ManyToManyField(User, through='UserWmsLayer')
  show_legend_image = models.BooleanField( default=True )
  legend_style = models.CharField( max_length=100, null=True, blank=True )
  raster_legend = models.ForeignKey( RasterLegend, null=True, blank=True )
  legend_group = models.ForeignKey( LegendGroup, default=0, null=False, blank=False )

  class Meta:
    db_table=("wmslayer")
    verbose_name=_("WMS Layer")
    verbose_name_plural=_("WMS Layers")

  def save( self, *args, **kwargs ):
    """ Overrides standard save, generating the asOpenLayers javascript. """
    # save once to get a valid id
    super(WmsLayer, self).save( *args, **kwargs)
    # which is used when generating openlayer string
    self.as_open_layer = self.asOpenLayer()
    # then save again to save the ol string
    super(WmsLayer, self).save( *args, **kwargs)

  def baseLayerAsString( self ):
    myBaseLayer = None
    if self.is_visible:
      myBaseLayer = "true"
    else:
      myBaseLayer = "false"
    return myBaseLayer

  def transparencyAsString( self ):
    myTransparency = None
    if self.is_transparent:
      myTransparency = "true"
    else:
      myTransparency = "false"
    return myTransparency

  def asLegend( self ):
    """ Return a legend graphic image for this model from the cache directory. If it is empty it makes a wms request and populates the directory. """
    myFileName = str(self.id) + "." + str(self.image_format)

    myLocalPath = os.path.join( settings.LEGEND_IMAGE_ROOT, myFileName )
    myWebPath = os.path.join( settings.LEGEND_IMAGE_URL, myFileName )

    if not os.path.exists( myLocalPath ):
      logging.info('Get Legend Graphic not cached...fetching....')
      # the image is not into the expected dir, get it from WMS request..
      '''
      if (not self.legend_style is None) and (self.legend_style != ''):
         myFetchUrl = """%s?request=GetLegendGraphic&style=%s&version=1.0.0&format=image/png&width=20&height=20&layer=%s""" % ( self.url, self.legend_style, self.layers )
      else:
         myFetchUrl = """%s?request=GetLegendGraphic&version=1.0.0&format=image/png&width=20&height=20&layer=%s""" % ( self.url, self.layers )
      '''
      if re.search('\?', self.url):
        question_mark = '&'
      else:
        question_mark = '?'
      myFetchUrl = """%s%srequest=GetLegendGraphic&version=1.0.0&format=image/png&width=20&height=20&layer=%s""" % ( self.url, question_mark, self.layers )
      if (not self.legend_style is None) and (self.legend_style != ''):
        myFetchUrl += r'&style='+self.legend_style
      # .. and store into filesystem
      logging.debug('GET %s -> %s' % (myFetchUrl, myLocalPath))
      urllib.urlretrieve(myFetchUrl, myLocalPath)
    else:
      logging.info('Using cached LegendGraphic %s' % myLocalPath)

    myUrl = """<img src="%s" id="legend-image-%s" class="legend-image"/>""" % ( myWebPath, self.id )
    return myUrl

  def asOpenLayer( self ):
    """Return a string representation of this model as an open layers
    layer definition. The created layer def will be added
    to the openlayers map of name theMap (which defaults to "map". """

    myMaxScale = 1
    if ( self.max_scale ) : myMaxScale = self.max_scale
    myMinScale = 38000000
    if ( self.min_scale ) : myMinScale = self.min_scale
    myLayerDef = """%s = new OpenLayers.Layer.WMS(
        '%s','%s',
        {
          layers: '%s',
          transparent: '%s',
          format: '%s'
        },
        {
          minScale: %s,
          maxScale: %s
        },
        {
          isBaseLayer: %s
        }
      );
      gLayersDict[%s.id] = '%s'; 
      """ % ( "lyr" + str( self.id ),
              self.name.replace("'",""),
              self.url,
              self.layers,
              self.transparencyAsString(),
              self.image_format.mime_type,
              str( myMinScale ),
              str( myMaxScale ),
              self.baseLayerAsString(),
              "lyr" + str( self.id ),
              "lyr" + str( self.id )
              )

    return myLayerDef

class DateQueryLayer( WmsLayer ):
  """A layer model for storing user date range queries persistently"""
  sensor = models.ForeignKey( Sensor )
  start_date = models.DateTimeField( null=True, blank=True )
  end_date = models.DateTimeField( null=True, blank=True )

  class Meta:
    db_table=("datequerylayer")
    verbose_name=_("Date Query Layer")
    verbose_name_plural=_("Date Query Layers")


  def save( self, *args, **kwargs ):
    """ Overrides standard save, generating the asOpenLayers javascript. """
    # save once to get a valid id
    super(DateQueryLayer, self).save( *args, **kwargs)
    # which is used when generating openlayer string
    self.as_open_layer = self.asOpenLayer()
    # then save again to save the ol string
    super(DateQueryLayer, self).save( *args, **kwargs)


  def asOpenLayer( self ):
    """Return a string representation of this model as an open layers
    layer definition. The created layer def will be added
    to the openlayers map of name theMap (which defaults to "map". """

    myMaxScale = 1
    if ( self.max_scale ) : myMaxScale = self.max_scale
    myMinScale = 38000000
    if ( self.min_scale ) : myMinScale = self.min_scale
    myLayerDef = """%s = new OpenLayers.Layer.WMS(
        '%s','%s',
        {
          layers: '%s',
          transparent: '%s',
          format: '%s',
          filter: '<Filter><PropertyIsBetween><PropertyName>acqdatetime</PropertyName><LowerBoundary><Literal>%s</Literal></LowerBoundary><UpperBoundary><Literal>%s</Literal></UpperBoundary></PropertyIsBetween></Filter>'
        },
        {
          minScale: %s,
          maxScale: %s
        },
        {
          isBaseLayer: %s
        }
      );
    gLayersDict[%s.id] = '%s'; 
    
    """ % ("lyr" + str( self.id ),
              self.name.replace("'",""),
              self.url,
              self.layers,
              self.transparencyAsString(),
              self.image_format.mime_type,
              self.start_date.isoformat(), # aka LowerBoundary
              self.end_date.isoformat(), # aka UpperBoundary
              str( myMinScale ),
              str( myMaxScale ),
              self.baseLayerAsString(),
              "lyr" + str( self.id ),
              "lyr" + str( self.id )
              )
    return myLayerDef

class PlaceName(models.Model):
  name = models.CharField( max_length=256 )
  position = models.PointField( srid=4326, null=True, blank=True )
  objects = models.GeoManager()

  class Meta:
    db_table=("placename")
    verbose_name=_("Place Name")
    verbose_name_plural=_("Place Names")

  def __unicode__( self ):
    return self.name

class FireStats( models.Model ):
  """ Stores the fire status for moment in time. """
  date = models.DateTimeField(verbose_name="Date", auto_now=True, auto_now_add=True, help_text = "Not shown to users")
  last_48_hours = models.IntegerField( null=True, blank=True )
  last_24_hours = models.IntegerField( null=True, blank=True )

  class Meta:
    db_table=("firestats")
    verbose_name=_("Fire Statistics")
    verbose_name_plural=_("FireStatistics")


class UserWmsLayer( models.Model ):
  """ Stores custom user preferences for a layer. It's a many-to-many relationship between WmsLayer and User. """
  wmslayer = models.ForeignKey( WmsLayer )
  user = models.ForeignKey( User , default=User.objects.get(username="anonymous") )
  is_visible = models.NullBooleanField( null=True, blank=True, default=True )
  # boolean flag - users will flag what they won't see anymore but layers remain in the list
  is_deleted = models.NullBooleanField( null=True, blank=True, default=False )
  has_access = models.BooleanField( null=False, blank=False, default=True )
  order = models.IntegerField( blank=True, default=0 )
  is_default = models.NullBooleanField( null=True, blank=True, default=False,
          help_text="Whether this layer should be assigned as a default layer for all new users. The layer must be owned by anonymous too" )
  deleted_timestamp = models.DateTimeField( null=True, blank=True, default=None )  
  
  class Meta:
    db_table=("userwmslayer")
    verbose_name=_("User Wms Layer")
    verbose_name_plural=_("User Wms Layers")
    ordering = ['order']

