from django.shortcuts import render
from .models import Producto

# Create your views here.

def principal(request):
    productos = Producto.objects.all()
    data = {'productos' : productos}
    return render(request, 'core/cliente/principal.html', data)


