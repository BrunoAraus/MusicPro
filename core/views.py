from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from core.models import *
from core.Carrito import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django import forms
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db.models import Q


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

# RUTAS DE LOS MENÚ DE CADA VISTA...

def menuOpcionesVendedor(request):
    return render(request, 'core/Vendedor/menuOpcionesVendedor.html')

def menuOpcionesAdministrador(request):
    return render(request, 'core/Administrador/menuOpcionesAdministrador.html')

def menuOpcionesContador(request):
    return render(request, 'core/Contador/menuOpcionesContador.html')

def menuOpcionesBodeguero(request):
    return render(request, 'core/Bodeguero/menuOpcionesBodeguero.html')

# RUTAS DE LOS MENÚ DE CADA VISTA...

# BODEGUERO...

def eliminar_productos(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "¡Eliminado correctamente!")
    return redirect(to="listarProductosBodeguero")

def crear_ficha_producto(request):
    if request.method == 'POST':
        form = CrearProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listarProductosBodeguero')
    else:
        form = CrearProductoForm()
    
    context = {'form': form}
    return render(request, 'core/Bodeguero/crearFicha.html', context)


def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)
    
    data = {
        'form': ModificarProducto(instance=producto)
    }

    if request.method == 'POST':
        formulario = ModificarProducto(data=request.POST, instance=producto, files=request.FILES)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "¡Modificado correctamente!")
            return redirect(to="listarProductosBodeguero")
        data["form"] = formulario

    return render(request, 'core/Bodeguero/modificarFicha.html', data)

def listarProductosBodeguero(request):
    productos = Producto.objects.all()
    data = {'productos' : productos}
    return render(request, 'core/Bodeguero/listarProductos.html',data)

# BODEGUERO...

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

    productos = Producto.objects.filter(precio__gt=0)
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


from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Llama al método form_valid del padre para realizar la lógica de inicio de sesión normal
        response = super().form_valid(form)

        # Verificar si el usuario pertenece a un grupo específico
        user = self.request.user
        if user.groups.filter(name__in=['Administrador']).exists():
            return redirect('menuOpcionesAdministrador')
        elif user.groups.filter(name__in=['Bodeguero']).exists():
            return redirect('menuOpcionesBodeguero')
        elif user.groups.filter(name__in=['Vendedor']).exists():
            return redirect('menuOpcionesVendedor')
        elif user.groups.filter(name__in=['Contador']).exists():
            return redirect('menuOpcionesContador')
        else:
            return response

def GestionarUsuarios(request):
    usuarios_con_grupo = User.objects.exclude(Q(groups=None) | Q(groups__name='Administrador'))
    contexto = {'usuarios': usuarios_con_grupo}
    return render(request, 'core/Administrador/GestionarUsuarios.html', contexto)

def modificarUsuario(request, id):
    usuario = User.objects.get(id=id)
    contexto = {'form': RegistroUsuarioForm(instance=usuario)}
    
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            contexto["mensaje"] = "Usuario modificado."
            contexto['form'] = form
            return redirect('GestionarUsuarios')
    
    return render(request, 'core/Administrador/modificarUsuario.html', contexto)

def GestionarPrecios(request):
    precio_filtro = Producto.objects.filter(precio=0)
    contexto = {'producto': precio_filtro}
    return render(request, 'core/Administrador/GestionarPrecios.html', contexto)

def eliminarUsuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect(to="GestionarUsuarios")

def GestionarDatos(request):
    peticion_filtro = Peticion.objects.filter(estado='Aceptado')
    contexto = {'peticion': peticion_filtro}
    return render(request, 'core/Administrador/GestionarDatos.html', contexto)

def eliminarPeticion(request, id):
    peticion = Peticion.objects.get(id=id)
    peticion.delete()
    return redirect(to="GestionarDatos")

def VerPeticion(request, id):
    peticion_filtro = Peticion.objects.get(id=id)
    data = {'peticion' : peticion_filtro}
    return render(request, 'core/Administrador/VerPeticion.html', data)

def CrearPeticion(request):
    contexto = {'form': PeticionForm()}
    if request.method == "POST":
        Peticion = PeticionForm(request.POST)
        if Peticion.is_valid:
            Peticion.save()
            contexto["mensaje"] = "Peticion Creada!."
            return redirect(to="GestionarDatos")
    return render(request, 'core/Administrador/CrearPeticion.html',contexto)

def PaginaGrupos(request):
    return render(request, 'core/PaginaGrupos.html')


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


class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'password1', 'password2', 'email', 'groups']

class RegistroUsuarioView(CreateView):
    template_name = 'core/Administrador/CrearUsuarios.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('GestionarUsuarios')


def detalle_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    data = {'producto' : producto}

    return render(request, 'core/cliente/detalle_producto.html', data)

def descontar_stock(request):
    # Obtener el último ID de compra creado
    ultimo_id_compra = Datos_compra.objects.latest('id').id

    # Obtener los productos en el carrito de la última compra
    productos_carrito = Productos_Carrito.objects.filter(id_compra=ultimo_id_compra)

    for producto_carrito in productos_carrito:
        # Obtener el producto y restar la cantidad del stock
        producto = Producto.objects.get(id=producto_carrito.producto)
        cantidad_carrito = producto_carrito.cantidad
        producto.stock -= cantidad_carrito
        producto.save()

from django.db.models import Q

def estado_venta(request):
    filtro = Datos_compra.objects.filter(Q(estado='Aceptado') & Q(validacion='N/A'))
    contexto = {'peticion': filtro}
    return render(request, 'core/Vendedor/gestionarPedidos.html', contexto)

def validar_ventas(request, id):
    filtro_validar = Datos_compra.objects.get(id=id)
    filtro_validar.validacion = 'Aceptado'
    filtro_validar.save()

    return redirect(to="estado_venta")

def rechazado_ventas(request, id):
    filtro_validar = Datos_compra.objects.get(id=id)
    filtro_validar.validacion = 'Rechazado'
    filtro_validar.save()

    return redirect(to="estado_venta")

# BODEGUERO....

def listar_ordenes(request):
    filtro = Datos_compra.objects.filter(Q(enviado='N/A') & Q(validacion='Aceptado'))
    contexto = {'peticion': filtro}
    return render(request, 'core/Bodeguero/listarPedidos.html', contexto)

def ver_carrito(request, id):
    filtro = Productos_Carrito.objects.filter(id_compra=id)
    contexto = {'peticion': filtro}
    return render(request, 'core/Bodeguero/gestionarSalidas.html',contexto)

def validar_enviado(request, id):
    filtro_validar = Datos_compra.objects.get(id=id)
    filtro_validar.enviado = 'Aceptado'
    filtro_validar.save()

    return redirect(to="listar_ordenes")

def rechazado_enviado(request, id):
    filtro_validar = Datos_compra.objects.get(id=id)
    filtro_validar.enviado = 'Rechazado'
    filtro_validar.save()

    return redirect(to="listar_ordenes")

# BODEGUERO....



# CONTADOR....

# CONTADOR...
def VistaContador(request):
    transferencias = Datos_compra.objects.filter(estado='Pendiente')
    contexto = {'peticion': transferencias}
    return render(request, 'core/Contador/VistaContador.html', contexto)

def ver_carrito_t(request, id):
    filtro = Productos_Carrito.objects.filter(id_compra=id)
    contexto = {'peticion': filtro}
    suma = 0
    for carrito in filtro:
        suma += carrito.precio
    contexto['suma'] = suma
    return render(request, 'core/Contador/verProductosCarrito.html', contexto)

def validar_transferencia(request, id):
    filtro_validar = Datos_compra.objects.get(id=id)
    filtro_validar.estado = 'Aceptado'
    filtro_validar.save()

    return redirect(to="VistaContador")

def rechazar_transferencia(request, id):
    filtro_validar = Datos_compra.objects.get(id=id)
    filtro_validar.estado = 'Rechazado'
    filtro_validar.save()

    return redirect(to="VistaContador")

# CONTADOR....




# VISUALIZAR PETICIONES
def ver_peticiones(request):
    peticiones = Peticion.objects.filter(estado='Pendiente')
    contexto = {'peticion': peticiones}
    return render(request, 'core/Vendedor/verPeticiones.html', contexto)

def modificar_peticion(request, id):
    peticion = Peticion.objects.get(id=id)
    contexto = {'form': PeticionForm2(instance=peticion)}
    
    if request.method == "POST":
        form = PeticionForm2(request.POST, instance=peticion)
        if form.is_valid():
            form.save()
            peticion.estado = 'Aceptado'
            peticion.save()
            contexto["mensaje"] = "¡Peticion respondida!"
            contexto['form'] = form
            return redirect('ver_peticiones')
    
    return render(request, 'core/Vendedor/modificarPeticion.html', contexto)






def aceptarWebPay(request):
    ultimo_id_compra = Datos_compra.objects.latest('id').id
    datos_validados = Datos_compra.objects.filter(id=ultimo_id_compra)
    datos_validados = Datos_compra.objects.get(id=ultimo_id_compra)
    datos_validados.estado = 'Aceptado'
    datos_validados.save()

def EditarPrecios(request, id):
    producto = Producto.objects.get(id=id)
    contexto = {'form': ProductoForm(instance=producto)}
    if request.method == "POST":
        producto = ProductoForm(request.POST, instance=producto)
        if producto.is_valid():
            producto.save()
            contexto["mensaje"] = "Precio Añadido!."
            contexto['form'] = producto
            return redirect('GestionarPrecios')
    return render(request, 'core/Administrador/EditarPrecios.html', contexto)

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
    descontar_stock(request)
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
                if nueva_compra.tipo_pago == 'Transferencia':
                    nueva_compra.estado = 'Pendiente'
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
                if nueva_compra.tipo_pago == 'Transferencia':
                    nueva_compra.estado = 'Pendiente'
                nueva_compra.save()
            carrito = Carrito(request)
            productos_carrito = carrito.carrito.values()  # Obtener los productos del carrito
            for producto in productos_carrito:
                nuevo_producto_carrito = Productos_Carrito(
                    id_compra=nueva_compra,
                    producto=producto['producto_id'],
                    nombre=producto['nombre'],
                    precio=producto['acumulado'],
                    cantidad=producto['cantidad'],
                )
                nuevo_producto_carrito.save()
            if nueva_compra.tipo_pago == 'Transferencia':
                return redirect('datosTransferencia')
            else:
                return redirect('transbank')
        contexto["mensaje"] = "Datos Guardados."
    return render(request, 'core/cliente/datosCompra.html', contexto)

# VISTA VENDEDOR
def vendedor_principal(request):
    productos = Producto.objects.all()    
    return render(request, 'core/vendedor/TemplateVendedor.html',{
        "productos": productos
    })

def list_productos(request):
    productos = list(Producto.objects.values())
    data = {'productos': productos}
    return JsonResponse(data)

def list_pedidos(request):
    pedidos = list(Datos_compra.objects.values())
    data = {'pedidos': pedidos}
    return JsonResponse(data)

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
    aceptarWebPay(request)
    descontar_stock(request)

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

