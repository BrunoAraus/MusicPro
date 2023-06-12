from urllib import response
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from core.models import Producto
from .serializers import ProductoSerializer
#mapa
from django.shortcuts import render
from django.conf import settings






@api_view(['GET', 'POST'])
def lista_prod(request):
    if request.method == 'GET':
        sus = Producto.objects.all()
        serializer = ProductoSerializer(sus, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def detalle_prod(request, id):
    try:
        sus = Producto.objects.get(id=id)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductoSerializer(sus)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductoSerializer(sus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        sus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









def mapa(request):
    context = {
    'api_key' : 'AIzaSyB2tWManwQ46akf6zW_YTNDTSY9Zf2hTbI'
    }
    return render(request, 'mapa.html', context)

# API GOOGLE MAP
#CLAVE DE LA API: AIzaSyB2tWManwQ46akf6zW_YTNDTSY9Zf2hTbI
#from pprint import pprint
#import googlemaps # pip instal googlemaps
#api_key = 'AIzaSyB2tWManwQ46akf6zW_YTNDTSY9Zf2hTbI'

#map_client = googlemaps.Client(api_key)
#work_place_address = 'DuocUC, melipilla'
#response = map_client.geocode(work_place_address)
#pprint(response)
#print(response[0]['geometry'])



