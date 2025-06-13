from django import forms
from empleados.models import Horarios, AsignacionHorario

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horarios
        fields = ['turno', 'dia', 'hora_entrada', 'hora_salida', 'cantidad_personal']
        
class AsignarHorarioForm(forms.ModelForm):
    class Meta:
        model = AsignacionHorario
        fields = ['empleado', 'horario', 'estado']