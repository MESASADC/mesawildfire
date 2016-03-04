from django.forms import widgets
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers, filters
from rest_framework.validators import UniqueValidator


from mesa import models

class FirePixelSerializer(GeoFeatureModelSerializer):
    """ A class to serialize active fire pixels as GeoJSON compatible data """
            
    class Meta:
        model = models.FirePixel
        geo_field = "point"

class FireEventSerializer(GeoFeatureModelSerializer):
    """ A class to serialize fires for an event table """
            
    class Meta:
        model = models.FireEvent
        geo_field = "border"

class FdiPointSerializer(GeoFeatureModelSerializer):
    """ A class to serialize FDI points of interest as GeoJSON compatible data """
            
    class Meta:
        model = models.FdiPoint
        geo_field = "point"
        fields = ('name', 'id', 'url', 'type', 'point', 'lat', 'lon', 'station_id', 'station_name')

class FdiMeasurementSerializer(ModelSerializer):
    """ A class to serialize FDI points of interest as GeoJSON compatible data """
            
    class Meta:
        model = models.FdiMeasurement

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('date_time')
    ordering = ('date_time',)


class FdiGraphDataSerializer(ModelSerializer):
    """ A class to serialize FDI graph data as JSON compatible data """
            
    class Meta:
        model = models.FdiGraphData

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('date_time')
    ordering = ('date_time',)



class ConfigSerializer(ModelSerializer):
    
    class Meta:
        model = models.ConfigSetting

    def validate(self, data):
        
        # Null values are allowed
        if data['value'] is None:
            return data
        
        # Check float or int is numeric and that int is not float
        if data['type'] in ('float', 'int'):
            try:
                f = float(data['value'])
            except:
                raise serializers.ValidationError({'value': ['Value must be numeric.'], 'type': ['Value type does not match.']})
            else:
                if data['type'] == 'int':
                    if not f.is_integer():
                        raise serializers.ValidationError({'value': ['Value must be an integer.'], 'type': ['Value type does not match.']})

        try:
            unicode(data['value'])
        except:
            raise serializers.ValidationError({'value': ['Failed to store the value as string.']})
        
        return data
            

