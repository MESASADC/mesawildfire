from django.forms import widgets
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from mesa.rest.models import AfModis

class AfModisSerializer(GeoFeatureModelSerializer):
    """ A class to serialize MODIS active fire locations as GeoJSON compatible data """

    class Meta:
        model = AfModis
        geo_field = "point"


'''
class AfModisSerializer(serializers.Serializer):
    
    pk = serializers.IntegerField(read_only=True)
    type = serializers.CharField(required=False, allow_blank=True, max_length=100)
    geom = serializers.PointField()
    lon = serializers.DecimalField()
    lat = serializers.DecimalField()
    date_time = serializers.DateTimeField(blank=True, null=True)
    src = serializers.CharField(blank=True, default='')
    sat = serializers.CharField(blank=True, default='')
    frp = serializers.DecimalField()
    btemp = serializers.DecimalField()

    def create(self, validated_data):
        """
        Create and return a new AfModis instance
        """
        return AfModis(**validated_data)
        
    def update(self, instance, validated_data):
        """
        Update and return an AfModis instance
        """
        instance.type = validated_data.get('type', instance.type)     
        instance.geom = validated_data.get('geom', instance.geom)
        instance.lon = validated_data.get('lon', instance.lon)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.date_time = validated_data.get('date_time', instance.date_time)
        instance.src = validated_data.get('src', instance.src)
        instance.sat = validated_data.get('sat', instance.sat)
        instance.frp = validated_data.get('frp', instance.frp)
        instance.btemp = validated_data.get('btemp', instance.btemp)
        instance.save()
        return instance
        
    
        
'''
