
from mesa import models 
from mesa.rest import serializers 
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets


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

class FdiPointDataViewSet(viewsets.ModelViewSet):
    """
    FdiTable data for Fire Danger Index, can be weather station or just a location
    """
    queryset = models.FdiPointData.objects.all()
    serializer_class = serializers.FdiPointDataSerializer


class FdiMeasurementViewSet(viewsets.ModelViewSet):
    """
    Fire Danger Index as calculated from weatherstation measurements
    """
    queryset = models.FdiMeasurement.objects.all()
    serializer_class = serializers.FdiMeasurementSerializer


class FdiForecastViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Fire Danger Index as calculated from weather forecast model data
    """
    queryset = models.FdiForecast.objects.all()
    serializer_class = serializers.FdiForecastSerializer


class FireViewSet(viewsets.ModelViewSet):
    """
    Fire as detected and updated over time
    """
    queryset = models.Fire.objects.all()
    serializer_class = serializers.FireSerializer


class FirePixelViewSet(viewsets.ModelViewSet):
    """
    Active fire pixels as detected by satellite
    """
    queryset = models.FirePixel.objects.all()
    serializer_class = serializers.FirePixelSerializer


