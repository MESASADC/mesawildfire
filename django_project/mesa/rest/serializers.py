from django.forms import widgets
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from mesa.models import ConfigSetting, AfModis, FdiPoint, FdiMeasurement, FdiForecast, FdiTable, Fire


class AfModisSerializer(GeoFeatureModelSerializer):
    """ A class to serialize MODIS active fire locations as GeoJSON compatible data """
            
    class Meta:
        model = AfModis
        geo_field = "point"

class FireSerializer(GeoFeatureModelSerializer):
    """ A class to serialize fires as GeoJSON compatible data """
            
    class Meta:
        model = Fire
        geo_field = "geom"

class FdiPointSerializer(GeoFeatureModelSerializer):
    """ A class to serialize FDI points of interest as GeoJSON compatible data """
            
    class Meta:
        model = FdiPoint
        geo_field = "point"
        fields = ('name', 'id', 'url', 'type', 'point', 'lat', 'lon', 'station_id', 'station_name')

class FdiMeasurementSerializer(ModelSerializer):
    """ A class to serialize FDI points of interest as GeoJSON compatible data """
            
    class Meta:
        model = FdiMeasurement


class FdiForecastSerializer(ModelSerializer):
    """ A class to serialize FDI points of interest as GeoJSON compatible data """
            
    class Meta:
        model = FdiForecast

class FdiTableSerializer(GeoFeatureModelSerializer):
    """ A class to serialize FDI table data as GeoJSON compatible data """
            
    class Meta:
        model = FdiTable
        geo_field = "point"



class ConfigSerializer(ModelSerializer):
    
    class Meta:
        model = ConfigSetting

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
            

