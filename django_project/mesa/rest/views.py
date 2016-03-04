
from mesa import models 
from django.db.models import Max
from mesa.rest import serializers 
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from datetime import datetime, timedelta

class ConfigViewSet(viewsets.ModelViewSet):
    """
    Configuration settings
    """
    queryset = models.ConfigSetting.objects.all()
    serializer_class = serializers.ConfigSerializer
    #permission_classes = [permissions.DjangoModelPermissions]
    

class FdiPointViewSet(viewsets.ModelViewSet):
    """
    Points of interest for Fire Danger Index, can be weather station or just a location
    """
    queryset = models.FdiPoint.objects.all()
    serializer_class = serializers.FdiPointSerializer


class FdiGraphDataViewSet(viewsets.ModelViewSet):
    """
    Fdi Graph data 
    """
    queryset = models.FdiGraphData.objects.all()
    serializer_class = serializers.FdiGraphDataSerializer


class FdiMeasurementViewSet(viewsets.ModelViewSet):
    """
    Fire Danger Index as calculated from weatherstation measurements
    """
    queryset = models.FdiMeasurement.objects.all()
    serializer_class = serializers.FdiMeasurementSerializer


class FirePixelViewSet(viewsets.ModelViewSet):
    """
    Active fire pixels as detected by satellite
    """
    queryset = models.FirePixel.objects.all()
    serializer_class = serializers.FirePixelSerializer

''' 
class FireFeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Fire features
    """
    queryset = models.FireFeature.objects.all()
    serializer_class = serializers.FireFeatureSerializer
'''

class FireEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Fire as detected and updated over time
    """
    queryset = models.FireEvent.objects.none()
    serializer_class = serializers.FireEventSerializer
    
    #def get_queryset(self):
    #    return models.FireEvent.objects.filter(last_seen__gte=datetime.today()-timedelta(days=6))

