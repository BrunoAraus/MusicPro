from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *
from django.shortcuts import redirect
from django.contrib.auth.views import logout_then_login
from .views import CustomLoginView

urlpatterns = [
    path('', principal,name="principal"),
    path('accounts/profile/', lambda request: redirect('/'), name='redireccionar_principal'),
    path('datosCompra', datosCompra , name="datosCompra"),
    path('datosTransferencia', datosTransferencia , name="datosTransferencia"),
    path('productos/', filtro_productos, name='filtro_productos'),
    path('detalle_producto/<int:producto_id>', detalle_producto, name="detalle_producto"),
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="limpiar"),
    path('login/', CustomLoginView.as_view(template_name='core/login.html'), name="login"),
    path('logout/', logout_then_login, {'login_url': 'principal'}, name='logout'),
    path('registro', registro,name="registro"),
    path('transbank/', transbank, name='transbank'),
    path('resultado_compra/', resultado_compra, name='resultado_compra'),
    path('mapa', mapa, name='mapa'),
    path('resultado_compra_error/', resultado_compra_error, name='resultado_compra_error'),
    path('PaginaGrupos/', PaginaGrupos, name='PaginaGrupos'),
    path('CrearUsuarios/', RegistroUsuarioView.as_view(), name='CrearUsuarios'),
    path('GestionarUsuarios/', GestionarUsuarios, name='GestionarUsuarios'),
    path('eliminarUsuario/<id>', eliminarUsuario, name="eliminarUsuario"),
    path('modificarUsuario/<id>', modificarUsuario, name="modificarUsuario"),
    path('GestionarPrecios', GestionarPrecios, name="GestionarPrecios"),
    path('EditarPrecios/<id>', EditarPrecios, name="EditarPrecios"),
    path('GestionarDatos', GestionarDatos, name="GestionarDatos"),
    path('VerPeticion/<id>', VerPeticion, name="VerPeticion"),
    path('CrearPeticion', CrearPeticion, name="CrearPeticion"),
    path('eliminarPeticion/<id>', eliminarPeticion, name="eliminarPeticion"),
    path('crearFicha', crear_ficha, name="crearFicha"),
]