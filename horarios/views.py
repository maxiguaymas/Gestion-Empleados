from django.shortcuts import render, redirect
from .forms import HorarioForm
from .forms import AsignarHorarioForm
from empleados.models import Horarios
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

def ver_horarios_asig(request):
    horarios = Horarios.objects.select_related('empleado').all()
    return render(request, 'horarios/ver_horarios_asig.html', {'horarios': horarios})

