from django.shortcuts import render, redirect
from .forms import HorarioForm
from empleados.models import Horarios,Empleado,AsignacionHorario
from django.contrib import messages
# Create your views here.
def cargar_horario(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asignar_horario')
    else:
        form = HorarioForm()
    return render(request, 'cargar_horario.html', {'form': form})

def asignar_horario(request):
    horarios = Horarios.objects.all()
    empleados = Empleado.objects.all()

    if request.method == 'POST':
        asignaciones_realizadas = 0
        for horario in horarios:
            for i in range(1, horario.cantidad_personal + 1):
                empleado_id = request.POST.get(f"empleado_{horario.id}_{i}")
                if empleado_id:
                    empleado = Empleado.objects.get(id=empleado_id)
                    # Evita asignaciones duplicadas
                    if not AsignacionHorario.objects.filter(id_empl=empleado, id_horario=horario).exists():
                        AsignacionHorario.objects.create(
                            id_empl=empleado,
                            id_horario=horario,
                            estado='Asignado'
                        )
                        asignaciones_realizadas += 1
        if asignaciones_realizadas:
            messages.success(request, f"{asignaciones_realizadas} asignaciones realizadas correctamente.")
        else:
            messages.info(request, "No se realizaron nuevas asignaciones.")
        return redirect('asignar_horario')

    return render(request, 'asignar_horario.html', {
        'horarios': horarios,
        'empleados': empleados,
    })

def ver_horarios_asig(request):
    horarios = []
    dni = request.GET.get('dni')
    if dni:
        try:
            empleado = Empleado.objects.get(dni=dni)
            horarios = AsignacionHorario.objects.filter(id_empl=empleado).select_related('id_empl', 'id_horario')
        except Empleado.DoesNotExist:
            horarios = []

    return render(request, 'ver_horarios_asig.html', {
        'horarios': horarios,
    })


