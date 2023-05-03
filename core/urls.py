from django.urls import path
from .views import *

urlpatterns = [
    path('', principal,name="principal"),
    path('detalle_producto/<id>', detalle_producto, name="detalle_producto")
]