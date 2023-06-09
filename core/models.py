from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    us = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.us

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=50)

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
    descripcion = models.CharField(null=True, max_length=5000)
    descripcion_p2 = models.CharField(null=True, max_length=5000)
    descripcion_p3 = models.CharField(null=True, max_length=5000)
    descripcion_p4 = models.CharField(null=True, max_length=5000)
    imagen1 = models.CharField(null=False, max_length=400, blank=True)
    imagen2 = models.CharField(null=False, max_length=400, blank=True)
    imagen3 = models.CharField(null=False, max_length=400, blank=True)
    imagen4 = models.CharField(null=False, max_length=400, blank=True)
    marca = models.CharField(blank=True, max_length=400, default='N/A')
    dimensiones = models.CharField(blank=True, max_length=400, default='N/A')
    peso = models.CharField(blank=True, max_length=400,default='N/A')
    otros = models.CharField(blank=True, max_length=400, default='N/A')
    #amplificadores
    potencia = models.CharField(blank=True, max_length=400, default='N/A')
    altavoz = models.CharField(blank=True, max_length=400, default='N/A')
    #guitarras
    cuerpo = models.CharField(blank=True, max_length=400, default='N/A')
    pastillas = models.CharField(blank=True, max_length=400, default='N/A')
    #manual
    manual = models.CharField(blank=True, max_length=400, default='N/A')
    
    def __str__(self):
        return f'{self.nombre} -> {self.precio}'
    

class Datos_compra(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(null=False, max_length=100)
    apellido = models.CharField(null=False, max_length=100)
    correo = models.EmailField(null=False, max_length=100)
    celular = models.IntegerField(null=False)
    nombre_calle = models.CharField(null=True,max_length=100, default='N/A')
    numero_calle = models.IntegerField(null=True,default=0)
    region = models.CharField(null=True,max_length=50)
    tipo_pago = models.CharField(null=False,max_length=15)
    estado = models.CharField(null=True, default='N/A', max_length=50)
    validacion = models.CharField(null=True, default='N/A', max_length=50)
    enviado = models.CharField(null=True, default='N/A', max_length=50)


class Productos_Carrito(models.Model):
    id_compra = models.ForeignKey(Datos_compra, on_delete=models.CASCADE)
    producto = models.IntegerField(null=False)
    nombre = models.CharField(null=False,max_length=100)
    precio = models.IntegerField(null=False)
    cantidad = models.IntegerField(null=False)

class Datos_venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey(Datos_compra, on_delete=models.CASCADE)
    monto_pagado = models.IntegerField(null=False)
    estado_pago = models.CharField(null=False,max_length=50)
    orden_compra = models.CharField(null=False,max_length=50)
    sesion_id = models.CharField(null=False,max_length=100)
    fecha = models.CharField(null=False,max_length=50)
    codigo_autorizacion = models.CharField(null=False,max_length=50)


class Peticion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_peticion = models.CharField(null=False,max_length=100)
    detalle = models.TextField(null=False,max_length=800)
    fechas = models.CharField(null=False,max_length=100)
    tipo = models.CharField(null=False,max_length=100)
    desempeño = models.CharField(null=True,default='N/A',max_length=500)
    cancelaciones = models.IntegerField(null=True,default=0)
    total_venta_mes_1 = models.IntegerField(null=True,default=0)
    total_venta_mes_2 = models.IntegerField(null=True,default=0)
    productos_vendidos_mes_1 = models.IntegerField(null=True,default=0)
    productos_vendidos_mes_2 = models.IntegerField(null=True,default=0)
    estado = models.CharField(null=True,default='Pendiente',max_length=100)