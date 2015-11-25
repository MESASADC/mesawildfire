from django.contrib.gis import admin
from models import *

class ImageFormatAdmin(admin.ModelAdmin):
    list_display = ('name','mime_type', )
    list_filter = ('name', )
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', )
class PlaceNameAdmin(admin.GeoModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
class WmsLayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_visible', 'is_base_layer', 'is_transparent', 'owner', )
    list_filter = ('is_visible', 'is_base_layer', 'is_transparent', )
    exclude = ( 'as_open_layer', )
class DateQueryLayerAdmin(admin.ModelAdmin):
    list_display = ('sensor','name', 'is_visible', 'is_base_layer', 'is_transparent', 'owner', )
    list_filter = ('is_visible', 'is_base_layer', 'is_transparent', )
    exclude = ( 'as_open_layer', )
class UserWmsLayerAdmin(admin.ModelAdmin):
    list_display = ('user','wmslayer','is_visible','is_deleted','order', 'is_default', )
    list_filter = ('is_visible','is_deleted', )

admin.site.register(ImageFormat, ImageFormatAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(PlaceName, PlaceNameAdmin)
admin.site.register(WmsLayer, WmsLayerAdmin)
admin.site.register(DateQueryLayer, DateQueryLayerAdmin)
admin.site.register(UserWmsLayer, UserWmsLayerAdmin)
