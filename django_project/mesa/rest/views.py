
from mesa.models import ConfigSetting, AfModis, FdiPoint, FdiMeasurement, FdiForecast, FdiTable
from mesa.rest.serializers import ConfigSerializer, AfModisSerializer, FdiPointSerializer, FdiMeasurementSerializer, FdiForecastSerializer, FdiTableSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets


    

class ConfigViewSet(viewsets.ModelViewSet):
    """
    Configuration settings
    """
    queryset = ConfigSetting.objects.all()
    serializer_class = ConfigSerializer
    #permission_classes = [permissions.DjangoModelPermissions]
    

class FdiPointViewSet(viewsets.ModelViewSet):
    """
    Points of interest for Fire Danger Index, can be weather station or just a location
    """
    queryset = FdiPoint.objects.all()
    serializer_class = FdiPointSerializer

class FdiTableViewSet(viewsets.ModelViewSet):
    """
    FdiTable data for Fire Danger Index, can be weather station or just a location
    """
    queryset = FdiTable.objects.all()
    serializer_class = FdiTableSerializer


class FdiMeasurementViewSet(viewsets.ModelViewSet):
    """
    Fire Danger Index as calculated from weatherstation measurements
    """
    queryset = FdiMeasurement.objects.all()
    serializer_class = FdiMeasurementSerializer

class FdiForecastViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Fire Danger Index as calculated from weather forecast model data
    """
    queryset = FdiForecast.objects.all()
    serializer_class = FdiForecastSerializer



class AfModisList(generics.ListCreateAPIView):
    queryset = AfModis.objects.all()
    serializer_class = AfModisSerializer


class AfModisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AfModis.objects.all()
    serializer_class = AfModisSerializer


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'af_modis': reverse('af_modis-list', request=request, format=format),
        'config': reverse('config', request=request, format=format),
    })


'''
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST']):
def af_modis_list(request):
    """
    List all AfModis objects, or create one
    """
    if request.method == 'GET':
        records = AfModis.objects.all()
        serializer = AfModisSerializer(records, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AfModisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE']):
def af_modis_detail(request, pk):
    """
    Retrieve, update or delete an AfModis object
    """
    try:
        record = AfModis.objects.get(pk=pk)
    except AfModis.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = AfModisSerializer(record)
        return Respose(serializer.data)
    elif request.method == 'PUT':
        serializer = AfModisSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
'''



    
