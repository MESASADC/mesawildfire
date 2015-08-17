
from mesa.rest.models import AfModis
from mesa.rest.serializers import AfModisSerializer 
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

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



    
