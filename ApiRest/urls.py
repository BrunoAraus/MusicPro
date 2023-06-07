from django.urls import URLPattern, path
from ApiRest.views import detalle_prod, lista_prod

urlpatterns = [
    path('lista_prod', lista_prod, name="lista_prod"),
    path('detalle_prod/<id>', detalle_prod, name="detalle_prod"),
]