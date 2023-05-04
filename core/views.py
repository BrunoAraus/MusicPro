from django.shortcuts import render
from .models import *
from django.shortcuts import render, HttpResponse, redirect
from core.Carrito import *

# Create your views here.

def principal(request):
    productos = Producto.objects.all()
    data = {'productos' : productos}
    return render(request, 'core/cliente/principal.html', data)

def detalle_producto(request, id):
    verProducto = Producto.objects.get(idProducto=id)
    data = {'verProducto' : verProducto}
    return render(request, 'core/cliente/detalle_producto.html', data)

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("principal")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("principal")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("principal")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("principal")




