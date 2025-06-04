from django import forms
from .models import Recibo_Sueldos

class ReciboSueldosForm(forms.ModelForm):
    class Meta:
        model = Recibo_Sueldos
        fields = ['id_empl', 'fecha_emision', 'periodo', 'ruta_pdf', 'ruta_imagen']