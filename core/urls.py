from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *
from django.shortcuts import redirect
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('', principal,name="principal"),
    path('compra', compra, name="compra"),
    path('detalle_producto/<int:producto_id>', detalle_producto, name="detalle_producto"),
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="limpiar"),
    path('login', LoginView.as_view(template_name='core/login.html'), name="login"),
    path('logout/', logout_then_login, {'login_url': 'principal'}, name='logout'),
    path('registro', registro,name="registro"),
    path('accounts/profile/', lambda request: redirect('principal'), name='redireccionar_principal'),
    path('datosTransferencia',datosTransferencia , name="datosTransferencia"),
]