from django.shortcuts import render
from .models import Producto

# Create your views here.

def principal(request):
    productos = Producto.objects.all()
    data = {'productos' : productos}
    return render(request, 'core/cliente/principal.html', data)

<<<<<<< Updated upstream
def detalle_producto(request, id):
    verProducto = Producto.objects.get(idProducto=id)
    data = {'verProducto' : verProducto}
    return render(request, 'core/cliente/detalle_producto.html', data)
=======



>>>>>>> Stashed changes
