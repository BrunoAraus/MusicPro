from rest_framework import serializers
from core.models import Producto

#aqui serializamos un modelo con todos los datos del producto, 
#que son los que vamos a pedir cuando productoserializer sea llamado

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
