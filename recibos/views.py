from django.shortcuts import render, redirect
from django.contrib import messages
from empleados.models import Recibo_Sueldos, Empleado
from .forms import ReciboSueldoForm  # Debes crear este formulario

def cargar_recibo(request):
    # Solo permitir acceso a usuarios del grupo 'Administradores'
   
    if request.method == 'POST':
        form = ReciboSueldoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Recibo cargado correctamente.")
            return redirect('ver_recibos')
    else:
        form = ReciboSueldoForm()
    return render(request, 'cargar_recibo.html', {'form': form})

def ver_recibos(request):
    recibos = []
    mensaje = None
    dni = request.GET.get('dni')

    if dni:
        try:
            empleado = Empleado.objects.get(dni=dni)
            recibos = Recibo_Sueldos.objects.filter(id_empl=empleado)
            if not recibos:
                mensaje = "No hay recibos para este empleado."
        except Empleado.DoesNotExist:
            mensaje = "No se encontró un empleado con ese DNI."

    return render(request, 'ver_recibos.html', {
        'recibos': recibos,
        'mensaje': mensaje,
        'dni': dni,
    })