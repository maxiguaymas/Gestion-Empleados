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
    # Solo permitir acceso a usuarios autenticados
    try:
        empleado = Empleado.objects.get(email=request.user.email)
        recibos = Recibo_Sueldos.objects.filter(id_empl=empleado)
    except Empleado.DoesNotExist:
        recibos = []
    return render(request, 'ver_recibos.html', {'recibos': recibos})