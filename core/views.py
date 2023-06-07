from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from core.models import *
from core.Carrito import *
from .forms import *

# LIBRERIA E IMPORTACIÓN PARA USAR LAS "API'S"
from django.http import JsonResponse, HttpResponseRedirect
import requests
import uuid
import json
# Create your views here.


#Aqui se crea la view que muestra la pagina principal
#Esta view realiza un calculo automatico del precio descuento en base al descuento
#Tambien para redigirir al index cuando se desea con el nombre "principal"
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

# Aca es una función para que exista un filtro por la categoria que elija, y se muestre lo que corresponde.
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

# Aca se redirige al html de transferencia en donde se muestran información de este html.
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
                return redirect('transbank')
        contexto["mensaje"] = "Datos Guardados."
    return render(request, 'core/cliente/datosCompra.html', contexto)


# FALTA SACAR LOS TOKEN DE LA URL
# FALTA CREAR UNA PAGINA QUE MUESTRE SI ESTÁ APROBADO O RECHAZADO
# FALTA COLOCAR LOS DATOS DE LA TIENDA, ES DECIR, SESSION ID DEL CLIENTE, ORDEN DE COMPRA, EL MONTO QUE LE CORRESPONDE PAGAR... 


# API WEBPAY PLUS
def get_ws(data, method, type, endpoint):
    if type == 'live':
        TbkApiKeyId = '597055555532'
        TbkApiKeySecret = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
        url = "https://webpay3g.transbank.cl" + endpoint  # Live
    else:
        TbkApiKeyId = '597055555532'
        TbkApiKeySecret = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
        url = "https://webpay3gint.transbank.cl" + endpoint  # Testing

    headers = {
        'Tbk-Api-Key-Id': TbkApiKeyId,
        'Tbk-Api-Key-Secret': TbkApiKeySecret,
        'Content-Type': 'application/json'
    }

    response = requests.request(method, url, headers=headers, data=data)
    return response.json()

def transbank(request):
    baseurl = request.build_absolute_uri('/')

    action = request.GET.get("action", "init")
    message = None

    if action == "init":
        message = 'init'
        buy_order = 'AAA1'
        session_id = 'A1A1'
        amount = 150000
        return_url = baseurl + "?action=getResult"
        type = "sandbox"
        data = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": amount,
            "return_url": return_url
        }
        data = json.dumps(data)
        method = 'POST'
        endpoint = '/rswebpaytransaction/api/webpay/v1.2/transactions'

        response = get_ws(data, method, type, endpoint)
        token = response.get("token")
        url = response.get("url")
        redirect_url = f"{url}?token_ws={token}"
        return HttpResponseRedirect(redirect_url)

    elif action == "getResult":
        message = request.POST
        if 'token_ws' not in request.POST:
            return JsonResponse({'message': message})

        token = request.POST.get('token_ws')

        data = json.dumps({'token': token})
        method = 'PUT'
        type = 'sandbox'
        endpoint = f'/rswebpaytransaction/api/webpay/v1.2/transactions/{token}'

        response = get_ws(data, method, type, endpoint)
        return JsonResponse(response)

    elif action == "getStatus":
        message = request.POST
        if 'token_ws' not in request.POST:
            return JsonResponse({'message': message})

        token = request.POST.get('token_ws')

        data = json.dumps({'token': token})
        method = 'GET'
        type = 'sandbox'
        endpoint = f'/rswebpaytransaction/api/webpay/v1.2/transactions/{token}'

        response = get_ws(data, method, type, endpoint)
        return JsonResponse(response)

    elif action == "refund":
        message = request.POST
        if 'token_ws' not in request.POST:
            return JsonResponse({'message': message})

        token = request.POST.get('token_ws')
        amount = 150000

        data = json.dumps({'amount': amount})
        method = 'POST'
        type = 'sandbox'
        endpoint = f'/rswebpaytransaction/api/webpay/v1.2/transactions/{token}/refunds'

        response = get_ws(data, method, type, endpoint)
        return JsonResponse(response)

    return JsonResponse({'message': message})