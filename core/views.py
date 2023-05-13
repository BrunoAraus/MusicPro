from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from core.models import *
from core.Carrito import *
from .forms import *

# Create your views here.


#aqui se crea la view que muestra la pagina principal
#esta view realiza un calculo automatico del precio descuento en base al descuento
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


#aqui se realiza el registro del usuario 
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


#views para las funciones del carrito de compra
#aqui estan los modulos agregar, eliminar, restar, limpiar del carrito
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
    return redirect('principal')

#-----------------------------------------------------------------------------------------------

def filtro_productos(request):
    categorias = Categoria.objects.all()
    categoria_seleccionada = request.GET.get('categoria')

    if categoria_seleccionada == 'todas_las_categorias':
        productos = Producto.objects.all()
    elif categoria_seleccionada:
        productos = Producto.objects.filter(categoria__nombreCategoria=categoria_seleccionada)
    else:
        productos = Producto.objects.all()

    context = {'categorias': categorias, 'productos': productos, 'categoria_seleccionada': categoria_seleccionada}
    return render(request, 'core/cliente/categoriaProductos.html', context)


def datosTransferencia(request):
    return render(request, 'core/cliente/datosTransferencia.html')


#aqui se carga la pagina detectando el formulario
def datosCompra(request):
    contexto = {'form': PagoForm()}
    if request.method == "POST":
        datos = PagoForm(request.POST)
        if datos.is_valid():
            # aqui se Crea una nueva instancia de Datos_compra con el usuario actual o un usuario temporal
            if request.user.is_authenticated:
                nueva_compra = datos.save(commit=False)
                nueva_compra.user = request.user
                nueva_compra.save()
            else:
                # aqui se utiliza el nombre del formulario para nombrar al usuario temporal
                username = datos.cleaned_data['nombre']
                password = 'temporal123'  # aqui se establece una contraseña temporal para el usuario
                user = User.objects.create_user(
                    username=username, password=password)
                nueva_compra = datos.save(commit=False)
                nueva_compra.user = user
                nueva_compra.save()
            if nueva_compra.tipo_pago == 'Transferencia':
                return redirect('datosTransferencia')
            else:
                # colocar pagina falsa de webpay
                return redirect('principal')
        contexto["mensaje"] = "Datos Guardados."
    return render(request, 'core/cliente/datosCompra.html', contexto)
