#Primero se realizan las importaciones 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Producto
from .serializers import ProductoSerializer
#mapa
from django.shortcuts import render
from django.conf import settings





#Aqui se Llama a Api_View que nos entrega un listado de metodos hppt que vamos a utilizar en la api

@api_view(['GET', 'POST'])
def lista_prod(request):     
    #Aqui llamamos a Lista_prod y preguntamos para saber si el metodo es get o post
    if request.method == 'GET':     
        #cuando el metodo es get se llama a todos los productos y se guardan en sus 
        sus = Producto.objects.all()   
        #luego se llama al serializer que es el encargado de definir los datos a entregar de los productos
        serializer = ProductoSerializer(sus, many=True) 
        return Response(serializer.data) # lo que nos retorna los datos requeridos
    elif request.method == 'POST':  
        # si es post se llama al serializer y se define el nuevo producto
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() #finalmente se guarda en el sistema 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#se vuelve a llamar a api_view

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_prod(request, id): #definimos detalle_prod y pedimos el id del producto
    try:
        sus = Producto.objects.get(id=id) #llamamos al producto en base a su id 
    except Producto.DoesNotExist:  #si no existe nos entrega un excepcion indicando que no existe y da un error 404  
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': #al ser get 
        serializer = ProductoSerializer(sus) # llamamos al id guardado en sus y lo utilizamos en el serializer
        return Response(serializer.data) #obtenemos el producto
    elif request.method == 'PUT': #cuando es put
        serializer = ProductoSerializer(sus, data=request.data) #realizamos el proceso de pedir el id del producto, ademas pedimos los nuevos datos editados
        if serializer.is_valid():
            serializer.save() #luego de ser valido lo guardamos
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        sus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






#-------------------------------------------------------------------------------------------------------------#


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



