from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from empleados.models import Recibo_Sueldos, Empleado
from .forms import ReciboSueldoForm  # Debes crear este formulario
from empleados.views import es_admin
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(es_admin)
def cargar_recibo(request):
    # Solo permitir acceso a usuarios logeados
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para cargar un recibo.")
        return redirect('login')
    
    if request.method == 'POST':
        form = ReciboSueldoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Recibo cargado correctamente.")
            return redirect('ver_recibos')
    else:
        form = ReciboSueldoForm()
    return render(request, 'cargar_recibo.html', {'form': form})

@user_passes_test(es_admin)
def ver_recibos(request):
    # Solo permitir acceso a usuarios logeados
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para ver los recibos.")
        return redirect('login')
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
    
def ajax_buscar_empleado(request):
    q = request.GET.get('q', '')
    empleados = Empleado.objects.filter(dni__icontains=q)[:10]
    results = []
    for emp in empleados:
        results.append({
            'id': emp.dni,
            'text': f"{emp.dni} - {emp.nombre} {emp.apellido}"
        })
    return JsonResponse({'results': results})


