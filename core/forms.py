from django.forms import ModelForm
from django import forms
from .models import *

class PagoForm(forms.ModelForm):
    OPCIONES_DESPACHO = (
        ('Despacho', 'Despacho'),
        ('Domicilio', 'Domicilio')
    )
    OPCIONES_PAGO = (
        ('Transferencia', 'Transferencia'),
        ('WebPay', 'WebPay')
    )
    OPCIONES_REGION = (
        ('Metropolitana', 'Metropolitana'),
        ('Biobio', 'Biobio'),
        ('Los Lagos', 'Los Lagos'),
        ('Valparaiso', 'Valparaiso')
    )
    tipo_pago = forms.ChoiceField(choices=OPCIONES_PAGO)
    despacho = forms.ChoiceField(choices=OPCIONES_DESPACHO)
    region = forms.ChoiceField(choices=OPCIONES_REGION)
    
    class Meta:
        model = Datos_compra
        fields = ['nombre','apellido','correo','celular','despacho','nombre_calle','numero_calle','tipo_pago','region']
