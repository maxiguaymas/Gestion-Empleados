from django import forms
from empleados.models import Incidente, Empleado

class IncidenteForm(forms.ModelForm):
    # Este campo nos permitirá seleccionar múltiples empleados.
    # No está en el modelo Incidente, lo manejaremos en la vista.
    empleados_involucrados = forms.ModelMultipleChoiceField(
        queryset=Empleado.objects.filter(estado='Activo'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=True,
        label="Empleados Involucrados"
    )

    # Campo para las observaciones que se guardarán en IncidenteEmpleadoDescargo
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        label="Observaciones Generales (para todos los involucrados)"
    )

    class Meta:
        model = Incidente
        fields = [
            'nombre_incid',
            'fecha_incid',
            'descripcion_incid',
            'tipo_incid',
            'estado_incid',
        ]
        widgets = {
            'fecha_incid': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre_incid': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_incid': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_incid': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_incid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre_incid': 'Nombre del Incidente',
            'fecha_incid': 'Fecha del Incidente',
            'descripcion_incid': 'Descripción',
            'tipo_incid': 'Tipo de Incidente',
            'estado_incid': 'Estado Activo',
        }