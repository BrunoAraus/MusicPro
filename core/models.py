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
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=100)
    precio = models.IntegerField(blank=True, default=0)
    preciodescuento = models.IntegerField(null=True, blank=True, default=0)
    descuento = models.IntegerField(null=True, default=0)
    stock = models.IntegerField(null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.CharField(null=False, max_length=5000)
    imagen1 = models.CharField(null=False, max_length=400, blank=True)
    imagen2 = models.CharField(null=False, max_length=400, blank=True)
    imagen3 = models.CharField(null=False, max_length=400, blank=True)
    imagen4 = models.CharField(null=False, max_length=400, blank=True)
    marca = models.CharField(blank=True, max_length=400, default='N/A')
    diametro = models.CharField(blank=True, max_length=400, default='N/A')
    impedancia = models.CharField(blank=True, max_length=400, default='N/A')
    potencia = models.CharField(blank=True, max_length=400, default='N/A')
    dimensiones = models.CharField(blank=True, max_length=400, default='N/A')
    peso = models.CharField(blank=True, max_length=400,default='N/A')
    respuesta = models.CharField(blank=True, max_length=400, default='N/A')
    
    def __str__(self):
        return f'{self.nombre} -> {self.precio}'