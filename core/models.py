from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.us

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nombreCategoria

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=100)
    precio = models.IntegerField(blank=True, default=0)
    preciodescuento = models.IntegerField(null=True, blank=True, default=0)
    descuento = models.IntegerField(null=True, default=0)
    stock = models.IntegerField(null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(null=False, max_length=50)
    imagen1 = models.CharField(null=False, max_length=400, blank=True)
    imagen2 = models.CharField(null=False, max_length=400, blank=True)
    imagen3 = models.CharField(null=False, max_length=400, blank=True)
    marca = models.CharField(blank=True, max_length=400, default='N/A')
    diametro = models.CharField(blank=True, max_length=400, default='N/A')
    independencia = models.CharField(blank=True, max_length=400, default='N/A')
    peso = models.CharField(blank=True, max_length=400)
    respuesta = models.CharField(blank=True, max_length=400, default='N/A')
    
    def __str__(self) -> str:
        return self.nombre

class Carrito(models.Model):
    idCarrito = models.AutoField(primary_key=True)
    productos = models.ManyToManyField(Producto)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(null=False, max_length=100)
    precio = models.IntegerField(null=False)
    cantidad = models.IntegerField(null=False, default=1)
    imagen = models.CharField(null=False, max_length=400, blank=False)

    def __str__(self):
        return self.nombre


