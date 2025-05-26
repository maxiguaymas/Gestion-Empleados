from django import forms
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance or not self.instance.pk:
            self.fields['fecha_egreso'].widget = forms.HiddenInput()
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.label_suffix = ''  # Opcional: quita los dos puntos automáticos
            field.widget.attrs['placeholder'] = field.label  # Opcional: placeholder igual al label
            # Agrega la clase al label
            field.widget.attrs['label_class'] = 'form-label'

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'  # Bootstrap 5 recomienda 'form-select' para select
            else:
                field.widget.attrs['class'] = 'form-control'
