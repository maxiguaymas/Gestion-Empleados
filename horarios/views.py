from django.shortcuts import render, redirect
from .forms import HorarioForm
from .forms import AsignarHorarioForm

# Create your views here.
def cargar_horario(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_horarios')
    else:
        form = HorarioForm()
    return render(request, 'cargar_horario.html', {'form': form})

def asignar_horario(request):
    if request.method == 'POST':
        form = AsignarHorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_horarios')
    else:
        form = AsignarHorarioForm()
    return render(request, 'asignar_horario.html', {'form': form})

def ver_horario_asig(request):
    from .models import Horarios  # Asegúrate de tener el modelo Horarios
    horarios = Horarios.objects.select_related('empleado').all()
    return render(request, 'ver_horario_asig.html', {'horarios': horarios})


