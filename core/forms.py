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
    tipo_pago = forms.ChoiceField(choices=OPCIONES_PAGO)
    despacho = forms.ChoiceField(choices=OPCIONES_DESPACHO)
    
    class Meta:
        model = Datos_compra
        fields = ['nombre','apellido','correo','celular','despacho','nombre_calle','numero_calle','tipo_pago']
