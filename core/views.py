from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from core.models import *
from core.Carrito import *

# Create your views here.

def principal(request):
    productos = Producto.objects.all()
    for producto in productos:
        if producto.descuento > 0:
            producto.preciodescuento = producto.precio - (producto.precio * producto.descuento/100)
        else:
            producto.precio = producto.precio
            producto.preciodescuento = 0
        producto.save()
    data = {'productos': productos}
    return render(request, 'core/cliente/principal.html', data)

def registro(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="login")
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html',{'form':form})

def detalle_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    data = {'producto' : producto}
    return render(request, 'core/cliente/detalle_producto.html', data)

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect(request.META.get('HTTP_REFERER'))

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect(request.META.get('HTTP_REFERER'))

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect(request.META.get('HTTP_REFERER'))

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect(request.META.get('HTTP_REFERER'))



def compra(request):
    return render(request, 'core/cliente/datosCompra.html')