from django import forms
from empleados.models import SancionEmpleado, Sancion, Resolucion

class SancionEmpleadoForm(forms.ModelForm):
    # Este campo mostrará un dropdown con las sanciones predefinidas y activas.
    id_sancion = forms.ModelChoiceField(
        queryset=Sancion.objects.filter(estado=True),
        label="Tipo de Sanción",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = SancionEmpleado
        # Excluimos los campos que se llenarán automáticamente en la vista.
        exclude = ['id_empl', 'responsable', 'estado', 'incidente_asociado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin (Opcional)',
            'motivo': 'Motivo / Descripción Detallada',
        }

class SancionMasivaForm(forms.Form):
    id_sancion = forms.ModelChoiceField(
        queryset=Sancion.objects.filter(estado=True),
        label="Tipo de Sanción a Aplicar",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de Inicio"
    )
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label="Fecha de Fin (Opcional)")
    motivo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label="Motivo / Descripción Detallada"
    )
    
class ResolucionForm(forms.ModelForm):
    class Meta:
        model = Resolucion
        fields = ['fecha_resolucion', 'descripcion']
        widgets = {
            'fecha_resolucion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'fecha_resolucion': 'Fecha de la Resolución',
            'descripcion': 'Descripción de la Resolución',
        }