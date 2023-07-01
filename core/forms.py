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


