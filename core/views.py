from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from core.models import *
from core.Carrito import *
from .forms import *

# LIBRERIA E IMPORTACIÓN PARA USAR LAS "API'S"
from django.http import JsonResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import uuid
import json
# Create your views here.

datos_compra = None

id_sesion = None


def mapa(request):
    return render(request, 'core/cliente/mapa.html')
#Aqui se crea la view que muestra la pagina principal
#Esta view realiza un calculo automatico del precio descuento en base al descuento
#Tambien para redigirir al index cuando se desea con el nombre "principal"
def principal(request):
    #API BANCO CENTRAL
    url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=211737212&pass=kilOfk917B1z&firstdate=2023-06-07&lastdate=2023-12-30&timeseries=F073.TCO.PRE.Z.D&function=GetSeries"
    response = requests.get(url)
    response = response.json()
    dolar = response["Series"]["Obs"][0]["value"] #se le asigna el valor "value" a la variable 'dolar'

    productos = Producto.objects.all()
    for producto in productos:
        if producto.descuento > 0:
            producto.preciodescuento = producto.precio - (producto.precio * producto.descuento/100)
            precio1 = producto.preciodescuento
            precio_dolar_descuento = (precio1 / float(dolar))
            print(f'precios1: {precio_dolar_descuento}')
        else:
            producto.precio = producto.precio
            producto.preciodescuento = 0
            precio2 = producto.precio
            precio_dolar = (precio2 / float(dolar))
            print(f'precios2: {precio_dolar}')
        producto.save()
       

    data = {'productos': productos,        
            'precio_dolar_descuento': precio_dolar_descuento,
            'precio_dolar': precio_dolar}
    
    print(f'DATA: {data}')
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
import random

def datosCompra(request):
    contexto = {'form': PagoForm()}
    if request.method == "POST":
        datos = PagoForm(request.POST)
        if datos.is_valid():
            # Aquí se crea una nueva instancia de Datos_compra con el usuario actual o un usuario temporal
            if request.user.is_authenticated:
                nueva_compra = datos.save(commit=False)
                nueva_compra.user = request.user
                nueva_compra.save()
            else:
                # Aquí se utiliza el nombre del formulario para nombrar al usuario temporal
                nombre = datos.cleaned_data['nombre']
                password = 'temporal123'  # Aquí se establece una contraseña temporal para el usuario
                # Generar un número aleatorio entre 1000 y 9999
                numero_aleatorio = random.randint(1000, 9999)
                # Concatenar el número aleatorio al nombre
                username = f"{nombre}_{numero_aleatorio}"
                user = User.objects.create_user(
                    username=username, password=password)
                nueva_compra = datos.save(commit=False)
                nueva_compra.user = user
                nueva_compra.save()
            carrito = Carrito(request)
            productos_carrito = carrito.carrito.values()  # Obtener los productos del carrito
            for producto in productos_carrito:
                nuevo_producto_carrito = Productos_Carrito(
                    id_compra=nueva_compra,
                    producto=producto['producto_id'],
                    nombre=producto['nombre'],
                    precio=producto['acumulado'],
                    cantidad=producto['cantidad']
                )
                nuevo_producto_carrito.save()
            if nueva_compra.tipo_pago == 'Transferencia':
                return redirect('datosTransferencia')
            else:
                return redirect('transbank')
        contexto["mensaje"] = "Datos Guardados."
    return render(request, 'core/cliente/datosCompra.html', contexto)

def vendedor_principal(request):
    return render(request, 'core/vendedor/TemplateVendedor.html')

# API TRANSBANK COMPLETA Y SUS FUNCIONES
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
        'Content-Type': 'application/json;charset=UTF-8',
        "Access-Control-Allow-Origin": "*",
    }

    response = requests.request(method, url, headers=headers, data=data)
    return response.json()

def resultado_compra_error(request):
    return render(request, 'core/cliente/resultadoCompraError.html')

def guardar_resultado(request,monto_pagado,estado,numero_orden,fecha,comprobante):
    global id_sesion
    global datos_compra
    if not Datos_venta.objects.filter(orden_compra=numero_orden).exists() or Datos_venta.objects.filter(orden_compra=numero_orden).first().orden_compra != numero_orden:
        Datos = Datos_venta(
            id_compra=datos_compra,
            monto_pagado=monto_pagado,
            estado_pago=estado,
            orden_compra=numero_orden,
            sesion_id=id_sesion,
            fecha=fecha,
            codigo_autorizacion=comprobante
        )
        Datos.save()

@csrf_exempt
def resultado_compra(request):
    # Cuando el token no existe (o cambia) me manda a la página de error
    token_ws = request.GET.get('token_ws')
    if not token_ws:
        return redirect('/resultado_compra_error')  # Redirige a la página de error
    
    endpoint = f'/rswebpaytransaction/api/webpay/v1.2/transactions/{token_ws}'
    response = get_ws('', 'PUT', type, endpoint)
    # data es la variable que tendrá toda la respuesta de la API que viene de 'response'
    data = response
    
    # Ejemplo de los datos que trae
    print(data)
    
    # Datos que deseo pasar al html, y los almaceno
    estado = data.get('status')
    fecha = data.get('transaction_date')
    numero_tarjeta = data.get('card_detail', {}).get('card_number')
    monto_pagado = data.get('amount')
    comprobante = data.get('authorization_code')
    numero_orden = data.get('buy_order')

    # Todo aquello igual a este estado 'FAILED', mandará error. (existen distintas formas, no solo AUTHORIZED para saber que algo se pagó)
    if estado == 'FAILED':
        return redirect('/resultado_compra_error') # Redirige a la página de error
    
    # Guardar los datos de la venta acá
    guardar_resultado(request,monto_pagado=monto_pagado, estado=estado, numero_orden=numero_orden, fecha=fecha, comprobante=comprobante)

    # Funcion para eliminar el carrito del usuario.
    carrito = Carrito(request)
    carrito.limpiar()

    # Manda los datos del resultado de compra al html
    return render(request, 'core/cliente/resultadoCompra.html', {
        'estado': estado,
        'numero_tarjeta': numero_tarjeta,
        'fecha': fecha,
        'monto_pagado': monto_pagado,
        'comprobante': comprobante,
        'numero_orden': numero_orden
    })
    

def transbank(request):
    baseurl = request.build_absolute_uri('/')
    action = request.GET.get("action", "init")
    message = None

    # Generar el idSesion único
    global id_sesion
    id_sesion = str(uuid.uuid4())


    # Obtener el objeto Datos_compra correspondiente a la compra más reciente
    global datos_compra
    datos_compra = Datos_compra.objects.latest('id')

    # Crear una instancia de la clase Carrito
    carrito = Carrito(request)

    # Obtener el precio total del carrito
    total_carrito_data = carrito.total_carrito()
    total_carrito = total_carrito_data["total_carrito"]
    total_carrito_descuento = total_carrito_data["total_carrito_descuento"]

    if action == "init":
        message = 'init'
        amount = total_carrito_descuento if total_carrito_descuento > 0 else total_carrito
        return_url = baseurl + "resultado_compra/"
        type = "sandbox"
        data = {
            "buy_order": datos_compra.id,
            "session_id": id_sesion,
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
        return redirect(redirect_url)

    elif action == "getResult":
        token = request.GET.get('token_ws')
        if not token:
            return redirect('/resultado_compra_error')  # Redirige a la página de error

        data = json.dumps({'token': token})
        method = 'PUT'
        type = 'sandbox'
        endpoint = f'/rswebpaytransaction/api/webpay/v1.2/transactions/{token}'

        response = get_ws(data, method, type, endpoint)

        if response.get('status') == 'FAILED':
            return redirect('resultado_compra_error/')

        return JsonResponse(response)

    elif action == "getStatus":
        token = request.GET.get('token_ws')
        if not token:
            return redirect('/resultado_compra_error')  # Redirige a la página de error

        data = json.dumps({'token': token})
        method = 'GET'
        type = 'sandbox'
        endpoint = f'/rswebpaytransaction/api/webpay/v1.2/transactions/{token}/status'

        response = get_ws(data, method, type, endpoint)

        if response.get('status') == 'FAILED':
            return redirect('resultado_compra_error/')

        return JsonResponse(response)

    elif action == "refund":
        token = request.GET.get('token_ws')
        message = request.POST
        if not token:
            return redirect('/resultado_compra_error')  # Redirige a la página de error

        amount = total_carrito_descuento if total_carrito_descuento > 0 else total_carrito

        data = json.dumps({'amount': amount})
        method = 'POST'
        type = 'sandbox'
        endpoint = f'/rswebpaytransaction/api/webpay/v1.2/transactions/{token}/refunds'

        response = get_ws(data, method, type, endpoint)
        return JsonResponse(response)
    
    return JsonResponse({'message': message})

