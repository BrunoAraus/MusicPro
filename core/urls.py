from django.urls import path

from .views import *

urlpatterns = [
    path('', principal,name="principal"),
    path('detalle_producto/<id>', detalle_producto, name="detalle_producto"),
    path('agregar/<int:producto_id>/', agregar_producto, name="Add"),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('restar/<int:producto_id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="limpiar"),
]