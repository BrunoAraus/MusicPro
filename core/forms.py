from django.forms import ModelForm
from django import forms
from .models import *

class PagoForm(forms.ModelForm):
    OPCIONES_REGION = (
        ('Metropolitana', 'Metropolitana'),
        ('Biobio', 'Biobio'),
        ('Los Lagos', 'Los Lagos'),
        ('Valparaiso', 'Valparaiso')
    )
    OPCIONES_PAGO = (
        ('Transferencia', 'Transferencia'),
        ('WebPay', 'WebPay')
    )
    tipo_pago = forms.ChoiceField(choices=OPCIONES_PAGO)
    region = forms.ChoiceField(choices=OPCIONES_REGION)
    
    class Meta:
        model = Datos_compra
        fields = ['nombre','apellido','correo','celular','nombre_calle','numero_calle','region','tipo_pago']


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'marca', 'precio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['readonly'] = True
        self.fields['categoria'].widget.attrs['readonly'] = True
        self.fields['marca'].widget.attrs['readonly'] = True




class PeticionForm(forms.ModelForm):
    OPCIONES_TIPO = (
        ('Ventas', 'Ventas'),
        ('Desempeño', 'Desempeño')
    )
    tipo = forms.ChoiceField(choices=OPCIONES_TIPO)
    
    class Meta:
        model = Peticion
        fields = ['nombre_peticion','detalle','fechas','tipo']







